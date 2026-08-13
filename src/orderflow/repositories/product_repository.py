from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from orderflow.models.product import Product


class ProductRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, product: Product) -> Product:
        self._session.add(product)
        self._session.flush()
        return product

    def get(self, product_id: int) -> Product | None:
        return self._session.get(Product, product_id)

    def get_by_sku(self, sku: str) -> Product | None:
        statement = select(Product).where(Product.sku == sku)
        return self._session.scalar(statement)

    def list_active(self, limit: int = 100) -> list[Product]:
        statement = select(Product).where(Product.is_active.is_(True)).limit(limit)
        return list(self._session.scalars(statement))
