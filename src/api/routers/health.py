"""
CustomerCore API — Health & Readiness Router (Phase 10)

WHY TWO SEPARATE ENDPOINTS?
------------------------------
Kubernetes distinguishes between two types of probes:

  /health (Liveness probe):
    "Is the process alive and not stuck in a deadlock?"
    Kubernetes restarts the pod if this returns non-200.
    Should be fast and simple — just return 200 if the process is running.
    Never check external services here — if Redis is down, we don't want Kubernetes
    to restart our pods in a loop (that makes the outage worse).

  /ready (Readiness probe):
    "Is the pod ready to receive traffic?"
    Kubernetes removes the pod from the load balancer if this returns non-200.
    SHOULD check external dependencies — if Redis or ChromaDB is unreachable,
    we tell Kubernetes to stop sending us traffic until they recover.
    This prevents cascading failures where pods accept requests they can't serve.

This distinction is called the "liveness vs readiness" pattern and is a standard
Kubernetes production practice.
"""

from __future__ import annotations

import os
import time

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.api.models import HealthResponse

router = APIRouter(prefix="/api/v1", tags=["Health"])

# Track API start time for uptime reporting
_START_TIME = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 if the API process is alive. Used by Kubernetes liveness probes. "
                "Does NOT check external service connectivity.",
)
async def health() -> HealthResponse:
    """
    Liveness probe — always returns 200 if the process is running.

    Kubernetes uses this to decide: "Should I restart this pod?"
    Answer: Only if the process itself is stuck/crashed, not if a dependency is down.
    """
    return HealthResponse(
        status="ok",
        version="1.0.0",
        services={},  # No external checks — intentionally empty for liveness
    )


@router.get(
    "/ready",
    summary="Readiness probe",
    description="Returns 200 if all dependencies are reachable. Used by Kubernetes readiness "
                "probes. Checks Redis, ChromaDB, and optionally Supabase connectivity.",
)
async def readiness() -> JSONResponse:
    """
    Readiness probe — checks all critical external dependencies.

    Kubernetes uses this to decide: "Should I send traffic to this pod?"
    If Redis is down, return 503 — let another pod handle the request.
    """
    service_status: dict[str, str] = {}
    overall_ok = True

    # ── Check Redis ──────────────────────────────────────────────────────────
    try:
        import redis as redis_lib  # type: ignore
        r = redis_lib.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379"),
            socket_connect_timeout=1,
            socket_timeout=1,
        )
        r.ping()
        service_status["redis"] = "ok"
    except Exception as exc:
        service_status["redis"] = f"error: {exc}"
        overall_ok = False

    # ── Check ChromaDB ───────────────────────────────────────────────────────
    try:
        import chromadb  # type: ignore
        client = chromadb.HttpClient(
            host=os.getenv("CHROMADB_HOST", "localhost"),
            port=int(os.getenv("CHROMADB_PORT", "8000")),
        )
        client.heartbeat()
        service_status["chromadb"] = "ok"
    except Exception as exc:
        service_status["chromadb"] = f"error: {exc}"
        # ChromaDB is not critical for basic triage (BM25 fallback exists)
        # Don't mark overall as failed for ChromaDB — degraded mode is acceptable

    # ── Supabase (optional — only if configured) ─────────────────────────────
    supabase_url = os.getenv("SUPABASE_URL")
    if supabase_url:
        try:
            import httpx
            resp = httpx.get(f"{supabase_url}/rest/v1/", timeout=2.0)
            service_status["supabase"] = "ok" if resp.status_code < 500 else f"http_{resp.status_code}"
        except Exception as exc:
            service_status["supabase"] = f"error: {exc}"
            overall_ok = False
    else:
        service_status["supabase"] = "not_configured"

    uptime_seconds = int(time.time() - _START_TIME)

    body = {
        "status": "ok" if overall_ok else "degraded",
        "version": "1.0.0",
        "uptime_seconds": uptime_seconds,
        "services": service_status,
    }
    return JSONResponse(
        content=body,
        status_code=200 if overall_ok else 503,
    )
