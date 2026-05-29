from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from user_service.core.config import settings
from user_service.schemas.address import AddressBase
from user_service.schemas.social import SocialBase


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
    id: UUID
    password: str = Field(..., min_length=8)
    address: AddressBase | None = None
    social: SocialBase | None = None


# UPDATE (PATCH-style)
class UserUpdate(UserBase):
    password: str
    address: AddressBase | None = None
    social: SocialBase | None = None


# READ RESPONSE (API OUTPUT)
class UserRead(UserBase):
    id: UUID

    address: AddressBase | None = None
    social: SocialBase | None = None

    model_config = {"from_attributes": True}
