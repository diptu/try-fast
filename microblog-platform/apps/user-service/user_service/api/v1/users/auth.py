"""
Authentication Routes
---------------------

Endpoints for user authentication and token generation.
"""

from datetime import timedelta
from typing import Annotated

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from user_service.core.config import settings
from user_service.core.security import create_access_token
from user_service.dependencies.services import UserServiceDep
from user_service.docs.auth.login import (
    LOGIN_USER_DESCRIPTION,
    LOGIN_USER_RESPONSES,
    LOGIN_USER_SUMMARY,
)
from user_service.schemas.token import TokenResponse

router = APIRouter()


@router.post(
    "/login",
    summary=LOGIN_USER_SUMMARY,
    description=LOGIN_USER_DESCRIPTION,
    responses=LOGIN_USER_RESPONSES,
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    name="login_user",
)
async def login_user(
    email: Annotated[EmailStr, Form(...)],
    password: Annotated[str, Form(...)],
    name: Annotated[str, Form(...)],
    image: Annotated[UploadFile | None, File()] = None,
    service: UserServiceDep = None,  # type: ignore[assignment]
) -> TokenResponse:
    """
    Authenticate a user and return a JWT access token.
    """
    try:
        user = await service.authenticate_user(
            name=name,
            email=email,
            password=password,
            image=image,
        )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
            },
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            ),
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
                "or a credential conflict occurred."
            ),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "An internal error occurred while processing "
                "the authentication request."
            ),
        ) from exc
