from typing import Literal

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.core.config import settings
from user_service.core.file_storage import save_image_file
from user_service.core.security import hash_password, verify_password
from user_service.models.user import User
from user_service.repositories.user import UserRepository
from user_service.schemas.user import UserRead


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def create_user(
        self,
        name: str,
        email: str,
        password_hash: str,  # <-- Ensure this is explicitly named password_hash
        role: Literal["customer", "admin", "superadmin"],
        status_value: Literal["active", "suspended", "archived"],
        is_email_verified: bool,
        image: UploadFile | None,
    ) -> UserRead:
        try:
            image_path = await save_image_file(image)
            default_image = settings.DEFAULT_USER_IMAGE

            user_data = {
                "name": name,
                "email": email,
                "role": role,
                "status": status_value,
                "is_email_verified": is_email_verified,
                "image": image_path if image_path else default_image,
            }

            # Map the incoming hash string directly to your SQLModel/SQLAlchemy property
            user = User(
                **user_data,
                password_hash=password_hash,
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

    async def authenticate_user(
        self,
        name: str,
        email: str,
        password: str,
        image: UploadFile | None,
    ) -> UserRead:
        # 1. Look for an existing profile by email first
        user = await self.repository.get_by_email(email)

        # 2. Check if user exists AND the password matches the database hash
        if user and verify_password(password, user.password_hash):
            return UserRead.model_validate(user)

        # 3. Fallback A: Email exists but password check failed (Wrong password)
        if user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )

        # 4. Fallback B: User doesn't exist at all -> Register them on the fly
        hashed = hash_password(password)
        return await self.create_user(
            name=name,
            email=email,
            password_hash=hashed,  # <-- This matches line 21 perfectly now
            role="customer",
            status_value="active",
            is_email_verified=False,
            image=image,
        )

    async def get_user_profile(self, user_id: str) -> UserRead:
        """Retrieve complete model details for an authenticated user session."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile could not be found.",
            )
        return UserRead.model_validate(user)
