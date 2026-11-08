"""Validation of Kazakhstan business (BIN) and individual (IIN) identification numbers.

Both are 12 digits; the last digit is a check digit computed with two weight
sequences modulo 11. If the second pass also yields 10, the number is invalid.

Limitation: the 11th digit has weight 11 (= 0 mod 11) in the first pass, so most
typos in that position still pass. A valid checksum is a format check, not proof
that the entity exists; existence is confirmed only by the registry lookup.
"""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS_FIRST = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
_WEIGHTS_SECOND = (3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2)
LENGTH = 12


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Outcome of a BIN/IIN check; `reason` explains a failure in plain words."""

    valid: bool
    reason: str | None = None


def check_digit(first_eleven: str) -> int | None:
    """Return the check digit for 11 leading digits, or None if no valid digit exists."""
    if len(first_eleven) != LENGTH - 1 or not first_eleven.isdigit():
        raise ValueError("expected exactly 11 digits")
    digits = [int(c) for c in first_eleven]
    control = sum(d * w for d, w in zip(digits, _WEIGHTS_FIRST, strict=True)) % 11
    if control == 10:
        control = sum(d * w for d, w in zip(digits, _WEIGHTS_SECOND, strict=True)) % 11
        if control == 10:
            return None
    return control


def check(value: str) -> CheckResult:
    """Check that `value` is a well-formed BIN/IIN with a correct check digit."""
    cleaned = value.strip()
    if not cleaned.isdigit():
        return CheckResult(False, "must contain digits only")
    if len(cleaned) != LENGTH:
        return CheckResult(False, f"must be exactly {LENGTH} digits, got {len(cleaned)}")
    expected = check_digit(cleaned[:-1])
    if expected is None:
        return CheckResult(False, "no valid check digit exists for the first 11 digits")
    if int(cleaned[-1]) != expected:
        return CheckResult(False, f"check digit mismatch: expected {expected}, got {cleaned[-1]}")
    return CheckResult(True)
