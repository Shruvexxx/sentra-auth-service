from pydantic import EmailStr
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # -----------------------------
    # App
    # -----------------------------
    PROJECT_NAME: str = "Sentra Auth Service"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # -----------------------------
    # Database
    # -----------------------------
    DATABASE_URL: str

    # -----------------------------
    # Security / JWT
    # -----------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # -----------------------------
    # OTP
    # -----------------------------
    OTP_EXPIRE_MINUTES: int = 10

    # -----------------------------
    # Google OAuth
    # -----------------------------
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # -----------------------------
    # Email (SMTP)
    # -----------------------------
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: EmailStr
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: EmailStr
    EMAILS_FROM_NAME: str = "Sentra"

    # -----------------------------
    # CORS
    # -----------------------------
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
