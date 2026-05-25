# ─────────────────────────────────────────────────────────────────────────────
# CustomerCore — Production Dockerfile (Phase 10)
#
# WHY MULTI-STAGE BUILD?
# Multi-stage builds separate the build environment from the runtime environment.
# Stage 1 (builder): Installs all dependencies including build tools (gcc, etc.)
# Stage 2 (runtime): Copies only the installed packages, not the build tools.
# Result: Final image is ~60% smaller, has a smaller attack surface (no gcc in prod).
#
# This image is for the full CustomerCore stack including PySpark/JVM.
# For Hugging Face Spaces deployment (2 vCPU, 16GB RAM), use Dockerfile.hf
# which strips PySpark to fit within HF's resource limits.
#
# BASE IMAGE CHOICE: python:3.12-slim-bookworm
# - slim: Minimal Debian Bookworm (no docs, man pages, debug tools)
# - bookworm: Debian 12 LTS — security patches until 2028
# - Not alpine: PySpark's JVM has compatibility issues with Alpine's musl libc
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: Builder ─────────────────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

# Set build environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies (only needed at build time, not runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a prefix directory (not system Python)
# This makes it easy to copy just the packages into the runtime stage
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    sed -i '/pywin32/d' requirements.txt && \
    pip install --prefix=/install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS runtime

# Labels for Docker Hub / GitHub Container Registry metadata
LABEL org.opencontainers.image.title="CustomerCore API" \
      org.opencontainers.image.description="Enterprise B2B AI Customer Support Platform" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Saibalaji Namburi" \
      org.opencontainers.image.source="https://github.com/saibalajinamburi/CustomerCore"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    APP_ENV=production \
    PORT=8080

# Runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (security best practice)
# Running as root in a container is a major security risk:
# if the container is compromised, root in the container = root on the host
# when using certain Docker configurations.
RUN groupadd -r customercore && useradd -r -g customercore customercore

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source code
COPY src/ ./src/
COPY pyproject.toml .

# Create directories that the app needs at runtime
RUN mkdir -p logs data/bronze data/silver data/gold \
    && chown -R customercore:customercore /app

# Switch to non-root user
USER customercore

# Health check — Docker checks this every 30s to know if the container is healthy
# If it fails 3 times in a row, Docker marks the container as unhealthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/v1/health || exit 1

# Expose the API port
EXPOSE ${PORT}

# Production server command:
# - uvicorn: ASGI server for FastAPI
# - workers: Set to CPU count (2 for HF Spaces, 4+ for Kubernetes)
# - host 0.0.0.0: Listen on all interfaces (required in containers)
# - log-level warning: Reduce noise (our structlog middleware handles request logging)
# - no-access-log: Disabled — our middleware logs structured JSON instead
CMD ["uvicorn", "src.api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8080", \
     "--workers", "2", \
     "--log-level", "warning", \
     "--no-access-log"]
