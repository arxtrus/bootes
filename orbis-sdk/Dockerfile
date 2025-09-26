# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install runtime deps
COPY pyproject.toml /app/pyproject.toml
COPY README.md /app/README.md
COPY src /app/src
COPY examples /app/examples

RUN pip install --upgrade pip && \
    pip install .[fastapi]

# Expose example FastAPI on 8001
EXPOSE 8001

CMD ["python", "-m", "uvicorn", "examples.fastapi_example:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]


