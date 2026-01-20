from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get the currently authenticated user's profile.
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "auth_provider": current_user.auth_provider,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
    }
