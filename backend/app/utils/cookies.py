from fastapi import Response
from datetime import timedelta


ACCESS_TOKEN_COOKIE_NAME = "access_token"
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
    access_token_expiry_minutes: int,
    refresh_token_expiry_days: int,
) -> None:
    """
    Set HTTP-only authentication cookies.
    """
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=False,  # set True in production (HTTPS)
        samesite="lax",
        max_age=access_token_expiry_minutes * 60,
        path="/",
    )

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=False,  # set True in production (HTTPS)
        samesite="lax",
        max_age=refresh_token_expiry_days * 24 * 60 * 60,
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    """
    Clear authentication cookies (logout).
    """
    response.delete_cookie(key=ACCESS_TOKEN_COOKIE_NAME, path="/")
    response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME, path="/")
