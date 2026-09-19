"""작업 단위 장치 (reliability-design.md §2, BR5.1~BR5.3).

저장소를 만지지 않는다 — 세션은 가짜를 쓰고, 장치가 세션을 **어떻게 다루는지**만 본다.
기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import inspect
import json

import pytest

from app.common.unit_of_work import run_unit_of_work


class FakeSession:
    """세션이 받은 명령을 순서대로 기록하는 가짜."""

    def __init__(self, *, fail_on_commit: bool = False) -> None:
        self.calls: list[str] = []
        self._fail_on_commit = fail_on_commit

    def commit(self) -> None:
        self.calls.append("commit")
        if self._fail_on_commit:
            raise RuntimeError("확정이 실패했다")

    def rollback(self) -> None:
        self.calls.append("rollback")

    def close(self) -> None:
        self.calls.append("close")


class SessionFactory:
    """부를 때마다 새 세션을 준다 — 몇 번 열렸는지가 그대로 보인다."""

    def __init__(self, *, fail_on_commit_for: set[int] | None = None) -> None:
        self.sessions: list[FakeSession] = []
        self._fail_for = fail_on_commit_for or set()

    def __call__(self) -> FakeSession:
        session = FakeSession(fail_on_commit=len(self.sessions) in self._fail_for)
        self.sessions.append(session)
        return session


def test_successful_job_commits_exactly_once() -> None:
    factory = SessionFactory()

    outcome = run_unit_of_work(
        component="conversation",
        job_name="전사",
        work=lambda session: None,
        session_factory=factory,
    )

    assert outcome.succeeded is True
    assert factory.sessions[0].calls == ["commit", "close"]
    assert len(factory.sessions) == 1


def test_failing_job_rolls_back() -> None:
    factory = SessionFactory()

    def _boom(session: object) -> None:
        raise RuntimeError("전사가 실패했다")

    outcome = run_unit_of_work(
        component="conversation", job_name="전사", work=_boom, session_factory=factory
    )

    assert outcome.succeeded is False
    assert outcome.error_type == "RuntimeError"
    assert factory.sessions[0].calls == ["rollback", "close"]


def test_failure_is_recorded_on_a_separate_connection() -> None:
    """되돌린 연결로는 실패 기록도 함께 사라진다 (reliability-design.md §1 의 B)."""
    factory = SessionFactory()
    recorded: list[object] = []

    def _boom(session: object) -> None:
        raise RuntimeError("전사가 실패했다")

    outcome = run_unit_of_work(
        component="conversation",
        job_name="전사",
        work=_boom,
        record_failure=recorded.append,
        session_factory=factory,
    )

    assert outcome.failure_recorded is True
    assert len(factory.sessions) == 2, "실패 기록이 같은 연결에서 일어났다"
    assert recorded[0] is factory.sessions[1]
    assert factory.sessions[1].calls == ["commit", "close"]


def test_failing_to_record_failure_only_logs(caplog: pytest.LogCaptureFixture) -> None:
    """실패 기록 실패가 무한 되돌림이 되지 않게 한다."""
    factory = SessionFactory(fail_on_commit_for={1})

    def _boom(session: object) -> None:
        raise RuntimeError("전사가 실패했다")

    with caplog.at_level("ERROR"):
        outcome = run_unit_of_work(
            component="conversation",
            job_name="전사",
            work=_boom,
            record_failure=lambda session: None,
            session_factory=factory,
        )

    assert outcome.failure_recorded is False
    messages = [json.loads(record.getMessage())["message"] for record in caplog.records]
    assert any("실패 상태를 적는 것마저 실패했다" in message for message in messages)
    assert factory.sessions[1].calls == ["commit", "close"], "다시 되돌리려 했다"


def test_every_path_closes_the_session() -> None:
    for work in (lambda session: None, _raise):
        factory = SessionFactory()
        run_unit_of_work(
            component="assessment",
            job_name="분석",
            work=work,
            record_failure=lambda session: None,
            session_factory=factory,
        )
        for session in factory.sessions:
            assert session.calls[-1] == "close", "닫히지 않은 연결이 있다"


def _raise(session: object) -> None:
    raise RuntimeError("분석이 실패했다")


def test_work_function_never_receives_a_request_session() -> None:
    """장치가 연결을 직접 연다 — 요청 연결이 흘러들어올 자리가 없다 (BR5.1)."""
    signature = inspect.signature(run_unit_of_work)
    assert (
        "session" not in signature.parameters
    ), "장치가 열린 세션을 인자로 받으면 요청 연결이 흘러들어올 수 있다"

    factory = SessionFactory()
    request_session = FakeSession()
    seen: list[object] = []

    run_unit_of_work(
        component="assessment",
        job_name="분석",
        work=seen.append,
        session_factory=factory,
    )

    assert seen[0] is factory.sessions[0]
    assert seen[0] is not request_session
    assert request_session.calls == []
