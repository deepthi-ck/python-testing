from __future__ import annotations

from dataclasses import dataclass

from orderflow.models.order import Order


class PaymentError(ValueError):
    pass


@dataclass(frozen=True)
class PaymentResult:
    accepted: bool
    reference: str
    amount_cents: int


class PaymentService:
    def authorize(self, order: Order, method: str = "card") -> PaymentResult:
        amount = order.total_cents
        if amount <= 0:
            raise PaymentError("cannot authorize a zero-total order")
        if method not in {"card", "wallet", "invoice"}:
            raise PaymentError(f"unsupported payment method {method}")
        if method == "invoice" and amount > 250_000:
            raise PaymentError("invoice limit exceeded")
        reference = f"pay-{order.id}-{method}-{amount}"
        return PaymentResult(accepted=True, reference=reference, amount_cents=amount)

    def capture_allowed(self, order: Order, authorized: bool) -> bool:
        status_ok = order.status in {"confirmed", "paid"}
        total_ok = order.total_cents > 0
        return authorized and status_ok and total_ok
