from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from orderflow.analysis.risk import classify_fulfillment_risk, remaining_defs_uses
from orderflow.api.deps import (
    RequireApiKey,
    get_order_service,
    get_packing_service,
    get_reporting_service,
)
from orderflow.schemas.order import OrderCreate, OrderRead, OrderTransition
from orderflow.services.order_service import OrderService
from orderflow.services.packing_service import PackingService
from orderflow.services.reporting_service import ReportingService
from orderflow.validators.input_sanitizer import InputValidationError

router = APIRouter(tags=["orders"])


@router.post(
    "/orders",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[RequireApiKey],
)
def create_order(
    payload: OrderCreate,
    service: OrderService = Depends(get_order_service),
) -> OrderRead:
    try:
        order = service.create_order(payload)
    except InputValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return OrderRead.model_validate(order)


@router.get("/orders/{order_id}", response_model=OrderRead, dependencies=[RequireApiKey])
def get_order(order_id: int, service: OrderService = Depends(get_order_service)) -> OrderRead:
    try:
        order = service.get_order(order_id)
    except InputValidationError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return OrderRead.model_validate(order)


@router.post(
    "/orders/{order_id}/transition",
    response_model=OrderRead,
    dependencies=[RequireApiKey],
)
def transition_order(
    order_id: int,
    payload: OrderTransition,
    service: OrderService = Depends(get_order_service),
) -> OrderRead:
    try:
        order = service.transition(order_id, payload.target_status)
    except InputValidationError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return OrderRead.model_validate(order)


@router.get("/orders/{order_id}/invoice", dependencies=[RequireApiKey])
def invoice(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    reporting: ReportingService = Depends(get_reporting_service),
) -> dict[str, object]:
    order = _load(service, order_id)
    document = reporting.render_invoice(order)
    document["risk"] = classify_fulfillment_risk(
        status=order.status,
        region=order.customer.region if order.customer else "US",
        line_count=len(order.lines),
        total_cents=order.total_cents,
        is_gold=bool(order.customer and order.customer.tier == "gold"),
        has_promo=bool(order.promo_code),
    )
    document["dataflow"] = remaining_defs_uses(order)
    return document


@router.get("/orders/{order_id}/packing-slip", dependencies=[RequireApiKey])
def packing_slip(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    packing: PackingService = Depends(get_packing_service),
) -> dict[str, object]:
    order = _load(service, order_id)
    return packing.render_packing_slip(order)


def _load(service: OrderService, order_id: int):
    try:
        return service.get_order(order_id)
    except InputValidationError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
