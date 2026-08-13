from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from orderflow.api.deps import RequireApiKey, get_catalog_service
from orderflow.schemas.customer import CustomerCreate, CustomerRead
from orderflow.schemas.product import ProductCreate, ProductRead
from orderflow.services.order_service import CatalogService
from orderflow.validators.input_sanitizer import InputValidationError

router = APIRouter(tags=["catalog"])


@router.post(
    "/customers",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[RequireApiKey],
)
def create_customer(
    payload: CustomerCreate,
    service: CatalogService = Depends(get_catalog_service),
) -> CustomerRead:
    try:
        customer = service.create_customer(payload)
    except InputValidationError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return CustomerRead.model_validate(customer)


@router.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[RequireApiKey],
)
def create_product(
    payload: ProductCreate,
    service: CatalogService = Depends(get_catalog_service),
) -> ProductRead:
    try:
        product = service.create_product(payload)
    except InputValidationError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return ProductRead.model_validate(product)
