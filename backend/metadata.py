
"""
SUPREMESETUHUB Backend Metadata
"""

from backend.constants import BACKEND_NAME, BACKEND_VERSION, BACKEND_STATUS


def get_backend_metadata() -> dict:
    """Return backend service metadata."""

    return {
        "name": BACKEND_NAME,
        "version": BACKEND_VERSION,
        "status": BACKEND_STATUS,
    }
