from __future__ import annotations

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    email: str = Field(min_length=5, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    full_name: str = Field(min_length=2, max_length=120)
    tier: str = Field(default="standard", pattern="^(standard|silver|gold)$")
    region: str = Field(default="US", min_length=2, max_length=8)


class CustomerRead(BaseModel):
    id: int
    email: str
    full_name: str
    tier: str
    region: str
    is_active: bool

    model_config = {"from_attributes": True}
