from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from user_service.core.security import is_authenticated

CurrentUserDep = Annotated[
    UUID,
    Depends(is_authenticated),
]


async def verify_profile_owner(
    id: UUID,
    current_user_id: Annotated[
        UUID,
        Depends(is_authenticated),
    ],
) -> None:
    """
    Ensure the authenticated user owns the profile.
    """
    if id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )


__all__ = [
    "verify_profile_owner",
    "CurrentUserDep",
]
