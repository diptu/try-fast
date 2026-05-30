"""
Profile Routes
--------------

Endpoints for retrieving and updating user profiles.
"""

from typing import Annotated
from uuid import UUID

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

from user_service.core.security import is_authenticated
from user_service.dependencies.services import UserServiceDep
from user_service.docs.user.me import (
    GET_MY_PROFILE_DESCRIPTION,
    GET_MY_PROFILE_RESPONSES,
    GET_MY_PROFILE_SUMMARY,
)
from user_service.docs.user.retrieve import (
    GET_USER_PROFILE_DESCRIPTION,
    GET_USER_PROFILE_RESPONSES,
    GET_USER_PROFILE_SUMMARY,
)
from user_service.docs.user.update import (
    UPDATE_USER_PROFILE_DESCRIPTION,
    UPDATE_USER_PROFILE_RESPONSES,
    UPDATE_USER_PROFILE_SUMMARY,
)
from user_service.schemas.user import UserRead

router = APIRouter()


@router.get(
    "/me",
    summary=GET_MY_PROFILE_SUMMARY,
    description=GET_MY_PROFILE_DESCRIPTION,
    responses=GET_MY_PROFILE_RESPONSES,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    name="get_my_profile",
)
async def get_my_profile(
    current_user_id: Annotated[
        UUID,
        Depends(is_authenticated),
    ],
    service: UserServiceDep,
) -> UserRead:
    """
    Retrieve the currently authenticated user's profile.
    """
    return await service.get_user_profile(
        user_id=current_user_id,
    )


@router.get(
    "/{id}",
    summary=GET_USER_PROFILE_SUMMARY,
    description=GET_USER_PROFILE_DESCRIPTION,
    responses=GET_USER_PROFILE_RESPONSES,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    name="get_user_profile_by_id",
)
async def get_user_profile(
    id: UUID,
    service: UserServiceDep,
) -> UserRead:
    """
    Retrieve a user profile by ID.
    """
    return await service.get_user_profile(
        user_id=id,
    )


@router.put(
    "/{id}",
    summary=UPDATE_USER_PROFILE_SUMMARY,
    description=UPDATE_USER_PROFILE_DESCRIPTION,
    responses=UPDATE_USER_PROFILE_RESPONSES,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    name="update_user_profile",
)
async def update_user_profile(
    id: UUID,
    current_user_id: Annotated[
        str,
        Depends(is_authenticated),
    ],
    name: Annotated[
        str | None,
        Form(),
    ] = None,
    email: Annotated[
        EmailStr | None,
        Form(),
    ] = None,
    password: Annotated[
        str | None,
        Form(),
    ] = None,
    image: Annotated[
        UploadFile | None,
        File(),
    ] = None,
    service: UserServiceDep = None,  # type: ignore[assignment]
) -> UserRead:
    """
    Update a user's profile.

    Users may only update their own profile.
    """
    if str(id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("You do not have permission to update this profile."),
        )

    return await service.update_user_profile(
        user_id=id,
        name=name,
        email=email,
        password=password,
        image=image,
    )
