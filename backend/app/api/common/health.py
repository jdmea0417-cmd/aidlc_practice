"""헬스체크 — `GET /api/v1/health` (계약 C1, AC9.1.1, AC9.3.4).

응답에 현재 분석 모드를 함께 싣는다. 시연 리허설이 그 값이 `mock` 임을 **단언**할 수
있어야
하기 때문이다 — 눈으로 확인하는 것에 기대면 시연 당일에는 확인하지 않게 된다 (BR3.2).

분석 모드는 기동 시 정해진 값을 그대로 읽는다. 여기서 다시 판별하지 않는다 (BR1.3).
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.common.error_handlers import build_error_envelope
from app.service import health as health_service

router = APIRouter(prefix="/api/v1", tags=["common"])


class HealthResponse(BaseModel):
    """계약 C1 의 헬스체크 응답."""

    status: Literal["ok"]
    analysisMode: Literal["mock", "live"]


@router.get(
    "/health",
    response_model=HealthResponse,
    responses={503: {"description": "저장소가 응답하지 않는다"}},
)
def get_health(request: Request) -> HealthResponse | JSONResponse:
    """저장소까지 확인한 뒤에만 정상이라고 답한다."""
    settings = request.app.state.settings
    healthy = health_service.check_storage(
        request.app.state.engine,
        timeout_seconds=settings.health_check_query_timeout_seconds,
    )

    if not healthy:
        # 컨테이너 준비 확인이 이 결과를 그대로 쓴다 — 정상이 아니면 2xx 로 답하지
        # 않는다.
        return JSONResponse(
            status_code=503,
            content=build_error_envelope(
                "STORAGE_UNAVAILABLE", "저장소에 연결하지 못했습니다."
            ),
        )

    return HealthResponse(status="ok", analysisMode=request.app.state.analysis_mode)
