"""Migrations Alembic : l'URL vient de DATABASE_URL (jamais écrite dans un fichier)."""
from alembic import context
from sqlalchemy import engine_from_config, pool

from goldpilot.config import settings
from goldpilot.db import Base

config = context.config
config.set_main_option("sqlalchemy.url", settings().database_url)
target_metadata = Base.metadata


def run_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=connection.dialect.name == "sqlite")
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_offline()
else:
    run_online()
