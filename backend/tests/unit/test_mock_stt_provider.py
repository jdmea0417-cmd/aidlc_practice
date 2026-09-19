"""Mock 전사 — 시연이 매번 같은 결과로 재현된다 (BR4.1, BR4.2, BR4.3).

대화 선택 규칙 자체를 검증하므로 시험 이름은 한국어다.
기대값은 픽스처에서 읽는다 — 시험 코드에 전사를 옮겨 적지 않는다.
"""

from __future__ import annotations

import pytest

from app.fixtures.loader import FIXTURE_FILES, load_fixture
from app.providers.stt_mock import MockSttProvider


@pytest.fixture()
def provider() -> MockSttProvider:
    return MockSttProvider()


@pytest.mark.ac("AC9.2.2")
def test_알려진_대화_키로_그_대화를_고른다(provider: MockSttProvider) -> None:
    for key in FIXTURE_FILES:
        result = provider.transcribe("/data/audio/x.webm", file_name=f"{key}.webm")
        assert result.conversation_key == key


@pytest.mark.ac("AC9.2.3")
def test_대화_키가_없으면_S1_으로_처리한다(provider: MockSttProvider) -> None:
    result = provider.transcribe("/data/audio/x.webm", file_name="어제대화.webm")
    assert result.conversation_key == "conv_repair_01"


@pytest.mark.ac("AC9.2.3")
def test_모르는_키이면_S1_으로_처리한다(provider: MockSttProvider) -> None:
    result = provider.transcribe("/data/audio/x.webm", file_name="conv_unknown_99.webm")
    assert result.conversation_key == "conv_repair_01"


@pytest.mark.ac("AC9.2.3")
def test_브라우저_녹음이면_S1_으로_처리한다(provider: MockSttProvider) -> None:
    """녹음에는 파일 이름이 없다 — 실패로 만들지 않는다."""
    result = provider.transcribe("/data/audio/rec.webm", file_name="")
    assert result.conversation_key == "conv_repair_01"


def test_전사_내용이_픽스처와_정확히_같다(provider: MockSttProvider) -> None:
    result = provider.transcribe("/data/audio/x.webm", file_name="conv_unclear_03.webm")

    assert result.utterances == load_fixture("conv_unclear_03").transcript(1)
    assert result.model_name == MockSttProvider.model_name
