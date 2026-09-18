"""저장소 연결과 세션.

- 동기 엔진이다 (D-54). 라우트도 동기 `def` 로 쓴다.
- **연결 풀 크기 5** (infrastructure-specification.md §2·§2.1). 작게 잡아 연결 누수가
빨리
  드러나게 한다. 정상 동작의 동시 점유 상한은 3이라 여유가 2 남는다. `max_overflow=0` 을
  함께
  두는 이유가 이것이다 — 넘치면 조용히 늘어나는 대신 기다리고, 그 기다림이 신호가 된다.
- 요청 경로는 `Depends(get_session)` 로 **요청당 세션 하나**를 받는다.
- 응답 이후에 도는 작업은 그 세션을 재사용하지 않는다 (BR5.1). `new_session()` 으로 자기
  세션을 새로 연다 — 실제 수명 관리는 `app/common/unit_of_work.py` 가 맡는다 (BR5.2).
"""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    """기동 시 한 번 만들어 재사용하는 엔진."""
    global _engine
    if _engine is None:
        from app.config import get_settings

        settings = get_settings()
        _engine = create_engine(
            settings.database_url,
            pool_size=settings.db_pool_size,
            max_overflow=0,
            pool_pre_ping=True,
            future=True,
        )
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    """세션 팩토리. 응답 이후 작업이 자기 세션을 열 때 쓴다 (계약 공통 규칙)."""
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(
            bind=get_engine(), autoflush=False, expire_on_commit=False
        )
    return _session_factory


def new_session() -> Session:
    """새 세션 하나. 요청 세션을 재사용하지 않는 자리에서만 쓴다 (BR5.1)."""
    return get_session_factory()()


def get_session() -> Iterator[Session]:
    """요청당 세션 하나를 주입한다. 커밋은 `service` 경계에서 한 번 한다 (BR5.3)."""
    session = new_session()
    try:
        yield session
    finally:
        session.close()


def reset_engine() -> None:
    """엔진과 세션 팩토리를 버린다. 설정을 바꿔 다시 만들어야 하는 시험에서만 쓴다."""
    global _engine, _session_factory
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_factory = None
