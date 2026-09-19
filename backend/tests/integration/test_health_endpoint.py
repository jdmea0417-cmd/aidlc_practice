"""헬스체크 (W2, BR3.1, BR3.2, AC9.1.1, AC9.3.4).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import time

import pytest
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.pool import NullPool

pytestmark = pytest.mark.integration


@pytest.mark.ac("AC9.1.1")
@pytest.mark.ac("AC9.3.4")
def test_health_reports_ok_and_the_analysis_mode(api_client) -> None:
    response = api_client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "analysisMode": "mock"}


@pytest.mark.ac("AC9.1.1")
def test_health_is_not_ok_when_storage_does_not_answer(api_client) -> None:
    """컨테이너는 떴는데 저장소에 못 붙은 상태를 통과시키지 않는다."""
    api_client.app.state.engine = create_engine(
        "postgresql+psycopg://nobody@/none?host=/tmp/there-is-no-socket-here",
        poolclass=NullPool,
    )

    response = api_client.get("/api/v1/health")

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "STORAGE_UNAVAILABLE"


def test_health_query_carries_the_configured_timeout(
    api_client, db_engine: Engine
) -> None:
    """저장소가 매달릴 때 헬스체크까지 매달리면 컨테이너 준비 확인이 멈춘다.

    (NFR10.15)
    """
    statements: list[str] = []

    @event.listens_for(db_engine, "before_cursor_execute")
    def _capture(conn, cursor, statement, parameters, context, executemany) -> None:
        statements.append(statement)

    try:
        api_client.get("/api/v1/health")
    finally:
        event.remove(db_engine, "before_cursor_execute", _capture)

    timeout_ms = int(
        api_client.app.state.settings.health_check_query_timeout_seconds * 1000
    )
    assert f"SET statement_timeout = {timeout_ms}" in statements
    assert timeout_ms == 1000


def test_health_responds_within_200ms(api_client) -> None:
    api_client.get("/api/v1/health")  # 첫 호출의 연결 수립은 재지 않는다

    started = time.monotonic()
    response = api_client.get("/api/v1/health")
    elapsed_ms = (time.monotonic() - started) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 200, f"헬스체크가 {elapsed_ms:.0f}ms 걸렸다"
