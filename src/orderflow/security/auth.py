from __future__ import annotations

from fastapi import Header, HTTPException, status

from orderflow.config import get_settings
from orderflow.utils.hashing import hash_secret, secrets_match


def expected_api_key_hash() -> str:
    return hash_secret(get_settings().api_key)


def authenticate_request(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    if not x_api_key or not secrets_match(x_api_key, expected_api_key_hash()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid api key")
    return x_api_key
