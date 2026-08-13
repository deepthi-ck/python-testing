from __future__ import annotations

import re

from orderflow.config import get_settings

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_HTML_TAG = re.compile(r"<[^>]*>")
_SQL_META = re.compile(r"(--|;|/\*|\*/)", re.IGNORECASE)


class InputValidationError(ValueError):
    pass


def sanitize_text(value: str | None, field_name: str, max_length: int = 500) -> str | None:
    if value is None:
        return None
    cleaned = _CONTROL_CHARS.sub("", value).strip()
    cleaned = _HTML_TAG.sub("", cleaned)
    if _SQL_META.search(cleaned):
        raise InputValidationError(f"{field_name} contains disallowed characters")
    if len(cleaned) > max_length:
        raise InputValidationError(f"{field_name} exceeds {max_length} characters")
    return cleaned or None


def sanitize_promo_code(value: str | None) -> str | None:
    cleaned = sanitize_text(value, "promo_code", max_length=32)
    if cleaned is None:
        return None
    normalized = cleaned.upper()
    if not re.fullmatch(r"[A-Z0-9\-]{3,32}", normalized):
        raise InputValidationError("promo_code must be alphanumeric")
    return normalized


def require_positive_id(value: int, field_name: str) -> int:
    if value < 1:
        raise InputValidationError(f"{field_name} must be a positive identifier")
    return value


def require_quantity(quantity: int) -> int:
    settings = get_settings()
    if quantity < settings.min_quantity:
        raise InputValidationError("quantity is below the minimum boundary")
    if quantity > settings.max_quantity:
        raise InputValidationError("quantity exceeds the maximum boundary")
    return quantity
