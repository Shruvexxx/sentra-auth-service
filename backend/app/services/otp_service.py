import random
from sqlalchemy.orm import Session

from app.models.otp import OTP
from app.core.security import hash_otp, verify_otp, otp_expired


class OTPService:
    """
    Business logic for OTP lifecycle.
    No HTTP, no email sending here.
    """

    @staticmethod
    def generate_otp() -> str:
        """
        Generate a random 6-digit OTP as string.
        """
        return f"{random.randint(100000, 999999)}"

    @staticmethod
    def create_otp(db: Session, email: str) -> str:
        """
        Create and store a new OTP for an email.

        Returns the plaintext OTP (for sending via email).
        """
        otp_code = OTPService.generate_otp()
        hashed = hash_otp(email, otp_code)

        otp_record = OTP(
            email=email,
            hashed_otp=hashed,
            is_used=False,
        )

        db.add(otp_record)
        db.commit()

        return otp_code

    @staticmethod
    def verify_otp(db: Session, email: str, otp_code: str) -> bool:
        """
        Verify an OTP:
        - must exist
        - must match
        - must not be expired
        - must not be used
        """
        otp_record = (
            db.query(OTP)
            .filter(
                OTP.email == email,
                OTP.is_used.is_(False),
            )
            .order_by(OTP.created_at.desc())
            .first()
        )

        if not otp_record:
            return False

        if otp_expired(otp_record.created_at):
            return False

        if not verify_otp(email, otp_code, otp_record.hashed_otp):
            return False

        otp_record.is_used = True
        db.commit()

        return True
