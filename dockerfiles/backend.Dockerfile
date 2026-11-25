FROM python:3.12-slim

# Copy the uv binary from the official image (same version as used locally)
COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /usr/local/bin/uv

WORKDIR /app

# Layer 1: only the dependency files. Docker reuses this layer until they change.
COPY pyproject.toml uv.lock .python-version ./
COPY backend/pyproject.toml backend/pyproject.toml
COPY frontend/pyproject.toml frontend/pyproject.toml
RUN uv sync --package cvoice-backend --frozen --no-dev --no-install-workspace

# Layer 2: the source code, then install the backend package itself
COPY backend/src backend/src
RUN uv sync --package cvoice-backend --frozen --no-dev


# Use the virtual environment that uv created
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "cvoice_backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
