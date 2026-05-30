import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from user_service.db import Base


class Social(Base):
    __tablename__ = "socials"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    facebook: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    linkedin: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    twitter: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    instagram: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    tiktok: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    youtube: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    github: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
