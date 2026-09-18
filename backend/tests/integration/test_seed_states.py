"""시드 상태 — 누적이고, 값은 픽스처에서 읽는다 (계약 C16, W6, BR2.1, BR4.3).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.fixtures.constants import SEED_USER_DISPLAY_NAME, SEED_USER_ID
from app.fixtures.loader import load_fixture
from app.repository.models import ContextInfo, Conversation, User, Utterance
from scripts import seed as seed_script

pytestmark = pytest.mark.integration

S1_KEY = "conv_repair_01"


@pytest.mark.ac("AC9.2.1")
def test_base_creates_the_fixed_user_before_consent(db_session: Session) -> None:
    seed_script.seed_base(db_session)

    user = db_session.get(User, SEED_USER_ID)
    assert user is not None
    assert user.display_name == SEED_USER_DISPLAY_NAME
    assert user.consented_at is None, "종단 시험이 동의 화면부터 시작해야 한다 (BR2.1)"


def test_consented_builds_on_base(db_session: Session) -> None:
    seed_script.seed_consented(db_session)

    user = db_session.get(User, SEED_USER_ID)
    assert user is not None, "consented 가 base 를 포함하지 않았다"
    assert user.consented_at is not None


def test_s1_transcribed_builds_on_consented(db_session: Session) -> None:
    seed_script.seed_s1_transcribed(db_session)

    user = db_session.get(User, SEED_USER_ID)
    assert (
        user is not None and user.consented_at is not None
    ), "앞 상태를 포함하지 않았다"

    conversation = db_session.execute(
        select(Conversation).where(Conversation.conversation_key == S1_KEY)
    ).scalar_one()
    assert conversation.transcript_status == "TRANSCRIBED"
    assert conversation.analysis_status == "NOT_ANALYZED"

    utterance_count = db_session.execute(
        select(func.count())
        .select_from(Utterance)
        .where(Utterance.conversation_id == conversation.id)
    ).scalar_one()
    assert utterance_count == len(load_fixture(S1_KEY).transcript(1))


def test_seed_values_come_from_the_fixture(db_session: Session) -> None:
    """시드가 값을 다시 적지 않는다 — 픽스처가 단일 출처다 (BR4.3)."""
    seed_script.seed_s1_transcribed(db_session)
    fixture_context = load_fixture(S1_KEY).context

    conversation = db_session.execute(
        select(Conversation).where(Conversation.conversation_key == S1_KEY)
    ).scalar_one()
    context = db_session.execute(
        select(ContextInfo).where(ContextInfo.conversation_id == conversation.id)
    ).scalar_one()

    assert context.relation_value == fixture_context.relation
    assert context.place_value == fixture_context.place
    assert context.purpose_value == fixture_context.purpose
    assert context.user_goal_value == fixture_context.user_goal
    assert context.user_goal_status == "UNKNOWN", "S1 의 사용자 목표는 미상이다"
