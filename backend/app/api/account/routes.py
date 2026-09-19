"""현재 사용자와 첫 방문 동의 (W3, W4, 계약 C1).

인증을 요구하지 않는다. **클라이언트가 보낸 사용자 식별자를 읽지 않는다** — 현재
사용자는
`service/current_user.py` 한 곳이 결정한다 (BR2.3, NFR6.1).

모든 라우트에 응답 모델을 선언한다 — ORM 객체가 응답으로 새는 일을 구조적으로 막는다.
라우트는 동기 `def` 다 (D-54).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.account.schemas import ConsentRequest, MeResponse
from app.db import get_session
from app.service.account import service as account_service

router = APIRouter(prefix="/api/v1", tags=["account"])


@router.get("/me", response_model=MeResponse)
def get_me(session: Session = Depends(get_session)) -> MeResponse:
    """현재 사용자(Must 는 시드 고정 사용자)."""
    return MeResponse.model_validate(account_service.get_me(session))


@router.post("/me/consent", response_model=MeResponse)
def post_consent(
    body: ConsentRequest, session: Session = Depends(get_session)
) -> MeResponse:
    """첫 방문 안내에 동의한다. 여러 번 보내도 처음 시각이 남는다 (BR2.2)."""
    del body  # 값은 `Literal[True]` 검증으로 이미 확인되었다
    return MeResponse.model_validate(account_service.give_consent(session))
