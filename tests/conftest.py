from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("ORDERFLOW_DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("ORDERFLOW_ENVIRONMENT", "test")
os.environ.setdefault("ORDERFLOW_API_KEY", "test-key")

from orderflow.api.deps import reset_engine
from orderflow.config import get_settings
from orderflow.main import create_app


@pytest.fixture(autouse=True)
def _reset_settings() -> None:
    get_settings.cache_clear()
    reset_engine()
    yield
    reset_engine()
    get_settings.cache_clear()


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"X-API-Key": "test-key"}
