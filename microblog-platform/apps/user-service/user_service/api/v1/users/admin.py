"""
Admin User Routes
-----------------

Administrative endpoints for managing users.

Endpoints
---------
DELETE /{id}
    Soft delete (archive) a user account.

Access
------
Admin
SuperAdmin
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from user_service.dependencies.services import get_user_service
from user_service.docs.user.delete import (
    DELETE_USER_DESCRIPTION,
    DELETE_USER_SUMMARY,
)
from user_service.schemas.user import UserDeleteResponse
from user_service.services.role import RoleChecker
from user_service.services.user import UserService

router = APIRouter()

allow_administrative_roles = RoleChecker(
    allowed_roles=[
        "admin",
        "superadmin",
    ],
)


@router.delete(
    "/{id}",
    summary=DELETE_USER_SUMMARY,
    description=DELETE_USER_DESCRIPTION,
    response_model=UserDeleteResponse,
    status_code=status.HTTP_200_OK,
    name="soft_delete_user_account",
)
async def delete_user(
    id: UUID,
    _: Annotated[
        str,
        Depends(allow_administrative_roles),
    ],
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> UserDeleteResponse:
    """
    Soft delete (archive) a user account.

    Restricted to:
    - Admin
    - SuperAdmin
    """
    await service.soft_delete_user(user_id=id)
    return UserDeleteResponse(
        id=id,
        status="archived",
        message=f"User {id} successfully archived by administrator.",
    )
