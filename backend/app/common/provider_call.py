"""제공자 호출을 한 자리로 모은다 (security-design.md §2).

모든 STT·LLM 호출은 이 장치 하나를 지난다. 네 가지(타임아웃·재시도·시간 측정·로그)를 한
곳에
모은 이유는, 같은 규칙을 네 어댑터에 흩어 쓰면 한 곳이 빠뜨려도 드러나지 않기 때문이다.

    1. 소요 시간 재기 시작
    2. 연결 타임아웃 5초 / 읽기 타임아웃 60초 (설정값)
    3. 실제 호출
    4. 타임아웃·연결 실패면 1회만 재시도
    5. 4xx 는 재시도하지 않음
    6. 제공자 예외 -> 앱 오류로 변환 (ProviderError / ProviderTimeoutError)
    7. 로그: 모델명·프롬프트 버전·소요 시간·식별자

**이 장치는 요청 본문을 받지 않는다.** 메타데이터만 로그에 넘기므로 전사가 로그 함수에
도달할
경로가 없다 (BR6.3, NFR12.1).

어댑터는 HTTP 도구를 직접 import 하지 않는다 — 이 장치가 만든 클라이언트를 인자로
받는다.
그래서 "반드시 이 장치를 거친다"가 사람의 주의력이 아니라 검사가 된다
(`tests/unit/test_layer_boundaries.py`). 클라이언트는 재사용한다 — 호출마다 새로 만들면
연결
수립 비용이 반복된다 (performance-design.md §3).
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

import httpx

from app.common.exceptions import ProviderError, ProviderTimeoutError
from app.common.logging import get_logger

T = TypeVar("T")

_log = get_logger(component="providers")
_client: httpx.Client | None = None


def get_http_client() -> httpx.Client:
    """설정된 타임아웃을 단 클라이언트 하나를 재사용한다."""
    global _client
    if _client is None:
        from app.config import get_settings

        settings = get_settings()
        _client = httpx.Client(
            timeout=httpx.Timeout(
                connect=settings.provider_connect_timeout_seconds,
                read=settings.provider_read_timeout_seconds,
                write=settings.provider_read_timeout_seconds,
                pool=settings.provider_connect_timeout_seconds,
            )
        )
    return _client


def reset_http_client() -> None:
    """클라이언트를 버린다. 설정을 바꿔 다시 만들어야 하는 시험에서만 쓴다."""
    global _client
    if _client is not None:
        _client.close()
    _client = None


def call_provider(
    call: Callable[[httpx.Client], T],
    *,
    operation: str,
    model_name: str,
    prompt_version: str | None = None,
    client: httpx.Client | None = None,
    retry_count: int | None = None,
) -> T:
    """제공자를 한 번 부른다. 실패는 전부 앱 오류로 바뀌어 나간다."""
    if retry_count is None:
        from app.config import get_settings

        retry_count = get_settings().provider_retry_count

    http_client = client if client is not None else get_http_client()
    attempts = retry_count + 1
    started = time.monotonic()

    for attempt in range(1, attempts + 1):
        try:
            result = call(http_client)
        except httpx.TimeoutException as exc:
            if attempt < attempts:
                _log.warning(
                    "제공자 호출이 시간을 넘겨 다시 한 번 시도한다",
                    operation=operation,
                    model_name=model_name,
                    prompt_version=prompt_version,
                    attempt=attempt,
                    error_type=type(exc).__name__,
                )
                continue
            duration_ms = int((time.monotonic() - started) * 1000)
            _log.error(
                "제공자 호출이 시간을 넘겼다",
                operation=operation,
                model_name=model_name,
                prompt_version=prompt_version,
                duration_ms=duration_ms,
                error_type=type(exc).__name__,
            )
            raise ProviderTimeoutError("제공자 응답이 제한 시간을 넘겼습니다.") from exc
        except httpx.HTTPStatusError as exc:
            # 4xx 는 우리가 보낸 요청의 문제다. 다시 보내도 같은 답이 온다.
            duration_ms = int((time.monotonic() - started) * 1000)
            _log.error(
                "제공자가 요청을 거부했다",
                operation=operation,
                model_name=model_name,
                prompt_version=prompt_version,
                duration_ms=duration_ms,
                status_code=exc.response.status_code,
                error_type=type(exc).__name__,
            )
            raise ProviderError("제공자가 요청을 처리하지 못했습니다.") from exc
        except httpx.TransportError as exc:
            if attempt < attempts:
                _log.warning(
                    "제공자에 연결하지 못해 다시 한 번 시도한다",
                    operation=operation,
                    model_name=model_name,
                    prompt_version=prompt_version,
                    attempt=attempt,
                    error_type=type(exc).__name__,
                )
                continue
            duration_ms = int((time.monotonic() - started) * 1000)
            _log.error(
                "제공자에 연결하지 못했다",
                operation=operation,
                model_name=model_name,
                prompt_version=prompt_version,
                duration_ms=duration_ms,
                error_type=type(exc).__name__,
            )
            raise ProviderError("제공자에 연결하지 못했습니다.") from exc
        except Exception as exc:
            duration_ms = int((time.monotonic() - started) * 1000)
            _log.error(
                "제공자 호출이 실패했다",
                operation=operation,
                model_name=model_name,
                prompt_version=prompt_version,
                duration_ms=duration_ms,
                error_type=type(exc).__name__,
            )
            raise ProviderError("제공자 호출이 실패했습니다.") from exc
        else:
            duration_ms = int((time.monotonic() - started) * 1000)
            _log.info(
                "제공자 호출이 끝났다",
                operation=operation,
                model_name=model_name,
                prompt_version=prompt_version,
                duration_ms=duration_ms,
                attempt=attempt,
            )
            return result

    raise AssertionError(
        "도달할 수 없다 — 위 반복문이 반드시 값을 돌려주거나 예외를 던진다"
    )
