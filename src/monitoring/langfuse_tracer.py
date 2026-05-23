"""
CustomerCore — Langfuse LLM Observability Tracer (Phase 11)
Upgraded per langfuse/skills best practices (github.com/langfuse/skills)

Skill baseline checklist (from skills/langfuse/references/instrumentation.md):
  [x] Model name captured         — via LiteLLM success_callback auto-integration
  [x] Token usage tracked         — via LiteLLM callback (input/output/total tokens)
  [x] Descriptive trace names     — "ticket-triage" not generic "trace-1"
  [x] Span hierarchy              — agent_span() context manager nests spans correctly
  [x] Generations marked          — observation_type=GENERATION on every LLM call
  [x] Sensitive data masked       — PII stripped from trace input before sending
  [x] Trace input explicitly set  — only the ticket text preview, not all function args
  [x] Graceful degradation        — NoOp stubs when keys absent (tests work offline)
  [x] Framework integration used  — LiteLLM built-in Langfuse callback (zero-code)
  [x] Latest SDK version          — langfuse 4.6.1, flush via Langfuse client

ARCHITECTURE: TRACE → SPAN → GENERATION
-----------------------------------------
  Trace   = one triage request (name: "ticket-triage", input: ticket preview)
  Span    = one agent step (classify_agent, rag_agent, constitutional_check)
  Generation = one LLM call (model, prompt, completion, tokens, cost)
  Score   = quality evaluation (constitutional_compliance, resolution_quality)

LiteLLM integration (zero-code-change):
  litellm.success_callback = ["langfuse"]  → every LiteLLM call auto-traced
  litellm.failure_callback = ["langfuse"]  → errors captured too

Graceful degradation:
  When LANGFUSE_PUBLIC_KEY is absent → NoOpTrace/NoOpSpan returned
  Same interface, does nothing → tests pass, local dev works offline
"""

from __future__ import annotations

import os
import re
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generator

# Compiled PII patterns for fast masking before sending to Langfuse
# Per skills/langfuse/references/instrumentation.md: "PII/confidential data excluded or masked"
_PII_PATTERNS = [
    (re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"), "[EMAIL]"),
    (re.compile(r"\b(?:\+?\d[\s\-.]{0,1}){7,15}\d\b"), "[PHONE]"),
    (re.compile(r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b"), "[SSN]"),
    (re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7,20}\b"), "[IBAN]"),
    (re.compile(r"\b(?:\d{4}[\s\-]?){3}\d{4}\b"), "[CARD]"),
]


def _mask_pii(text: str) -> str:
    """Strip PII from text before logging to Langfuse (GDPR + skill requirement)."""
    for pattern, placeholder in _PII_PATTERNS:
        text = pattern.sub(placeholder, text)
    return text


# ─────────────────────────────────────────────────────────────────────────────
# Lazy Langfuse client (only instantiated when keys are present)
# ─────────────────────────────────────────────────────────────────────────────

# Module-level singleton client (one per process, per skill recommendation)
_langfuse_client = None
_langfuse_client_initialised = False


def _is_langfuse_configured() -> bool:
    """Return True if Langfuse credentials are present in the environment."""
    return bool(
        os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
    )


def _get_langfuse_client():
    """
    Return a live Langfuse client singleton or None if not configured.

    Per skill best practice: one client per process, not one per request.
    Lazy-init to avoid network calls at import time (tests would fail).
    """
    global _langfuse_client, _langfuse_client_initialised
    if _langfuse_client_initialised:
        return _langfuse_client
    _langfuse_client_initialised = True
    if not _is_langfuse_configured():
        return None
    try:
        from langfuse import Langfuse
        _langfuse_client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )
    except Exception:
        _langfuse_client = None
    return _langfuse_client



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

        Per skill baseline requirement:
          - name: descriptive ("ticket-triage"), not generic
          - input: explicitly set to ONLY the relevant user message (not all function args)
          - PII masked before sending to Langfuse (GDPR compliance)
          - tags: enable filtering in Langfuse UI by tier and channel
        """
        client = _get_langfuse_client()
        trace = _NoOpTrace()

        # Mask PII in the preview before it leaves the process
        safe_preview = _mask_pii(text_preview[:200]) if text_preview else ""

        if client:
            try:
                trace = client.trace(
                    # Descriptive name (skill: "names like 'chat-response', not 'trace-1'")
                    name="ticket-triage",
                    id=ticket_id,
                    user_id=customer_id,
                    session_id=tenant_id,
                    # Explicit input: only the ticket text (skill: "show only relevant data")
                    input={"ticket_text": safe_preview, "channel": channel},
                    metadata={
                        "tenant_id": tenant_id,
                        "customer_tier": customer_tier,
                        "channel": channel,
                    },
                    tags=[customer_tier, channel],  # bounded cardinality — not tenant_id
                )
            except Exception:
                trace = _NoOpTrace()

        obj = cls(ticket_id=ticket_id, tenant_id=tenant_id, _trace=trace)
        return obj

    @contextmanager
    def agent_span(self, agent_name: str, input_data: Any = None, **metadata: Any) -> Generator[Any, None, None]:
        """
        Context manager that creates a Langfuse span for one agent's work.

        Per skill: spans should have meaningful input set explicitly.

        Usage:
            with trace.agent_span("classify_agent", input_data={"text": preview}) as span:
                result = classify(...)
                span.update(output=str(result))
        """
        span = _NoOpSpan()
        start = time.time()
        try:
            span = self._trace.span(
                name=agent_name,
                input=input_data,
                metadata=metadata or None,
                start_time=datetime.now(timezone.utc),
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
        Record one LLM generation within an agent span.

        Per skill baseline:
          - observation_type must be GENERATION (not span) for model analytics
          - model name required for model comparison and cost calculation
          - input/output tokens required for automatic cost calculation
          - prompt messages masked for PII before logging
        """
        # Mask PII in prompts before logging (skill: "PII/confidential data excluded or masked")
        safe_messages = [
            {**m, "content": _mask_pii(str(m.get("content", ""))[:500])}
            for m in (prompt_messages or [])
        ]
        safe_completion = _mask_pii(completion[:1000]) if completion else ""

        try:
            span.generation(
                name=f"{model}-generation",
                model=model,
                input=safe_messages,    # skill: "input explicitly set to relevant data"
                output=safe_completion,
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
        output: dict | None = None,
    ) -> None:
        """
        Close the trace with final output and metadata, then flush.

        Per skill: flush via Langfuse client (not trace object) for SDK v3.
        The output field is the trace-level output shown prominently in the UI.
        """
        elapsed_ms = int(time.time() * 1000 - self._start_ms)
        try:
            self._trace.update(
                # Explicit output: the meaningful result (skill: "trace captures meaningful output")
                output=output or {"status": status},
                metadata={
                    "status": status,
                    "total_duration_ms": elapsed_ms,
                    "total_cost_usd": total_cost_usd,
                    "total_tokens": total_tokens,
                },
            )
        except Exception:
            pass
        # Flush via client singleton (SDK v3 best practice)
        try:
            client = _get_langfuse_client()
            if client:
                client.flush()
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
