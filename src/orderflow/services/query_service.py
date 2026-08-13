from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from orderflow.models.inventory import InventoryLot
from orderflow.models.order import Order
from orderflow.models.product import Product


class CatalogQueryService:
    """Single-shot ORM reads. Never issues a query inside a Python loop (N+1)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def products_by_skus(self, skus: Sequence[str]) -> dict[str, Product]:
        if not skus:
            return {}
        unique = list(dict.fromkeys(skus))
        statement = select(Product).where(Product.sku.in_(unique), Product.is_active.is_(True))
        rows = list(self._session.scalars(statement))
        return {product.sku: product for product in rows}

    def lots_by_skus(self, skus: Sequence[str]) -> dict[str, InventoryLot]:
        if not skus:
            return {}
        unique = list(dict.fromkeys(skus))
        statement = select(InventoryLot).where(InventoryLot.sku.in_(unique))
        rows = list(self._session.scalars(statement))
        return {lot.sku: lot for lot in rows}

    def order_with_lines(self, order_id: int) -> Order | None:
        statement = (
            select(Order)
            .options(selectinload(Order.lines), selectinload(Order.customer))
            .where(Order.id == order_id)
        )
        return self._session.scalar(statement)
