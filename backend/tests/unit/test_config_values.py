"""설정값이 코드가 아니라 설정에 있다 (NFR4, tech-stack-decisions.md §3).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

from app.config import Settings


def test_provider_timeouts_default_to_five_and_sixty_seconds() -> None:
    settings = Settings()
    assert settings.provider_connect_timeout_seconds == 5.0
    assert settings.provider_read_timeout_seconds == 60.0


def test_provider_retry_count_defaults_to_one() -> None:
    assert Settings().provider_retry_count == 1


def test_upload_max_bytes_is_configurable_not_hardcoded() -> None:
    """코드에 숫자를 박지 않는다 — 값을 주면 그 값이 쓰인다."""
    assert Settings().upload_max_bytes > 0
    assert Settings(upload_max_bytes=1234).upload_max_bytes == 1234


def test_audio_retention_defaults_to_thirty_days() -> None:
    """PM-04 — 설정값이 노출되고 기본값이 30일이다."""
    assert Settings().audio_retention_days == 30


def test_operational_defaults_match_the_decided_values() -> None:
    """PM-01·PM-02·PM-03 과 로그 기본 수준."""
    settings = Settings()
    assert settings.recording_max_seconds == 300
    assert settings.mock_analysis_target_seconds == 3.0
    assert settings.min_opportunities == 3
    assert settings.log_level == "INFO"
