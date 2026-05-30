"""
Permission Dependencies
-----------------------

Reusable authorization dependencies.

These dependencies enforce ownership and role-based access
control policies while keeping route handlers focused on
HTTP concerns.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from user_service.core.security import is_authenticated
from user_service.services.role import RoleChecker

# ------------------------------------------------------------------
# Authentication Dependencies
# ------------------------------------------------------------------

CurrentUserIdDep = Annotated[
    str,
    Depends(is_authenticated),
]


# ------------------------------------------------------------------
# Ownership Permissions
# ------------------------------------------------------------------


async def verify_profile_owner(
    id: str,
    current_user_id: CurrentUserIdDep,
) -> None:
    """
    Ensure that the authenticated user owns the target profile.

    Args:
        id: User ID from the path parameter.
        current_user_id: Authenticated user ID.

    Raises:
        HTTPException: If the authenticated user does not own
        the target profile.
    """
    if id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )


# ------------------------------------------------------------------
# Role-Based Permissions
# ------------------------------------------------------------------

allow_admin = RoleChecker(
    allowed_roles=[
        "admin",
        "superadmin",
    ],
)

allow_superadmin = RoleChecker(
    allowed_roles=[
        "superadmin",
    ],
)


AdminUserDep = Annotated[
    str,
    Depends(allow_admin),
]

SuperAdminDep = Annotated[
    str,
    Depends(allow_superadmin),
]


# ------------------------------------------------------------------
# Exports
# ------------------------------------------------------------------

__all__ = [
    "CurrentUserIdDep",
    "AdminUserDep",
    "SuperAdminDep",
    "verify_profile_owner",
]
