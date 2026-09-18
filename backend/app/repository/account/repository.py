"""사용자 저장소 접근.

- **커밋하지 않는다** — 확정은 `service` 경계에서 한 번이다 (BR5.3).
- 예외를 잡아 `None` 을 돌려주지 않는다. "없음"과 "실패"는 서로 다른 값이다.
  없으면 `None`, 실패하면 예외가 그대로 올라간다.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.repository.models import User


def get_user_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    """식별자로 사용자를 찾는다. 없으면 `None` 이다."""
    return session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()


def set_consented_at(session: Session, user: User, consented_at: datetime) -> User:
    """동의 시각을 적는다. 커밋은 하지 않는다."""
    user.consented_at = consented_at
    session.add(user)
    session.flush()
    return user
