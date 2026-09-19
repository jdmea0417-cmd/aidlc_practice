"""앱 조립 — 기동 흐름 W1.

    1. 설정을 한 번 읽는다 (BR1.3)
    2. 분석 모드를 정한다 (BR1.1)
    3. live 면 키를 확인한다. 없으면 기동 중단 (BR1.2)
    4. 결정된 모드의 제공자만 만든다 (NFR5.3)
    5. 저장소 연결을 준비한다
    6. 요청 식별자·오류 봉투·경로를 조립한다 (BR6.1)
    7. 기동 완료 — 이 시점부터 헬스체크가 응답한다

**스키마 적용을 기동 흐름에 넣지 않는다.** 마이그레이션은 `scripts/migrate.sh` 가 도는
별도
단계다 — 기동마다 적용하면 컨테이너가 동시에 뜰 때 경쟁이 생긴다 (functional-spec.md
W1).
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.account.routes import router as account_router
from app.api.common.health import router as health_router
from app.common.error_handlers import register_error_handlers
from app.common.logging import configure_logging, get_logger
from app.common.middleware import RequestContextMiddleware
from app.config import get_settings, resolve_analysis_mode
from app.db import get_engine
from app.providers.factory import build_providers


def create_app() -> FastAPI:
    """앱을 만든다. 설정이 어긋나면 여기서 기동이 멈춘다."""
    settings = get_settings()
    configure_logging(settings.log_level)
    log = get_logger(component="common")

    analysis_mode = resolve_analysis_mode(settings)
    providers = build_providers(analysis_mode, settings)

    app = FastAPI(title="SCD 코칭 MVP 백엔드", version="1")
    app.state.settings = settings
    app.state.analysis_mode = analysis_mode
    app.state.providers = providers
    app.state.engine = get_engine()

    app.add_middleware(RequestContextMiddleware)
    register_error_handlers(app)
    app.include_router(health_router)
    app.include_router(account_router)

    log.info("기동이 끝났다", analysis_mode=analysis_mode)
    return app


app = create_app()
