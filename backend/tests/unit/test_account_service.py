"""동의 업무 로직 (W3, W4, BR2.2, BR5.3, SM-C).

저장소를 만지지 않는다 — 세션과 저장소 호출을 가짜로 둔다.
동의 규칙 자체를 검증하는 것은 한국어, 배관 동작은 영어로 이름을 쓴다.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

import pytest

from app.repository.models import User
from app.service.account import service as account_service

BACKEND_ROOT = Path(__file__).resolve().parents[2]
FIXED_NOW = datetime(2026, 9, 18, 10, 0, tzinfo=UTC)
LATER = datetime(2026, 9, 18, 11, 0, tzinfo=UTC)


class FakeSession:
    def __init__(self) -> None:
        self.commits = 0

    def add(self, obj: object) -> None:  # pragma: no cover - 가짜 세션의 빈 동작
        pass

    def flush(self) -> None:  # pragma: no cover - 가짜 세션의 빈 동작
        pass

    def commit(self) -> None:
        self.commits += 1


@pytest.fixture()
def user() -> User:
    return User(display_name="합성 사용자")


@pytest.fixture(autouse=True)
def _fixed_user(monkeypatch: pytest.MonkeyPatch, user: User) -> None:
    monkeypatch.setattr(account_service, "resolve_current_user", lambda session: user)


@pytest.mark.ac("AC9.2.1")
def test_동의_전_사용자는_동의_시각이_비어_있다(user: User) -> None:
    assert account_service.get_me(FakeSession()).consented_at is None  # type: ignore[arg-type]


@pytest.mark.ac("AC9.2.1")
def test_첫_동의는_동의_시각을_적는다(user: User) -> None:
    session = FakeSession()

    updated = account_service.give_consent(session, now=lambda: FIXED_NOW)  # type: ignore[arg-type]

    assert updated.consented_at == FIXED_NOW
    assert session.commits == 1, "확정은 service 경계에서 한 번이다 (BR5.3)"


def test_이미_동의했으면_처음_시각을_유지한다(user: User) -> None:
    user.consented_at = FIXED_NOW
    session = FakeSession()

    updated = account_service.give_consent(session, now=lambda: LATER)  # type: ignore[arg-type]

    assert (
        updated.consented_at == FIXED_NOW
    ), "같은 동의를 다시 보냈더니 시각이 갱신되었다"
    assert session.commits == 0, "바꿀 것이 없는데 확정했다"


def test_동의는_되돌아가지_않는다(user: User) -> None:
    """SM-C — 되돌아가는 전이가 없다. 동의 철회는 이번 범위 밖이다."""
    session = FakeSession()
    account_service.give_consent(session, now=lambda: FIXED_NOW)  # type: ignore[arg-type]

    for _ in range(3):
        account_service.give_consent(session, now=lambda: LATER)  # type: ignore[arg-type]

    assert user.consented_at == FIXED_NOW
    assert session.commits == 1


def test_service_layer_never_raises_http_exceptions() -> None:
    """TC-14 — HTTP 로의 번역은 common 의 예외 처리기 한 곳이 담당한다."""
    sources = list((BACKEND_ROOT / "app" / "service").rglob("*.py"))
    assert sources, "service 계층에 파일이 없다"

    used = re.compile(
        r"raise\s+HTTPException|import\s+HTTPException|HTTPException\s*\("
    )
    offenders = [
        str(path.relative_to(BACKEND_ROOT))
        for path in sources
        if used.search(path.read_text(encoding="utf-8"))
    ]
    assert offenders == [], f"service 가 HTTPException 을 던진다: {offenders}"
