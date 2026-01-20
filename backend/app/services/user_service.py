from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models.user import User, AuthProviderEnum


class UserService:
    """
    Business logic related to users.
    No HTTP, no JWT, no OTP here.
    """

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """
        Fetch an active user by email.
        Soft-deleted users are excluded.
        """
        return (
            db.query(User)
            .filter(
                User.email == email,
                User.deleted_at.is_(None),
            )
            .first()
        )

    @staticmethod
    def get_by_id(db: Session, user_id) -> Optional[User]:
        """
        Fetch an active user by ID.
        """
        return (
            db.query(User)
            .filter(
                User.id == user_id,
                User.deleted_at.is_(None),
            )
            .first()
        )

    @staticmethod
    def create_local_user(
        db: Session,
        email: str,
        hashed_password: str,
    ) -> User:
        """
        Create a new local-auth user (email/password).

        User is NOT verified by default.
        """
        user = User(
            email=email,
            hashed_password=hashed_password,
            auth_provider=AuthProviderEnum.LOCAL,
            is_verified=False,
        )

        db.add(user)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(user)
        return user

    @staticmethod
    def create_google_user(
        db: Session,
        email: str,
        google_id: str,
    ) -> User:
        """
        Create a new Google-auth user.

        Google users are auto-verified.
        """
        user = User(
            email=email,
            google_id=google_id,
            auth_provider=AuthProviderEnum.GOOGLE,
            is_verified=True,
        )

        db.add(user)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(user)
        return user

    @staticmethod
    def mark_verified(db: Session, user: User) -> User:
        """
        Mark a user as verified.
        """
        user.is_verified = True
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def soft_delete(db: Session, user: User) -> None:
        """
        Soft delete a user.
        """
        user.deleted_at = datetime.utcnow()
        db.commit()
