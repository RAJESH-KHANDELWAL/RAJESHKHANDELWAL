
"""
SUPREMESETUHUB Backend Utilities
"""

from datetime import datetime, timezone


def get_current_utc_time() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""

    return datetime.now(timezone.utc).isoformat()


def normalize_text(value: str) -> str:
    """Remove extra spaces from text."""

    return value.strip()


def normalize_identifier(value: str) -> str:
    """Normalize an identifier to uppercase."""

    return value.strip().upper()
