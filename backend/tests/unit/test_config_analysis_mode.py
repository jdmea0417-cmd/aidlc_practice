"""분석 모드 해석 — 안전한 쪽으로만 닫힌다 (BR1.1, BR1.2, SC-04).

판정 규칙 자체를 검증하므로 시험 이름은 한국어다 (unit-test-instructions §7).
"""

from __future__ import annotations

import pytest

from app.common.exceptions import StartupAbort
from app.config import Settings, resolve_analysis_mode


def _settings(**overrides: object) -> Settings:
    """환경변수·`.env` 에 기대지 않고 값을 직접 준다."""
    base: dict[str, object] = {
        "analysis_mode": "mock",
        "stt_api_key": None,
        "llm_api_key": None,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


@pytest.mark.ac("AC9.1.2")
def test_미설정이면_mock_으로_뜬다() -> None:
    assert (
        resolve_analysis_mode(
            _settings(analysis_mode=Settings.model_fields["analysis_mode"].default)
        )
        == "mock"
    )


@pytest.mark.ac("AC9.1.2")
def test_빈_값이면_mock_으로_뜬다() -> None:
    assert resolve_analysis_mode(_settings(analysis_mode="   ")) == "mock"


@pytest.mark.ac("AC9.1.2")
def test_모르는_값이면_mock_으로_뜨고_그_사실이_로그에_남는다(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level("WARNING"):
        assert resolve_analysis_mode(_settings(analysis_mode="banana")) == "mock"

    assert any(
        "banana" in record.getMessage() for record in caplog.records
    ), "모르는 값이었다는 사실이 로그에 남지 않았다"


def test_mock_이면_mock_이다() -> None:
    assert resolve_analysis_mode(_settings(analysis_mode="mock")) == "mock"


def test_live_이고_키가_있으면_live_다() -> None:
    settings = _settings(analysis_mode="live", stt_api_key="키1", llm_api_key="키2")
    assert resolve_analysis_mode(settings) == "live"


@pytest.mark.ac("AC9.1.3")
def test_live_인데_키가_없으면_기동을_거부한다() -> None:
    with pytest.raises(StartupAbort) as raised:
        resolve_analysis_mode(_settings(analysis_mode="live", llm_api_key="키2"))

    assert "STT_API_KEY" in str(raised.value), "어떤 키가 없는지 알려 주지 않는다"
