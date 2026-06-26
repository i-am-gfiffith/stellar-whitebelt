from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping


_ADDRESS_PATTERN = re.compile(r"^[A-Z2-7]{56}$")
_SECRET_PATTERN = re.compile(r"^[S-Z2-7]{56}$")


def is_valid_address(value: Any) -> bool:
    """Return True when value looks like a Stellar public address."""

    return isinstance(value, str) and bool(_ADDRESS_PATTERN.fullmatch(value))


def is_valid_secret_seed(value: Any) -> bool:
    """Return True when value looks like a Stellar secret seed."""

    return isinstance(value, str) and bool(_SECRET_PATTERN.fullmatch(value))


def normalize_amount(value: Any) -> Decimal:
    """Convert an amount-like value into a Decimal."""

    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float, str)):
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return Decimal("0")
    return Decimal("0")


def format_amount(value: Any, places: int = 7) -> str:
    """Format an amount-like value as a string with fixed precision."""

    return format(normalize_amount(value).quantize(Decimal("1." + ("0" * places))), f".{places}f")


def ensure_mapping(value: Any) -> Mapping[str, Any]:
    """Ensure a mapping-like object is a plain mapping."""

    if not isinstance(value, Mapping):
        raise TypeError("Expected a mapping")
    return value
