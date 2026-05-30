from typing import Annotated

from fastapi import Depends, HTTPException, status
from user_service.core.security import is_authenticated


async def verify_profile_owner(
    id: str,
    current_user_id: Annotated[
        str,
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
