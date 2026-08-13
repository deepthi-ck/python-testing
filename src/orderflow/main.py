from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from orderflow import __version__
from orderflow import models  # noqa: F401  — register metadata
from orderflow.api.deps import get_engine, reset_engine
from orderflow.api.routers.catalog import router as catalog_router
from orderflow.api.routers.health import router as health_router
from orderflow.api.routers.orders import router as orders_router
from orderflow.config import get_settings
from orderflow.database import Base, install_triggers


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    engine = get_engine()
    Base.metadata.create_all(engine)
    install_triggers(engine)
    yield
    reset_engine()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Retail order fulfillment API for Testable Python metric validation.",
        lifespan=lifespan,
        openapi_tags=[
            {"name": "health", "description": "Liveness and database trigger status"},
            {"name": "catalog", "description": "Customers and products"},
            {"name": "orders", "description": "Order capture, payment, and fulfillment"},
        ],
    )
    app.include_router(health_router)
    app.include_router(catalog_router)
    app.include_router(orders_router)
    return app


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run("orderflow.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    run()
