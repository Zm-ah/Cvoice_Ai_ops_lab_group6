"""API tests."""

# Paths that fail before an embedding.
# CI runs without NVIDIA_API. For now, a real upload is checked manually.

from fastapi.testclient import TestClient

from cvoice_backend.api import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_rejects_unsupported_file_type() -> None:
    response = client.post(
        "/profiles",
        files={"files": ("cv.docx", b"not a pdf", "application/octet-stream")},
    )
    assert response.status_code == 415
    assert ".docx" in response.json()["detail"]


def test_upload_rejects_a_bad_profile_id() -> None:
    response = client.post(
        "/profiles",
        files={"files": ("cv.txt", b"some text", "text/plain")},
        data={"profile_id": "not a valid id!"},
    )
    assert response.status_code == 422


def test_delete_rejects_a_bad_profile_id() -> None:
    assert client.delete("/profiles/not valid!").status_code == 422