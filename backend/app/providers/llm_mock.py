"""Mock 판정 제공자 — 대화 키와 전사 버전으로 기대 판정을 고른다 (BR4.1, BR4.2, BR4.3).

전사 버전을 함께 받는 이유는 정정 전·후 S3 를 구분하기 위해서다. 이 값이 빠지면 재분석
시연 경로가 재현되지 않는다 (계약 C14).

Mock 은 프롬프트를 읽지 않는다 — 그래서 TC-08 은 이 경로에서 증명되지 않고, 프롬프트
조립
시험이 따로 그것을 본다.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.fixtures.loader import DEFAULT_CONVERSATION_KEY, FIXTURE_FILES, load_fixture
from app.service.ports import (
    CoachTurnResult,
    ContextView,
    EvidenceRef,
    JudgmentCandidate,
    ScenarioView,
    TranscriptBlock,
)


class MockLlmProvider:
    """픽스처가 정한 값을 그대로 돌려준다."""

    model_name = "mock-llm-v1"

    def assess_conversation(
        self,
        *,
        prompt_id: str,
        prompt_version: str,
        criteria_version: str,
        transcript_block: TranscriptBlock,
        context: ContextView,
        conversation_key: str | None,
        transcript_version: int,
    ) -> Sequence[JudgmentCandidate]:
        key = (
            conversation_key
            if conversation_key in FIXTURE_FILES
            else DEFAULT_CONVERSATION_KEY
        )
        return load_fixture(key).judgment_candidates(transcript_version)

    def coach_turn(
        self,
        *,
        prompt_id: str,
        prompt_version: str,
        scenario: ScenarioView,
        attempt_text_block: TranscriptBlock,
        attempt_order: int,
    ) -> CoachTurnResult:
        """연습 기대값도 픽스처에서 읽는다.

        지금 픽스처가 담은 원형은 S1 의 `tpl_repair_person_01` 하나다. 다른 원형과 턴은
        u7-f05-practice 가 자기 기능 설계 뒤에 픽스처에 더한다 — 여기서 값을 지어내지
        않는다.
        """
        fixture = load_fixture(DEFAULT_CONVERSATION_KEY)
        turn = fixture.practice_turns.get(attempt_order)
        if turn is None:
            raise KeyError(
                f"픽스처에 없는 연습 턴이다: template={scenario.template_id!r}, "
                f"attempt_order={attempt_order}. u7-f05-practice 가 픽스처에 더한다"
            )

        raw = turn.get("judgment")
        judgment = None
        if raw is not None:
            judgment = JudgmentCandidate(
                group=raw["group"],
                opportunity=raw["opportunity"],
                result=raw.get("result"),
                hold_reason=raw.get("holdReason"),
                performance_mode=raw.get("performanceMode"),
                evidence=tuple(
                    EvidenceRef(utterance_id=ref["utteranceId"], role=ref.get("role"))
                    for ref in raw.get("evidence", [])
                ),
            )
        return CoachTurnResult(partner_text=turn["partnerText"], judgment=judgment)
