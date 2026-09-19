"""요청 식별자·작업 식별자 문맥 (BR6.1, BR6.2).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import json

import pytest

from app.common.logging import get_logger
from app.common.request_context import (
    current_job_id,
    current_request_id,
    job_context,
    request_context,
)


def _lines(caplog: pytest.LogCaptureFixture) -> list[dict]:
    return [json.loads(record.getMessage()) for record in caplog.records]


def test_request_id_is_attached_automatically(caplog: pytest.LogCaptureFixture) -> None:
    log = get_logger(component="common")
    with caplog.at_level("INFO"), request_context("요청-7"):
        log.info("요청을 받았다")

    assert _lines(caplog)[0]["request_id"] == "요청-7"


def test_job_id_is_attached_automatically(caplog: pytest.LogCaptureFixture) -> None:
    log = get_logger(component="conversation")
    with caplog.at_level("INFO"), job_context("작업-3", "요청-7"):
        log.info("작업을 시작한다")

    assert _lines(caplog)[0]["job_id"] == "작업-3"


def test_job_carries_the_request_id_that_created_it(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """요청 문맥은 이미 끝나 있으므로 작업이 값을 인자로 받아 자기 문맥에 담는다."""
    log = get_logger(component="conversation")
    with caplog.at_level("INFO"), job_context("작업-3", "요청-7"):
        log.info("작업이 끝났다")

    line = _lines(caplog)[0]
    assert (line["request_id"], line["job_id"]) == ("요청-7", "작업-3")


def test_job_id_is_empty_on_the_request_path() -> None:
    with request_context("요청-7"):
        assert current_request_id() == "요청-7"
        assert current_job_id() == ""


def test_both_ids_are_empty_outside_any_context() -> None:
    assert current_request_id() == ""
    assert current_job_id() == ""
