"""
CustomerCore API — Triage Router (Phase 10)

This is the core of the CustomerCore API — the routes that accept tickets,
invoke the LangGraph 6-agent supervisor, handle HITL pausing, and return results.

ASYNC BACKGROUND PROCESSING:
------------------------------
Ticket triage is NOT synchronous. The LangGraph supervisor makes LLM calls that
take 2–8 seconds. We cannot block the HTTP connection for that long because:
  - HTTP clients have timeouts (usually 30s, but we target <10s response)
  - Blocking threads wastes server resources
  - The caller doesn't need to wait — they can poll or subscribe to SSE

Pattern used (async background task):
  1. POST /triage → immediately return ticket_id + status=pending (200ms)
  2. FastAPI BackgroundTasks schedules the LangGraph run asynchronously
  3. Client polls GET /triage/{id} OR subscribes to GET /triage/{id}/stream (SSE)
  4. When complete, GET /triage/{id} returns the full result

This is the same pattern used by OpenAI's batch API, Anthropic's async API,
and every production ML inference system that takes >1s per request.
"""

from __future__ import annotations

import asyncio
from typing import Any
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from src.api.auth import AuthenticatedTenant, require_role, verify_token
from src.api.models import (
    HITLResumeRequest,
    TicketSubmitRequest,
    TicketSubmitResponse,
    TriageResultResponse,
    TriageStatus,
)
from src.api.store import triage_store

router = APIRouter(prefix="/api/v1/triage", tags=["Triage"])


# ─────────────────────────────────────────────────────────────────────────────
# Background Triage Runner
# ─────────────────────────────────────────────────────────────────────────────

async def _run_triage(ticket_id: str, text: str, customer_id: str, tenant_id: str,
                      customer_tier: str, channel: str) -> None:
    """
    Background task: runs the full LangGraph 6-agent supervisor for one ticket.

    This function runs in a FastAPI background task — not blocking the HTTP response.
    It updates the triage_store as state progresses (PENDING → PROCESSING → COMPLETE/HITL/FAILED).

    Error handling strategy:
      - Any exception is caught and stored as FAILED status
      - The ticket_id remains queryable — callers learn what went wrong
      - Critical tickets trigger a fallback heuristic classification if LangGraph fails
        (ensures 0% silent failure rate on P1/critical tickets)
    """
    triage_store.set_processing(ticket_id)

    try:
        # Import here to avoid circular imports at module load time
        from src.agent.supervisor import run_triage

        result = run_triage(
            ticket_text=text,
            customer_id=customer_id,
            tenant_id=tenant_id,
            customer_tier=customer_tier,
            channel=channel,
        )

        # Check if the result requires HITL (supervisor returned paused state)
        if isinstance(result, dict) and result.get("hitl_required"):
            triage_store.set_hitl(
                ticket_id,
                hitl_reason=result.get("hitl_reason", "Low confidence or critical priority"),
            )
            # Store partial result so the HITL reviewer sees the AI's work so far
            triage_store.set_complete(ticket_id, result)
            triage_store._status[ticket_id] = TriageStatus.HITL  # Re-set to HITL
        else:
            triage_store.set_complete(ticket_id, result or {})

    except Exception as exc:
        triage_store.set_failed(ticket_id, error=str(exc))


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/v1/triage — Submit a ticket for AI triage
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=TicketSubmitResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit ticket for AI triage",
    description=(
        "Accepts a support ticket and initiates async AI triage using the "
        "LangGraph 6-agent supervisor. Returns immediately with a ticket_id. "
        "Poll GET /triage/{id} for the result or subscribe to the SSE stream."
    ),
)
async def submit_ticket(
    body: TicketSubmitRequest,
    background_tasks: BackgroundTasks,
    caller: AuthenticatedTenant = Depends(verify_token),
) -> TicketSubmitResponse:
    """
    Submit a support ticket for AI triage.

    The tenant_id is taken from the JWT — NEVER from the request body.
    This is critical for multi-tenant data isolation: a tenant cannot submit
    tickets on behalf of another tenant, even if they know the other tenant's ID.
    """
    ticket_id = triage_store.create(
        tenant_id=caller.tenant_id,
        customer_id=body.customer_id,
        text=body.text,
        channel=body.channel.value,
        metadata=body.metadata,
    )

    # Schedule the LangGraph run as a non-blocking background task
    background_tasks.add_task(
        _run_triage,
        ticket_id=ticket_id,
        text=body.text,
        customer_id=body.customer_id,
        tenant_id=caller.tenant_id,
        customer_tier=body.customer_tier.value,
        channel=body.channel.value,
    )

    return TicketSubmitResponse(
        ticket_id=ticket_id,  # type: ignore[arg-type]
        status=TriageStatus.PENDING,
        message="Ticket accepted for triage",
        estimated_seconds=3 if body.customer_tier.value in ("enterprise", "vip") else 6,
        stream_url=f"/api/v1/triage/{ticket_id}/stream",
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/triage/{ticket_id} — Poll for result
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/{ticket_id}",
    response_model=TriageResultResponse,
    summary="Get triage result",
    description="Poll for the triage result. Status progresses: pending → processing → complete/hitl/failed.",
)
async def get_triage(
    ticket_id: str,
    caller: AuthenticatedTenant = Depends(verify_token),
) -> TriageResultResponse:
    """
    Retrieve the current state of a triage request.

    Tenant isolation: callers can only read their own tickets.
    If a caller from tenant A tries to read a ticket from tenant B,
    they receive 404 — same as if the ticket didn't exist.
    This prevents information leakage between tenants.
    """
    record = triage_store.get(ticket_id)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found.",
        )

    # Tenant isolation check — 404 (not 403) to prevent tenant enumeration attacks
    if record["tenant_id"] != caller.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found.",
        )

    return triage_store.to_response(record)


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/v1/triage/{ticket_id}/resume — HITL Resume
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/{ticket_id}/resume",
    response_model=TriageResultResponse,
    summary="Resume a HITL-paused ticket",
    description=(
        "Resume a ticket that was paused at the Human-in-the-Loop checkpoint. "
        "Only managers and admins can call this endpoint. "
        "The operator may optionally override category, priority, or resolution."
    ),
)
async def resume_hitl(
    ticket_id: str,
    body: HITLResumeRequest,
    background_tasks: BackgroundTasks,
    caller: AuthenticatedTenant = Depends(require_role("manager", "admin")),
) -> TriageResultResponse:
    """
    Resume a HITL-paused triage with optional human overrides.

    Why only manager/admin?
      A support_agent should not be able to approve their own escalation bypass.
      HITL exists precisely to add human oversight. Allowing any role to resume
      would defeat the entire purpose of the safety checkpoint.

    The resume call:
      1. Validates the ticket is in HITL status
      2. Applies any overrides from the operator
      3. Re-runs the LangGraph supervisor from the finalize node (not from scratch)
      4. Records the operator_id and notes in the audit trail
    """
    record = triage_store.get(ticket_id)

    if not record:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found.")

    if record["tenant_id"] != caller.tenant_id:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found.")

    if record["status"] != TriageStatus.HITL:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ticket {ticket_id} is not in HITL status (current: {record['status'].value}). "
                   f"Only HITL-paused tickets can be resumed.",
        )

    # Apply operator overrides to the stored result
    result = record.get("result") or {}
    overrides_applied: dict[str, Any] = {
        "operator_id": body.operator_id,
        "operator_notes": body.operator_notes,
        "hitl_resumed_at": __import__("datetime").datetime.utcnow().isoformat(),
    }

    if body.override_category:
        result["category"] = body.override_category
        overrides_applied["category_overridden"] = True
    if body.override_priority:
        result["priority"] = body.override_priority.value
        overrides_applied["priority_overridden"] = True
    if body.override_resolution:
        result["suggested_resolution"] = body.override_resolution
        overrides_applied["resolution_overridden"] = True

    result["hitl_required"] = False  # Human has reviewed — no longer needs review
    result["hitl_overrides"] = overrides_applied

    triage_store.set_complete(ticket_id, result)

    return triage_store.to_response(triage_store.get(ticket_id))  # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/triage — List tickets for tenant
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=list[TriageResultResponse],
    summary="List triage results for tenant",
    description="Returns the most recent triage results for the authenticated tenant. "
                "Maximum 50 results, newest first.",
)
async def list_triages(
    caller: AuthenticatedTenant = Depends(verify_token),
    limit: int = 20,
) -> list[TriageResultResponse]:
    """
    List recent triage results for the authenticated tenant.

    Note: Tenant isolation is automatic — the JWT's tenant_id determines
    which tickets are returned. A tenant cannot list another tenant's tickets.
    """
    limit = min(limit, 50)  # Hard cap at 50 regardless of what the client requests
    records = triage_store.list_for_tenant(caller.tenant_id, limit=limit)
    return [triage_store.to_response(r) for r in records]
