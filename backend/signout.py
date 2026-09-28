
"""
SUPREMESETUHUB Backend Sign Out
"""

from pydantic import BaseModel


class SignOutRequest(BaseModel):
    """Sign-out request data."""

    access_token: str


class SignOutResponse(BaseModel):
    """Sign-out response data."""

    success: bool
    message: str


def create_signout_response(
    success: bool = True,
    message: str = "SIGNOUT_SUCCESSFUL",
) -> SignOutResponse:
    """Create a standardized sign-out response."""

    return SignOutResponse(
        success=success,
        message=message,
    )
