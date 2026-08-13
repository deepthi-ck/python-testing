from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from orderflow.database import create_db_engine, create_session_factory, get_settings
from orderflow.repositories.customer_repository import CustomerRepository
from orderflow.repositories.inventory_repository import InventoryRepository
from orderflow.repositories.order_repository import OrderRepository
from orderflow.repositories.product_repository import ProductRepository
from orderflow.security.auth import authenticate_request
from orderflow.services.fulfillment_service import FulfillmentService
from orderflow.services.inventory_service import InventoryService
from orderflow.services.order_service import CatalogService, OrderService
from orderflow.services.packing_service import PackingService
from orderflow.services.payment_service import PaymentService
from orderflow.services.pricing_service import PricingService
from orderflow.services.reporting_service import ReportingService

_ENGINE = None
_FACTORY = None


def reset_engine() -> None:
    global _ENGINE, _FACTORY
    _ENGINE = None
    _FACTORY = None


def get_engine():
    global _ENGINE, _FACTORY
    if _ENGINE is None:
        _ENGINE = create_db_engine(get_settings())
        _FACTORY = create_session_factory(_ENGINE)
    return _ENGINE


def get_session() -> Generator[Session, None, None]:
    get_engine()
    assert _FACTORY is not None
    session = _FACTORY()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_catalog_service(session: Session = Depends(get_session)) -> CatalogService:
    return CatalogService(
        CustomerRepository(session),
        ProductRepository(session),
        InventoryRepository(session),
    )


def get_order_service(session: Session = Depends(get_session)) -> OrderService:
    inventory_repo = InventoryRepository(session)
    return OrderService(
        orders=OrderRepository(session),
        customers=CustomerRepository(session),
        products=ProductRepository(session),
        inventory=InventoryService(inventory_repo),
        pricing=PricingService(),
        fulfillment=FulfillmentService(),
        payments=PaymentService(),
    )


def get_reporting_service() -> ReportingService:
    return ReportingService()


def get_packing_service() -> PackingService:
    return PackingService()


RequireApiKey = Depends(authenticate_request)
