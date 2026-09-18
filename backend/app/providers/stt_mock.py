"""Mock 전사 제공자 — 시연이 매번 같은 결과로 재현되게 한다 (BR4.1, BR4.2).

값은 전부 픽스처에서 읽는다. 여기에 전사를 옮겨 적지 않는다 (BR4.3).
"""

from __future__ import annotations

from app.fixtures.loader import load_fixture, resolve_conversation_key
from app.service.ports import TranscriptionResult


class MockSttProvider:
    """파일 이름의 대화 키로 합성 전사를 고른다."""

    model_name = "mock-stt-v1"

    def transcribe(self, audio_path: str, *, file_name: str) -> TranscriptionResult:
        conversation_key = resolve_conversation_key(file_name)
        fixture = load_fixture(conversation_key)
        return TranscriptionResult(
            utterances=fixture.transcript(1),
            model_name=self.model_name,
            conversation_key=conversation_key,
        )
