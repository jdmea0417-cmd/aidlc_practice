"""요청 식별자·작업 식별자 문맥 (BR6.1, BR6.2).

식별자를 **문맥에 넣고 로그가 자동으로 읽는다.** 로그 호출마다 넘기게 하면 빠뜨리는
자리가
생기고, 빠뜨려도 드러나지 않는다 (observability-design.md §1.2).

두 식별자를 나눈 이유: 작업 한 번이 한 묶음이 되면서도 원래 요청으로 거슬러 갈 수 있다.
요청 경로의 로그에서 작업 식별자는 비어 있고, 작업 경로의 로그에는 둘 다 담긴다.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

_request_id: ContextVar[str] = ContextVar("request_id", default="")
_job_id: ContextVar[str] = ContextVar("job_id", default="")


def new_id() -> str:
    """식별자를 하나 발급한다."""
    return str(uuid.uuid4())


def current_request_id() -> str:
    """지금 문맥의 요청 식별자. 문맥 밖에서는 빈 값이다."""
    return _request_id.get()


def current_job_id() -> str:
    """지금 문맥의 작업 식별자. 요청 경로에서는 빈 값이다."""
    return _job_id.get()


@contextmanager
def request_context(request_id: str) -> Iterator[str]:
    """요청 하나의 문맥. 미들웨어가 요청마다 연다."""
    token = _request_id.set(request_id)
    try:
        yield request_id
    finally:
        _request_id.reset(token)


@contextmanager
def job_context(job_id: str, request_id: str) -> Iterator[str]:
    """응답 이후 작업 하나의 문맥.

    요청 문맥은 이미 끝나 있어 읽을 수 없으므로, 작업은 원래 요청의 식별자를 **인자로
    받아**
    자기 문맥에 담는다 (BR6.2).
    """
    request_token = _request_id.set(request_id)
    job_token = _job_id.set(job_id)
    try:
        yield job_id
    finally:
        _job_id.reset(job_token)
        _request_id.reset(request_token)
