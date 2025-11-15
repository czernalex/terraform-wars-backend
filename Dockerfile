FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y curl gettext && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_CACHE_DIR=/tmp/uv-cache

RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 -m app

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-cache

COPY --chown=app:app . .

RUN chmod +x /app/entrypoints/entrypoint-server.sh

USER app

EXPOSE $PORT
