from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.services.user_service import UserService
from app.services.otp_service import OTPService
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.models.user import User
from app.utils.email import EmailClient


class AuthService:
    """
    High-level authentication workflows.

    This service orchestrates:
    - signup
    - OTP verification
    - login
    - token issuance

    No HTTP, no FastAPI dependencies.
    """

    @staticmethod
    def signup(db: Session, email: str, password: str) -> None:
        """
        Signup flow for email/password users.

        Steps:
        - ensure user does not exist
        - create unverified user
        - generate OTP
        - send OTP via email
        """
        existing_user = UserService.get_by_email(db, email)
        if existing_user:
            raise ValueError("User already exists")

        hashed_password = hash_password(password)

        try:
            UserService.create_local_user(
                db=db,
                email=email,
                hashed_password=hashed_password,
            )
        except IntegrityError:
            raise ValueError("User already exists")

        otp_code = OTPService.create_otp(db, email)

        EmailClient().send_otp_email(
            to_email=email,
            otp=otp_code,
        )

    @staticmethod
    def verify_otp(db: Session, email: str, otp_code: str) -> None:
        """
        OTP verification flow.

        Steps:
        - validate OTP
        - mark user as verified
        """
        user = UserService.get_by_email(db, email)
        if not user:
            raise ValueError("User not found")

        valid = OTPService.verify_otp(
            db=db,
            email=email,
            otp_code=otp_code,
        )

        if not valid:
            raise ValueError("Invalid or expired OTP")

        UserService.mark_verified(db, user)

    @staticmethod
    def login(db: Session, email: str, password: str) -> dict:
        """
        Login flow for email/password users.

        Steps:
        - fetch user
        - check verification
        - verify password
        - issue JWT tokens
        """
        user: User = UserService.get_by_email(db, email)
        if not user:
            raise ValueError("Invalid credentials")

        if not user.is_verified:
            raise PermissionError("Email not verified")

        if not user.hashed_password:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

from authlib.integrations.starlette_client import OAuthError
from app.core.oauth import oauth


class AuthService:
    ...

    @staticmethod
    async def google_login(db, request):
        """
        Handle Google OAuth callback.
        """
        try:
            token = await oauth.google.authorize_access_token(request)
        except OAuthError:
            raise ValueError("Google authentication failed")

        user_info = token.get("userinfo")
        if not user_info:
            raise ValueError("Google user info not available")

        email = user_info["email"]
        google_id = user_info["sub"]

        user = UserService.get_by_email(db, email)

        if not user:
            user = UserService.create_google_user(
                db=db,
                email=email,
                google_id=google_id,
            )

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
