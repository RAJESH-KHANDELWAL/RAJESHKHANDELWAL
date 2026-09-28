
"""
SUPREMESETUHUB Backend Email Verification
"""

from pydantic import BaseModel, EmailStr, Field


class EmailVerificationRequest(BaseModel):
    """Request an email verification."""

    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    """Confirm email verification using a token."""

    email: EmailStr
    verification_token: str = Field(min_length=1)


class EmailVerificationResponse(BaseModel):
    """Email verification response."""

    success: bool
    message: str
    verified: bool = False


def create_email_verification_response(
    success: bool,
    message: str,
    verified: bool = False,
) -> EmailVerificationResponse:
    """Create a standardized email verification response."""

    return EmailVerificationResponse(
        success=success,
        message=message,
        verified=verified,
    )
