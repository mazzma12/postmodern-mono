# Stage 1: Build the python dependencies
FROM python:3.13.1-slim-bookworm AS builder

# This approximately follows this guide: https://hynek.me/articles/docker-uv/
# Which creates a standalone environment with the dependencies.
# - Silence uv complaining about not being able to use hard links,
# - tell uv to byte-compile packages for faster application startups,
# - prevent uv from accidentally downloading isolated Python builds,
# - pick a Python (use `/usr/bin/python3.13` on uv 0.5.0 and later),
# - and finally declare `/app` as the target for `uv sync`.
ENV PYTHONUNBUFFERED=True \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Synchronize dependencies.
# This layer is cached until uv.lock or pyproject.toml change.
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
      --frozen \
      --no-dev \
      --no-install-workspace \
      --package=postmodern-server

COPY . /app

RUN --mount=type=cache,target=/root/.cache \
    uv sync --frozen \
        --package=postmodern-server

# Stage 2: Final runtime image
FROM python:3.13.1-slim-bookworm

# Create non-root user
RUN groupadd -r app && \
    useradd -r -d /app -g app -N app

USER app
WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app /app

# make sure we use the virtualenv python by default
ENV PATH="/app/.venv/bin:$PATH"

# smoke test that the application can, in fact, be imported.
RUN python -V && \
    python -Im site && \
    python -c "import postmodern.server"

CMD ["python", "/app/apps/server/postmodern/server/run.py"]
