"""구조화 로그 — 한 줄의 모양을 고정한다 (observability-design.md §1).

모든 로그 줄이 공통으로 갖는 필드는 **여섯 개**다: 시각·수준·메시지·컴포넌트·요청
식별자·
작업 식별자. 앞의 넷은 항상 값이 있고, 뒤의 둘은 문맥에서 자동으로 채워진다.

컴포넌트는 **로거를 만들 때 한 번** 넘긴다. 로그 호출마다 적게 하면 빠뜨리는 자리가
생긴다.
허용값을 여덟 개로 고정한 이유는 자유 문자열이면 `conv`/`conversation`/`Conversation`
으로
갈라지기 때문이다 — 팀 관행이 경계하는 이름 분기다.

**전사 본문이 로그에 들어갈 수 없게 한다** (BR6.3, NFR12.8):
- 예외 객체를 통째로 넘길 수 없다. 제공자 예외가 요청 본문을 품고 있을 수 있다.
- 본문으로 읽히는 이름의 필드를 거부한다. 진단 수준에서도 마찬가지다 —
  "개발 중에만 켠다"가 시연 환경에서 켜져 있을 수 있다.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

from app.common.request_context import current_job_id, current_request_id

#: 컴포넌트 허용값 여덟 개 (observability-design.md §1)
ALLOWED_COMPONENTS: tuple[str, ...] = (
    "conversation",
    "assessment",
    "training",
    "record",
    "account",
    "privacy",
    "common",
    "providers",
)

#: 전사 본문으로 읽히는 필드 이름. 어떤 수준에서도 받지 않는다.
FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "transcript",
        "transcript_text",
        "transcription",
        "utterances",
        "text",
        "prompt",
        "prompt_text",
        "body",
        "request_body",
        "response_body",
        "content",
    }
)

_configured = False


def configure_logging(level: str = "INFO") -> None:
    """표준 출력에 한 줄 하나를 낸다.

    수집기를 붙이는 날 앱을 고치지 않아도 되게 한다.
    """
    global _configured
    root = logging.getLogger()
    root.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(handler)
    root.setLevel(level.upper())
    _configured = True


class StructuredLogger:
    """컴포넌트가 붙은 로거. 여섯 필드를 빠뜨릴 수 없게 만든다."""

    def __init__(self, component: str) -> None:
        if component not in ALLOWED_COMPONENTS:
            raise ValueError(
                f"모르는 컴포넌트다: {component!r}. 허용값: {ALLOWED_COMPONENTS}"
            )
        self._component = component
        self._logger = logging.getLogger(f"app.{component}")

    @property
    def component(self) -> str:
        return self._component

    def _emit(self, level: int, message: str, fields: dict[str, Any]) -> None:
        for name, value in fields.items():
            if name in FORBIDDEN_FIELDS:
                raise ValueError(
                    f"로그에 남길 수 없는 필드다: {name!r}. "
                    "전사 본문은 로그에 남기지 않는다 (BR6.3)"
                )
            if isinstance(value, BaseException):
                raise TypeError(
                    f"예외 객체를 통째로 넘길 수 없다: {name!r}. "
                    "예외의 종류와 메시지만 따로 넘긴다 (observability-design.md §2)"
                )

        record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": logging.getLevelName(level),
            "message": message,
            "component": self._component,
            "request_id": current_request_id(),
            "job_id": current_job_id(),
        }
        record.update(fields)
        self._logger.log(level, json.dumps(record, ensure_ascii=False, default=str))

    def debug(self, message: str, **fields: Any) -> None:
        self._emit(logging.DEBUG, message, fields)

    def info(self, message: str, **fields: Any) -> None:
        self._emit(logging.INFO, message, fields)

    def warning(self, message: str, **fields: Any) -> None:
        self._emit(logging.WARNING, message, fields)

    def error(self, message: str, **fields: Any) -> None:
        self._emit(logging.ERROR, message, fields)


def get_logger(*, component: str) -> StructuredLogger:
    """모듈마다 한 번 부른다. 이 로거로 남긴 모든 줄에 컴포넌트가 자동으로 붙는다."""
    return StructuredLogger(component)
