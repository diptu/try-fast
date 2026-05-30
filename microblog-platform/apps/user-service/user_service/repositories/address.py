from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.models.address import Address


class AddressRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, address: Address) -> Address:
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def get_by_id(self, address_id: UUID) -> Address | None:
        """Fetch a user record by their unique database primary key ID."""
        # Converts string ID back to integer or UUID depending on your Model definitions
        statement = select(Address).where(Address.id == address_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def save(self, address: Address) -> Address:
        """Commit an updated user instance or refresh it within the session."""
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        return address
