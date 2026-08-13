from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.mark.functional
def test_happy_path_pass_rate(client: TestClient, auth_headers: dict[str, str]) -> None:
    customer = client.post(
        "/customers",
        json={"email": "happy@example.com", "full_name": "Happy Path", "tier": "standard", "region": "US"},
        headers=auth_headers,
    ).json()
    product = client.post(
        "/products",
        json={
            "sku": "JAR-9",
            "name": "Honey Jar",
            "category": "grocery",
            "unit_price_cents": 1500,
            "weight_grams": 500,
            "initial_on_hand": 10,
        },
        headers=auth_headers,
    ).json()
    order = client.post(
        "/orders",
        json={"customer_id": customer["id"], "lines": [{"sku": product["sku"], "quantity": 1}]},
        headers=auth_headers,
    )
    assert order.status_code == 201
    assert order.json()["status"] == "draft"


@pytest.mark.functional
def test_invalid_partition_is_rejected(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.post(
        "/customers",
        json={"email": "not-an-email", "full_name": "Bad", "tier": "platinum", "region": "US"},
        headers=auth_headers,
    )
    assert response.status_code == 422
