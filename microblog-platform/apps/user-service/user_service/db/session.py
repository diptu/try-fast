from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from user_service.core.config import settings

_engine = None
_session_maker: async_sessionmaker[AsyncSession] | None = None


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    """
    Lazily initialize async engine + sessionmaker.
    """
    global _engine, _session_maker

    if _session_maker is None:
        if not settings.DATABASE_URL:
            raise RuntimeError("DATABASE_URL must be set")

        _engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            poolclass=NullPool,
        )

        _session_maker = async_sessionmaker(
            bind=_engine,
            expire_on_commit=False,
        )

    return _session_maker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_session_maker()

    async with session_maker() as session:
        yield session
