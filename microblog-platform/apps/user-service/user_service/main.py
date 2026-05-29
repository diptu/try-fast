from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI, status
from sqlalchemy import text

from user_service.core.config import settings
from user_service.db.session import get_session_maker

load_dotenv()

app = FastAPI(
    title=settings.SERVICE_NAME or "user-service",
    description="Microservice responsible for user management.",
    version=settings.SERVICE_VERSION or "0.1.0",
)


@app.get("/db_health")
async def database_health() -> dict[str, object]:
    try:
        session_maker = get_session_maker()

        async with session_maker() as session:
            await session.execute(text("SELECT 1"))

        return {
            "status_code": 200,
            "database": "healthy",
            "service": settings.SERVICE_NAME,
            "version": settings.SERVICE_VERSION,
        }

    except Exception as e:
        return {
            "status_code": 500,
            "database": "unhealthy",
            "error": str(e),
            "service": settings.SERVICE_NAME,
            "version": settings.SERVICE_VERSION,
        }


@app.get("/")
async def health() -> dict[str, object]:
    is_alive: bool = True

    return {
        "status_code": status.HTTP_200_OK
        if is_alive
        else status.HTTP_500_INTERNAL_SERVER_ERROR,
        "server": "healthy" if is_alive else "unhealthy",
        "service": settings.SERVICE_NAME,
        "version": settings.SERVICE_VERSION,
    }
