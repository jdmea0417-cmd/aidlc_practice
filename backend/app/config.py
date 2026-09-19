"""설정 — 기동 시 **한 번** 파싱한다 (BR1.3).

코드 곳곳에서 환경변수를 다시 읽지 않는다. 설정 객체 하나를 주입한다.
값은 전부 `tech-stack-decisions.md` §3 이 정한 것이며, 코드에 숫자를 박지 않는다 (NFR4).

분석 모드 결정은 이 모듈 한 곳에서만 일어난다 (security-design.md §1.1):

    값 없음 / 빈 값 / 모르는 값 -> mock  (그 사실을 로그에 남긴다)          BR1.1
    "mock"                     -> mock
    "live" + 키 있음           -> live
    "live" + 키 없음           -> 기동 중단 (어떤 키가 없는지 로그)         BR1.2
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.exceptions import StartupAbort
from app.common.logging import get_logger

AnalysisMode = Literal["mock", "live"]

#: 아는 분석 모드 값. 이 밖의 값은 전부 mock 으로 닫힌다 (BR1.1).
KNOWN_ANALYSIS_MODES: tuple[str, ...] = ("mock", "live")

_log = get_logger(component="common")


class Settings(BaseSettings):
    """평면 구조 + 접두사 규칙. 이름이 곧 환경변수 이름이다."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    # --- 분석 모드와 제공자 키 (SC-04) ---
    #: 원본 값이다. 해석된 값은 `resolve_analysis_mode()` 가 돌려준다.
    analysis_mode: str = "mock"
    stt_api_key: str | None = None
    llm_api_key: str | None = None

    # --- 저장소 ---
    database_url: str = (
        "postgresql+psycopg://scd:scd_local_dev@localhost:5432/scd_coach"
    )
    #: 연결 풀 크기 5 (infrastructure-specification.md §2.1)
    db_pool_size: int = 5

    # --- 제공자 호출 (tech-stack-decisions.md §3) ---
    provider_connect_timeout_seconds: float = 5.0
    provider_read_timeout_seconds: float = 60.0
    #: 타임아웃·연결 실패에만 1회. 4xx 는 재시도하지 않는다 (NFR13.4).
    provider_retry_count: int = 1

    # --- 업로드 ---
    #: 5분짜리 webm/opus 녹음에 여유를 둔 기본값. 코드에 박지 않고 여기서만 정한다.
    upload_max_bytes: int = 26_214_400
    upload_storage_path: str = "storage/audio"

    # --- 운영 파라미터 (PM-01~PM-04) ---
    recording_max_seconds: int = 300
    mock_analysis_target_seconds: float = 3.0
    min_opportunities: int = 3
    audio_retention_days: int = 30

    # --- 로그와 헬스체크 ---
    log_level: str = "INFO"
    #: 헬스체크 확인 질의의 시간 제한 (NFR10.15)
    health_check_query_timeout_seconds: float = 1.0


def resolve_analysis_mode(settings: Settings) -> AnalysisMode:
    """security-design.md §1.1 의 흐름 그대로. 절대 조용히 live 로 흘러가지 않는다."""
    raw = (settings.analysis_mode or "").strip().lower()

    if raw not in KNOWN_ANALYSIS_MODES:
        _log.warning(
            "분석 모드 설정을 알 수 없어 mock 으로 동작한다",
            configured_value=raw,
            resolved_mode="mock",
        )
        return "mock"

    if raw == "mock":
        _log.info("분석 모드를 결정했다", resolved_mode="mock")
        return "mock"

    missing = [
        name
        for name, value in (
            ("STT_API_KEY", settings.stt_api_key),
            ("LLM_API_KEY", settings.llm_api_key),
        )
        if not (value or "").strip()
    ]
    if missing:
        _log.error(
            "분석 모드가 live 인데 제공자 키가 없어 기동을 거부한다",
            missing_keys=",".join(missing),
        )
        raise StartupAbort(
            f"ANALYSIS_MODE=live 인데 다음 키가 없다: {', '.join(missing)}. "
            "조용히 mock 으로 되돌아가지 않는다 (BR1.2)"
        )

    _log.info("분석 모드를 결정했다", resolved_mode="live")
    return "live"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """기동 시 한 번 만들어 재사용하는 설정 객체 (BR1.3)."""
    return Settings()


def reset_settings() -> None:
    """설정 캐시를 버린다. 환경변수를 바꿔 다시 읽어야 하는 시험에서만 쓴다."""
    get_settings.cache_clear()
