import smtplib
from email.message import EmailMessage
from typing import Optional

from app.core.config import settings


class EmailClient:
    """
    Centralized email sending utility.

    Designed so SMTP can later be replaced with
    services like AWS SES, SendGrid, etc.
    """

    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        """
        Send a plain-text email.
        """
        message = EmailMessage()
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(message)

    def send_otp_email(self, to_email: str, otp: str) -> None:
        """
        Send OTP email.

        This method exists to keep OTP messaging
        consistent and reusable.
        """
        subject = "Verify your email"
        body = (
            "Your verification code is:\n\n"
            f"{otp}\n\n"
            f"This code expires in {settings.OTP_EXPIRE_MINUTES} minutes.\n\n"
            "If you did not request this, please ignore this email."
        )

        self.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
        )
