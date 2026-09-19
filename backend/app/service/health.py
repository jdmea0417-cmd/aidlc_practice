"""헬스체크 업무 로직 (BR3.1, observability-design.md §4).

프로세스 생존만 보지 않는다. 저장소에 가벼운 확인 질의를 보내 응답할 때만 정상이라고
답한다.
확인 질의에는 시간 제한을 건다 — 저장소가 매달릴 때 헬스체크까지 매달리면 컨테이너 준비
확인이 멈춘다 (NFR10.15).
"""

from __future__ import annotations

from sqlalchemy import Engine

from app.common.logging import get_logger
from app.repository import health as health_repository

_log = get_logger(component="common")


def check_storage(engine: Engine, *, timeout_seconds: float) -> bool:
    """저장소가 응답하면 참. 실패는 삼키지 않고 로그로 드러낸다."""
    try:
        health_repository.ping(engine, timeout_seconds=timeout_seconds)
    except Exception as exc:
        _log.error(
            "헬스체크 확인 질의가 실패했다",
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        return False
    return True
