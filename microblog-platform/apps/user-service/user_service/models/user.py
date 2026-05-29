import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from user_service.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    image: Mapped[str] = mapped_column(String(500), nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[str] = mapped_column(String(50), default="customer")
    status: Mapped[str] = mapped_column(String(50), default="active")

    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # relationships
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    social = relationship(
        "Social", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
