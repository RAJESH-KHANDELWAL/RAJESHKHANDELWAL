
"""
SUPREMESETUHUB Backend Response Utilities
"""

from typing import Any


def success_response(
    message: str,
    data: Any = None,
) -> dict:
    """Create a standardized success response."""

    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    message: str,
    code: str = "GENERAL_ERROR",
) -> dict:
    """Create a standardized error response."""

    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
