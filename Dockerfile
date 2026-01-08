FROM python:3.14-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.9.22 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

COPY . /app

FROM python:3.14-slim AS runtime

RUN apt update && apt install -y --no-install-recommends \
    curl \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid 999 app \
 && useradd --system --gid 999 --uid 999 --create-home app

COPY --from=build --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER app
WORKDIR /app
