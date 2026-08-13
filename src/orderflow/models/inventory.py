from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orderflow.database import Base


class InventoryLot(Base):
    __tablename__ = "inventory_lots"
    __table_args__ = (
        UniqueConstraint("sku", "warehouse", name="uq_inventory_sku_warehouse"),
        Index("ix_inventory_sku", "sku"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    sku: Mapped[str] = mapped_column(String(40), nullable=False)
    warehouse: Mapped[str] = mapped_column(String(20), nullable=False, default="ATL")
    on_hand: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reserved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())

    product = relationship("Product", back_populates="lots")

    @property
    def available(self) -> int:
        return max(self.on_hand - self.reserved, 0)
