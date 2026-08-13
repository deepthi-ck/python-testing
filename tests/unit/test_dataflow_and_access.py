from __future__ import annotations

from orderflow.analysis.risk import remaining_defs_uses
from orderflow.models.order import Order
from orderflow.security.access import can_place_order, can_view_audit
from orderflow.models.customer import Customer


def test_definition_use_pairs() -> None:
    order = Order(
        customer_id=1,
        status="paid",
        subtotal_cents=1000,
        discount_cents=100,
        shipping_cents=0,
        tax_cents=72,
        total_cents=972,
    )
    result = remaining_defs_uses(order)
    assert result["computed_total"] == 972
    assert result["matches_stored_total"] == 1
    assert result["band"] == 2
    zero = Order(customer_id=1, subtotal_cents=0, discount_cents=0, shipping_cents=0, tax_cents=0, total_cents=0)
    assert remaining_defs_uses(zero)["band"] == 0


def test_access_control() -> None:
    active = Customer(email="a@b.com", full_name="A", tier="gold", is_active=True)
    inactive = Customer(email="c@d.com", full_name="C", tier="gold", is_active=False)
    assert can_place_order(active) is True
    assert can_place_order(inactive) is False
    assert can_view_audit("admin") is True
    assert can_view_audit("picker") is False
