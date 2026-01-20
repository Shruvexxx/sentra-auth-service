from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine

from app.core.config import settings


# -----------------------------
# SQLAlchemy Engine
# -----------------------------
engine: Engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    future=True,
)


# -----------------------------
# Session Factory
# -----------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


# -----------------------------
# Base class for models
# -----------------------------
Base = declarative_base()


# -----------------------------
# Dependency for DB session
# -----------------------------
def get_db():
    """
    FastAPI dependency.
    Creates a database session per request and
    ensures it is closed after the request ends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
