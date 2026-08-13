from __future__ import annotations

from fastapi import Header, HTTPException, status

from orderflow.config import get_settings
from orderflow.utils.hashing import hash_secret, secrets_match


def expected_api_key_hash() -> str:
    return hash_secret(get_settings().api_key)


def authenticate_request(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    expected = get_settings().api_key
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="api key is not configured",
        )
    if not x_api_key or not secrets_match(x_api_key, hash_secret(expected)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid api key")
    return x_api_key
