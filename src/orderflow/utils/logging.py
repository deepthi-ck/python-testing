from __future__ import annotations

import logging
import re
from typing import Any

_PII_KEYS = frozenset({"email", "ssn", "password", "pan", "dob", "student_id", "full_name"})
_EMAIL_SHAPE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
_LOGGER = logging.getLogger("orderflow")


class PiiLogError(ValueError):
    pass


def _redact(value: Any) -> Any:
    if isinstance(value, str) and _EMAIL_SHAPE.search(value):
        return "[redacted]"
    return value


def info(event: str, **fields: Any) -> None:
    """Structured log helper that refuses PII field names (FERPA/COPPA)."""
    for key in fields:
        if key.lower() in _PII_KEYS:
            raise PiiLogError(f"refusing to log PII field {key}")
    safe = {key: _redact(value) for key, value in fields.items()}
    _LOGGER.info("%s %s", event, safe)
