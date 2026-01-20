from passlib.context import CryptContext
from datetime import datetime, timedelta
import hmac
import hashlib

from app.core.config import settings


# -----------------------------
# Password hashing (bcrypt)
# -----------------------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Note:
    bcrypt only uses the first 72 bytes of a password.
    We explicitly encode to UTF-8 to avoid ambiguity.
    """
    return pwd_context.hash(password.encode("utf-8"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.
    """
    return pwd_context.verify(
        plain_password.encode("utf-8"),
        hashed_password,
    )


# -----------------------------
# OTP hashing (HMAC-SHA256)
# -----------------------------
def hash_otp(email: str, otp: str) -> str:
    """
    Hash OTP using HMAC-SHA256.

    We include the email as part of the message to:
    - bind OTP to a specific identity
    - prevent OTP reuse across users
    """
    message = f"{email}:{otp}".encode("utf-8")
    secret = settings.JWT_SECRET_KEY.encode("utf-8")

    return hmac.new(
        key=secret,
        msg=message,
        digestmod=hashlib.sha256,
    ).hexdigest()


def verify_otp(email: str, otp: str, hashed_otp: str) -> bool:
    """
    Constant-time comparison of OTP hash.
    """
    expected_hash = hash_otp(email, otp)
    return hmac.compare_digest(expected_hash, hashed_otp)


def otp_expired(created_at: datetime) -> bool:
    """
    Check if OTP is expired based on configured expiry window.
    """
    return datetime.utcnow() > (
        created_at + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    )
