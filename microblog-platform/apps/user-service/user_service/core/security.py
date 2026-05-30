from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt
from fastapi import HTTPException, Request, status  # noqa: E402
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from user_service.core.config import settings

# Setup standard OAuth2 scheme mapping for automated schema documentation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# This tells FastAPI to look for an "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")


async def is_authenticated(request: Request) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token has expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Read from the standard 'Authorization' header instead of 'authheader'
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing required 'Authorization' header.",
        )

    # 2. Extract and strip out the "Bearer " prefix safely
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token scheme. Expected 'Bearer <token>'.",
        )

    token = auth_header.replace("Bearer ", "", 1)

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return user_id

    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError) as exc:
        raise credentials_exception from exc


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # Convert string to bytes
    password_bytes = password.encode("utf-8")
    # Generate random salt
    salt = bcrypt.gensalt(10)
    # Compute the hash
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Decode back to a readable UTF-8 string to save in DB
    return hashed_password.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a password against its hash."""
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Generate an OAuth2/JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(UTC) + (
        expires_delta
        if expires_delta is not None
        else timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
