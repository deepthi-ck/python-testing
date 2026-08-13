from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from orderflow.models.order import Order


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, order: Order) -> Order:
        self._session.add(order)
        self._session.flush()
        return order

    def get(self, order_id: int) -> Order | None:
        statement = (
            select(Order)
            .options(selectinload(Order.lines), selectinload(Order.customer))
            .where(Order.id == order_id)
        )
        return self._session.scalar(statement)

    def list_for_customer(self, customer_id: int, limit: int = 50) -> list[Order]:
        statement = (
            select(Order)
            .options(selectinload(Order.lines))
            .where(Order.customer_id == customer_id)
            .limit(limit)
        )
        return list(self._session.scalars(statement))
