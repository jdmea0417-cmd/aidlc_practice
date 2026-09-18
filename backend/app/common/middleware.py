"""요청마다 식별자를 발급하고 수신·완료를 남긴다 (BR6.1, observability-design.md §3).

헬스체크는 주기적으로 불리므로 접근 로그를 남기지 않는다 — 매번 남기면 로그가 그것으로
덮인다. 헬스체크 자신은 실패할 때만 로그를 남긴다 (observability-design.md §4).
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.common.logging import get_logger
from app.common.request_context import new_id, request_context

#: 접근 로그를 남기지 않는 경로
QUIET_PATHS: frozenset[str] = frozenset({"/api/v1/health"})

_log = get_logger(component="common")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """요청 식별자를 발급해 문맥에 넣고, 같은 값을 응답 머리에도 싣는다."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = new_id()
        quiet = request.url.path in QUIET_PATHS

        with request_context(request_id):
            if not quiet:
                _log.info("요청을 받았다", method=request.method, path=request.url.path)
            started = time.monotonic()
            response = await call_next(request)
            if not quiet:
                _log.info(
                    "요청을 처리했다",
                    method=request.method,
                    path=request.url.path,
                    status_code=response.status_code,
                    duration_ms=int((time.monotonic() - started) * 1000),
                )
            response.headers["X-Request-ID"] = request_id
            return response
