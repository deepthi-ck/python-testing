from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from orderflow.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, customer: Customer) -> Customer:
        self._session.add(customer)
        self._session.flush()
        return customer

    def get(self, customer_id: int) -> Customer | None:
        return self._session.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        statement = select(Customer).where(Customer.email == email)
        return self._session.scalar(statement)

    def list_active(self, limit: int = 50) -> list[Customer]:
        statement = select(Customer).where(Customer.is_active.is_(True)).limit(limit)
        return list(self._session.scalars(statement))
