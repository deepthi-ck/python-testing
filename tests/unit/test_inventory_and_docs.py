from __future__ import annotations

import pytest

from orderflow.database import Base, create_db_engine, create_session_factory, install_triggers
from orderflow.models.inventory import InventoryLot
from orderflow.models.order import Order, OrderLine
from orderflow.models.product import Product
from orderflow.repositories.inventory_repository import InventoryRepository
from orderflow.services.inventory_service import InsufficientStockError, InventoryService
from orderflow.services.packing_service import PackingService
from orderflow.services.reporting_service import ReportingService


def test_inventory_reserve_release_ship_and_restock() -> None:
    engine = create_db_engine()
    Base.metadata.create_all(engine)
    install_triggers(engine)
    session = create_session_factory(engine)()
    product = Product(sku="BOX-1", name="Box", category="packaging", unit_price_cents=200, weight_grams=50)
    session.add(product)
    session.flush()
    session.add(InventoryLot(product_id=product.id, sku="BOX-1", warehouse="ATL", on_hand=5, reserved=0))
    session.flush()
    service = InventoryService(InventoryRepository(session))
    service.reserve([("BOX-1", 2)])
    assert service.available("BOX-1") == 3
    service.release([("BOX-1", 1)])
    assert service.available("BOX-1") == 4
    service.ship([("BOX-1", 1)])
    assert service.available("BOX-1") == 4
    service.restock("BOX-1", 2)
    assert service.available("BOX-1") == 6
    with pytest.raises(InsufficientStockError):
        service.reserve([("BOX-1", 99)])
    with pytest.raises(ValueError):
        service.restock("BOX-1", 0)
    session.close()


def test_reporting_and_packing_share_line_shape() -> None:
    order = Order(customer_id=1, status="paid", subtotal_cents=200, discount_cents=0, shipping_cents=0, tax_cents=16, total_cents=216, currency="USD")
    order.id = 3
    order.lines = [
        OrderLine(sku="A", quantity=2, unit_price_cents=100, line_total_cents=200),
    ]
    invoice = ReportingService().render_invoice(order)
    slip = PackingService().render_packing_slip(order)
    assert len(invoice["rows"]) == len(slip["rows"]) == 1
    assert invoice["title"] != slip["title"]
    assert ReportingService().summarize_status([order])["paid"] == 1
