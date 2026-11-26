"""Tests for reading documents and splitting them into chunks."""

# Nothing here calls a model, so these run without NVIDIA_API.

import pytest

from cvoice_backend.constants import SAMPLE_PROFILES_PATH
from cvoice_backend.ingestion import (
    UnsupportedDocument,
    build_chunks,
    normalise_whitespace,
    read_document,
    split_text,
)

KARIN_CV = SAMPLE_PROFILES_PATH / "karin_ekholm" / "cv.pdf"


# -------- reading --------


def test_read_txt() -> None:
    text = read_document(b"Hello  world\r\n\r\n\r\n\r\nSecond part", "notes.txt")
    assert text == "Hello world\n\nSecond part"


def test_read_rejects_unsupported_type() -> None:
    with pytest.raises(UnsupportedDocument):
        read_document(b"anything", "cv.docx")


def test_read_rejects_file_without_extension() -> None:
    with pytest.raises(UnsupportedDocument):
        read_document(b"anything", "cv")


def test_read_sample_pdf() -> None:
    """The sample CVs are committed, so this is a real end to end extraction."""
    text = read_document(KARIN_CV.read_bytes(), KARIN_CV.name)

    assert "Karin Ekholm" in text
    assert "Arcwise Payments AB" in text
    assert len(text) > 500


def test_normalise_whitespace_collapses_runs() -> None:
    assert normalise_whitespace("a   b\n\n\n\n\nc  ") == "a b\n\nc"


# -------- splitting --------


def test_short_text_is_one_chunk() -> None:
    assert split_text("A short CV.", chunk_size=900, overlap=150) == ["A short CV."]


def test_empty_text_gives_no_chunks() -> None:
    assert split_text("   \n  ") == []


def test_long_text_is_split_with_overlap() -> None:
    paragraph = "Data engineering at a Swedish company. " * 40
    chunks = split_text(paragraph, chunk_size=300, overlap=50)

    assert len(chunks) > 1
    # Nothing is lost at the boundaries: consecutive chunks share text.
    for first, second in zip(chunks, chunks[1:], strict=False):
        assert first[-20:] in " ".join([first, second])


def test_chunks_do_not_exceed_the_size() -> None:
    text = "word " * 1000
    for chunk in split_text(text, chunk_size=200, overlap=40):
        assert len(chunk) <= 200


def test_does_not_cut_inside_a_word() -> None:
    text = "Databricks " * 200
    for chunk in split_text(text, chunk_size=150, overlap=30):
        assert "Databrick " not in chunk


def test_overlap_must_be_smaller_than_chunk_size() -> None:
    with pytest.raises(ValueError):
        split_text("text", chunk_size=100, overlap=100)


# -------- chunk objects --------


def test_build_chunks_tags_every_piece() -> None:
    text = "Experience. " * 300
    chunks = build_chunks(text, profile_id="abc123", source="cv.pdf")

    assert len(chunks) > 1
    assert all(chunk.profile_id == "abc123" for chunk in chunks)
    assert all(chunk.source == "cv.pdf" for chunk in chunks)
    assert [chunk.position for chunk in chunks] == list(range(len(chunks)))
    assert len({chunk.chunk_id for chunk in chunks}) == len(chunks)