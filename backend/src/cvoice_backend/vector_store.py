"""Vector store: add, search and delete document chunks."""

# The rows carries a profile_id, every search filters on it.
# Without the filter, the two CVs uploaded in the same demo would blend together.

# LanceDB embeds the text itself through the registry in embedders.py file,
# nothing here handles the vectors directly.

import re
from functools import lru_cache

import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector

from cvoice_backend import embedders  # noqa: F401  (LLM-note: registers the embedder)
from cvoice_backend.constants import (
    CHUNKS_TABLE,
    EMBEDDER_NAME,
    KNOWLEDGE_BASE_PATH,
    SEARCH_TOP_K,
)
from cvoice_backend.data_models import Chunk

# As explained and sourced from LLMs:
# profile_ids are uuid hex strings we create ourselves. Checking them before
# they reach a filter expression keeps the query safe.
PROFILE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def check_profile_id(profile_id: str) -> str:
    """Raise if a profile_id is not one of ours."""
    if not PROFILE_ID_PATTERN.match(profile_id):
        raise ValueError(f"Invalid profile_id: {profile_id!r}")
    return profile_id


@lru_cache(maxsize=1)
def get_chunk_model() -> type[LanceModel]:
    """The table schema. text is embedded automatically into vector."""
    embedder = get_registry().get(EMBEDDER_NAME).create()

    class ChunkRecord(LanceModel):
        text: str = embedder.SourceField()
        vector: Vector(embedder.ndims()) = embedder.VectorField()
        chunk_id: str
        profile_id: str
        source: str
        position: int

    return ChunkRecord


def get_table() -> lancedb.table.Table:
    """Open the chunks table, creating it the first time."""
    KNOWLEDGE_BASE_PATH.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(KNOWLEDGE_BASE_PATH)
    return db.create_table(CHUNKS_TABLE, schema=get_chunk_model(), exist_ok=True)


def add_chunks(chunks: list[Chunk]) -> int:
    """Store chunks. LanceDB creates the embeddings. Returns rows written."""
    if not chunks:
        return 0

    rows = [
        {
            "text": chunk.text,
            "chunk_id": chunk.chunk_id,
            "profile_id": check_profile_id(chunk.profile_id),
            "source": chunk.source,
            "position": chunk.position,
        }
        for chunk in chunks
    ]
    get_table().add(rows)
    return len(rows)


def search(query: str, profile_id: str, limit: int = SEARCH_TOP_K) -> list[Chunk]:
    """Closest chunks for one profile. Never crosses into another profile."""
    check_profile_id(profile_id)
    table = get_table()
    if table.count_rows() == 0:
        return []

    hits = (
        table.search(query)
        .where(f"profile_id = '{profile_id}'", prefilter=True)
        .limit(limit)
        .to_list()
    )
    return [
        Chunk(
            chunk_id=hit["chunk_id"],
            profile_id=hit["profile_id"],
            text=hit["text"],
            source=hit["source"],
            position=hit["position"],
        )
        for hit in hits
    ]


def replace_profile_chunks(profile_id: str, chunks: list[Chunk]) -> int:
    """Swap one profile's chunks for new ones. What a re-upload does."""
    delete_profile(profile_id)
    return add_chunks(chunks)


def delete_profile(profile_id: str) -> None:
    """Remove every chunk belonging to one profile."""
    check_profile_id(profile_id)
    get_table().delete(f"profile_id = '{profile_id}'")


def count_chunks(profile_id: str | None = None) -> int:
    """Rows in the table, for everyone or for one profile."""
    table = get_table()
    if profile_id is None:
        return table.count_rows()
    check_profile_id(profile_id)
    return table.count_rows(f"profile_id = '{profile_id}'")