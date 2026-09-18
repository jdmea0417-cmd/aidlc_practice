"""오류 봉투 하나로 고정한다 (계약 공통 규칙, security-design.md §4.1).

    {"error": {"code": "<영어 고정 토큰>", "message": "<한국어>", "details": [...],
    "request_id":
    "..."}}

- `code` 는 프론트가 분기하는 기계용 값이라 영어로 안정적이어야 한다.
- `message` 는 사람이 읽는 값이라 한국어다 (OC-06).
- `details` 는 **입력 검증 실패에만** 쓴다. 그 밖에는 빈 배열이다 — 내부 정보가 새어
나갈
  통로를 좁히는 것이 이 선택의 목적이다.
- `request_id` 는 미들웨어가 발급한 값을 같은 문맥에서 읽으므로, 사용자가 본 값과 로그의
  값이 어긋날 수 없다.
- 처리되지 않은 예외는 500 + 같은 봉투로 나가되 **내부 메시지를 노출하지 않고** 스택은
  로그에만 남긴다.
"""

from __future__ import annotations

import traceback
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.exceptions import AppError
from app.common.logging import get_logger
from app.common.request_context import current_request_id

_log = get_logger(component="common")

#: 검증 실패 사유를 한국어로 옮긴다. 모르는 종류는 일반 문구로 답한다.
VALIDATION_REASONS: dict[str, str] = {
    "missing": "필수 항목입니다.",
    "literal_error": "허용되지 않는 값입니다.",
    "bool_parsing": "참/거짓 값이어야 합니다.",
    "int_parsing": "정수여야 합니다.",
    "string_type": "문자열이어야 합니다.",
    "uuid_parsing": "식별자 모양이 올바르지 않습니다.",
    "json_invalid": "본문이 올바른 JSON 이 아닙니다.",
    "value_error": "값이 올바르지 않습니다.",
}

INTERNAL_ERROR_MESSAGE = "요청을 처리하지 못했습니다. 잠시 후 다시 시도해 주세요."


def build_error_envelope(
    code: str, message: str, details: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """오류 응답의 유일한 모양."""
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
            "request_id": current_request_id(),
        }
    }


def _field_name(location: tuple[Any, ...]) -> str:
    parts = [str(part) for part in location if part not in ("body", "query", "path")]
    return ".".join(parts) if parts else "body"


def register_error_handlers(app: FastAPI) -> None:
    """예외를 HTTP 로 번역하는 자리 — 코드 전체에서 여기 한 곳이다."""

    @app.exception_handler(AppError)
    def _handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        _log.warning(
            "요청이 오류로 끝났다",
            path=request.url.path,
            error_code=exc.code,
            status_code=exc.http_status,
        )
        return JSONResponse(
            status_code=exc.http_status,
            content=build_error_envelope(exc.code, exc.message),
        )

    @app.exception_handler(RequestValidationError)
    def _handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = [
            {
                "field": _field_name(error.get("loc", ())),
                "reason": VALIDATION_REASONS.get(
                    str(error.get("type", "")), "값이 올바르지 않습니다."
                ),
            }
            for error in exc.errors()
        ]
        _log.warning(
            "입력 검증에 실패했다",
            path=request.url.path,
            error_code="VALIDATION_ERROR",
            invalid_field_count=len(details),
        )
        return JSONResponse(
            status_code=422,
            content=build_error_envelope(
                "VALIDATION_ERROR", "입력값을 확인해 주세요.", details
            ),
        )

    @app.exception_handler(Exception)
    def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        # 스택은 로그에만 남긴다. 예외 객체를 통째로 로거에 넘기지 않는다.
        _log.error(
            "처리되지 않은 예외가 났다",
            path=request.url.path,
            error_type=type(exc).__name__,
            error_message=str(exc),
            stack="".join(
                traceback.format_exception(type(exc), exc, exc.__traceback__)
            ),
        )
        return JSONResponse(
            status_code=500,
            content=build_error_envelope("INTERNAL_ERROR", INTERNAL_ERROR_MESSAGE),
        )
