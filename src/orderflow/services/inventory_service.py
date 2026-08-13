from __future__ import annotations

from dataclasses import dataclass

from orderflow.models.inventory import InventoryLot
from orderflow.repositories.inventory_repository import InventoryRepository


class InsufficientStockError(ValueError):
    pass


@dataclass(frozen=True)
class Reservation:
    sku: str
    quantity: int
    warehouse: str


class InventoryService:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    def reserve(self, items: list[tuple[str, int]], warehouse: str = "ATL") -> list[Reservation]:
        if not items:
            raise ValueError("nothing to reserve")
        reservations: list[Reservation] = []
        for sku, quantity in items:
            lot = self._require_lot(sku, warehouse)
            available = lot.on_hand - lot.reserved
            if available < quantity:
                raise InsufficientStockError(f"insufficient stock for {sku}")
            lot.reserved += quantity
            reservations.append(Reservation(sku=sku, quantity=quantity, warehouse=warehouse))
        return reservations

    def release(self, items: list[tuple[str, int]], warehouse: str = "ATL") -> None:
        for sku, quantity in items:
            lot = self._require_lot(sku, warehouse)
            lot.reserved = max(lot.reserved - quantity, 0)

    def ship(self, items: list[tuple[str, int]], warehouse: str = "ATL") -> None:
        for sku, quantity in items:
            lot = self._require_lot(sku, warehouse)
            if lot.reserved < quantity or lot.on_hand < quantity:
                raise InsufficientStockError(f"cannot ship {sku}")
            lot.reserved -= quantity
            lot.on_hand -= quantity

    def restock(self, sku: str, quantity: int, warehouse: str = "ATL") -> InventoryLot:
        if quantity < 1:
            raise ValueError("restock quantity must be positive")
        lot = self._require_lot(sku, warehouse)
        lot.on_hand += quantity
        return lot

    def available(self, sku: str, warehouse: str = "ATL") -> int:
        lot = self._repository.get_by_sku(sku, warehouse)
        if lot is None:
            return 0
        return max(lot.on_hand - lot.reserved, 0)

    def _require_lot(self, sku: str, warehouse: str) -> InventoryLot:
        lot = self._repository.get_by_sku(sku, warehouse)
        if lot is None:
            raise InsufficientStockError(f"unknown sku {sku}")
        return lot
