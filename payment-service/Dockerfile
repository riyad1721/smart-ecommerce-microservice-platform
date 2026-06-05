FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip setuptools wheel \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt \
    && /opt/venv/bin/pip uninstall -y pip setuptools wheel


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    APP_PORT=8004

WORKDIR /app

RUN groupadd --system appuser \
    && useradd --system --gid appuser --home-dir /app --shell /usr/sbin/nologin appuser

COPY --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appuser app ./app

USER appuser

EXPOSE 8004

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import json, os, urllib.request; r=urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"APP_PORT\", \"8004\")}/api/v1/health', timeout=3); data=json.load(r); raise SystemExit(0 if r.status == 200 and data.get('status') == 'UP' else 1)"

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT:-8004} --proxy-headers"]
