"""작업 단위 장치 — 실패 기록이 빠질 수 없는 구조 (reliability-design.md §2).

응답 이후에 도는 작업(전사·분석·재분석)이 모두 이 모양을 따른다. U1 은 모양을 만들고,
실제 작업 내용은 각 기능 단위가 채운다.

    작업 시작
      +-- 자기 작업 식별자 발급, 요청 식별자와 함께 문맥에 담기        BR6.2
      +-- [장치가 연결을 직접 연다]  <- 요청 연결을 쓰지 않는다        BR5.1
      |     +-- 성공 --> 한 번 확정 --> 닫기                          BR5.3
      |     +-- 예외 --> 되돌리기 --> 닫기
      |                   +-- [별도 연결] 실패 기록 --> 확정 --> 닫기
      +-- 어느 경로든 로그를 남긴다 (컴포넌트 + 두 식별자)

**실패 기록마저 실패하면 로그만 남기고 넘어간다.** 다시 되돌리지 않는다 — 실패 기록
실패가
무한 되돌림이 되지 않게 하는 것이 목적이다. 그 경우 상태는 진행 중으로 남지만 로그에는
실패가
남아 사람이 도달할 수 있다.

예약 수단은 웹 프레임워크의 기본 배경 작업이다 (`[Q1]` OQ-F5 의 답 A). 작업 큐·브로커를
도입하지 않는다.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.common.logging import get_logger
from app.common.request_context import current_request_id, job_context, new_id

#: 작업 함수. 장치가 연 세션을 받는다 — 요청 세션이 흘러들어올 자리가 없다.
JobFn = Callable[[Session], None]
#: 실패 기록 함수. 되돌린 뒤 **새로 연** 세션을 받는다.
FailureFn = Callable[[Session], None]


@dataclass(frozen=True)
class JobOutcome:
    """작업 한 번의 결과."""

    job_id: str
    succeeded: bool
    failure_recorded: bool
    duration_ms: int
    error_type: str | None = None


def run_unit_of_work(
    *,
    component: str,
    job_name: str,
    work: JobFn,
    record_failure: FailureFn | None = None,
    request_id: str | None = None,
    session_factory: Callable[[], Session] | None = None,
) -> JobOutcome:
    """작업 하나를 돌린다. 연결의 열기·확정·되돌리기·닫기를 이 장치가 전부 맡는다."""
    if session_factory is None:
        from app.db import new_session

        session_factory = new_session

    log = get_logger(component=component)
    job_id = new_id()
    origin_request_id = request_id if request_id is not None else current_request_id()

    with job_context(job_id, origin_request_id):
        started = time.monotonic()
        log.info("작업을 시작한다", job_name=job_name)

        error_type: str | None = None
        session = session_factory()
        try:
            work(session)
            session.commit()
        except Exception as exc:
            session.rollback()
            error_type = type(exc).__name__
            error_message = str(exc)
        finally:
            session.close()

        duration_ms = int((time.monotonic() - started) * 1000)

        if error_type is None:
            log.info("작업이 끝났다", job_name=job_name, duration_ms=duration_ms)
            return JobOutcome(
                job_id=job_id,
                succeeded=True,
                failure_recorded=False,
                duration_ms=duration_ms,
            )

        log.error(
            "작업이 실패했다",
            job_name=job_name,
            duration_ms=duration_ms,
            error_type=error_type,
            error_message=error_message,
        )

        failure_recorded = False
        if record_failure is not None:
            # 되돌린 연결로는 실패 기록도 함께 사라진다. 그래서 **새 연결**을 연다.
            failure_session = session_factory()
            try:
                record_failure(failure_session)
                failure_session.commit()
                failure_recorded = True
            except Exception as exc:
                log.error(
                    "실패 상태를 적는 것마저 실패했다 — 로그만 남기고 넘어간다",
                    job_name=job_name,
                    error_type=type(exc).__name__,
                    error_message=str(exc),
                )
            finally:
                failure_session.close()

        return JobOutcome(
            job_id=job_id,
            succeeded=False,
            failure_recorded=failure_recorded,
            duration_ms=duration_ms,
            error_type=error_type,
        )


def schedule_unit_of_work(background_tasks: Any, **kwargs: Any) -> None:
    """요청 경로가 작업을 예약한다. **식별자만** 넘기고 열린 연결을 넘기지 않는다
    (BR5.1).

    `background_tasks` 는 웹 프레임워크가 주는 배경 작업 모음이다. 지금 문맥의 요청
    식별자를
    여기서 붙잡아 작업으로 넘긴다 — 작업이 도는 시점에는 요청 문맥이 이미 끝나 있다.
    """
    kwargs.setdefault("request_id", current_request_id())
    background_tasks.add_task(run_unit_of_work, **kwargs)
