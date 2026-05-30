from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user record by their unique email address."""
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Fetch a user record by their unique database primary key ID."""
        # Converts string ID back to integer or UUID depending on your Model definitions
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def save(self, user: User) -> User:
        """Commit an updated user instance or refresh it within the session."""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
