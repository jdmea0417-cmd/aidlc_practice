"""사용자 저장소 접근 (Step 6 — 저장소 계층 구현 뒤).

기술적·배관 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from app.repository.account import repository as account_repository
from app.repository.models import User

pytestmark = pytest.mark.integration


def _make_user(session: Session, *, display_name: str = "합성 사용자") -> User:
    user = User(id=uuid.uuid4(), display_name=display_name)
    session.add(user)
    session.flush()
    return user


@pytest.mark.ac("AC9.2.1")
def test_get_user_by_id_returns_the_user(db_session: Session) -> None:
    user = _make_user(db_session)

    found = account_repository.get_user_by_id(db_session, user.id)

    assert found is not None
    assert found.id == user.id
    assert found.consented_at is None, "새로 만든 사용자는 동의 전이다 (BR2.1)"


def test_missing_user_and_failure_are_different_values(db_session: Session) -> None:
    """ "없음"은 `None`, "실패"는 예외다 — 저장소가 둘을 섞지 않는다."""
    assert account_repository.get_user_by_id(db_session, uuid.uuid4()) is None

    db_session.execute(text("ALTER TABLE users RENAME TO users_temporarily_gone"))
    try:
        with pytest.raises(DBAPIError):
            account_repository.get_user_by_id(db_session, uuid.uuid4())
    finally:
        db_session.rollback()


def test_repository_does_not_commit(db_session: Session) -> None:
    """BR5.3 — 저장소는 확정하지 않는다. 확정은 service 경계에서 한 번이다."""
    user = _make_user(db_session)
    committed: list[str] = []

    original_commit = Session.commit

    def _record_commit(self: Session) -> None:  # pragma: no cover - 불리면 실패다
        committed.append("commit")
        original_commit(self)

    Session.commit = _record_commit  # type: ignore[method-assign]
    try:
        account_repository.set_consented_at(db_session, user, user.created_at)
    finally:
        Session.commit = original_commit  # type: ignore[method-assign]

    assert committed == [], "repository 가 커밋했다"
    assert user.consented_at is not None, "동의 시각은 세션에 반영되어 있어야 한다"
