FROM python:3.13-slim

# Copy the uv binary from the official image (same version as used locally)
COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /usr/local/bin/uv

WORKDIR /app

# Layer 1: only the dependency files. Docker reuses this layer until they change.
COPY pyproject.toml uv.lock .python-version ./
COPY backend/pyproject.toml backend/pyproject.toml
COPY frontend/pyproject.toml frontend/pyproject.toml
RUN uv sync --package cvoice-frontend --frozen --no-dev --no-install-workspace

# Layer 2: the source code and the Streamlit settings, then install the frontend package
COPY frontend/src frontend/src
COPY frontend/.streamlit .streamlit
RUN uv sync --package cvoice-frontend --frozen --no-dev

# Use the virtual environment that uv created
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8501
CMD ["streamlit", "run", "frontend/src/cvoice_frontend/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]