"""
User API Routes
---------------

Aggregates all user-related route modules into a single router.

Endpoints
---------
Authentication:
    POST   /login

User Management:
    POST   /

Profile:
    GET    /me
    GET    /{id}
    PUT    /{id}

Administration:
    DELETE /{id}
"""

from fastapi import APIRouter

from user_service.api.v1.users.address import router as address_router
from user_service.api.v1.users.admin import router as admin_router
from user_service.api.v1.users.auth import router as auth_router
from user_service.api.v1.users.create import router as create_router
from user_service.api.v1.users.profile import router as profile_router

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

router.include_router(create_router)
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(admin_router)
router.include_router(address_router)


__all__ = ["router"]
