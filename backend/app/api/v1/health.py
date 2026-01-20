from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def health_check():
    """
    Health check endpoint.

    Used by:
    - load balancers
    - uptime monitors
    - deployment systems
    """
    return {
        "status": "ok",
        "service": "sentra-auth-service",
    }
