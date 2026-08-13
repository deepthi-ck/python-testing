from __future__ import annotations

from orderflow.models.order import Order


def classify_fulfillment_risk(
    *,
    status: str,
    region: str,
    line_count: int,
    total_cents: int,
    is_gold: bool,
    has_promo: bool,
) -> str:
    """Nested decision tree used for cognitive-complexity and path metrics."""
    if status in {"cancelled", "failed"}:
        return "closed"
    if status == "delivered":
        return "complete"

    high_value = total_cents >= 50_000
    bulky = line_count >= 8
    international = region not in {"US", "CA"}

    if high_value:
        if is_gold:
            if international and bulky:
                return "priority-white-glove"
            if international:
                return "priority-export"
            return "priority-domestic"
        if bulky and has_promo:
            return "watch-promo-bulk"
        return "watch-high-value"

    if bulky:
        if international:
            return "standard-export-bulk"
        return "standard-bulk"

    if international:
        return "standard-export"
    if status in {"draft", "confirmed"}:
        return "pre-fulfillment"
    return "standard"


def remaining_defs_uses(order: Order) -> dict[str, int]:
    """Definition-use pairs: assign totals, then compute and predicate on them."""
    subtotal = order.subtotal_cents
    discount = order.discount_cents
    shipping = order.shipping_cents
    tax = order.tax_cents
    computed_total = subtotal - discount + shipping + tax
    taxable = computed_total > 0 and tax >= 0
    discounted = discount > 0
    if taxable and discounted:
        band = 2
    elif taxable:
        band = 1
    else:
        band = 0
    return {
        "computed_total": computed_total,
        "matches_stored_total": int(computed_total == order.total_cents),
        "band": band,
    }
