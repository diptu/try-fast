from typing import Literal

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.core.security import is_authenticated
from user_service.db.session import get_db
from user_service.services.user import UserService


class RoleChecker:
    def __init__(self, allowed_roles: list[Literal["customer", "admin", "superadmin"]]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        current_user_id: str = Depends(is_authenticated),  # noqa: B008
        session: AsyncSession = Depends(get_db),  # noqa: B008
    ) -> str:
        """
        Validates that the authenticated user possesses an authorized role.
        Returns the user ID if successful.
        """
        if session is None:
            raise RuntimeError("Database session dependency was not injected.")

        service = UserService(session)
        user_profile = await service.get_user_profile(user_id=current_user_id)

        if user_profile.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation refused. Minimum administrative privileges not met.",
            )

        return current_user_id
