from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class OTP(Base):
    __tablename__ = "otps"

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
    # Identity binding
    # -----------------------------
    email = Column(
        String(255),
        nullable=False,
        index=True,
    )

    # -----------------------------
    # Security
    # -----------------------------
    hashed_otp = Column(
        String,
        nullable=False,
    )

    is_used = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # -----------------------------
    # Lifecycle
    # -----------------------------
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # -----------------------------
    # Indexes
    # -----------------------------
    __table_args__ = (
        Index("ix_otps_email_created_at", "email", "created_at"),
    )
