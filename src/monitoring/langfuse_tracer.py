"""
CustomerCore — Langfuse LLM Observability Tracer (Phase 11)

WHY LANGFUSE?
--------------
When you have 6 AI agents each making multiple LLM calls per triage request, you need
to answer questions like:
  - Which agent is slowest? (latency by agent)
  - Which model costs the most? (cost by model)
  - Why did this specific ticket get the wrong classification? (drill into prompt/completion)
  - How has response quality changed over the last 30 days? (quality score trend)
  - Which constitutional rules are violated most often? (compliance heatmap)

Without LLM observability, you're flying blind. print() statements and logs show you
that something happened — Langfuse shows you exactly WHAT happened, WHY it happened,
and HOW MUCH it cost, for every single LLM call, with full prompt and completion text.

ARCHITECTURE: TRACE → SPAN → GENERATION
-----------------------------------------
Langfuse organises observability data in a hierarchy:

  Trace   = one end-to-end user request (one triage, one HTTP call)
             Has metadata: tenant_id, customer_id, ticket_id, total latency, total cost

  Span    = one logical step within a trace (one agent's work)
             Examples: "classify_agent", "rag_agent", "constitutional_check"

  Generation = one LLM API call within a span
             Records: model name, prompt messages, completion text,
                      prompt tokens, completion tokens, latency, cost

  Score   = a quality evaluation attached to a trace or generation
             Examples: constitutional_score, resolution_relevance, rag_grounding

Visual in Langfuse dashboard:
  Triage (trace, total 4.2s, $0.0003)
    ├── classify_agent (span, 1.1s)
    │    └── gemma3:4b (generation, prompt: 340 tokens, completion: 48 tokens, $0.00)
    ├── rag_agent (span, 2.3s)
    │    └── llama-3.1-8b (generation, prompt: 890 tokens, completion: 210 tokens, $0.0001)
    ├── churn_agent (span, 0.5s)
    │    └── gemma3:4b (generation, prompt: 520 tokens, completion: 32 tokens, $0.00)
    └── constitutional_check (span, 0.3s)
         ├── Score: constitutional_score = 0.95
         └── Score: resolution_relevance = 0.88

INTEGRATION WITH LITELLM:
  LiteLLM has built-in Langfuse support via callbacks. We set:
    litellm.success_callback = ["langfuse"]
    litellm.failure_callback = ["langfuse"]
  This automatically captures every LiteLLM call — model, tokens, latency, cost.
  For agent-level spans, we create them manually using the Langfuse Python SDK
  and pass the trace context via metadata.

GRACEFUL DEGRADATION:
  All functions check if LANGFUSE_PUBLIC_KEY is configured. If not, they return
  no-op stub objects that have the same interface but do nothing. This ensures:
    - Unit tests pass without a Langfuse account
    - Local development works offline
    - The exact same code runs in dev and production — no if/else branching in business logic
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Generator


# ─────────────────────────────────────────────────────────────────────────────
# Lazy Langfuse client (only instantiated when keys are present)
# ─────────────────────────────────────────────────────────────────────────────

def _is_langfuse_configured() -> bool:
    """Return True if Langfuse credentials are present in the environment."""
    return bool(
        os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
    )


def _get_langfuse_client():
    """
    Return a live Langfuse client or None if not configured.

    We lazy-init (not at import time) because importing langfuse triggers
    network activity — we don't want tests to fail if Langfuse is unreachable.
    """
    if not _is_langfuse_configured():
        return None
    try:
        from langfuse import Langfuse
        return Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# No-op stubs — returned when Langfuse is not configured
# ─────────────────────────────────────────────────────────────────────────────

class _NoOpSpan:
    """Stub span that silently does nothing — same interface as a real Langfuse span."""

    def update(self, **kwargs: Any) -> None:
        pass

    def end(self, **kwargs: Any) -> None:
        pass

    def score(self, **kwargs: Any) -> None:
        pass

    def generation(self, **kwargs: Any) -> "_NoOpSpan":
        return _NoOpSpan()

    def span(self, **kwargs: Any) -> "_NoOpSpan":
        return _NoOpSpan()

    def event(self, **kwargs: Any) -> None:
        pass

    @property
    def id(self) -> str:
        return "noop"


class _NoOpTrace(_NoOpSpan):
    """Stub trace that silently does nothing."""

    def flush(self) -> None:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# TriageTrace — the main observability object created per triage request
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class TriageTrace:
    """
    Represents one end-to-end triage observation in Langfuse.

    Created at the start of each triage request, passed through the agent graph,
    and closed when the triage completes (with final scores).

    Usage in triage router:
        trace = TriageTrace.start(
            ticket_id=ticket_id,
            tenant_id=caller.tenant_id,
            customer_tier="enterprise",
        )
        # Pass trace through agent calls
        with trace.agent_span("classify_agent") as span:
            result = classify_agent.run(...)
            span.update(output=result)
        # At completion
        trace.score_constitutional(0.95)
        trace.finish(status="complete", total_cost_usd=0.0003)
    """

    ticket_id: str
    tenant_id: str
    _trace: Any = field(default=None, repr=False)
    _start_ms: float = field(default_factory=lambda: time.time() * 1000, repr=False)

    @classmethod
    def start(
        cls,
        *,
        ticket_id: str,
        tenant_id: str,
        customer_id: str,
        customer_tier: str,
        channel: str,
        text_preview: str = "",
    ) -> "TriageTrace":
        """
        Open a new Langfuse trace for one triage request.

        The text_preview is the first 200 characters of the ticket — enough
        to identify the ticket in the Langfuse dashboard without logging full PII.
        """
        client = _get_langfuse_client()
        trace = _NoOpTrace()

        if client:
            try:
                trace = client.trace(
                    name="triage",
                    id=ticket_id,
                    user_id=customer_id,
                    session_id=tenant_id,
                    metadata={
                        "tenant_id": tenant_id,
                        "customer_tier": customer_tier,
                        "channel": channel,
                        "text_preview": text_preview[:200],
                    },
                    tags=[tenant_id, customer_tier, channel],
                )
            except Exception:
                trace = _NoOpTrace()

        obj = cls(ticket_id=ticket_id, tenant_id=tenant_id, _trace=trace)
        return obj

    @contextmanager
    def agent_span(self, agent_name: str, **metadata: Any) -> Generator[Any, None, None]:
        """
        Context manager that creates a Langfuse span for one agent's work.

        Usage:
            with trace.agent_span("classify_agent", input_lang="de") as span:
                result = classify(...)
                span.update(output=str(result))
        """
        span = _NoOpSpan()
        start = time.time()
        try:
            span = self._trace.span(
                name=agent_name,
                metadata=metadata,
                start_time=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
            )
        except Exception:
            pass

        try:
            yield span
        finally:
            elapsed_ms = int((time.time() - start) * 1000)
            try:
                span.end(metadata={"duration_ms": elapsed_ms})
            except Exception:
                pass

    def record_generation(
        self,
        *,
        span: Any,
        model: str,
        prompt_messages: list[dict],
        completion: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        latency_ms: int = 0,
        cost_usd: float = 0.0,
    ) -> None:
        """
        Record one LLM generation (prompt → completion) within an agent span.

        This is the atomic unit of LLM observability: for every LiteLLM call,
        we record exactly what was sent and what came back, with token counts and cost.
        This data enables:
          - Prompt debugging (why did the model say X?)
          - Cost attribution (which agent is most expensive?)
          - Token usage optimisation (are our prompts too long?)
        """
        try:
            span.generation(
                name=f"{model}_generation",
                model=model,
                input=prompt_messages,
                output=completion,
                usage={
                    "input": prompt_tokens,
                    "output": completion_tokens,
                    "total": prompt_tokens + completion_tokens,
                    "unit": "TOKENS",
                },
                metadata={
                    "latency_ms": latency_ms,
                    "cost_usd": cost_usd,
                },
            )
        except Exception:
            pass

    def record_retrieval(
        self,
        *,
        span: Any,
        query: str,
        num_results: int,
        retrieval_method: str,
        latency_ms: int,
        cache_hit: bool = False,
    ) -> None:
        """Record a RAG retrieval event — not an LLM call but a vector/BM25 search."""
        try:
            span.event(
                name="rag_retrieval",
                metadata={
                    "query_preview": query[:100],
                    "num_results": num_results,
                    "retrieval_method": retrieval_method,
                    "latency_ms": latency_ms,
                    "cache_hit": cache_hit,
                },
            )
        except Exception:
            pass

    def score_constitutional(self, score: float, comment: str = "") -> None:
        """Attach a constitutional compliance score (0–1) to this trace."""
        try:
            self._trace.score(
                name="constitutional_compliance",
                value=score,
                comment=comment or (
                    "All rules passed" if score >= 1.0
                    else f"Score: {score:.2f} — some rules flagged"
                ),
            )
        except Exception:
            pass

    def score_resolution_quality(self, score: float, comment: str = "") -> None:
        """Attach a resolution quality score (0–1) — how well did RAG answer the question?"""
        try:
            self._trace.score(
                name="resolution_quality",
                value=score,
                comment=comment,
            )
        except Exception:
            pass

    def score_rag_grounding(self, score: float) -> None:
        """Are the KB citations in the resolution real and relevant?"""
        try:
            self._trace.score(
                name="rag_grounding",
                value=score,
                comment="Fraction of KB citations that are valid references",
            )
        except Exception:
            pass

    def finish(
        self,
        *,
        status: str,
        total_cost_usd: float = 0.0,
        total_tokens: int = 0,
    ) -> None:
        """
        Close the trace with final metadata.
        Must be called when triage completes (complete, hitl, or failed).
        """
        elapsed_ms = int(time.time() * 1000 - self._start_ms)
        try:
            self._trace.update(
                metadata={
                    "status": status,
                    "total_duration_ms": elapsed_ms,
                    "total_cost_usd": total_cost_usd,
                    "total_tokens": total_tokens,
                },
                output={"status": status},
            )
            # Flush ensures the trace is sent to Langfuse even in short-lived processes
            if hasattr(self._trace, "flush"):
                self._trace.flush()
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# LiteLLM Langfuse callback registration
# ─────────────────────────────────────────────────────────────────────────────

def setup_litellm_tracing() -> bool:
    """
    Register Langfuse as a LiteLLM callback.

    LiteLLM has built-in Langfuse support — every completion() call is
    automatically traced when langfuse is in the success/failure callback lists.
    This is the zero-code-change integration: existing LLM router calls in
    src/rag/llm_client.py are traced without modifying them.

    Returns True if Langfuse callbacks were successfully registered.

    Called during API lifespan startup (src/api/main.py).
    """
    if not _is_langfuse_configured():
        return False

    try:
        import litellm
        if "langfuse" not in litellm.success_callback:
            litellm.success_callback.append("langfuse")
        if "langfuse" not in litellm.failure_callback:
            litellm.failure_callback.append("langfuse")

        # Set Langfuse environment variables that LiteLLM's callback reads
        # (LiteLLM reads these directly from os.environ)
        os.environ.setdefault("LANGFUSE_PUBLIC_KEY", os.getenv("LANGFUSE_PUBLIC_KEY", ""))
        os.environ.setdefault("LANGFUSE_SECRET_KEY", os.getenv("LANGFUSE_SECRET_KEY", ""))
        os.environ.setdefault("LANGFUSE_HOST", os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"))
        return True
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Module-level setup on import
# ─────────────────────────────────────────────────────────────────────────────

_LITELLM_TRACING_ENABLED = setup_litellm_tracing()
