from typing import Literal

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.core.config import settings
from user_service.core.file_storage import save_image_file
from user_service.core.security import hash_password
from user_service.models.user import User
from user_service.repositories.user import UserRepository
from user_service.schemas.user import UserCreate, UserRead


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def create_user(
        self,
        name: str,
        email: str,
        password: str,
        role: Literal["customer", "admin", "superadmin"],
        status_value: Literal["active", "suspended", "archived"],
        is_email_verified: bool,
        image: UploadFile | None,
    ) -> UserRead:
        try:
            image_path = await save_image_file(image)
            default_image = settings.DEFAULT_USER_IMAGE

            payload = UserCreate(
                name=name,
                email=email,
                password=password,
                role=role,
                status=status_value,
                is_email_verified=is_email_verified,
                image=image_path if image_path else default_image,
            )

            user = User(
                **payload.model_dump(exclude={"password"}),
                password_hash=hash_password(payload.password),
            )

            created_user = await self.repository.create(user)
            return UserRead.model_validate(created_user)

        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
