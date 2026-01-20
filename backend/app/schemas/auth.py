from pydantic import BaseModel, EmailStr, Field


# -----------------------------
# Signup
# -----------------------------
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password (8–128 characters)",
    )


class SignupResponse(BaseModel):
    message: str


# -----------------------------
# OTP Verification
# -----------------------------
class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(
        min_length=6,
        max_length=6,
        description="6-digit OTP code",
        example="123456",
    )


class VerifyOTPResponse(BaseModel):
    message: str


# -----------------------------
# Login
# -----------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    message: str


# -----------------------------
# Google OAuth
# -----------------------------
class GoogleLoginRequest(BaseModel):
    google_token: str


class GoogleLoginResponse(BaseModel):
    message: str
