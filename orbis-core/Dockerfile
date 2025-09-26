# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Copy SDK and Core to install in editable mode
COPY orbis-sdk/pyproject.toml /workspace/orbis-sdk/pyproject.toml
COPY orbis-sdk/README.md /workspace/orbis-sdk/README.md
COPY LICENSE /workspace/orbis-sdk/LICENSE
COPY orbis-sdk/src /workspace/orbis-sdk/src
COPY orbis-core/pyproject.toml /workspace/orbis-core/pyproject.toml
COPY orbis-core/README.md /workspace/orbis-core/README.md
COPY LICENSE /workspace/orbis-core/LICENSE
COPY orbis-core/src /workspace/orbis-core/src

RUN pip install --upgrade pip && \
    pip install -e /workspace/orbis-sdk[fastapi] && \
    pip install -e /workspace/orbis-core

ENV PYTHONPATH="/workspace/orbis-core/src:/workspace/orbis-sdk/src:${PYTHONPATH}"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--app-dir", "/workspace/orbis-core/src"]


