# from user_service.core.security import hash_password
from user_service.models.user import User
from user_service.schemas.user import UserCreate


class UserService:
    """User Business Logic Layer"""

    def create_user(self, data: UserCreate) -> dict[str, User] | None:
        pass
        # hashed = hash_password(data.password)
