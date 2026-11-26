"""Test file for the vector store, a fake embedder instead of Nvidia Build."""

# Our own code is tested: a profile only sees its own chunks,
# when re-uploading it will replace instead of duplicate.

import numpy as np
import pytest
from lancedb.embeddings import TextEmbeddingFunction, get_registry

from cvoice_backend import vector_store
from cvoice_backend.data_models import Chunk

FAKE_EMBEDDER_NAME = "fake-test-embedder"
# Change, if needed.
FAKE_DIMENSIONS = 8


@get_registry().register(FAKE_EMBEDDER_NAME)
class FakeEmbedding(TextEmbeddingFunction):
    """Deterministic vectors from the text itself. No network."""

    dimensions: int = FAKE_DIMENSIONS

    def ndims(self) -> int:
        return self.dimensions

    def _embed_one(self, text: str) -> np.ndarray:
        rng = np.random.default_rng(abs(hash(text)) % (2**32))
        return rng.random(self.dimensions, dtype=np.float32)

    def generate_embeddings(self, texts, *args, **kwargs):
        return [self._embed_one(text) for text in self.sanitize_input(texts)]

    def compute_source_embeddings(self, texts, *args, **kwargs):
        return self.generate_embeddings(texts)

    def compute_query_embeddings(self, query, *args, **kwargs):
        return self.generate_embeddings(query)


@pytest.fixture
def store(tmp_path, monkeypatch):
    """Point the store at a temp folder and the fake embedder."""
    monkeypatch.setattr(vector_store, "KNOWLEDGE_BASE_PATH", tmp_path / "knowledge_base")
    monkeypatch.setattr(vector_store, "EMBEDDER_NAME", FAKE_EMBEDDER_NAME)
    vector_store.get_chunk_model.cache_clear()
    yield vector_store
    vector_store.get_chunk_model.cache_clear()


def make_chunks(profile_id: str, texts: list[str], source: str = "cv.pdf") -> list[Chunk]:
    return [
        Chunk(
            chunk_id=f"{profile_id}-{position}",
            profile_id=profile_id,
            text=text,
            source=source,
            position=position,
        )
        for position, text in enumerate(texts)
    ]


def test_add_and_count(store) -> None:
    written = store.add_chunks(make_chunks("aaa111", ["Python and Spark", "Azure and dbt"]))

    assert written == 2
    assert store.count_chunks("aaa111") == 2


def test_adding_nothing_is_allowed(store) -> None:
    assert store.add_chunks([]) == 0


def test_search_never_crosses_profiles(store) -> None:
    store.add_chunks(make_chunks("aaa111", ["Karin works with Snowflake"]))
    store.add_chunks(make_chunks("bbb222", ["Jonas works with Kafka"]))

    hits = store.search("Snowflake", profile_id="aaa111", limit=5)

    assert hits, "expected at least one hit for the profile that has the text"
    assert all(hit.profile_id == "aaa111" for hit in hits)
    assert all("Jonas" not in hit.text for hit in hits)


def test_delete_profile_leaves_the_others_alone(store) -> None:
    store.add_chunks(make_chunks("aaa111", ["one", "two"]))
    store.add_chunks(make_chunks("bbb222", ["three"]))

    store.delete_profile("aaa111")

    assert store.count_chunks("aaa111") == 0
    assert store.count_chunks("bbb222") == 1


def test_reupload_replaces_instead_of_duplicating(store) -> None:
    """What the upload endpoint does when it is given a profile_id."""
    store.add_chunks(make_chunks("aaa111", ["old version of the CV"]))

    written = store.replace_profile_chunks(
        "aaa111", make_chunks("aaa111", ["new version", "with more detail"])
    )

    assert written == 2
    assert store.count_chunks("aaa111") == 2


def test_search_on_an_empty_table_returns_nothing(store) -> None:
    assert store.search("anything", profile_id="aaa111") == []


@pytest.mark.parametrize("bad_id", ["", "not valid!", "../escape", "a" * 65])
def test_invalid_profile_ids_are_rejected(bad_id: str) -> None:
    with pytest.raises(ValueError):
        vector_store.check_profile_id(bad_id)