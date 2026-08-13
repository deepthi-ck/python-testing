from __future__ import annotations

from orderflow.models.customer import Customer


def can_place_order(customer: Customer) -> bool:
    return bool(customer.is_active and customer.tier in {"standard", "silver", "gold"})


def can_view_audit(role: str) -> bool:
    return role in {"admin", "auditor"}
