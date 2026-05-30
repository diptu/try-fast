from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from user_service.core.config import settings


class UserBase(BaseModel):
    name: str
    image: str = Field(default_factory=lambda: settings.DEFAULT_USER_IMAGE)
    email: EmailStr

    role: Literal["customer", "admin", "superadmin"] = "customer"
    status: Literal["active", "suspended", "archived"] = "active"

    is_email_verified: bool = False

    def get_default_user_image(self) -> str:
        return settings.DEFAULT_USER_IMAGE


# CREATE
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


# UPDATE (PATCH-style)
class UserUpdate(UserBase):
    password: str


# READ RESPONSE (API OUTPUT)


class UserRead(UserBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        validate_by_name=True,
    )
