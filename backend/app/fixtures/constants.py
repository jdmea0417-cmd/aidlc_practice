"""시드 고정 사용자 상수 — 이 한 자리에서만 읽는다 (OQ-F2 의 답, `[Q2]`).

Must 경로는 인증 없이 이 사용자 한 명으로 돈다 (FR11.1, BR2.3). 식별자를 고정값으로 둔
이유는
시드·시험·픽스처가 같은 값을 보게 하기 위해서다. 값을 다른 모듈에 옮겨 적지 않는다.
모두 합성 데이터다 (SC-02).
"""

from __future__ import annotations

import uuid

# : 시드 고정 사용자의 식별자. 이 값을 읽는 자리는 `app/service/current_user.py` 와
# 시드뿐이다.
SEED_USER_ID: uuid.UUID = uuid.UUID("00000000-0000-4000-8000-000000000001")

#: 화면에 보이는 이름. 합성 데이터다.
SEED_USER_DISPLAY_NAME: str = "합성 사용자"

#: 시드 고정 사용자는 주 사용자다 (entities.md §1).
SEED_USER_ROLE: str = "USER"
