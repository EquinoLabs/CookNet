import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from database.database import Base  # <-- Adjust import path accordingly
import api

from dotenv import load_dotenv

# Load .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
CONNECTION_NEON_DB = os.getenv("CONNECTION_NEON_DB")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# If DATABASE_URL is defined in .env, override the ini setting
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", f"{DATABASE_URL}{CONNECTION_NEON_DB}")

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_async():
    asyncio.run(run_migrations_online())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_async()
