from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from orderflow.models.inventory import InventoryLot


class InventoryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, lot: InventoryLot) -> InventoryLot:
        self._session.add(lot)
        self._session.flush()
        return lot

    def get_by_sku(self, sku: str, warehouse: str = "ATL") -> InventoryLot | None:
        statement = select(InventoryLot).where(
            InventoryLot.sku == sku,
            InventoryLot.warehouse == warehouse,
        )
        return self._session.scalar(statement)

    def list_for_skus(self, skus: list[str]) -> list[InventoryLot]:
        if not skus:
            return []
        statement = select(InventoryLot).where(InventoryLot.sku.in_(skus))
        return list(self._session.scalars(statement))
