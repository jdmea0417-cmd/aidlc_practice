"""사용자 조회와 첫 방문 동의 (W3, W4).

- `fastapi` 를 import 하지 않는다. `HTTPException` 도 던지지 않는다 (TC-14).
- **확정은 이 경계에서 한 번** 한다. 저장소 계층은 커밋하지 않는다 (BR5.3).
- 동의는 한 번 저장되면 되돌리지 않는다. 이미 동의한 사용자가 다시 보내면 **처음 동의
시각을
  유지하고** 성공으로 답한다 (BR2.2, SM-C).
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.common.logging import get_logger
from app.repository.account import repository as account_repository
from app.repository.models import User
from app.service.current_user import resolve_current_user

_log = get_logger(component="account")


def _now() -> datetime:
    return datetime.now(UTC)


def get_me(session: Session) -> User:
    """현재 사용자를 돌려준다. 동의 시각이 비어 있으면 아직 동의 전이다."""
    return resolve_current_user(session)


def give_consent(session: Session, *, now: Callable[[], datetime] = _now) -> User:
    """첫 방문 안내에 동의한다. 여러 번 보내도 처음 시각이 남는다 (BR2.2)."""
    user = resolve_current_user(session)

    if user.consented_at is not None:
        _log.info("이미 동의한 사용자의 동의 요청이라 처음 시각을 유지한다")
        return user

    account_repository.set_consented_at(session, user, now())
    session.commit()
    _log.info("첫 방문 동의를 저장했다")
    return user
