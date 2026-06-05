# syntax=docker/dockerfile:1.7

FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/opt/venv

WORKDIR /build

RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip setuptools wheel


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    APP_PORT=8002

WORKDIR /app

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup --home /app --no-create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appgroup app ./app

USER appuser

EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"APP_PORT\", \"8002\")}/api/v1/health', timeout=3).read()" || exit 1

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT:-8002} --proxy-headers"]
