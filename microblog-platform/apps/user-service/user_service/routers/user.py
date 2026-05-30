from datetime import timedelta
from typing import Annotated, Literal

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.core.config import settings
from user_service.core.security import (
    create_access_token,
    hash_password,
    is_authenticated,
)
from user_service.db.session import get_db
from user_service.schemas.token import TokenResponse
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
    role: Annotated[
        Literal["customer", "admin", "superadmin"],
        Form(),
    ] = "customer",
    status_value: Annotated[
        Literal["active", "suspended", "archived"],
        Form(),
    ] = "active",
    is_email_verified: Annotated[bool, Form()] = False,
    image: Annotated[UploadFile | None, File()] = None,
    session: Annotated[AsyncSession, Depends(get_db)] = None,  # type: ignore[assignment]
) -> UserRead:
    """
    Create a new user account.
    """
    if session is None:
        raise RuntimeError("Database session dependency was not injected.")

    service = UserService(session)

    return await service.create_user(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        status_value=status_value,
        is_email_verified=is_email_verified,
        image=image,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    email: Annotated[EmailStr, Form(...)],
    password: Annotated[str, Form(...)],
    name: Annotated[str, Form(...)],
    image: Annotated[UploadFile | None, File()] = None,
    session: Annotated[AsyncSession, Depends(get_db)] = None,  # type: ignore[assignment]
) -> TokenResponse:
    """
    Authenticate a user and return a JWT access token.
    """
    if session is None:
        raise RuntimeError("Database session dependency was not injected.")

    try:
        service = UserService(session)

        user = await service.authenticate_user(
            name=name,
            email=email,
            password=password,
            image=image,
        )

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
            },
            expires_delta=access_token_expires,
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user,
        )

    except HTTPException:
        raise

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "A user with this email address already exists "
                "or credential conflicts occurred."
            ),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "An internal error occurred while processing "
                "your authentication request."
            ),
        ) from exc


@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    name="get_my_profile",
)
async def my_profile(
    current_user_id: Annotated[str, Depends(is_authenticated)],
    session: Annotated[AsyncSession, Depends(get_db)] = None,  # type: ignore[assignment]
) -> UserRead:
    """
    Get the current authenticated user's profile metadata.
    """
    if session is None:
        raise RuntimeError("Database session dependency was not injected.")

    service = UserService(session)
    return await service.get_user_profile(user_id=current_user_id)


@router.get(
    "/{id}",  # Prefix handling automatically appends this to: /api/v1/users/{id}
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    name="get_user_profile_by_id",
)
async def get_user(
    id: str,  # Switched to str to remain consistent
    # with your other user_id implementations
    session: Annotated[AsyncSession, Depends(get_db)] = None,  # type: ignore[assignment]
) -> UserRead:
    """
    Retrieve a single user profile by its unique ID string.
    """
    if session is None:
        raise RuntimeError("Database session dependency was not injected.")

    service = UserService(session)

    # Downstream service tier naturally handles raising 404s if the profile isn't found
    return await service.get_user_profile(user_id=id)
