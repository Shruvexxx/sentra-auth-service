from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import health


def create_application() -> FastAPI:
    """
    Application factory.
    Using a factory makes testing and scaling easier.
    """

    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # -----------------------------
    # CORS (FIXED)
    # -----------------------------
    cors_origins = settings.BACKEND_CORS_ORIGINS

    # If origins are provided as comma-separated string, convert to list
    if isinstance(cors_origins, str):
        cors_origins = [origin.strip() for origin in cors_origins.split(",")]

    # Always allow Swagger UI itself
    cors_origins.extend([
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ])

    # Add SessionMiddleware first (order matters)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY if hasattr(settings, 'SECRET_KEY') else "your-secret-key-change-this"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(set(cors_origins)),  # remove duplicates
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------
    # Routers
    # -----------------------------
    app.include_router(auth.router, prefix=settings.API_V1_STR)
    app.include_router(users.router, prefix=settings.API_V1_STR)
    app.include_router(health.router, prefix=settings.API_V1_STR)

    return app


app = create_application()
