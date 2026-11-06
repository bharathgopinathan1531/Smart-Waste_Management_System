import re
from datetime import date
from decimal import Decimal, InvalidOperation


def validate_positive_quantity(value):
    try:
        quantity = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Quantity must be a valid number")

    if not quantity.is_finite():
        raise ValueError("Quantity must be finite")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    return float(quantity)


def validate_non_negative_quantity(value):
    try:
        quantity = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Quantity must be a valid number")

    if not quantity.is_finite():
        raise ValueError("Quantity must be finite")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    return float(quantity)


def sanitize_text(value: str, max_length: int = 500):
    if not isinstance(value, str):
        raise ValueError("Input must be text")

    cleaned = value.strip()

    if not cleaned:
        raise ValueError("Text cannot be empty")

    if len(cleaned) > max_length:
        raise ValueError(
            f"Text cannot exceed {max_length} characters"
        )

    if re.search(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", cleaned):
        raise ValueError("Text contains invalid control characters")

    return cleaned


def validate_date_range(start_date: date, end_date: date):
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")

    return True


def validate_positive_integer(value):
    if isinstance(value, bool):
        raise ValueError("Value must be a positive integer")

    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError("Value must be a positive integer")

    if str(number) != str(value) or number <= 0:
        raise ValueError("Value must be a positive integer")

    return number