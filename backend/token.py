
"""
👑 RAJESHKHANDELWAL 👑
Backend Token Models
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    """Token validation request."""

    access_token: str = Field(min_length=1)


class TokenInfo(BaseModel):
    """Token information."""

    token_id: str
    person_id: str
    issued_at: datetime
    expires_at: datetime
    is_revoked: bool = False


class TokenResponse(BaseModel):
    """Token validation response."""

    success: bool
    message: str
    token: Optional[TokenInfo] = None


def create_token_response(
    success: bool,
    message: str,
    token: Optional[TokenInfo] = None,
) -> TokenResponse:
    """Create a standardized token response."""

    return TokenResponse(
        success=success,
        message=message,
        token=token,
    )
