"""시드 적재 — `uv run python scripts/seed.py --state <name>` (계약 C16, 흐름 W6).

상태는 **누적**이다 — 뒤 상태가 앞 상태를 포함한다. 여러 번 돌려도 같은 결과가 되게
만든다.

    base            고정 사용자 1명(동의 전) + 시나리오 원형·검토된 변형
    consented       base + 동의 완료
    s1-transcribed  consented + S1(conv_repair_01) 전사 완료, 맥락 입력

U1 이 넣는 것은 위 세 상태다. 나머지 여섯 상태는 갈래 4 가 더한다 (D-115).

**값은 픽스처에서 읽는다. 다시 적지 않는다** (BR4.3). 실제 사용자 데이터는 넣지 않는다 —
전부 합성이다 (SC-02).

경계 하나를 적어 둔다: 계약 C16 의 `base` 는 시나리오 원형 **여섯 개**를 말하지만, 기존
명세가 이름을 적은 원형은 `tpl_repair_person_01` 하나뿐이다. 나머지 다섯의 식별자와
내용은
u7-f05-practice 가 자기 기능 설계에서 정하고 같은 자리에 더한다 — 여기서 지어내지 않는다
(BR8.1).
"""

from __future__ import annotations

import argparse
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import new_session
from app.fixtures.constants import (
    SEED_USER_DISPLAY_NAME,
    SEED_USER_ID,
    SEED_USER_ROLE,
)
from app.fixtures.loader import load_fixture
from app.repository.models import (
    AudioAsset,
    ContextInfo,
    Conversation,
    ScenarioTemplate,
    ScenarioVariant,
    User,
    Utterance,
)

#: 이 단위가 넣는 상태. 순서가 곧 누적 순서다.
STATES: tuple[str, ...] = ("base", "consented", "s1-transcribed")

S1_KEY = "conv_repair_01"


def seed_base(session: Session) -> User:
    """고정 사용자 한 명을 **동의 전** 상태로 만든다 (BR2.1).

    종단 시험이 동의 화면부터 시작해야 하므로 동의 시각을 비운 채로 만든다.
    """
    user = session.get(User, SEED_USER_ID)
    if user is None:
        user = User(
            id=SEED_USER_ID,
            display_name=SEED_USER_DISPLAY_NAME,
            role=SEED_USER_ROLE,
            consented_at=None,
        )
        session.add(user)

    template_id = load_fixture(S1_KEY).practice_template_id
    if template_id and session.get(ScenarioTemplate, template_id) is None:
        session.add(ScenarioTemplate(id=template_id))
        session.add(ScenarioVariant(template_id=template_id, variation_rules={}))

    session.flush()
    return user


def seed_consented(session: Session) -> User:
    """base + 동의 완료."""
    user = seed_base(session)
    if user.consented_at is None:
        user.consented_at = datetime.now(UTC)
    session.flush()
    return user


def seed_s1_transcribed(session: Session) -> Conversation:
    """consented + S1 전사 완료, 맥락 입력.

    전사 상태는 내부 값 `TRANSCRIBED` 다 — 계약 C16 이 적은 `READY` 는 API 값이며 같은
    상태를 가리킨다 (entities.md §4 대응표).

    발화 행은 순번만 넣는다. 화자·본문 컬럼은 `conversations`·`utterances` 의 컬럼을
    소유하는 u3-f01-capture 가 자기 리비전으로 더한 뒤 같은 자리에서 채운다 (BR8.1).
    """
    user = seed_consented(session)
    fixture = load_fixture(S1_KEY)

    conversation = session.execute(
        select(Conversation).where(Conversation.conversation_key == S1_KEY)
    ).scalar_one_or_none()

    if conversation is None:
        conversation = Conversation(
            id=uuid.uuid4(),
            user_id=user.id,
            conversation_key=S1_KEY,
            transcript_status="TRANSCRIBED",
            transcript_failure_reason=None,
            analysis_status="NOT_ANALYZED",
            transcript_version=1,
        )
        session.add(conversation)
        session.flush()

        session.add(AudioAsset(conversation_id=conversation.id))
        for order, _utterance in enumerate(fixture.transcript(1), start=1):
            session.add(
                Utterance(conversation_id=conversation.id, utterance_order=order)
            )

        context = fixture.context
        session.add(
            ContextInfo(
                conversation_id=conversation.id,
                relation_value=context.relation,
                relation_status="CONFIRMED" if context.relation else "UNKNOWN",
                place_value=context.place,
                place_status="CONFIRMED" if context.place else "UNKNOWN",
                purpose_value=context.purpose,
                purpose_status="CONFIRMED" if context.purpose else "UNKNOWN",
                user_goal_value=context.user_goal,
                user_goal_status="CONFIRMED" if context.user_goal else "UNKNOWN",
            )
        )

    session.flush()
    return conversation


SEEDERS = {
    "base": seed_base,
    "consented": seed_consented,
    "s1-transcribed": seed_s1_transcribed,
}


def seed(state: str, session: Session) -> None:
    """상태 하나를 적재한다. 확정은 여기서 한 번 한다."""
    if state not in SEEDERS:
        raise SystemExit(
            f"모르는 시드 상태다: {state}. 쓸 수 있는 값: {', '.join(STATES)}"
        )
    SEEDERS[state](session)
    session.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="시드 상태를 적재한다 (계약 C16)")
    parser.add_argument("--state", required=True, choices=list(STATES))
    arguments = parser.parse_args()

    session = new_session()
    try:
        seed(arguments.state, session)
    finally:
        session.close()
    print(f"시드 상태 {arguments.state} 를 적재했다")


if __name__ == "__main__":
    main()
