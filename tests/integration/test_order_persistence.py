from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from orderflow.database import Base, create_db_engine, create_session_factory, install_triggers
from orderflow.models.customer import Customer
from orderflow.models.inventory import InventoryLot
from orderflow.models.product import Product
from orderflow.repositories.customer_repository import CustomerRepository
from orderflow.repositories.inventory_repository import InventoryRepository
from orderflow.repositories.order_repository import OrderRepository
from orderflow.repositories.product_repository import ProductRepository
from orderflow.schemas.order import OrderCreate, OrderLineCreate
from orderflow.services.fulfillment_service import FulfillmentService
from orderflow.services.inventory_service import InsufficientStockError, InventoryService
from orderflow.services.order_service import OrderService
from orderflow.services.payment_service import PaymentService
from orderflow.services.pricing_service import PricingService


def _session() -> Session:
    engine = create_db_engine()
    Base.metadata.create_all(engine)
    install_triggers(engine)
    return create_session_factory(engine)()


def _seed(session: Session) -> tuple[Customer, Product]:
    customer = Customer(email="buyer@example.com", full_name="Buyer One", tier="silver", region="US")
    session.add(customer)
    session.flush()
    product = Product(sku="MUG-1", name="Ceramic Mug", category="home", unit_price_cents=1200, weight_grams=400)
    session.add(product)
    session.flush()
    session.add(InventoryLot(product_id=product.id, sku=product.sku, warehouse="ATL", on_hand=20, reserved=0))
    session.flush()
    return customer, product


@pytest.mark.integration
def test_create_order_reserves_stock_and_writes_audit() -> None:
    session = _session()
    customer, product = _seed(session)
    inventory = InventoryService(InventoryRepository(session))
    service = OrderService(
        orders=OrderRepository(session),
        customers=CustomerRepository(session),
        products=ProductRepository(session),
        inventory=inventory,
        pricing=PricingService(),
        fulfillment=FulfillmentService(),
        payments=PaymentService(),
    )
    order = service.create_order(
        OrderCreate(customer_id=customer.id, lines=[OrderLineCreate(sku=product.sku, quantity=2)])
    )
    session.commit()
    assert order.total_cents > 0
    assert inventory.available(product.sku) == 18
    rows = session.execute(
        __import__("sqlalchemy").text("SELECT COUNT(*) FROM audit_events WHERE entity_type='order'")
    ).scalar()
    assert int(rows or 0) >= 1
    session.close()


@pytest.mark.integration
def test_insufficient_stock_is_rejected() -> None:
    session = _session()
    customer, product = _seed(session)
    service = OrderService(
        orders=OrderRepository(session),
        customers=CustomerRepository(session),
        products=ProductRepository(session),
        inventory=InventoryService(InventoryRepository(session)),
        pricing=PricingService(),
        fulfillment=FulfillmentService(),
        payments=PaymentService(),
    )
    with pytest.raises(InsufficientStockError):
        service.create_order(
            OrderCreate(customer_id=customer.id, lines=[OrderLineCreate(sku=product.sku, quantity=500)])
        )
    session.close()
