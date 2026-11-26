"""All API endpoints. Logfire is configured once here."""

import uuid
from typing import Annotated

import logfire
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile

from cvoice_backend import vector_store
from cvoice_backend.constants import APP_NAME, MAX_UPLOAD_BYTES
from cvoice_backend.data_models import UploadResponse
from cvoice_backend.ingestion import UnsupportedDocument, build_chunks, read_document

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


@app.post("/profiles", response_model=UploadResponse)
async def create_profile(
    files: Annotated[list[UploadFile], File(description="CV, cover letter: pdf, txt or md")],
    profile_id: Annotated[str | None, Form(description="reuse an id to replace it")] = None,
) -> UploadResponse:
    """Read the uploaded documents, split them and store them in LanceDB.

    Pass an existing profile_id to replace that person's documents.
    """
    if profile_id:
        try:
            vector_store.check_profile_id(profile_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from None
    else:
        profile_id = uuid.uuid4().hex

    sources: list[str] = []
    characters = 0
    chunks = []

    with logfire.span("upload documents", profile_id=profile_id):
        for upload in files:
            filename = upload.filename or "document.txt"
            data = await upload.read()

            if len(data) > MAX_UPLOAD_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail=f"{filename} is larger than {MAX_UPLOAD_BYTES // 1024 // 1024} MB",
                )

            try:
                text = read_document(data, filename)
            except UnsupportedDocument as exc:
                raise HTTPException(status_code=415, detail=str(exc)) from None

            if not text.strip():
                raise HTTPException(
                    status_code=422,
                    detail=(
                        f"No text found in {filename}. "
                        "A scanned PDF has to be run through OCR first."
                    ),
                )

            sources.append(filename)
            characters += len(text)
            chunks.extend(build_chunks(text, profile_id, filename))

        # Replace rather than append, re-uploading will not duplicate the CV.
        chunk_count = vector_store.replace_profile_chunks(profile_id, chunks)

    return UploadResponse(
        profile_id=profile_id,
        sources=sources,
        chunk_count=chunk_count,
        characters=characters,
    )


@app.delete("/profiles/{profile_id}", status_code=204)
def delete_profile(profile_id: str) -> Response:
    """Delete every chunk for one profile. A CV should not linger."""
    try:
        vector_store.delete_profile(profile_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    return Response(status_code=204)