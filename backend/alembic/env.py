"""Alembic 실행 환경.

연결 문자열은 설정 객체에서 읽는다 — 코드에도 ini 에도 박지 않는다 (BR6.4).
시험은 `sqlalchemy.url` 을 직접 넣어 이 파일을 그대로 쓴다 (NFR14.3).
"""

from __future__ import annotations

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.repository.models import Base

config = context.config

if config.get_main_option("sqlalchemy.url", None) is None:
    from app.config import get_settings

    config.set_main_option("sqlalchemy.url", get_settings().database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
