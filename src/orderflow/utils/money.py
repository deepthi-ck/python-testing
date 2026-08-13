from __future__ import annotations


def clamp_cents(value: int, minimum: int = 0, maximum: int = 2_147_483_647) -> int:
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def cents_to_display(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    absolute = abs(cents)
    dollars, remainder = divmod(absolute, 100)
    return f"{sign}{dollars}.{remainder:02d}"
