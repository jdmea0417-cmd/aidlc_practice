"""현재 사용자 결정 지점 — **코드에서 한 곳** (security-design.md §6, NFR6.1, NFR6.2).

Must 경로는 인증 없이 시드 고정 사용자로 돈다 (FR11.1, BR2.3). 이것은 로컬 전용이라는
전제
위에서 받아들인 위험이지 빠뜨린 것이 아니다. 설계가 하는 일은 **나중에 인증이 들어올 때
고칠
자리를 하나로 모아 두는 것**이다.

    요청 --> [이 함수] --> 나머지 코드는 "사용자"만 안다
                +-- 지금:     시드 고정 사용자를 돌려준다
                +-- u11 이후: 세션을 확인해 로그인한 사용자를 돌려준다

**클라이언트가 보낸 사용자 식별자를 읽지 않는다.** 그래서 이 함수는 요청을 인자로 받지
않는다 —
지금 읽지 않으면 나중에 신뢰하게 될 일도 없다.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.common.exceptions import NotFoundError
from app.fixtures.constants import SEED_USER_ID
from app.repository.account import repository as account_repository
from app.repository.models import User


def resolve_current_user(session: Session) -> User:
    """지금 요청을 처리할 사용자. 없으면 시드가 아직 적재되지 않은 것이다."""
    user = account_repository.get_user_by_id(session, SEED_USER_ID)
    if user is None:
        raise NotFoundError(
            "고정 사용자를 찾을 수 없습니다. 시드를 먼저 적재해 주세요.",
            code="SEED_USER_NOT_FOUND",
        )
    return user
