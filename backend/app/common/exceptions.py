"""앱 오류 — HTTP 로의 번역은 `common/` 의 예외 처리기 한 곳이 담당한다.

`service` 는 이 예외들만 던진다. `HTTPException` 을 던지지 않는다 (TC-14).
`code` 는 프론트가 분기하는 기계용 값이라 **영어 고정 토큰**이고, `message` 는 사람이
읽는
값이라 **한국어**다 (계약 공통 규칙).
"""

from __future__ import annotations


class AppError(Exception):
    """모든 앱 오류의 기반."""

    code: str = "INTERNAL_ERROR"
    http_status: int = 500

    def __init__(
        self, message: str, *, code: str | None = None, http_status: int | None = None
    ) -> None:
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        if http_status is not None:
            self.http_status = http_status


class NotFoundError(AppError):
    code = "NOT_FOUND"
    http_status = 404


class PermissionDeniedError(AppError):
    code = "PERMISSION_DENIED"
    http_status = 403


class ValidationError(AppError):
    code = "VALIDATION_ERROR"
    http_status = 422


class ConflictError(AppError):
    code = "CONFLICT"
    http_status = 409


class ProviderError(AppError):
    code = "PROVIDER_ERROR"
    http_status = 502


class ProviderTimeoutError(ProviderError):
    code = "PROVIDER_TIMEOUT"
    http_status = 504


class StartupAbort(Exception):
    """기동을 중단시키는 설정 오류 (BR1.2).

    앱 오류가 아니다 — HTTP 로 번역되지 않는다. 프로세스가 뜨지 않아야 사람이 바로
    알아챈다.
    """
