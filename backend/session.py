
"""
SUPREMESETUHUB Backend Session Management
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SessionCreate(BaseModel):
    """Create a user session."""

    person_id: str
    access_token: str
    expires_at: datetime


class SessionInfo(BaseModel):
    """Session information."""

    session_id: str
    person_id: str
    created_at: datetime
    expires_at: datetime
    is_active: bool = True


class SessionResponse(BaseModel):
    """Session API response."""

    success: bool
    message: str
    session: Optional[SessionInfo] = None


def create_session_response(
    success: bool,
    message: str,
    session: Optional[SessionInfo] = None,
) -> SessionResponse:
    """Create a standardized session response."""

    return SessionResponse(
        success=success,
        message=message,
        session=session,
    )
