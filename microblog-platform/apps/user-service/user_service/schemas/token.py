from pydantic import BaseModel

from user_service.schemas.user import UserRead


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# Add this schema model to resolve the ImportError
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
