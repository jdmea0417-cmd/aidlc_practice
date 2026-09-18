"""제공자 호출 감싸기 (security-design.md §2, NFR13.3~13.5).

외부로 나가지 않는다 — 호출 대상만 가짜로 두고 타임아웃·4xx·성공을 흉내 낸다.
기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import json

import httpx
import pytest

from app.common.exceptions import ProviderError, ProviderTimeoutError
from app.common.provider_call import call_provider, get_http_client, reset_http_client
from app.config import Settings


@pytest.fixture()
def http_client() -> httpx.Client:
    return httpx.Client()


def test_client_carries_connect_and_read_timeouts_from_settings() -> None:
    reset_http_client()
    try:
        client = get_http_client()
        settings = Settings()
        assert client.timeout.connect == settings.provider_connect_timeout_seconds
        assert client.timeout.read == settings.provider_read_timeout_seconds
        assert client.timeout.connect != client.timeout.read, "연결과 읽기를 따로 둔다"
    finally:
        reset_http_client()


def test_timeout_is_retried_once_then_becomes_a_timeout_error(
    http_client: httpx.Client,
) -> None:
    attempts: list[int] = []

    def _call(client: httpx.Client) -> None:
        attempts.append(1)
        raise httpx.ReadTimeout("응답이 없다")

    with pytest.raises(ProviderTimeoutError):
        call_provider(
            _call,
            operation="llm.assess",
            model_name="테스트모델",
            client=http_client,
            retry_count=1,
        )

    assert len(attempts) == 2, "타임아웃에 정확히 한 번 다시 시도해야 한다"


def test_connection_failure_is_retried_once(http_client: httpx.Client) -> None:
    attempts: list[int] = []

    def _call(client: httpx.Client) -> str:
        attempts.append(1)
        if len(attempts) == 1:
            raise httpx.ConnectError("연결할 수 없다")
        return "두 번째에 성공"

    result = call_provider(
        _call,
        operation="stt.transcribe",
        model_name="테스트모델",
        client=http_client,
        retry_count=1,
    )

    assert result == "두 번째에 성공"
    assert len(attempts) == 2


def test_4xx_is_not_retried(http_client: httpx.Client) -> None:
    """우리가 보낸 요청의 문제다 — 다시 보내도 같은 답이 온다."""
    attempts: list[int] = []

    def _call(client: httpx.Client) -> None:
        attempts.append(1)
        request = httpx.Request("POST", "https://provider.invalid/v1")
        raise httpx.HTTPStatusError(
            "잘못된 요청",
            request=request,
            response=httpx.Response(400, request=request),
        )

    with pytest.raises(ProviderError):
        call_provider(
            _call,
            operation="llm.assess",
            model_name="테스트모델",
            client=http_client,
            retry_count=1,
        )

    assert len(attempts) == 1


def test_provider_exceptions_do_not_cross_the_boundary(
    http_client: httpx.Client,
) -> None:
    """어댑터 경계에서 앱 오류로 바뀐다 — 위쪽 코드가 제공자를 모르게 된다 (TC-06)."""

    def _call(client: httpx.Client) -> None:
        raise ValueError("제공자 SDK 안에서 난 오류")

    with pytest.raises(ProviderError) as raised:
        call_provider(
            _call,
            operation="llm.assess",
            model_name="테스트모델",
            client=http_client,
            retry_count=0,
        )

    assert not isinstance(raised.value, ValueError)
    assert isinstance(raised.value.__cause__, ValueError)


def test_log_carries_model_prompt_version_and_duration(
    http_client: httpx.Client, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level("INFO"):
        call_provider(
            lambda client: "판정",
            operation="llm.assess",
            model_name="테스트모델",
            prompt_version="v1",
            client=http_client,
            retry_count=0,
        )

    line = json.loads(caplog.records[-1].getMessage())
    assert line["model_name"] == "테스트모델"
    assert line["prompt_version"] == "v1"
    assert isinstance(line["duration_ms"], int)
    assert line["component"] == "providers"


def test_wrapper_never_receives_the_request_body() -> None:
    """전사가 로그 함수에 도달할 경로가 없다 (BR6.3, NFR12.1)."""
    import inspect

    parameters = set(inspect.signature(call_provider).parameters)
    assert parameters == {
        "call",
        "operation",
        "model_name",
        "prompt_version",
        "client",
        "retry_count",
    }, f"감싸기 장치가 받는 것이 메타데이터 말고 더 있다: {parameters}"
