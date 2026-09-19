"""제공자 선택 — **결정된 모드의 객체만 만든다** (NFR5.3, security-design.md §1.2).

`mock` 모드로 뜬 프로세스 안에는 외부로 나가는 경로를 가진 객체가 존재하지 않는다.
실수로
호출할 대상 자체가 없다. 그래서 live 구현은 **함수 안에서** import 한다 — 모듈을
불러오는
것만으로 live 구현이 딸려 들어오면 그 보장이 깨진다.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.config import AnalysisMode, Settings
from app.service.ports import LlmProvider, SttProvider


@dataclass(frozen=True)
class Providers:
    """이 프로세스가 쓰는 제공자 한 벌."""

    mode: AnalysisMode
    stt: SttProvider
    llm: LlmProvider


def build_providers(mode: AnalysisMode, settings: Settings) -> Providers:
    """분석 모드가 이미 결정된 뒤에 부른다.

    여기서 모드를 다시 판별하지 않는다 (BR1.3).
    """
    if mode == "mock":
        from app.providers.llm_mock import MockLlmProvider
        from app.providers.stt_mock import MockSttProvider

        return Providers(mode=mode, stt=MockSttProvider(), llm=MockLlmProvider())

    from app.providers.llm_live import LiveLlmProvider
    from app.providers.stt_live import LiveSttProvider

    return Providers(
        mode=mode,
        stt=LiveSttProvider(settings.stt_api_key or ""),
        llm=LiveLlmProvider(settings.llm_api_key or ""),
    )
