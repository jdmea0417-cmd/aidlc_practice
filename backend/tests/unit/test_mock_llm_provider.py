"""Mock 판정 — 기대 판정이 픽스처와 정확히 일치한다 (BR4.1~BR4.3, NFR14.1).

이 대조가 없으면 픽스처가 기대 판정표에서 한 칸 어긋났을 때 시연도 종단 시험도 단위
시험도
전부 초록인 채로 전 구간이 일관되게 거짓말한다.

판정 규칙 자체를 검증하므로 시험 이름은 한국어다.
"""

from __future__ import annotations

import pytest

from app.fixtures.loader import FIXTURE_FILES, load_fixture
from app.providers.llm_mock import MockLlmProvider
from app.service.ports import ContextView, TranscriptBlock


@pytest.fixture()
def provider() -> MockLlmProvider:
    return MockLlmProvider()


def _assess(provider: MockLlmProvider, key: str | None, version: int = 1):
    return provider.assess_conversation(
        prompt_id="assess",
        prompt_version="v1",
        criteria_version="c1",
        transcript_block=TranscriptBlock(),
        context=ContextView(),
        conversation_key=key,
        transcript_version=version,
    )


@pytest.mark.ac("AC9.2.2")
def test_S1_판정이_픽스처와_정확히_같다(provider: MockLlmProvider) -> None:
    assert tuple(_assess(provider, "conv_repair_01")) == load_fixture(
        "conv_repair_01"
    ).judgment_candidates(1)


@pytest.mark.ac("AC9.2.2")
def test_S2_판정이_픽스처와_정확히_같다(provider: MockLlmProvider) -> None:
    assert tuple(_assess(provider, "conv_topic_02")) == load_fixture(
        "conv_topic_02"
    ).judgment_candidates(1)


@pytest.mark.ac("AC9.2.2")
def test_S3_판정이_픽스처와_정확히_같다(provider: MockLlmProvider) -> None:
    assert tuple(_assess(provider, "conv_unclear_03")) == load_fixture(
        "conv_unclear_03"
    ).judgment_candidates(1)


def test_정정_전_전사_버전은_보류를_유지한다(provider: MockLlmProvider) -> None:
    candidates = {c.group: c for c in _assess(provider, "conv_unclear_03", version=1)}
    assert candidates["RESPONSE_RELEVANCE"].result is None
    assert candidates["RESPONSE_RELEVANCE"].hold_reason == "UNCLEAR_TRANSCRIPT"


def test_정정_후_전사_버전은_다른_판정을_돌려준다(provider: MockLlmProvider) -> None:
    """이 값이 빠지면 재분석 시연 경로가 재현되지 않는다 (계약 C14)."""
    before = {c.group: c for c in _assess(provider, "conv_unclear_03", version=1)}
    after = {c.group: c for c in _assess(provider, "conv_unclear_03", version=2)}

    assert before["RESPONSE_RELEVANCE"] != after["RESPONSE_RELEVANCE"]
    assert (
        after["RESPONSE_RELEVANCE"]
        == {c.group: c for c in load_fixture("conv_unclear_03").judgment_candidates(2)}[
            "RESPONSE_RELEVANCE"
        ]
    )


@pytest.mark.ac("AC9.2.3")
def test_모르는_키이면_S1_판정을_돌려준다(provider: MockLlmProvider) -> None:
    assert "conv_unknown_99" not in FIXTURE_FILES
    assert tuple(_assess(provider, "conv_unknown_99")) == load_fixture(
        "conv_repair_01"
    ).judgment_candidates(1)
