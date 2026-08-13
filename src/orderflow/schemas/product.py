from __future__ import annotations

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str = Field(min_length=3, max_length=40, pattern=r"^[A-Z0-9\-]+$")
    name: str = Field(min_length=2, max_length=160)
    category: str = Field(default="general", max_length=60)
    unit_price_cents: int = Field(ge=1, le=10_000_000)
    weight_grams: int = Field(ge=1, le=100_000)
    initial_on_hand: int = Field(default=0, ge=0, le=1_000_000)


class ProductRead(BaseModel):
    id: int
    sku: str
    name: str
    category: str
    unit_price_cents: int
    weight_grams: int
    is_active: bool

    model_config = {"from_attributes": True}
