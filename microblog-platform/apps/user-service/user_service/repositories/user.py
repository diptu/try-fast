from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.models.user import User


class UserRepository:
    """User Data Access Layer"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        stmt = select(User).where(User.email == email)

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
