from __future__ import annotations

import threading

import pytest

from orderflow.services.concurrency import LockedCounter, StockLedger
from orderflow.utils.logging import PiiLogError, info
from orderflow.utils.memory import bounded_map, stream_rows


def test_stock_ledger_is_thread_safe() -> None:
    ledger = StockLedger()
    ledger.seed("SKU-1", 100)
    errors: list[str] = []

    def worker() -> None:
        try:
            for _ in range(10):
                ledger.reserve("SKU-1", 1)
        except ValueError as exc:
            errors.append(str(exc))

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert not errors
    assert ledger.snapshot("SKU-1") == 50


def test_locked_counter() -> None:
    counter = LockedCounter()
    assert counter.increment(3) == 3
    assert counter.value == 3


def test_memory_streaming_is_linear() -> None:
    chunks = list(stream_rows(list(range(10)), chunk_size=4))
    assert chunks[0] == [0, 1, 2, 3]
    assert bounded_map([1, 2, 3, 4], limit=2) == [1, 2]
    with pytest.raises(ValueError):
        list(stream_rows([1], chunk_size=0))


def test_pii_logging_is_blocked() -> None:
    info("order_created", order_id=12)
    with pytest.raises(PiiLogError):
        info("customer_created", email="hidden")
