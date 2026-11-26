"""Read documents: PDF to text, then split into chunks."""

# Pure functions only, no network and no database.
# This is the part of the pipeline that can be tested without an API key.

import io
import re
import uuid
from pathlib import Path

from pypdf import PdfReader

from cvoice_backend.constants import ALLOWED_SUFFIXES, CHUNK_OVERLAP, CHUNK_SIZE
from cvoice_backend.data_models import Chunk


class UnsupportedDocument(ValueError):
    """Raised when a file type we cannot read is uploaded."""


def read_document(data: bytes, filename: str) -> str:
    """Turn an uploaded file into plain text."""
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise UnsupportedDocument(
            f"{filename}: {suffix or 'no file extension'} is not supported. "
            f"Allowed: {', '.join(ALLOWED_SUFFIXES)}"
        )

    if suffix == ".pdf":
        reader = PdfReader(io.BytesIO(data))
        text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        text = data.decode("utf-8", errors="replace")

    return normalise_whitespace(text)


def normalise_whitespace(text: str) -> str:
    """Clean up the ragged spacing that PDF extraction leaves behind."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks, preferring paragraph breaks.

    The overlap is what lets a sentence on a boundary be found from either side.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:].strip())
            break

        # Cut at a paragraph break if there is one, then a sentence end,
        # then a space. Never in the middle of a word.
        window = text[start:end]
        cut = max(window.rfind("\n\n"), window.rfind(". "), window.rfind("\n"))
        if cut < chunk_size // 2:
            cut = window.rfind(" ")
        if cut < chunk_size // 2:
            cut = len(window)

        chunks.append(text[start : start + cut].strip())
        start = start + cut - overlap

    return [chunk for chunk in chunks if chunk]


def build_chunks(text: str, profile_id: str, source: str) -> list[Chunk]:
    """Split a document and tag every piece with the profile it belongs to."""
    return [
        Chunk(
            chunk_id=str(uuid.uuid4()),
            profile_id=profile_id,
            text=piece,
            source=source,
            position=position,
        )
        for position, piece in enumerate(split_text(text))
    ]