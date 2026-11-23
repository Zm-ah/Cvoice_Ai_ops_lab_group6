FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer
COPY backend/pyproject.toml ./pyproject.toml
COPY backend/src ./src
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD ["uvicorn", "cvoice_backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
