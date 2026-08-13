from __future__ import annotations

from orderflow.models.order import Order
from orderflow.validators.order_rules import assert_transition, is_terminal


class IllegalTransitionError(ValueError):
    pass


class FulfillmentService:
    """Order lifecycle with nested path, loop, and exception coverage."""

    def advance(self, order: Order, target_status: str) -> Order:
        try:
            assert_transition(order.status, target_status)
        except ValueError as exc:
            raise IllegalTransitionError(str(exc)) from exc
        if is_terminal(order.status):
            raise IllegalTransitionError("terminal orders cannot move")
        order.status = target_status
        return order

    def can_pick(self, order: Order) -> bool:
        has_lines = bool(order.lines)
        paid = order.status == "paid"
        positive_total = order.total_cents > 0
        return has_lines and paid and positive_total

    def pick_waves(self, quantities: list[int], capacity: int) -> list[list[int]]:
        """Split pick quantities into waves. Covers zero, one, and n-trip loops."""
        if capacity < 1:
            raise ValueError("capacity must be positive")
        waves: list[list[int]] = []
        current: list[int] = []
        loaded = 0
        for quantity in quantities:
            if quantity <= 0:
                continue
            if loaded + quantity > capacity and current:
                waves.append(current)
                current = []
                loaded = 0
            current.append(quantity)
            loaded += quantity
        if current:
            waves.append(current)
        return waves

    def sla_hours(self, status: str, region: str, is_gold: bool) -> int:
        if status in {"delivered", "cancelled"}:
            return 0
        if region in {"US", "CA"}:
            baseline = 24
        elif region in {"EU", "UK"}:
            baseline = 48
        else:
            baseline = 72
        if is_gold and status in {"paid", "picking", "packed"}:
            return max(baseline // 2, 6)
        if status == "failed":
            return baseline + 12
        return baseline
