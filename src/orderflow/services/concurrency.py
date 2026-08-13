from __future__ import annotations

import threading
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class LockedCounter:
    """Shared mutable counter protected by a threading lock (no unsynchronized writes)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._value = 0

    def increment(self, delta: int = 1) -> int:
        with self._lock:
            self._value += delta
            return self._value

    @property
    def value(self) -> int:
        with self._lock:
            return self._value


class StockLedger:
    """In-memory stock adjustments used by concurrent reservation workers."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._on_hand: dict[str, int] = {}

    def seed(self, sku: str, quantity: int) -> None:
        with self._lock:
            self._on_hand[sku] = quantity

    def reserve(self, sku: str, quantity: int) -> int:
        with self._lock:
            available = self._on_hand.get(sku, 0)
            if available < quantity:
                raise ValueError(f"insufficient stock for {sku}")
            remaining = available - quantity
            self._on_hand[sku] = remaining
            return remaining

    def snapshot(self, sku: str) -> int:
        with self._lock:
            return self._on_hand.get(sku, 0)


def run_exclusive(lock: threading.Lock, action: Callable[[], T]) -> T:
    with lock:
        return action()
