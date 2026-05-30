"""
Address Creation Routes
-----------------------

Endpoints for creating user addresses.
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    status,
)

from user_service.dependencies.auth import CurrentUserDep
from user_service.dependencies.services import AddressServiceDep
from user_service.schemas.address import (
    AddressCreate,
    AddressListResponse,
    AddressResponse,
)

router = APIRouter()


@router.get(
    "/me/addresses",
    response_model=AddressListResponse,
    name="list_addresses",
)
async def list_addresses(
    current_user: CurrentUserDep,
    address_service: AddressServiceDep,
) -> AddressListResponse:
    """
    List all addresses belonging to the authenticated user.
    """

    addresses = await address_service.list_addresses(
        user_id=current_user,
    )

    return AddressListResponse(
        items=[AddressResponse.model_validate(address) for address in addresses]
    )


@router.get(
    "/me/addresses/{id}",
    response_model=AddressResponse,
    name="get_address",
)
async def get_address(
    id: UUID,
    current_user: CurrentUserDep,
    address_service: AddressServiceDep,
) -> AddressResponse:
    """
    Retrieve a specific address belonging to the authenticated user.
    """

    address = await address_service.get_address(
        user_id=current_user,
        address_id=id,
    )

    return AddressResponse.model_validate(address)


@router.post(
    "/me/addresses",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(
    payload: AddressCreate,
    current_user: CurrentUserDep,
    address_service: AddressServiceDep,
) -> AddressResponse:

    address = await address_service.create_address(
        user_id=current_user,
        payload=payload,
    )

    return AddressResponse.model_validate(address)
