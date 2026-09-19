"""STT·LLM 포트 — 계약 C14 (U1 -> U3·U5·U7).

**인터페이스는 `providers/` 가 아니라 여기에 둔다** (team.md § Code Style). 인터페이스가
구현체와 같은 패키지에 있으면 `service` 가 `providers` 를 import 하게 되고, 패키지
초기화를
타고 `live` 구현이 함께 불러와져 `ANALYSIS_MODE=mock` 인데 live SDK 가 없다고 죽는
실패가 난다.

`service` 는 이 Protocol 로만 제공자를 부른다. 어느 구현이 들어왔는지 알지 못한다
(TC-06).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class UtteranceView:
    """발화 하나. 판정의 근거가 되는 최소 단위다."""

    id: str
    speaker: str
    text: str
    unclear: bool = False


@dataclass(frozen=True)
class TranscriptBlock:
    """프롬프트에 넣을 전사 묶음.

    지시문과 데이터를 섞지 않는다 (TC-08). 구분자 시퀀스는 **조립할 때** 이스케이프한다
    —
    이 자료구조는 원문을 그대로 들고 있고, 격리는 조립기가 한다.
    """

    utterances: tuple[UtteranceView, ...] = ()


@dataclass(frozen=True)
class TranscriptionResult:
    """전사 결과."""

    utterances: tuple[UtteranceView, ...]
    model_name: str
    conversation_key: str | None = None


@dataclass(frozen=True)
class ContextView:
    """맥락 네 항목. 값이 없으면 `None` 이고, 그것이 곧 "미상"이다."""

    relation: str | None = None
    place: str | None = None
    purpose: str | None = None
    user_goal: str | None = None


@dataclass(frozen=True)
class EvidenceRef:
    """판정이 가리키는 발화. `role` 은 그 발화가 기회인지 반응인지를 나타낸다."""

    utterance_id: str
    role: str | None = None


@dataclass(frozen=True)
class JudgmentCandidate:
    """LLM·Mock 이 낸 판정 후보.

    저장 규칙(근거 검증, 보류, 배타성, 버전)은 U5 의 입구가 맡는다. U1 은 모양만 정한다.
    `result` 와 `hold_reason` 은 동시에 값을 가지지 않는다
    (docs/input/04_domain-model.md §3).
    """

    group: str
    opportunity: str
    result: str | None = None
    hold_reason: str | None = None
    performance_mode: str | None = None
    evidence: tuple[EvidenceRef, ...] = ()


@dataclass(frozen=True)
class ScenarioView:
    """모의 대화 원형·변형. 내용 상세는 u7-f05-practice 가 채운다."""

    template_id: str
    partner_prompt: str = ""
    variation_rules: dict = field(default_factory=dict)


@dataclass(frozen=True)
class CoachTurnResult:
    """모의 대화 한 턴. 상대 발화와 시도 판정 후보를 함께 돌려준다 (계약 C14)."""

    partner_text: str
    judgment: JudgmentCandidate | None = None


class SttProvider(Protocol):
    """음성을 전사로 바꾼다."""

    model_name: str

    def transcribe(self, audio_path: str, *, file_name: str) -> TranscriptionResult:
        """Mock 은 `file_name` 의 대화 키로 합성 전사를 고른다 (BR4.1, BR4.2)."""
        ...


class LlmProvider(Protocol):
    """전사를 판정으로, 시도를 코칭 한 턴으로 바꾼다."""

    model_name: str

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
        """Mock 은 대화 키와 전사 버전으로 기대 판정 픽스처를 고른다.

        정정 후 S3 를 포함한다.
        """
        ...

    def coach_turn(
        self,
        *,
        prompt_id: str,
        prompt_version: str,
        scenario: ScenarioView,
        attempt_text_block: TranscriptBlock,
        attempt_order: int,
    ) -> CoachTurnResult:
        """상대 발화와 시도 판정 후보를 함께 돌려준다."""
        ...
