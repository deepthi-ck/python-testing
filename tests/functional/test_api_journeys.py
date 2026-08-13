from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def _catalog(client: TestClient, headers: dict[str, str]) -> tuple[int, str]:
    customer = client.post(
        "/customers",
        json={"email": "ada@example.com", "full_name": "Ada Lovelace", "tier": "gold", "region": "US"},
        headers=headers,
    )
    assert customer.status_code == 201, customer.text
    product = client.post(
        "/products",
        json={
            "sku": "TEA-100",
            "name": "Assam Tea",
            "category": "grocery",
            "unit_price_cents": 850,
            "weight_grams": 150,
            "initial_on_hand": 40,
        },
        headers=headers,
    )
    assert product.status_code == 201, product.text
    return customer.json()["id"], product.json()["sku"]


@pytest.mark.functional
def test_health_and_openapi_contract(client: TestClient) -> None:
    health = client.get("/health")
    assert health.status_code == 200
    body = health.json()
    assert body["status"] == "ok"
    assert body["database"] == "up"
    spec = client.get("/openapi.json")
    assert spec.status_code == 200
    payload = spec.json()
    assert payload["openapi"].startswith("3.")
    assert "/orders" in payload["paths"]
    assert "/health" in payload["paths"]


@pytest.mark.functional
def test_critical_order_journey(client: TestClient, auth_headers: dict[str, str]) -> None:
    customer_id, sku = _catalog(client, auth_headers)
    created = client.post(
        "/orders",
        json={"customer_id": customer_id, "lines": [{"sku": sku, "quantity": 3}], "promo_code": "SAVE10"},
        headers=auth_headers,
    )
    assert created.status_code == 201, created.text
    order_id = created.json()["id"]
    assert created.json()["total_cents"] > 0
    for target in ("confirmed", "paid"):
        moved = client.post(f"/orders/{order_id}/transition", json={"target_status": target}, headers=auth_headers)
        assert moved.status_code == 200, moved.text
        assert moved.json()["status"] == target
    invoice = client.get(f"/orders/{order_id}/invoice", headers=auth_headers)
    packing = client.get(f"/orders/{order_id}/packing-slip", headers=auth_headers)
    assert invoice.status_code == 200
    assert packing.status_code == 200
    assert invoice.json()["rows"]
    assert packing.json()["rows"]
    assert invoice.json()["risk"]
    assert invoice.json()["dataflow"]["matches_stored_total"] in {0, 1}


@pytest.mark.functional
def test_boundary_and_auth_failures(client: TestClient, auth_headers: dict[str, str]) -> None:
    unauthorized = client.post("/customers", json={"email": "x@y.com", "full_name": "Nope"})
    assert unauthorized.status_code == 401
    too_small = client.post(
        "/products",
        json={"sku": "X", "name": "n", "unit_price_cents": 0, "weight_grams": 1, "initial_on_hand": 0},
        headers=auth_headers,
    )
    assert too_small.status_code == 422
    customer_id, sku = _catalog(client, auth_headers)
    over_max = client.post(
        "/orders",
        json={"customer_id": customer_id, "lines": [{"sku": sku, "quantity": 50_000}]},
        headers=auth_headers,
    )
    assert over_max.status_code == 422
    missing = client.get("/orders/9999", headers=auth_headers)
    assert missing.status_code == 404
    duplicate = client.post(
        "/customers",
        json={"email": "ada@example.com", "full_name": "Ada Lovelace", "tier": "gold", "region": "US"},
        headers=auth_headers,
    )
    assert duplicate.status_code == 409
    unknown_sku = client.post(
        "/orders",
        json={"customer_id": customer_id, "lines": [{"sku": "NOPE", "quantity": 1}]},
        headers=auth_headers,
    )
    assert unknown_sku.status_code == 400
    created = client.post(
        "/orders",
        json={"customer_id": customer_id, "lines": [{"sku": sku, "quantity": 1}]},
        headers=auth_headers,
    )
    assert created.status_code == 201
    illegal = client.post(
        f"/orders/{created.json()['id']}/transition",
        json={"target_status": "shipped"},
        headers=auth_headers,
    )
    assert illegal.status_code == 409
    cancelled = client.post(
        f"/orders/{created.json()['id']}/transition",
        json={"target_status": "cancelled"},
        headers=auth_headers,
    )
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
