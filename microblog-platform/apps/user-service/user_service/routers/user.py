from typing import Annotated, Literal

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    status,
)
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.db.session import get_db
from user_service.schemas.user import UserRead
from user_service.services.user import UserService

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    name: Annotated[str, Form(...)],
    email: Annotated[EmailStr, Form(...)],
    password: Annotated[str, Form(...)],
    role: Annotated[Literal["customer", "admin", "superadmin"], Form()] = "customer",
    status: Annotated[Literal["active", "suspended", "archived"], Form()] = "active",
    is_email_verified: Annotated[bool, Form()] = False,
    image: Annotated[UploadFile | None, File()] = None,
    session: Annotated[AsyncSession, Depends(get_db)] = None,  # type: ignore[assignment]
) -> UserRead:
    # Safe check in case the framework pipeline is bypassed during unit tests
    if session is None:
        raise RuntimeError("Database session dependency was not injected.")

    service = UserService(session)

    return await service.create_user(
        name=name,
        email=email,
        password=password,
        role=role,
        status_value=status,
        is_email_verified=is_email_verified,
        image=image,
    )
