import os
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from alembic import context
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env
load_dotenv()

# Get the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Alembic Config object which gives access to values in the .ini file
config = context.config

# Setup logging using the configuration file if provided
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models here to access their metadata
from database.makedb import Base  # Adjust this to the actual import path of your models

# Assign the target metadata to the metadata of your Base class
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = DATABASE_URL  # Use the value from the .env file
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        DATABASE_URL,  # Use the value from the .env file
        poolclass=pool.NullPool,
    )
    async_session = sessionmaker(connectable, expire_on_commit=False)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection) -> None:
    """Run migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

# Run migrations in offline or online mode based on the context
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
