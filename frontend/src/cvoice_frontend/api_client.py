"""All HTTP calls to the backend live here."""

# No view builds a URL or reads a status code, 
# an endpoint change touches this file only.

from typing import Any

import httpx

from cvoice_frontend.constants import API_URL, REQUEST_TIMEOUT, UPLOAD_TIMEOUT


class ApiError(RuntimeError):
    """A backend call failed in a way the user should see."""


def _request(method: str, path: str, timeout: float = REQUEST_TIMEOUT, **kwargs: Any) -> Any:
    """One place for error handling, so every view fails the same way."""
    try:
        response = httpx.request(method, f"{API_URL}{path}", timeout=timeout, **kwargs)
    except httpx.RequestError as exc:
        raise ApiError(f"Could not reach the backend at {API_URL}. Is it running?") from exc

    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise ApiError(f"{response.status_code}: {detail}")

    if response.headers.get("content-type", "").startswith("application/json"):
        return response.json()
    return response.content


def upload_documents(
    files: list[tuple[str, bytes]], profile_id: str | None = None
) -> dict[str, Any]:
    """Send CV and cover letter. Pass a profile_id to replace an earlier upload."""
    payload = [("files", (name, data)) for name, data in files]
    data = {"profile_id": profile_id} if profile_id else None
    return _request("POST", "/profiles", timeout=UPLOAD_TIMEOUT, files=payload, data=data)


def delete_profile(profile_id: str) -> None:
    _request("DELETE", f"/profiles/{profile_id}")