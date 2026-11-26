"""Embedding function for LanceDB, backed by Nvidia Build."""

# Source: course repo.
# One change from the original: client is built on first use, not at import.
# Importing this, not require NVIDIA_API, or CI cannot run.

import os
from functools import lru_cache

import numpy as np
from lancedb.embeddings import TextEmbeddingFunction, get_registry
from openai import OpenAI

from cvoice_backend.constants import (
    EMBEDDER_NAME,
    EMBEDDING_DIMENSIONS,
    EMBEDDING_MODEL_NAME,
    NVIDIA_BASE_URL,
)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    """Nvidia Build speaks the OpenAI API, so the OpenAI client works here."""
    return OpenAI(
        base_url=NVIDIA_BASE_URL,
        api_key=os.environ["NVIDIA_API"],
        max_retries=3,
        timeout=60.0,
    )


@get_registry().register(EMBEDDER_NAME)
class NvidiaNemotronEmbedding(TextEmbeddingFunction):
    """Lets LanceDB embed text on its own when rows are added or searched."""

    model: str = EMBEDDING_MODEL_NAME
    dimensions: int = EMBEDDING_DIMENSIONS

    def ndims(self) -> int:
        return self.dimensions

    def _embed_one(self, text: str, input_type: str) -> np.ndarray:
        # Note, the model wants to know whether it is embedding a stored passage 
        # or a search query. 
        # The vectors differ.
        response = get_client().embeddings.create(
            model=self.model,
            input=[text],
            extra_body={"input_type": input_type},
        )
        return np.asarray(response.data[0].embedding, dtype=np.float32)

    def generate_embeddings(self, texts, *args, **kwargs):
        texts = self.sanitize_input(texts)
        return [self._embed_one(text, input_type="passage") for text in texts]

    def compute_source_embeddings(self, texts, *args, **kwargs):
        return self.generate_embeddings(texts)

    def compute_query_embeddings(self, query, *args, **kwargs):
        texts = self.sanitize_input(query)
        return [self._embed_one(text, input_type="query") for text in texts]