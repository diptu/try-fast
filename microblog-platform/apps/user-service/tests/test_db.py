import pytest
from sqlalchemy import text
from user_service.db.session import get_session_maker


@pytest.mark.asyncio
async def test_db_connection() -> None:
    """
    Verify database connectivity using SELECT 1.
    """

    session_maker = get_session_maker()

    async with session_maker() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar_one()

    assert value == 1
