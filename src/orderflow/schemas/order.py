from __future__ import annotations

from pydantic import BaseModel, Field


class OrderLineCreate(BaseModel):
    sku: str = Field(min_length=3, max_length=40)
    quantity: int = Field(ge=1, le=10_000)


class OrderCreate(BaseModel):
    customer_id: int = Field(ge=1)
    lines: list[OrderLineCreate] = Field(min_length=1, max_length=50)
    promo_code: str | None = Field(default=None, max_length=32)
    notes: str | None = Field(default=None, max_length=500)


class OrderLineRead(BaseModel):
    sku: str
    quantity: int
    unit_price_cents: int
    line_total_cents: int

    model_config = {"from_attributes": True}


class OrderRead(BaseModel):
    id: int
    customer_id: int
    status: str
    subtotal_cents: int
    discount_cents: int
    shipping_cents: int
    tax_cents: int
    total_cents: int
    promo_code: str | None
    lines: list[OrderLineRead]

    model_config = {"from_attributes": True}


class OrderTransition(BaseModel):
    target_status: str = Field(
        pattern="^(confirmed|paid|picking|packed|shipped|delivered|cancelled|failed)$"
    )
