from __future__ import annotations

from dataclasses import dataclass

from orderflow.config import get_settings
from orderflow.utils.money import clamp_cents

TIER_DISCOUNT_BPS = {"standard": 0, "silver": 500, "gold": 1000}
PROMO_BPS = {"SAVE10": 1000, "SAVE20": 2000, "FREESHIP": 0, "VIP25": 2500}
REGION_TAX_BPS = {"US": 800, "CA": 1200, "EU": 1900, "UK": 2000, "IN": 1800}
ZONE_SHIPPING = {
    "US": 799,
    "CA": 1299,
    "EU": 1899,
    "UK": 1599,
    "IN": 999,
}


@dataclass(frozen=True)
class LineQuote:
    sku: str
    quantity: int
    unit_price_cents: int
    weight_grams: int
    line_total_cents: int


@dataclass(frozen=True)
class PriceQuote:
    subtotal_cents: int
    discount_cents: int
    shipping_cents: int
    tax_cents: int
    total_cents: int
    applied_promo: str | None
    lines: tuple[LineQuote, ...]


class PricingService:
    """Quote builder with nested commercial rules.

    Cyclomatic and cognitive complexity come from real pricing forks:
    customer tier, volume breaks, promo stacking, shipping zones, and tax.
    All branches are O(n) over line items — no nested collection scans.
    """

    def quote(
        self,
        *,
        lines: list[tuple[str, int, int, int]],
        customer_tier: str,
        region: str,
        promo_code: str | None,
        customer_is_active: bool,
    ) -> PriceQuote:
        if not customer_is_active:
            raise ValueError("inactive customers cannot be quoted")
        if not lines:
            raise ValueError("at least one line is required")

        quoted_lines = []
        subtotal = 0
        total_weight = 0
        total_units = 0
        for sku, quantity, unit_price_cents, weight_grams in lines:
            line_total = unit_price_cents * quantity
            quoted_lines.append(
                LineQuote(
                    sku=sku,
                    quantity=quantity,
                    unit_price_cents=unit_price_cents,
                    weight_grams=weight_grams,
                    line_total_cents=line_total,
                )
            )
            subtotal += line_total
            total_weight += weight_grams * quantity
            total_units += quantity

        volume_bps = self._volume_discount_bps(total_units)
        tier_bps = TIER_DISCOUNT_BPS.get(customer_tier, 0)
        promo_bps, free_shipping_promo = self._promo_discount(promo_code, customer_tier)
        combined_bps = min(volume_bps + tier_bps + promo_bps, 4000)
        discount = clamp_cents((subtotal * combined_bps) // 10_000)
        discounted_subtotal = max(subtotal - discount, 0)

        shipping = self._shipping_cents(
            region=region,
            discounted_subtotal=discounted_subtotal,
            total_weight=total_weight,
            free_shipping_promo=free_shipping_promo,
            customer_tier=customer_tier,
        )
        tax = self._tax_cents(region, discounted_subtotal)
        total = clamp_cents(discounted_subtotal + shipping + tax)
        return PriceQuote(
            subtotal_cents=subtotal,
            discount_cents=discount,
            shipping_cents=shipping,
            tax_cents=tax,
            total_cents=total,
            applied_promo=promo_code,
            lines=tuple(quoted_lines),
        )

    def _volume_discount_bps(self, total_units: int) -> int:
        if total_units >= 50:
            return 1500
        if total_units >= 20:
            return 1000
        if total_units >= 10:
            return 500
        if total_units >= 5:
            return 200
        return 0

    def _promo_discount(self, promo_code: str | None, customer_tier: str) -> tuple[int, bool]:
        if promo_code is None:
            return 0, False
        if promo_code == "FREESHIP":
            return 0, True
        if promo_code == "VIP25":
            if customer_tier != "gold":
                return 0, False
            return PROMO_BPS["VIP25"], False
        return PROMO_BPS.get(promo_code, 0), False

    def _shipping_cents(
        self,
        *,
        region: str,
        discounted_subtotal: int,
        total_weight: int,
        free_shipping_promo: bool,
        customer_tier: str,
    ) -> int:
        settings = get_settings()
        qualifies_threshold = discounted_subtotal >= settings.free_shipping_threshold_cents
        gold_always_free = customer_tier == "gold" and discounted_subtotal > 0
        if free_shipping_promo or qualifies_threshold or gold_always_free:
            return 0
        base = ZONE_SHIPPING.get(region, 1499)
        if total_weight > 10_000:
            return base + 1200
        if total_weight > 5_000:
            return base + 600
        if total_weight > 2_000:
            return base + 250
        return base

    def _tax_cents(self, region: str, discounted_subtotal: int) -> int:
        bps = REGION_TAX_BPS.get(region, get_settings().default_tax_bps)
        if discounted_subtotal <= 0:
            return 0
        return clamp_cents((discounted_subtotal * bps) // 10_000)
