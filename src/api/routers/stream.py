"""
CustomerCore API — Server-Sent Events (SSE) Stream Router (Phase 10)

WHY SERVER-SENT EVENTS INSTEAD OF WEBSOCKETS?
-----------------------------------------------
Both SSE and WebSockets provide real-time server → client communication.
The key difference:

  WebSocket:
    - Bidirectional (both client and server can send messages)
    - More complex to implement (requires upgrade handshake, heartbeats, reconnection logic)
    - Better for chat applications, collaborative editing, live games

  Server-Sent Events (SSE):
    - Unidirectional (server → client only)
    - Uses a regular HTTP connection — works through proxies and firewalls that block WebSockets
    - Browsers handle reconnection automatically (EventSource API)
    - Built-in support in FastAPI via StreamingResponse
    - Ideal for: progress updates, live logs, dashboard feeds

CustomerCore's triage stream is read-only from the client's perspective — the client
watches triage progress but doesn't send messages. SSE is the correct choice.

HOW IT WORKS:
  1. Client subscribes: GET /api/v1/triage/{ticket_id}/stream
  2. Server opens a long-lived HTTP connection
  3. As the triage progresses, the server pushes status events:
       data: {"status": "processing", "step": "classify_agent"}\n\n
       data: {"status": "processing", "step": "rag_agent"}\n\n
       data: {"status": "complete", "result": {...}}\n\n
  4. Client closes the connection when it receives status=complete or status=failed

SSE EVENT FORMAT (per the W3C spec):
  data: <json_payload>\n\n
  The double newline signals the end of one event — the browser's EventSource parses this.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from src.api.auth import AuthenticatedTenant, verify_token
from src.api.models import TriageStatus
from src.api.store import triage_store

router = APIRouter(prefix="/api/v1/triage", tags=["Streaming"])

# How often to check for status updates (seconds)
_POLL_INTERVAL = 0.5
# Maximum wait time before giving up and closing the stream
_MAX_WAIT_SECONDS = 120


@router.get(
    "/{ticket_id}/stream",
    summary="Real-time SSE stream for triage progress",
    description=(
        "Subscribe to Server-Sent Events for a ticket's triage progress. "
        "The stream emits status events as each agent completes. "
        "Closes automatically when triage reaches complete/hitl/failed status."
    ),
    response_class=StreamingResponse,
)
async def stream_triage(
    ticket_id: str,
    caller: AuthenticatedTenant = Depends(verify_token),
) -> StreamingResponse:
    """
    Stream real-time triage progress via Server-Sent Events.

    Client usage (JavaScript):
        const source = new EventSource(
          '/api/v1/triage/{ticket_id}/stream',
          { headers: { Authorization: 'Bearer <token>' } }
        );
        source.onmessage = (e) => {
          const event = JSON.parse(e.data);
          if (event.status === 'complete') {
            source.close();
            showResult(event.result);
          }
        };
    """
    record = triage_store.get(ticket_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found.")
    if record["tenant_id"] != caller.tenant_id:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found.")

    async def event_generator():
        """
        Async generator that polls the triage store and yields SSE events.

        Why polling instead of true async events?
          The LangGraph supervisor runs in a background thread (via BackgroundTasks).
          True async event propagation would require a pub/sub system (Redis pub/sub
          or asyncio.Queue) — that's Phase 12 territory. For now, lightweight polling
          every 500ms is sufficient and still provides near-real-time updates.
          With Phase 12 (Supabase + Redis), we'll upgrade to Supabase Realtime
          (PostgreSQL logical replication → WebSocket push) for zero-latency events.
        """
        elapsed = 0.0
        terminal_statuses = {TriageStatus.COMPLETE, TriageStatus.HITL, TriageStatus.FAILED}
        last_status = None

        # Send initial connection confirmation event
        yield _sse_event({
            "type": "connected",
            "ticket_id": ticket_id,
            "timestamp": datetime.utcnow().isoformat(),
        })

        while elapsed < _MAX_WAIT_SECONDS:
            await asyncio.sleep(_POLL_INTERVAL)
            elapsed += _POLL_INTERVAL

            current_status = triage_store.get_status(ticket_id)

            # Only emit an event if status changed (avoids flooding the client)
            if current_status != last_status:
                last_status = current_status

                if current_status == TriageStatus.PROCESSING:
                    yield _sse_event({
                        "type": "status",
                        "status": "processing",
                        "message": "AI agents are analyzing your ticket...",
                        "elapsed_ms": int(elapsed * 1000),
                    })

                elif current_status == TriageStatus.HITL:
                    rec = triage_store.get(ticket_id)
                    yield _sse_event({
                        "type": "hitl",
                        "status": "hitl",
                        "message": "Ticket flagged for human review.",
                        "hitl_reason": rec.get("hitl_reason") if rec else None,
                        "elapsed_ms": int(elapsed * 1000),
                    })
                    yield _sse_event({"type": "done"})
                    return

                elif current_status == TriageStatus.COMPLETE:
                    rec = triage_store.get(ticket_id)
                    result = rec.get("result", {}) if rec else {}
                    yield _sse_event({
                        "type": "complete",
                        "status": "complete",
                        "category": result.get("category"),
                        "priority": result.get("priority"),
                        "confidence": result.get("confidence"),
                        "churn_risk": result.get("churn_risk"),
                        "hitl_required": result.get("hitl_required", False),
                        "processing_ms": rec.get("processing_ms") if rec else None,
                        "elapsed_ms": int(elapsed * 1000),
                    })
                    yield _sse_event({"type": "done"})
                    return

                elif current_status == TriageStatus.FAILED:
                    rec = triage_store.get(ticket_id)
                    yield _sse_event({
                        "type": "error",
                        "status": "failed",
                        "error": rec.get("error", "Unknown error") if rec else "Unknown error",
                        "elapsed_ms": int(elapsed * 1000),
                    })
                    yield _sse_event({"type": "done"})
                    return

            # Send a keep-alive comment every 10 seconds (prevents proxy timeouts)
            if elapsed % 10 < _POLL_INTERVAL:
                yield ": keep-alive\n\n"

        # Timeout — stream ran too long
        yield _sse_event({
            "type": "timeout",
            "message": f"Stream timed out after {_MAX_WAIT_SECONDS}s. "
                       f"Poll GET /api/v1/triage/{ticket_id} for result.",
        })

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering (critical for SSE)
            "Connection": "keep-alive",
        },
    )


def _sse_event(data: dict) -> str:
    """Format a dictionary as a W3C-compliant SSE event string."""
    return f"data: {json.dumps(data)}\n\n"
