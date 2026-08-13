from __future__ import annotations

from orderflow.analysis.risk import classify_fulfillment_risk
from orderflow.services.fulfillment_service import FulfillmentService
from orderflow.models.order import Order, OrderLine
from orderflow.utils.dates import utc_now_iso
from orderflow.utils.money import clamp_cents


def test_additional_risk_and_sla_branches() -> None:
    assert classify_fulfillment_risk(
        status="delivered", region="US", line_count=1, total_cents=10, is_gold=False, has_promo=False
    ) == "complete"
    assert classify_fulfillment_risk(
        status="paid", region="US", line_count=9, total_cents=80_000, is_gold=True, has_promo=False
    ) == "priority-domestic"
    assert classify_fulfillment_risk(
        status="paid", region="EU", line_count=1, total_cents=80_000, is_gold=True, has_promo=False
    ) == "priority-export"
    assert classify_fulfillment_risk(
        status="paid", region="US", line_count=9, total_cents=80_000, is_gold=False, has_promo=True
    ) == "watch-promo-bulk"
    assert classify_fulfillment_risk(
        status="paid", region="US", line_count=1, total_cents=80_000, is_gold=False, has_promo=False
    ) == "watch-high-value"
    assert classify_fulfillment_risk(
        status="paid", region="EU", line_count=9, total_cents=100, is_gold=False, has_promo=False
    ) == "standard-export-bulk"
    assert classify_fulfillment_risk(
        status="paid", region="US", line_count=9, total_cents=100, is_gold=False, has_promo=False
    ) == "standard-bulk"
    assert classify_fulfillment_risk(
        status="paid", region="EU", line_count=1, total_cents=100, is_gold=False, has_promo=False
    ) == "standard-export"
    assert classify_fulfillment_risk(
        status="draft", region="US", line_count=1, total_cents=100, is_gold=False, has_promo=False
    ) == "pre-fulfillment"


def test_can_pick_and_helpers() -> None:
    fulfillment = FulfillmentService()
    order = Order(customer_id=1, status="paid", total_cents=100)
    order.lines = [OrderLine(sku="A", quantity=1, unit_price_cents=100, line_total_cents=100)]
    assert fulfillment.can_pick(order) is True
    empty = Order(customer_id=1, status="draft", total_cents=0)
    empty.lines = []
    assert fulfillment.can_pick(empty) is False
    assert clamp_cents(99, minimum=100) == 100
    assert "T" in utc_now_iso()
