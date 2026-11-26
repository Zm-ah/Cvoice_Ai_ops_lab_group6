"""All API endpoints. Logfire is configured once here."""

import logfire
from dotenv import load_dotenv
from fastapi import FastAPI

from cvoice_backend.constants import APP_NAME

# Load .env into os.environ
load_dotenv()

# Configure Logfire once. Only sends traces if LOGFIRE_TOKEN is set.
logfire.configure(
    service_name=APP_NAME,
    send_to_logfire="if-token-present",
)

# Trace all PydanticAI agents
logfire.instrument_pydantic_ai()

app = FastAPI(title=APP_NAME)

# Trace every incoming request
logfire.instrument_fastapi(app)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple check that the service is running."""
    return {"status": "ok"}
