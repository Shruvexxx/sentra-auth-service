from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.oauth import oauth
from app.utils.cookies import set_auth_cookies
from app.core.config import settings
from app.api.deps import get_db_session
from app.services.auth_service import AuthService

router = APIRouter(prefix="/google", tags=["Google Auth"])


@router.get("/login")
async def google_login(request: Request):
    """
    Step 1: Redirect user to Google OAuth
    This MUST be triggered via browser navigation (not fetch).
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def google_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db_session),
):
    """
    Step 2: Google redirects here after user consents
    """
    try:
        tokens = await AuthService.google_login(db, request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    # Set HTTP-only auth cookies
    set_auth_cookies(
        response=response,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        access_token_expiry_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expiry_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    # ✅ OAuth MUST end with a redirect
    return RedirectResponse(
        url=settings.FRONTEND_OAUTH_SUCCESS_URL,
        status_code=302,
    )
