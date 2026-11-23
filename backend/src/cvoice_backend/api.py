"""All API endpoints. Logfire setup goes here later."""
from fastapi import FastAPI

from cvoice_backend.constants import APP_NAME

app = FastAPI(title=APP_NAME)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple check that the service is running."""
    return {"status": "ok"}
