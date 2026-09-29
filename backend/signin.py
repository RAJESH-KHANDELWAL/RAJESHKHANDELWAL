
"""
👑 RAJESHKHANDELWAL 👑
Backend Sign In
"""

from pydantic import BaseModel, Field


class SignInRequest(BaseModel):
    """Sign-in request data."""

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class SignInResponse(BaseModel):
    """Sign-in response data."""

    success: bool
    message: str
    access_token: str | None = None
    token_type: str = "bearer"


def create_signin_response(
    success: bool,
    message: str,
    access_token: str | None = None,
) -> SignInResponse:
    """Create a standardized sign-in response."""

    return SignInResponse(
        success=success,
        message=message,
        access_token=access_token,
    )
