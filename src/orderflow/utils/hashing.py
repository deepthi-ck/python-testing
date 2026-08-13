from __future__ import annotations

import hashlib
import hmac


def hash_secret(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def secrets_match(raw: str, expected_hash: str) -> bool:
    actual = hash_secret(raw)
    return hmac.compare_digest(actual, expected_hash)
