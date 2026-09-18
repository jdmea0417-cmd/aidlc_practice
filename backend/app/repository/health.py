"""저장소가 실제로 응답하는지 확인하는 질의 (BR3.1).

프로세스 생존만 보는 확인은 컨테이너는 떴는데 저장소에 못 붙은 상태를 통과시킨다.
질의에 **시간 제한**을 걸어 저장소가 매달릴 때 헬스체크까지 매달리지 않게 한다
(NFR10.15).
"""

from __future__ import annotations

from sqlalchemy import Engine


def ping(engine: Engine, *, timeout_seconds: float) -> None:
    """가벼운 확인 질의를 보낸다. 실패하면 예외를 그대로 올린다 — 삼키지 않는다."""
    timeout_ms = max(1, int(timeout_seconds * 1000))
    with engine.connect() as connection:
        connection.exec_driver_sql(f"SET statement_timeout = {timeout_ms}")
        connection.exec_driver_sql("SELECT 1")
