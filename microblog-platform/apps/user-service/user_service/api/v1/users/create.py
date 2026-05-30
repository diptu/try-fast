"""
User Creation Routes
--------------------

Endpoints for creating user accounts.
"""

from typing import Annotated, Literal

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
    status,
)
from pydantic import EmailStr

from user_service.core.security import hash_password
from user_service.dependencies.services import UserServiceDep
from user_service.docs.user.create import (
    CREATE_USER_DESCRIPTION,
    CREATE_USER_RESPONSES,
    CREATE_USER_SUMMARY,
)
from user_service.schemas.user import UserRead

UserRole = Literal["customer", "admin", "superadmin"]
UserStatus = Literal["active", "suspended", "archived"]

router = APIRouter()


@router.post(
    "/",
    summary=CREATE_USER_SUMMARY,
    description=CREATE_USER_DESCRIPTION,
    responses=CREATE_USER_RESPONSES,
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    name="create_user",
)
async def create_user(
    name: Annotated[str, Form(...)],
    email: Annotated[EmailStr, Form(...)],
    password: Annotated[str, Form(...)],
    role: UserRole = "customer",
    status_value: UserStatus = "active",
    is_email_verified: Annotated[
        bool,
        Form(),
    ] = False,
    image: Annotated[
        UploadFile | None,
        File(),
    ] = None,
    service: UserServiceDep = None,  # type: ignore[assignment]
) -> UserRead:
    """
    Create a new user account.
    """

    return await service.create_user(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        status_value=status_value,
        is_email_verified=is_email_verified,
        image=image,
    )
