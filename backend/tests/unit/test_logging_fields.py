"""로그 한 줄의 모양 (observability-design.md §1, BR6.3).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import json

import pytest

from app.common.logging import ALLOWED_COMPONENTS, get_logger
from app.common.request_context import request_context

SIX_FIELDS = {"timestamp", "level", "message", "component", "request_id", "job_id"}


def _emitted(caplog: pytest.LogCaptureFixture) -> dict:
    assert len(caplog.records) == 1, "로그 줄이 하나가 아니다"
    return json.loads(caplog.records[0].getMessage())


def test_every_line_carries_the_six_fields(caplog: pytest.LogCaptureFixture) -> None:
    log = get_logger(component="conversation")
    with caplog.at_level("INFO"), request_context("요청-1"):
        log.info("무언가 일어났다")

    line = _emitted(caplog)
    assert set(line) >= SIX_FIELDS
    assert line["request_id"] == "요청-1"
    assert line["job_id"] == ""


def test_component_is_attached_when_the_logger_is_created(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """로그 호출마다 컴포넌트를 적지 않는다 — 빠뜨리는 자리를 없앤다."""
    log = get_logger(component="providers")
    with caplog.at_level("INFO"):
        log.info("호출이 끝났다")

    assert _emitted(caplog)["component"] == "providers"


def test_unknown_component_is_refused() -> None:
    """자유 문자열이면 이름이 갈린다 — 허용값 여덟 개로 고정한다."""
    assert len(ALLOWED_COMPONENTS) == 8
    with pytest.raises(ValueError, match="모르는 컴포넌트"):
        get_logger(component="Conversation")


def test_exception_object_cannot_be_logged_whole() -> None:
    """제공자 예외가 요청 본문을 품고 있을 수 있다 — 종류와 메시지만 넘긴다."""
    log = get_logger(component="common")
    with pytest.raises(TypeError, match="예외 객체"):
        log.error("실패했다", error=RuntimeError("전사 본문이 여기 들어 있을 수 있다"))


def test_transcript_fields_are_refused_even_at_debug_level() -> None:
    """ "개발 중에만 켠다"가 시연 환경에서 켜져 있을 수 있다 (BR6.3)."""
    log = get_logger(component="assessment")
    with pytest.raises(ValueError, match="로그에 남길 수 없는 필드"):
        log.debug("판정을 만들었다", transcript="대화 본문이 들어 있는 문자열")
