from __future__ import annotations

from orderflow.models.order import ORDER_STATUSES
from orderflow.validators.input_sanitizer import InputValidationError

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "draft": {"confirmed", "cancelled"},
    "confirmed": {"paid", "cancelled"},
    "paid": {"picking", "cancelled", "failed"},
    "picking": {"packed", "failed"},
    "packed": {"shipped", "failed"},
    "shipped": {"delivered", "failed"},
    "delivered": set(),
    "cancelled": set(),
    "failed": set(),
}


def assert_transition(current: str, target: str) -> None:
    if target not in ORDER_STATUSES:
        raise InputValidationError(f"unknown status {target}")
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise InputValidationError(f"cannot move from {current} to {target}")


def is_terminal(status: str) -> bool:
    return status in {"delivered", "cancelled", "failed"}
