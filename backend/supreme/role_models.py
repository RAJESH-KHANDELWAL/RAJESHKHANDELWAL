
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# SUPREME / ADMIN / OWNER ROLE MODELS
# ============================================================


class RoleType(str, Enum):
    SUPREME = "SUPREME"
    ADMIN = "ADMIN"
    OWNER = "OWNER"


class RoleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"


# ============================================================
# REPOSITORY IDENTITY
# ============================================================


class RepositoryIdentity(BaseModel):
    repo_id: str
    repo_name: str
    repo_url: Optional[str] = None
    status: str = "ACTIVE"


# ============================================================
# ROLE IDENTITY
# ============================================================


class RoleIdentity(BaseModel):
    role_id: str
    role: RoleType
    person_id: str
    person_name: str
    status: RoleStatus = RoleStatus.PENDING


# ============================================================
# REPOSITORY ROLE MANAGEMENT
# ============================================================


class RepositoryRoleManagement(BaseModel):
    repository: RepositoryIdentity
    supreme: Optional[RoleIdentity] = None
    admin: Optional[RoleIdentity] = None
    owner: Optional[RoleIdentity] = None


# ============================================================
# ROLE ASSIGNMENT REQUEST
# ============================================================


class RoleAssignmentRequest(BaseModel):
    repo_id: str
    role: RoleType
    person_id: str
    person_name: str
    status: RoleStatus = RoleStatus.PENDING


# ============================================================
# ROLE ASSIGNMENT RESPONSE
# ============================================================


class RoleAssignmentResponse(BaseModel):
    success: bool = True
    message: str = "ROLE_ASSIGNMENT_CREATED"
    assignment: RoleIdentity


# ============================================================
# REPOSITORY ROLE RESPONSE
# ============================================================


class RepositoryRoleResponse(BaseModel):
    success: bool = True
    repository_roles: list[RepositoryRoleManagement] = Field(
        default_factory=list
    )
