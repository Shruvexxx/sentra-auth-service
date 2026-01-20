from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class AuthProviderEnum(str):
    LOCAL = "local"
    GOOGLE = "google"


class User(Base):
    __tablename__ = "users"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # -----------------------------
    # Identity
    # -----------------------------
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password = Column(
        String,
        nullable=True,  # nullable for OAuth users
    )

    auth_provider = Column(
        String(50),
        nullable=False,
        default=AuthProviderEnum.LOCAL,
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # -----------------------------
    # Lifecycle / Auditing
    # -----------------------------
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    deleted_at = Column(
        DateTime,
        nullable=True,
    )

    # -----------------------------
    # OAuth (Google)
    # -----------------------------
    google_id = Column(
        String(255),
        unique=True,
        nullable=True,
    )

    def is_active(self) -> bool:
        """
        A user is active if not soft-deleted.
        """
        return self.deleted_at is None
