"""계정 API 의 요청·응답 모델 (계약 C1).

ORM 모델을 그대로 내보내지 않는다. JSON 은 camelCase, Python 은 snake_case 로 두고
별칭으로 바꾼다 (계약 공통 규칙).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class MeResponse(BaseModel):
    """계약 C1 의 `Me`. `consentedAt` 이 비어 있으면 아직 동의 전이다."""

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )

    id: uuid.UUID
    display_name: str
    role: Literal["USER", "GUARDIAN"]
    consented_at: datetime | None


class ConsentRequest(BaseModel):
    """첫 방문 서비스 안내 동의 (FR9.2). `agreed` 는 참만 받는다."""

    # 한 단어라 별칭 규칙이 필요 없다 — 붙이면 아무 일도 하지 않으면서 경고만 남는다.
    agreed: Literal[True]
