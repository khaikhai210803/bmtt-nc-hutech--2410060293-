from typing import Any

import requests

API_BASE_URL = "http://127.0.0.1:5000"


class APIClientError(Exception):
    pass


def request_json(method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            timeout=10,
            **kwargs,
        )
    except requests.RequestException as exc:
        raise APIClientError(
            f"Cannot connect to the API at {API_BASE_URL}. Start api.py first."
        ) from exc

    try:
        payload = response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise APIClientError("The API returned an invalid JSON response.") from exc

    if not isinstance(payload, dict):
        raise APIClientError("The API response must be a JSON object.")

    if not response.ok:
        message = payload.get("error", response.reason)
        raise APIClientError(str(message))

    return payload
