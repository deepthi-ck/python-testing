from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import TypeVar

T = TypeVar("T")


def stream_rows(rows: Sequence[T], chunk_size: int = 256) -> Iterator[Sequence[T]]:
    """Yield bounded slices instead of materializing a second full copy."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")
    index = 0
    total = len(rows)
    while index < total:
        yield rows[index:index + chunk_size]
        index += chunk_size


def bounded_map(values: Sequence[int], limit: int) -> list[int]:
    """O(n) transform with a hard cap so loops do not allocate unbounded objects."""
    if limit < 0:
        raise ValueError("limit must be non-negative")
    output: list[int] = []
    for value in values[:limit]:
        output.append(value)
    return output
