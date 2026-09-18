"""live 전사 제공자 — 인터페이스를 지키는 뼈대 (`[Q3]` OQ-N1).

제공자가 아직 정해지지 않았다 (D2). 그래서 **키 없이** 둔다 — 키가 존재하지 않는
기간에는
유출될 키도 없다 (security-design.md §5).

TODO(제공자 확정 시): 실제 요청 조립과 응답 파싱을 여기에 채운다. 그때 바뀌는 것은 이
파일
하나이고, 타임아웃·재시도·로그는 `app/common/provider_call.py` 가 이미 맡고 있다.
이 모듈은 HTTP 도구를 직접 import 하지 않는다 — 클라이언트를 감싸기 장치에서 받는다.
"""

from __future__ import annotations

from app.common.exceptions import ProviderError
from app.common.provider_call import call_provider
from app.service.ports import TranscriptionResult


class LiveSttProvider:
    """실제 전사 제공자 어댑터."""

    model_name = "live-stt-unconfigured"

    def __init__(self, api_key: str) -> None:
        if not api_key.strip():
            raise ValueError("live 전사 제공자에는 키가 필요하다 (BR1.2)")
        self._api_key = api_key

    def transcribe(self, audio_path: str, *, file_name: str) -> TranscriptionResult:
        def _call(
            client: object,
        ) -> TranscriptionResult:  # pragma: no cover - 제공자 미정
            raise ProviderError("live 전사 제공자가 아직 선택되지 않았습니다.")

        return call_provider(
            _call, operation="stt.transcribe", model_name=self.model_name
        )
