from __future__ import annotations

from orderflow.models.customer import Customer
from orderflow.models.inventory import InventoryLot
from orderflow.models.order import Order, OrderLine
from orderflow.models.product import Product
from orderflow.repositories.customer_repository import CustomerRepository
from orderflow.repositories.inventory_repository import InventoryRepository
from orderflow.repositories.order_repository import OrderRepository
from orderflow.repositories.product_repository import ProductRepository
from orderflow.schemas.customer import CustomerCreate
from orderflow.schemas.order import OrderCreate
from orderflow.schemas.product import ProductCreate
from orderflow.security.access import can_place_order
from orderflow.services.fulfillment_service import FulfillmentService, IllegalTransitionError
from orderflow.services.inventory_service import InsufficientStockError, InventoryService
from orderflow.services.payment_service import PaymentError, PaymentService
from orderflow.services.pricing_service import PricingService
from orderflow.utils.logging import info as log_info
from orderflow.validators.input_sanitizer import (
    InputValidationError,
    require_quantity,
    sanitize_promo_code,
    sanitize_text,
)


class CatalogService:
    def __init__(
        self,
        customers: CustomerRepository,
        products: ProductRepository,
        inventory: InventoryRepository,
    ) -> None:
        self._customers = customers
        self._products = products
        self._inventory = inventory

    def create_customer(self, payload: CustomerCreate) -> Customer:
        existing = self._customers.get_by_email(payload.email.lower())
        if existing is not None:
            raise InputValidationError("email already registered")
        customer = Customer(
            email=payload.email.lower(),
            full_name=sanitize_text(payload.full_name, "full_name", 120) or payload.full_name,
            tier=payload.tier,
            region=payload.region.upper(),
        )
        return self._customers.add(customer)

    def create_product(self, payload: ProductCreate) -> Product:
        if self._products.get_by_sku(payload.sku) is not None:
            raise InputValidationError("sku already exists")
        product = Product(
            sku=payload.sku,
            name=payload.name,
            category=payload.category,
            unit_price_cents=payload.unit_price_cents,
            weight_grams=payload.weight_grams,
        )
        self._products.add(product)
        lot = InventoryLot(
            product_id=product.id,
            sku=product.sku,
            warehouse="ATL",
            on_hand=payload.initial_on_hand,
            reserved=0,
        )
        self._inventory.add(lot)
        return product


class OrderService:
    def __init__(
        self,
        orders: OrderRepository,
        customers: CustomerRepository,
        products: ProductRepository,
        inventory: InventoryService,
        pricing: PricingService,
        fulfillment: FulfillmentService,
        payments: PaymentService,
    ) -> None:
        self._orders = orders
        self._customers = customers
        self._products = products
        self._inventory = inventory
        self._pricing = pricing
        self._fulfillment = fulfillment
        self._payments = payments

    def create_order(self, payload: OrderCreate) -> Order:
        customer = self._customers.get(payload.customer_id)
        if customer is None:
            raise InputValidationError("customer not found")
        if not can_place_order(customer):
            raise InputValidationError("customer is not allowed to place orders")

        promo = sanitize_promo_code(payload.promo_code)
        notes = sanitize_text(payload.notes, "notes")
        skus = [line.sku for line in payload.lines]
        product_map = {
            product.sku: product
            for product in self._products.list_by_skus(skus)
            if product.is_active
        }
        priced_lines: list[tuple[str, int, int, int]] = []
        reserve_items: list[tuple[str, int]] = []
        for line in payload.lines:
            quantity = require_quantity(line.quantity)
            product = product_map.get(line.sku)
            if product is None:
                raise InputValidationError(f"unknown sku {line.sku}")
            priced_lines.append((product.sku, quantity, product.unit_price_cents, product.weight_grams))
            reserve_items.append((product.sku, quantity))

        quote = self._pricing.quote(
            lines=priced_lines,
            customer_tier=customer.tier,
            region=customer.region,
            promo_code=promo,
            customer_is_active=customer.is_active,
        )
        self._inventory.reserve(reserve_items)

        order = Order(
            customer_id=customer.id,
            status="draft",
            subtotal_cents=quote.subtotal_cents,
            discount_cents=quote.discount_cents,
            shipping_cents=quote.shipping_cents,
            tax_cents=quote.tax_cents,
            total_cents=quote.total_cents,
            promo_code=quote.applied_promo,
            notes=notes,
        )
        for quoted in quote.lines:
            product = product_map[quoted.sku]
            order.lines.append(
                OrderLine(
                    product_id=product.id,
                    sku=quoted.sku,
                    quantity=quoted.quantity,
                    unit_price_cents=quoted.unit_price_cents,
                    line_total_cents=quoted.line_total_cents,
                )
            )
        saved = self._orders.add(order)
        log_info("order_created", order_id=saved.id, line_count=len(saved.lines))
        return saved

    def get_order(self, order_id: int) -> Order:
        order = self._orders.get(order_id)
        if order is None:
            raise InputValidationError("order not found")
        return order

    def transition(self, order_id: int, target_status: str) -> Order:
        order = self.get_order(order_id)
        items = [(line.sku, line.quantity) for line in order.lines]
        previous = order.status
        try:
            if target_status == "paid":
                self._payments.authorize(order)
            self._fulfillment.advance(order, target_status)
            if target_status == "shipped":
                self._inventory.ship(items)
            if target_status == "cancelled" and previous in {"draft", "confirmed", "paid"}:
                self._inventory.release(items)
        except (IllegalTransitionError, PaymentError, InsufficientStockError) as exc:
            raise InputValidationError(str(exc)) from exc
        return order
