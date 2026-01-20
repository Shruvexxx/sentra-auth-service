from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.oauth import oauth
from app.utils.cookies import set_auth_cookies
from app.core.config import settings
from app.api.deps import get_db_session
from app.services.auth_service import AuthService

router = APIRouter()


@router.get("/google/login")
async def google_login(request: Request):
    """
    Redirect user to Google OAuth.
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db_session),
):
    """
    Google OAuth callback.
    """
    try:
        tokens = await AuthService.google_login(db, request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    set_auth_cookies(
        response=response,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        access_token_expiry_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expiry_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    return {"message": "Google login successful"}
