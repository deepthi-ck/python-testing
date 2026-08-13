from __future__ import annotations


def loop_trip_coverage(values: list[int], threshold: int) -> dict[str, int]:
    """Exercises zero-trip, one-trip, and n-trip loop paths."""
    accepted = 0
    rejected = 0
    for value in values:
        if value >= threshold:
            accepted += 1
        else:
            rejected += 1
    return {"accepted": accepted, "rejected": rejected, "seen": accepted + rejected}


def exception_path(numerator: int, denominator: int) -> int:
    try:
        if denominator == 0:
            raise ZeroDivisionError("denominator is zero")
        result = numerator // denominator
    except ZeroDivisionError:
        return 0
    else:
        if result < 0:
            return abs(result)
        return result


def nested_predicates(flag_a: bool, flag_b: bool, flag_c: bool) -> str:
    if flag_a and flag_b:
        if flag_c:
            return "abc"
        return "ab"
    if flag_a or flag_c:
        return "a_or_c"
    if not flag_b:
        return "not_b"
    return "b_only"
