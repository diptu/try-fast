from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, status
from sqlalchemy import text

from user_service.core.config import settings

# 1. CRITICAL: Import your Base metadata
from user_service.db import Base
from user_service.db.session import get_engine, get_session_maker
from user_service.routers import user

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # This runs when the server boots up
    engine = get_engine()

    async with engine.begin() as conn:
        # Inspects the database and creates any tables missing from Base.metadata
        await conn.run_sync(Base.metadata.create_all)

    yield
    # This runs when the server shuts down
    await engine.dispose()


app = FastAPI(
    title=settings.SERVICE_NAME or "user-service",
    description="Microservice responsible for user management.",
    version=settings.SERVICE_VERSION or "0.1.0",
    lifespan=lifespan,
)

# Include the routers into the main app
app.include_router(user.router)


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
