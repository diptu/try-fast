"""
Address Service
---------------

Business logic for managing user addresses.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.models.address import Address
from user_service.schemas.address import AddressCreate


class AddressService:
    """
    Service responsible for address-related operations.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create_address(
        self,
        user_id: UUID | str,
        payload: AddressCreate,
    ) -> Address:
        """
        Create a new address for a user.

        Business Rules
        --------------
        1. Users may have multiple addresses.
        2. Only one address can be default.
        3. The first address is automatically default.
        4. If a new address is marked default,
           existing defaults are removed.
        """

        # ---------------------------------------------------------
        # Count existing addresses
        # ---------------------------------------------------------

        count_stmt = (
            select(func.count()).select_from(Address).where(Address.user_id == user_id)
        )

        count_result = await self.session.execute(
            count_stmt,
        )

        address_count = count_result.scalar_one()

        # ---------------------------------------------------------
        # Determine default state
        # ---------------------------------------------------------

        is_default = payload.is_default

        if address_count == 0:
            is_default = True

        # ---------------------------------------------------------
        # Remove previous default
        # ---------------------------------------------------------

        if is_default:
            unset_default_stmt = (
                update(Address)
                .where(Address.user_id == user_id)
                .values(is_default=False)
            )

            await self.session.execute(
                unset_default_stmt,
            )

        # ---------------------------------------------------------
        # Create address
        # ---------------------------------------------------------

        address = Address(
            user_id=user_id,
            label=payload.label,
            street=payload.street,
            city=payload.city,
            state=payload.state,
            postal_code=payload.postal_code,
            country=payload.country,
            is_default=is_default,
        )

        self.session.add(address)

        await self.session.commit()

        await self.session.refresh(address)

        return address

    async def get_address(
        self,
        user_id: UUID | str,
        address_id: UUID,
    ) -> Address:
        """
        Retrieve a user address.

        Raises:
            HTTPException(404)
        """

        stmt = select(Address).where(
            Address.id == address_id,
            Address.user_id == user_id,
        )

        result = await self.session.execute(stmt)

        address = result.scalar_one_or_none()

        if address is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found.",
            )

        return address

    async def list_addresses(
        self,
        user_id: UUID | str,
    ) -> list[Address]:
        """
        Retrieve all addresses belonging to a user.
        """

        stmt = (
            select(Address)
            .where(Address.user_id == user_id)
            .order_by(Address.is_default.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
