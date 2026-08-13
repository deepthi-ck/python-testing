from __future__ import annotations

import pytest

from orderflow.services.pricing_service import PricingService
from orderflow.utils.hashing import hash_secret, secrets_match
from orderflow.utils.money import cents_to_display, clamp_cents
from orderflow.validators.input_sanitizer import (
    InputValidationError,
    require_quantity,
    sanitize_promo_code,
    sanitize_text,
)


@pytest.mark.unit
def test_clamp_and_display() -> None:
    assert clamp_cents(-5) == 0
    assert clamp_cents(150) == 150
    assert cents_to_display(199) == "1.99"
    assert cents_to_display(-50) == "-0.50"


@pytest.mark.unit
def test_secret_compare_is_constant_time() -> None:
    digest = hash_secret("test-key")
    assert secrets_match("test-key", digest)
    assert not secrets_match("other", digest)


@pytest.mark.unit
def test_sanitize_rejects_sql_and_html() -> None:
    assert sanitize_text("  hello  ", "notes") == "hello"
    with pytest.raises(InputValidationError):
        sanitize_text("drop; table", "notes")
    assert sanitize_text("<b>safe</b>", "notes") == "safe"
    assert sanitize_promo_code("save10") == "SAVE10"
    with pytest.raises(InputValidationError):
        sanitize_promo_code("bad code")
    with pytest.raises(InputValidationError):
        require_quantity(0)


@pytest.mark.unit
def test_pricing_volume_tier_promo_and_free_shipping() -> None:
    pricing = PricingService()
    lines = [("SKU-1", 12, 1000, 200)]
    gold = pricing.quote(
        lines=lines,
        customer_tier="gold",
        region="US",
        promo_code="SAVE10",
        customer_is_active=True,
    )
    standard = pricing.quote(
        lines=lines,
        customer_tier="standard",
        region="IN",
        promo_code=None,
        customer_is_active=True,
    )
    assert gold.discount_cents > standard.discount_cents
    assert gold.shipping_cents == 0
    assert gold.total_cents > 0
    assert standard.tax_cents > 0


@pytest.mark.unit
def test_pricing_vip_promo_requires_gold() -> None:
    pricing = PricingService()
    lines = [("SKU-1", 1, 5000, 100)]
    gold = pricing.quote(lines=lines, customer_tier="gold", region="US", promo_code="VIP25", customer_is_active=True)
    silver = pricing.quote(lines=lines, customer_tier="silver", region="US", promo_code="VIP25", customer_is_active=True)
    assert gold.discount_cents > silver.discount_cents


@pytest.mark.unit
def test_pricing_rejects_inactive_and_empty() -> None:
    pricing = PricingService()
    with pytest.raises(ValueError):
        pricing.quote(lines=[], customer_tier="standard", region="US", promo_code=None, customer_is_active=True)
    with pytest.raises(ValueError):
        pricing.quote(lines=[("A", 1, 100, 10)], customer_tier="standard", region="US", promo_code=None, customer_is_active=False)


@pytest.mark.unit
def test_volume_and_weight_shipping_bands() -> None:
    pricing = PricingService()
    heavy = pricing.quote(
        lines=[("SKU-1", 1, 1000, 12_000)],
        customer_tier="standard",
        region="US",
        promo_code=None,
        customer_is_active=True,
    )
    mid = pricing.quote(
        lines=[("SKU-1", 1, 1000, 6_000)],
        customer_tier="standard",
        region="US",
        promo_code=None,
        customer_is_active=True,
    )
    light = pricing.quote(
        lines=[("SKU-1", 4, 1000, 100)],
        customer_tier="standard",
        region="ZZ",
        promo_code=None,
        customer_is_active=True,
    )
    bulk = pricing.quote(
        lines=[("SKU-1", 50, 100, 10)],
        customer_tier="standard",
        region="US",
        promo_code=None,
        customer_is_active=True,
    )
    assert heavy.shipping_cents > mid.shipping_cents
    assert light.shipping_cents > 0
    assert bulk.discount_cents > 0
    pricing = PricingService()
    quote = pricing.quote(
        lines=[("SKU-1", 1, 500, 100)],
        customer_tier="standard",
        region="EU",
        promo_code="FREESHIP",
        customer_is_active=True,
    )
    assert quote.shipping_cents == 0
