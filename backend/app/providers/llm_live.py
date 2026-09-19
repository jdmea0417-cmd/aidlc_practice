"""live 판정 제공자 — 인터페이스를 지키는 뼈대 (`[Q3]` OQ-N1).

제공자가 아직 정해지지 않았다 (D2). 키 없이 둔다 (security-design.md §5).

TODO(제공자 확정 시): 실제 요청 조립과 응답 파싱을 여기에 채운다. 응답은 신뢰하지 않는
입력이므로 저장 전에 응답 모델로 검증하고, 맞지 않으면 강제 변환하지 말고 거부한다
(security-design.md §4). 이 모듈은 HTTP 도구를 직접 import 하지 않는다.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.common.exceptions import ProviderError
from app.common.provider_call import call_provider
from app.service.ports import (
    CoachTurnResult,
    ContextView,
    JudgmentCandidate,
    ScenarioView,
    TranscriptBlock,
)


class LiveLlmProvider:
    """실제 판정 제공자 어댑터."""

    model_name = "live-llm-unconfigured"

    def __init__(self, api_key: str) -> None:
        if not api_key.strip():
            raise ValueError("live 판정 제공자에는 키가 필요하다 (BR1.2)")
        self._api_key = api_key

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
        def _call(client: object) -> Sequence[JudgmentCandidate]:  # pragma: no cover
            raise ProviderError("live 판정 제공자가 아직 선택되지 않았습니다.")

        return call_provider(
            _call,
            operation="llm.assess_conversation",
            model_name=self.model_name,
            prompt_version=prompt_version,
        )

    def coach_turn(
        self,
        *,
        prompt_id: str,
        prompt_version: str,
        scenario: ScenarioView,
        attempt_text_block: TranscriptBlock,
        attempt_order: int,
    ) -> CoachTurnResult:
        def _call(client: object) -> CoachTurnResult:  # pragma: no cover
            raise ProviderError("live 판정 제공자가 아직 선택되지 않았습니다.")

        return call_provider(
            _call,
            operation="llm.coach_turn",
            model_name=self.model_name,
            prompt_version=prompt_version,
        )
