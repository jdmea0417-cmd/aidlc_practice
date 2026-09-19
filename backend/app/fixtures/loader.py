"""합성 대화 픽스처 로더 — 단일 출처를 읽는 유일한 자리 (BR4.3, NFR14.1).

Mock 제공자·백엔드 단위 시험·프론트엔드 모의 응답·종단 시험이 모두 같은 한 벌을 읽는다.
사람이 같은 표를 두 번 적는 자리를 0 으로 만든다 — 손으로 옮긴 사본은 반드시 어긋나고,
어긋나도 각자 초록이라 아무도 모른다.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from app.service.ports import (
    ContextView,
    EvidenceRef,
    JudgmentCandidate,
    UtteranceView,
)

FIXTURE_DIR = Path(__file__).resolve().parent

#: 대화 키 -> 픽스처 파일 이름 (BR4.1)
FIXTURE_FILES: dict[str, str] = {
    "conv_repair_01": "s1_repair.json",
    "conv_topic_02": "s2_topic.json",
    "conv_unclear_03": "s3_unclear.json",
}

#: 대화 키를 찾지 못했을 때 쓰는 기본 대화 (BR4.2). 실패로 만들지 않는다.
DEFAULT_CONVERSATION_KEY = "conv_repair_01"


@dataclass(frozen=True)
class ConversationFixture:
    """합성 대화 하나의 전부 — 전사와 기대 판정."""

    conversation_key: str
    scenario_id: str
    context: ContextView
    transcripts: dict[int, tuple[UtteranceView, ...]]
    judgments: dict[int, tuple[JudgmentCandidate, ...]]
    practice_turns: dict[int, dict[str, Any]]
    practice_template_id: str | None
    note: str

    def transcript(self, version: int = 1) -> tuple[UtteranceView, ...]:
        """그 버전의 전사. 없는 버전은 버전 1 로 되돌린다 — 정정 전 상태가 기본이다."""
        return self.transcripts.get(version, self.transcripts[1])

    def judgment_candidates(self, version: int = 1) -> tuple[JudgmentCandidate, ...]:
        """그 버전의 기대 판정. 없는 버전은 버전 1 로 되돌린다."""
        return self.judgments.get(version, self.judgments[1])


def resolve_conversation_key(file_name: str | None) -> str:
    """파일 이름에서 대화 키를 고른다.

    키가 없거나 / 키처럼 생겼지만 모르는 값이거나 / 브라우저 녹음이면 S1 으로 처리한다
    (BR4.1, BR4.2). 실패로 만들지 않는다 — 시연 중 이름이 다른 파일을 올려도 흐름이
    끊기지
    않아야 한다.
    """
    if not file_name:
        return DEFAULT_CONVERSATION_KEY
    lowered = file_name.lower()
    for key in FIXTURE_FILES:
        if key in lowered:
            return key
    return DEFAULT_CONVERSATION_KEY


def _to_utterances(raw: list[dict[str, Any]]) -> tuple[UtteranceView, ...]:
    return tuple(
        UtteranceView(
            id=item["id"],
            speaker=item["speaker"],
            text=item["text"],
            unclear=bool(item.get("unclear", False)),
        )
        for item in raw
    )


def _to_candidates(raw: list[dict[str, Any]]) -> tuple[JudgmentCandidate, ...]:
    return tuple(
        JudgmentCandidate(
            group=item["group"],
            opportunity=item["opportunity"],
            result=item.get("result"),
            hold_reason=item.get("holdReason"),
            performance_mode=item.get("performanceMode"),
            evidence=tuple(
                EvidenceRef(utterance_id=ref["utteranceId"], role=ref.get("role"))
                for ref in item.get("evidence", [])
            ),
        )
        for item in raw
    )


@cache
def load_fixture(conversation_key: str) -> ConversationFixture:
    """대화 키로 픽스처를 읽는다. 모르는 키는 오류다 — 여기서 조용히 되돌리지 않는다.

    되돌림은 `resolve_conversation_key()` 한 곳에서만 일어난다 (BR4.2). 두 자리에서
    되돌리면
    "모르는 키였다"는 사실이 어디서도 드러나지 않는다.
    """
    if conversation_key not in FIXTURE_FILES:
        raise KeyError(f"모르는 대화 키다: {conversation_key!r}")

    raw = json.loads(
        (FIXTURE_DIR / FIXTURE_FILES[conversation_key]).read_text(encoding="utf-8")
    )
    context = raw["context"]
    practice = raw.get("practice", {})

    return ConversationFixture(
        conversation_key=raw["conversationKey"],
        scenario_id=raw["scenarioId"],
        context=ContextView(
            relation=context.get("relation"),
            place=context.get("place"),
            purpose=context.get("purpose"),
            user_goal=context.get("userGoal"),
        ),
        transcripts={
            int(version): _to_utterances(items)
            for version, items in raw["transcripts"].items()
        },
        judgments={
            int(version): _to_candidates(items)
            for version, items in raw["judgments"].items()
        },
        practice_turns={
            int(turn["attemptOrder"]): turn for turn in practice.get("turns", [])
        },
        practice_template_id=practice.get("scenarioTemplateId"),
        note=raw["__note"],
    )


def load_all_fixtures() -> dict[str, ConversationFixture]:
    """세 대화를 모두 읽는다."""
    return {key: load_fixture(key) for key in FIXTURE_FILES}
