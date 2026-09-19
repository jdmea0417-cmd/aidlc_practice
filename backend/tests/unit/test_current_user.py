"""현재 사용자 결정 지점 (NFR6.1, NFR6.2, BR2.3).

저장소를 만지지 않는다 — 저장소 호출만 가짜로 둔다.
기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from app.common.exceptions import NotFoundError
from app.fixtures.constants import SEED_USER_ID
from app.service import current_user as current_user_module

BACKEND_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.ac("AC9.2.1")
def test_seed_user_is_resolved_without_any_credential(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    asked: list[object] = []
    sentinel = object()

    def _fake_get(session: object, user_id: object) -> object:
        asked.append(user_id)
        return sentinel

    monkeypatch.setattr(
        current_user_module.account_repository, "get_user_by_id", _fake_get
    )

    assert current_user_module.resolve_current_user(object()) is sentinel  # type: ignore[arg-type]
    assert asked == [SEED_USER_ID]


def test_missing_seed_user_is_a_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        current_user_module.account_repository,
        "get_user_by_id",
        lambda session, user_id: None,
    )

    with pytest.raises(NotFoundError) as raised:
        current_user_module.resolve_current_user(object())  # type: ignore[arg-type]

    assert raised.value.code == "SEED_USER_NOT_FOUND"


def test_the_seed_user_id_is_read_in_exactly_one_decision_point() -> None:
    """u11 이 들어올 때 고칠 자리가 하나여야 한다.

    클라이언트 식별자는 어디서도 읽지 않는다.
    """
    readers = sorted(
        str(path.relative_to(BACKEND_ROOT))
        for directory in ("app", "scripts")
        for path in (BACKEND_ROOT / directory).rglob("*.py")
        if "SEED_USER_ID" in path.read_text(encoding="utf-8")
    )

    allowed = {
        "app/fixtures/constants.py",  # 상수를 두는 자리
        "app/service/current_user.py",  # 결정 지점 하나
        "scripts/seed.py",  # 시드 적재
    }
    assert (
        set(readers) <= allowed
    ), f"고정 사용자 식별자를 읽는 자리가 늘었다: {readers}"
    assert "app/service/current_user.py" in readers, "결정 지점이 상수를 읽지 않는다"

    source = (BACKEND_ROOT / "app" / "service" / "current_user.py").read_text(
        encoding="utf-8"
    )
    assert not re.search(
        r"\brequest\b|\bheaders\b|\buser_id:", source
    ), "결정 지점이 클라이언트가 보낸 값을 읽는다"
