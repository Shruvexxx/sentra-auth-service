from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------
# Import SQLAlchemy Base & Models
# -----------------------------
from app.core.database import Base
from app.models.user import User
from app.models.otp import OTP

# IMPORTANT:
# This ensures Alembic is aware of all models
target_metadata = Base.metadata


# -----------------------------
# Database URL from environment
# -----------------------------
def get_database_url() -> str:
    """
    Fetch DATABASE_URL from environment.
    Alembic should NEVER hardcode credentials.
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url


# -----------------------------
# Offline migrations
# -----------------------------
def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This generates SQL scripts without a DB connection.
    """
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -----------------------------
# Online migrations
# -----------------------------
def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    This connects directly to the database.
    """
    connectable = engine_from_config(
        {
            "sqlalchemy.url": get_database_url()
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# -----------------------------
# Entrypoint
# -----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
