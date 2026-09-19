"""시험 실행기 준비.

Testcontainers 규약 (team.md § Testing Posture):
- 컨테이너는 **세션당 1개**.
- 스키마는 세션 시작 시 `alembic upgrade head` 로 한 번 만든다.
  `Base.metadata.create_all()` 을 쓰지 않는다 — 그래야 마이그레이션이 실제로 한 번은
  실행된다 (NFR14.3).
- 시험마다 트랜잭션을 열고 끝나면 되돌려 격리한다.

Docker 가 없는 환경에서는 `TEST_DATABASE_URL` 환경변수로 이미 떠 있는 저장소를 가리킬 수
있다.
둘 다 없으면 `integration` 표시가 붙은 시험만 건너뛴다 — 단위 시험은 저장소를 만지지
않으므로 그대로 돈다.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

BACKEND_ROOT = Path(__file__).resolve().parent.parent


def _apply_migrations(url: str) -> None:
    """스키마를 마이그레이션으로 만든다 (NFR14.3)."""
    from alembic import command
    from alembic.config import Config

    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", url)
    command.upgrade(config, "head")


@pytest.fixture(scope="session")
def database_url() -> Iterator[str]:
    """세션당 저장소 하나. 환경변수가 있으면 그것을 쓰고, 없으면 컨테이너를 띄운다."""
    external = os.environ.get("TEST_DATABASE_URL")
    if external:
        yield external
        return

    try:
        from testcontainers.postgres import PostgresContainer
    except ImportError as exc:  # pragma: no cover - 설치 누락은 환경 문제다
        pytest.skip(f"testcontainers 를 불러올 수 없다: {exc}")

    try:
        container = PostgresContainer("postgres:16", driver="psycopg")
        container.start()
    except Exception as exc:
        pytest.skip(
            "저장소를 띄울 수 없다(Docker 미가용으로 보인다). "
            f"TEST_DATABASE_URL 을 주면 그 저장소를 쓴다. 원인: {exc}"
        )

    try:
        yield container.get_connection_url()
    finally:
        container.stop()


@pytest.fixture(scope="session")
def db_engine(database_url: str) -> Iterator[Engine]:
    """세션 시작 시 마이그레이션을 한 번 적용한 엔진."""
    _apply_migrations(database_url)
    engine = create_engine(database_url, future=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture()
def db_session(db_engine: Engine) -> Iterator[Session]:
    """시험마다 트랜잭션을 열고 끝나면 되돌린다 — 시험 독립성은 타협 대상이 아니다."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def api_client(db_engine: Engine, db_session: Session):
    """앱을 세우고 요청 세션을 시험 트랜잭션에 묶는다.

    앱이 만든 엔진 대신 시험 저장소를 쓰게 한다 — 시험이 끝나면 모두 되돌아간다.
    """
    from fastapi.testclient import TestClient

    from app.db import get_session
    from app.main import create_app

    app = create_app()
    app.state.engine = db_engine
    app.dependency_overrides[get_session] = lambda: db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def seed_user(db_session: Session):
    """시드 고정 사용자 한 명 — 동의 전 상태로 시작한다 (BR2.1)."""
    from app.fixtures.constants import (
        SEED_USER_DISPLAY_NAME,
        SEED_USER_ID,
        SEED_USER_ROLE,
    )
    from app.repository.models import User

    user = User(
        id=SEED_USER_ID,
        display_name=SEED_USER_DISPLAY_NAME,
        role=SEED_USER_ROLE,
        consented_at=None,
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture(scope="session", autouse=True)
def connection_leak_guard(request: pytest.FixtureRequest) -> Iterator[None]:
    """연결이 새지 않는지 본다 (performance-design.md §5, NFR10.3).

    시험 세션이 끝난 뒤 저장소에 남아 있는 연결 수를 본다. 연결을 닫지 않는 경로가
    하나라도
    있으면 통합 시험을 반복하는 동안 수가 늘고, 풀 크기(5)를 넘어서면 바로 드러난다.
    저장소를 쓰지 않은 세션(단위 시험만 돈 경우)에는 볼 것이 없다.
    """
    yield

    try:
        url = request.getfixturevalue("database_url")
    except Exception:
        return

    probe = create_engine(url, poolclass=NullPool)
    try:
        with probe.connect() as connection:
            open_connections = connection.execute(
                text(
                    "SELECT count(*) FROM pg_stat_activity "
                    "WHERE datname = current_database() AND pid <> pg_backend_pid()"
                )
            ).scalar_one()
    finally:
        probe.dispose()

    assert open_connections <= 5, (
        f"시험이 끝났는데 연결 {open_connections}개가 남아 있다 — 풀 크기 5를 넘었다. "
        "닫지 않는 경로가 있다 (NFR10.3)"
    )
