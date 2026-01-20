from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import decode_token, is_access_token
from app.services.user_service import UserService
from app.utils.cookies import ACCESS_TOKEN_COOKIE_NAME


# -----------------------------
# Database Dependency
# -----------------------------
def get_db_session() -> Generator[Session, None, None]:
    """
    Provides a SQLAlchemy database session per request.
    Ensures the session is closed after the request lifecycle.
    """
    yield from get_db()


# -----------------------------
# Auth Dependency (Cookie-based)
# -----------------------------
def get_current_user(
    request: Request,
    db: Session = Depends(get_db_session),
):
    """
    Retrieve the currently authenticated user from an HTTP-only cookie.

    Authentication flow:
    1. Read access token from cookie
    2. Decode and validate JWT
    3. Ensure token is an access token
    4. Fetch active user from database
    """

    # 1️⃣ Read token from HTTP-only cookie
    token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # 2️⃣ Decode & validate JWT
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # 3️⃣ Ensure correct token type
    if not is_access_token(payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    # 4️⃣ Extract user ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # 5️⃣ Fetch active user
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user
