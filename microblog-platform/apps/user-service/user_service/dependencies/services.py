"""
Service Dependencies
--------------------

Centralized dependency providers for application services.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.db.session import get_db
from user_service.services.address import AddressService
from user_service.services.user import UserService

# ------------------------------------------------------------------
# Database Dependencies
# ------------------------------------------------------------------

SessionDep = Annotated[
    AsyncSession,
    Depends(get_db),
]


# ------------------------------------------------------------------
# Service Factories
# ------------------------------------------------------------------


async def get_user_service(
    session: SessionDep,
) -> UserService:
    """
    Construct a UserService instance.
    """
    return UserService(session)


async def get_address_service(
    session: SessionDep,
) -> AddressService:
    """
    Construct an AddressService instance.
    """
    return AddressService(session)


# ------------------------------------------------------------------
# Service Dependency Aliases
# ------------------------------------------------------------------

UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]

AddressServiceDep = Annotated[
    AddressService,
    Depends(get_address_service),
]

__all__ = [
    "SessionDep",
    "get_user_service",
    "UserServiceDep",
    "get_address_service",
    "AddressServiceDep",
]
