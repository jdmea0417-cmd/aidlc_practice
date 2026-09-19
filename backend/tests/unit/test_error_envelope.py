"""오류 봉투 (계약 공통 규칙, security-design.md §4.1).

저장소를 만지지 않는다 — 오류를 내는 작은 앱을 세워 봉투의 모양만 본다.
기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import json
import re

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.common.error_handlers import register_error_handlers
from app.common.exceptions import (
    AppError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
    ProviderError,
    ProviderTimeoutError,
    ValidationError,
)
from app.common.middleware import RequestContextMiddleware


class Body(BaseModel):
    count: int


@pytest.fixture()
def client() -> TestClient:
    app = FastAPI()
    app.add_middleware(RequestContextMiddleware)
    register_error_handlers(app)

    @app.get("/boom/{code}")
    def _boom(code: str) -> None:
        raise {
            "not-found": NotFoundError("대화를 찾을 수 없습니다."),
            "denied": PermissionDeniedError("권한이 없습니다."),
            "invalid": ValidationError("값이 올바르지 않습니다."),
            "conflict": ConflictError("이미 처리 중입니다."),
            "provider": ProviderError("제공자 호출이 실패했습니다."),
            "timeout": ProviderTimeoutError("제공자 응답이 늦습니다."),
        }[code]

    @app.get("/unexpected")
    def _unexpected() -> None:
        raise RuntimeError("내부 사정이 담긴 메시지 — 밖으로 나가면 안 된다")

    @app.post("/echo")
    def _echo(body: Body) -> dict:
        return {"count": body.count}

    return TestClient(app, raise_server_exceptions=False)


def test_envelope_has_exactly_four_fields(client: TestClient) -> None:
    payload = client.get("/boom/not-found").json()

    assert set(payload) == {"error"}
    assert set(payload["error"]) == {"code", "message", "details", "request_id"}


def test_code_is_an_english_token_and_message_is_korean(client: TestClient) -> None:
    error = client.get("/boom/not-found").json()["error"]

    assert error["code"] == "NOT_FOUND"
    assert re.fullmatch(r"[A-Z_]+", error["code"])
    assert re.search(r"[가-힣]", error["message"]), "message 가 한국어가 아니다"


def test_details_are_only_used_for_input_validation(client: TestClient) -> None:
    response = client.post("/echo", json={"count": "숫자가 아니다"})
    error = response.json()["error"]

    assert response.status_code == 422
    assert error["code"] == "VALIDATION_ERROR"
    assert error["details"], "검증 실패인데 details 가 비어 있다"
    assert set(error["details"][0]) == {"field", "reason"}
    assert error["details"][0]["field"] == "count"
    assert re.search(r"[가-힣]", error["details"][0]["reason"])


def test_every_other_error_has_empty_details(client: TestClient) -> None:
    for path in ("/boom/denied", "/boom/conflict", "/boom/provider", "/unexpected"):
        assert client.get(path).json()["error"]["details"] == [], path


def test_internal_error_does_not_leak_the_internal_message(client: TestClient) -> None:
    response = client.get("/unexpected")
    error = response.json()["error"]

    assert response.status_code == 500
    assert error["code"] == "INTERNAL_ERROR"
    assert "내부 사정이 담긴 메시지" not in json.dumps(error, ensure_ascii=False)


def test_request_id_matches_the_value_in_the_log(
    client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level("WARNING"):
        response = client.get("/boom/not-found")

    request_id = response.json()["error"]["request_id"]
    assert request_id
    assert response.headers["X-Request-ID"] == request_id
    logged = [json.loads(record.getMessage()) for record in caplog.records]
    assert any(
        line["request_id"] == request_id for line in logged
    ), "사용자가 본 값과 로그의 값이 어긋난다"


def test_each_exception_maps_to_its_status_code(client: TestClient) -> None:
    expected = {
        "not-found": (404, "NOT_FOUND"),
        "denied": (403, "PERMISSION_DENIED"),
        "invalid": (422, "VALIDATION_ERROR"),
        "conflict": (409, "CONFLICT"),
        "provider": (502, "PROVIDER_ERROR"),
        "timeout": (504, "PROVIDER_TIMEOUT"),
    }
    for path, (status, code) in expected.items():
        response = client.get(f"/boom/{path}")
        assert (response.status_code, response.json()["error"]["code"]) == (
            status,
            code,
        )

    assert AppError("무언가").http_status == 500
