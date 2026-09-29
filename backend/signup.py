
"""
👑 RAJESHKHANDELWAL 👑
Backend Sign Up
"""

from pydantic import BaseModel, Field, EmailStr


class SignUpRequest(BaseModel):
    """Sign-up request data."""

    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1, max_length=100)


class SignUpResponse(BaseModel):
    """Sign-up response data."""

    success: bool
    message: str
    person_id: str | None = None


def create_signup_response(
    success: bool,
    message: str,
    person_id: str | None = None,
) -> SignUpResponse:
    """Create a standardized sign-up response."""

    return SignUpResponse(
        success=success,
        message=message,
        person_id=person_id,
    )
