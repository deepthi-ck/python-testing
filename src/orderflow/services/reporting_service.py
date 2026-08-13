from __future__ import annotations

from orderflow.models.order import Order
from orderflow.utils.money import cents_to_display


class ReportingService:
    """Invoice-oriented document builder.

    Near-duplicate of PackingService on purpose so duplication detectors
    (jscpd / copydetect) have a realistic cloned formatting block.
    """

    def render_invoice(self, order: Order) -> dict[str, object]:
        rows: list[dict[str, object]] = []
        running = 0
        for line in order.lines:
            description = f"{line.sku} x {line.quantity}"
            amount = cents_to_display(line.line_total_cents)
            rows.append(
                {
                    "sku": line.sku,
                    "quantity": line.quantity,
                    "description": description,
                    "unit_price": cents_to_display(line.unit_price_cents),
                    "amount": amount,
                }
            )
            running += line.line_total_cents
        header = f"Invoice for order {order.id}"
        footer = f"Total {cents_to_display(order.total_cents)} {order.currency}"
        return {
            "title": header,
            "customer_id": order.customer_id,
            "status": order.status,
            "rows": rows,
            "subtotal": cents_to_display(order.subtotal_cents),
            "discount": cents_to_display(order.discount_cents),
            "shipping": cents_to_display(order.shipping_cents),
            "tax": cents_to_display(order.tax_cents),
            "total": cents_to_display(order.total_cents),
            "running_line_total": cents_to_display(running),
            "footer": footer,
        }

    def summarize_status(self, orders: list[Order]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for order in orders:
            counts[order.status] = counts.get(order.status, 0) + 1
        return counts
