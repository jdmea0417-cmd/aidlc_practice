"""픽스처가 단일 출처다 (BR4.3, NFR14.1).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from app.fixtures.loader import FIXTURE_FILES, load_all_fixtures, load_fixture

BACKEND_ROOT = Path(__file__).resolve().parents[2]


def test_all_three_conversations_load() -> None:
    fixtures = load_all_fixtures()

    assert set(fixtures) == {"conv_repair_01", "conv_topic_02", "conv_unclear_03"}
    for fixture in fixtures.values():
        assert fixture.transcript(1), "전사가 비어 있다"
        assert fixture.judgment_candidates(1), "기대 판정이 비어 있다"


def test_unknown_key_raises_instead_of_falling_back() -> None:
    """되돌림은 `resolve_conversation_key()` 한 곳에서만 일어난다."""
    with pytest.raises(KeyError):
        load_fixture("conv_unknown_99")


def test_no_fixture_value_is_duplicated_in_source_code() -> None:
    """손으로 옮긴 사본이 있으면 어긋나도 각자 초록이라 아무도 모른다."""
    texts = [
        utterance.text
        for fixture in load_all_fixtures().values()
        for utterance in fixture.transcript(1)
    ]
    sources = [
        path
        for directory in ("app", "tests", "scripts")
        for path in (BACKEND_ROOT / directory).rglob("*.py")
    ]

    offenders = [
        f"{path.relative_to(BACKEND_ROOT)}: {text!r}"
        for path in sources
        for text in texts
        if text in path.read_text(encoding="utf-8")
    ]
    assert offenders == [], f"픽스처 값이 코드에 옮겨 적혀 있다: {offenders}"


def test_each_fixture_file_declares_it_is_the_single_source() -> None:
    for file_name in FIXTURE_FILES.values():
        raw = (BACKEND_ROOT / "app" / "fixtures" / file_name).read_text(
            encoding="utf-8"
        )
        head = raw[: raw.index("\n", raw.index("__note"))]
        assert re.search("단일 출처", head), f"{file_name} 머리에 단일 출처 표기가 없다"
