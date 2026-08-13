from __future__ import annotations

import pytest

from orderflow.analysis.control_flow import exception_path, loop_trip_coverage, nested_predicates
from orderflow.analysis.risk import classify_fulfillment_risk
from orderflow.services.fulfillment_service import FulfillmentService, IllegalTransitionError
from orderflow.services.payment_service import PaymentError, PaymentService
from orderflow.models.order import Order
from orderflow.validators.order_rules import assert_transition, is_terminal


@pytest.mark.unit
def test_state_machine_happy_and_illegal() -> None:
    fulfillment = FulfillmentService()
    order = Order(customer_id=1, status="draft")
    fulfillment.advance(order, "confirmed")
    assert order.status == "confirmed"
    with pytest.raises(IllegalTransitionError):
        fulfillment.advance(order, "shipped")
    assert is_terminal("delivered")
    with pytest.raises(Exception):
        assert_transition("draft", "unknown")


@pytest.mark.unit
def test_pick_waves_zero_one_and_n_trips() -> None:
    fulfillment = FulfillmentService()
    assert fulfillment.pick_waves([], 10) == []
    assert fulfillment.pick_waves([4], 10) == [[4]]
    waves = fulfillment.pick_waves([4, 4, 4, 1], 10)
    assert waves[0] == [4, 4]
    assert sum(sum(wave) for wave in waves) == 13
    with pytest.raises(ValueError):
        fulfillment.pick_waves([1], 0)


@pytest.mark.unit
def test_sla_and_risk_branches() -> None:
    fulfillment = FulfillmentService()
    assert fulfillment.sla_hours("delivered", "US", True) == 0
    assert fulfillment.sla_hours("paid", "US", True) < fulfillment.sla_hours("paid", "IN", False)
    assert fulfillment.sla_hours("failed", "EU", False) > 48
    assert classify_fulfillment_risk(
        status="paid", region="EU", line_count=9, total_cents=80_000, is_gold=True, has_promo=True
    ) == "priority-white-glove"
    assert classify_fulfillment_risk(
        status="cancelled", region="US", line_count=1, total_cents=1, is_gold=False, has_promo=False
    ) == "closed"
    assert classify_fulfillment_risk(
        status="paid", region="US", line_count=1, total_cents=100, is_gold=False, has_promo=False
    ) == "standard"


@pytest.mark.unit
def test_control_flow_helpers() -> None:
    assert loop_trip_coverage([], 5)["seen"] == 0
    assert loop_trip_coverage([5], 5)["accepted"] == 1
    assert loop_trip_coverage([1, 9, 3], 5)["rejected"] == 2
    assert exception_path(10, 0) == 0
    assert exception_path(-4, 2) == 2
    assert exception_path(9, 3) == 3
    assert nested_predicates(True, True, True) == "abc"
    assert nested_predicates(True, True, False) == "ab"
    assert nested_predicates(True, False, False) == "a_or_c"
    assert nested_predicates(False, False, False) == "not_b"
    assert nested_predicates(False, True, False) == "b_only"


@pytest.mark.unit
def test_payment_authorize_paths() -> None:
    payments = PaymentService()
    order = Order(customer_id=1, status="confirmed", total_cents=5000)
    order.id = 7
    result = payments.authorize(order, "card")
    assert result.accepted is True
    with pytest.raises(PaymentError):
        payments.authorize(Order(customer_id=1, total_cents=0), "card")
    with pytest.raises(PaymentError):
        payments.authorize(order, "bitcoin")
    big = Order(customer_id=1, status="confirmed", total_cents=500_000)
    big.id = 8
    with pytest.raises(PaymentError):
        payments.authorize(big, "invoice")
    assert payments.capture_allowed(order, True) is True
    assert payments.capture_allowed(order, False) is False
