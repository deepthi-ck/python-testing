from __future__ import annotations

import argparse
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from orderflow.config import get_settings
from orderflow.database import Base, create_db_engine, create_session_factory, install_triggers
from orderflow.models.customer import Customer
from orderflow.models.inventory import InventoryLot
from orderflow.models.product import Product
from orderflow import models  # noqa: F401


def seed() -> None:
    settings = get_settings()
    engine = create_db_engine(settings)
    Base.metadata.create_all(engine)
    install_triggers(engine)
    session = create_session_factory(engine)()
    existing = session.scalar(select(func.count()).select_from(Customer)) or 0
    if existing > 0:
        session.close()
        return
    customers = [
        Customer(email="retail.buyer@example.com", full_name="Priya Shah", tier="gold", region="US"),
        Customer(email="cafe.owner@example.com", full_name="Noah Cole", tier="silver", region="UK"),
        Customer(email="school.shop@example.com", full_name="Jordan Lee", tier="standard", region="IN"),
    ]
    products = [
        Product(sku="MUG-ATL-1", name="Stoneware Mug", category="home", unit_price_cents=1400, weight_grams=380),
        Product(sku="TEA-ASSAM", name="Assam Tea 100g", category="grocery", unit_price_cents=850, weight_grams=120),
        Product(sku="NB-DOT-A5", name="Dotted Notebook", category="stationery", unit_price_cents=699, weight_grams=220),
    ]
    session.add_all(customers)
    session.add_all(products)
    session.flush()
    for product in products:
        session.add(InventoryLot(product_id=product.id, sku=product.sku, warehouse="ATL", on_hand=80, reserved=0))
    session.commit()
    session.close()
    db_path = settings.sqlite_path
    print(f"seeded database at {db_path or settings.database_url}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create schema, SQL triggers, and sample retail data.")
    parser.parse_args()
    Path("data/runtime").mkdir(parents=True, exist_ok=True)
    seed()


if __name__ == "__main__":
    main()
