
"""
👑 RAJESHKHANDELWAL 👑
Backend Password Reset
"""

from pydantic import BaseModel, Field, EmailStr


class PasswordResetRequest(BaseModel):
    """Password reset request data."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation data."""

    reset_token: str = Field(min_length=1)
    new_password: str = Field(min_length=8)


class PasswordResetResponse(BaseModel):
    """Password reset response data."""

    success: bool
    message: str


def create_password_reset_response(
    success: bool,
    message: str,
) -> PasswordResetResponse:
    """Create a standardized password reset response."""

    return PasswordResetResponse(
        success=success,
        message=message,
    )
