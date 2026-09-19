"""스키마가 마이그레이션으로 만들어졌는지 확인한다 (NFR14.3).

기술적·배관 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import pytest
from sqlalchemy import Engine, inspect, text

from app.repository.models import INITIAL_TABLES

pytestmark = pytest.mark.integration


def test_schema_was_created_by_migration(db_engine: Engine) -> None:
    """`alembic_version` 이 있고 초기 리비전이 적용되어 있다."""
    inspector = inspect(db_engine)
    assert (
        "alembic_version" in inspector.get_table_names()
    ), "alembic_version 이 없다 — 스키마가 마이그레이션이 아닌 다른 경로로 만들어졌다"

    with db_engine.connect() as connection:
        applied = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()
    assert applied == "0001_initial_schema"


@pytest.mark.ac("AC9.2.1")
def test_initial_revision_creates_twenty_tables(db_engine: Engine) -> None:
    """엔티티 20개 테이블이 모두 있다 (계약 C15)."""
    present = set(inspect(db_engine).get_table_names()) - {"alembic_version"}
    assert present == set(INITIAL_TABLES), (
        f"없는 테이블: {sorted(set(INITIAL_TABLES) - present)} / "
        f"더 있는 테이블: {sorted(present - set(INITIAL_TABLES))}"
    )


def test_application_startup_does_not_run_migrations(db_engine: Engine) -> None:
    """기동 흐름은 스키마를 건드리지 않는다 (functional-spec.md W1)."""
    from fastapi.testclient import TestClient

    from app.main import create_app

    with db_engine.connect() as connection:
        before = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()
        table_count_before = connection.execute(
            text("SELECT count(*) FROM pg_tables WHERE schemaname = 'public'")
        ).scalar_one()

    with TestClient(create_app()):
        pass

    with db_engine.connect() as connection:
        after = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()
        table_count_after = connection.execute(
            text("SELECT count(*) FROM pg_tables WHERE schemaname = 'public'")
        ).scalar_one()

    assert after == before, "기동이 마이그레이션을 돌렸다"
    assert table_count_after == table_count_before, "기동이 테이블을 만들었다"
