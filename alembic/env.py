import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Load app settings from root
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "app")))

from core.config import settings
from core.database import Base  # your models should be imported somewhere

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Override sqlalchemy.url from env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
