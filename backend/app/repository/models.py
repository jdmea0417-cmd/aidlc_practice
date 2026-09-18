"""SQLAlchemy 2.0 declarative 모델 — 초기 스키마의 테이블 20개.

**경계** (entities.md §3, BR8.1): `users` 만 U1 이 속성 전체를 소유한다. 나머지 19개는
계약과
기존 명세가 **글로 확정한 것만** 적고, 정해지지 않은 타입·제약·허용값은 추측해 적지
않는다.
각 테이블의 소유 단위가 자기 기능 설계 뒤에 리비전으로 더한다.

- 외래 키의 `ON DELETE CASCADE` 는 **그물로만** 둔다. 실제 삭제 순서는 계약 C13 과
privacy 의
  삭제 유스케이스가 정한다.
- 관계 기본값은 `lazy="raise"` 다 — ORM 객체가 API 쪽으로 새면 조용한 N+1 이 되지 않고
즉시 터진다.
- 음성 본문 컬럼을 두지 않는다 (TC-05, BR8.2).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """모든 모델의 기반."""


#: 관계 기본값은 `lazy="raise"` 다 (team.md § Code Style, performance-design.md §2).
# : ORM 객체가 API 쪽으로 새면 직렬화 시점에 조용한 N+1 이 되지 않고 **즉시 예외로**
# 터진다.
# : 관계를 더하는 단위는 `relationship(...)` 대신 이 도우미를 쓴다 — 기본값을 사람이
# 기억하지
#: 않아도 되게 하는 것이 목적이다.
def related(target: str, **kwargs: Any) -> Any:
    kwargs.setdefault("lazy", "raise")
    return relationship(target, **kwargs)


def _uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


# --- 내부 허용값 (entities.md §4, docs/input/04_domain-model.md) ---
TRANSCRIPT_STATUSES = ("UPLOADING", "TRANSCRIBING", "TRANSCRIBED", "TRANSCRIBE_FAILED")
TRANSCRIPT_FAILURE_REASONS = ("STORAGE", "TRANSCRIPTION")
ANALYSIS_STATUSES = ("NOT_ANALYZED", "ANALYZING", "ANALYZED", "ANALYZE_FAILED")
USER_ROLES = ("USER", "GUARDIAN")
CONTEXT_STATUSES = ("CONFIRMED", "USER_REPORTED", "UNKNOWN")
SHARING_LEVELS = ("NONE", "SUMMARY", "FULL")
DELETION_REQUEST_STATUSES = ("REQUESTED", "DONE", "PARTIAL")


def _enum_check(column: str, allowed: tuple[str, ...], name: str) -> CheckConstraint:
    values = ", ".join(f"'{value}'" for value in allowed)
    return CheckConstraint(f"{column} IN ({values})", name=name)


# ---------------------------------------------------------------------------
# users — U1 이 속성 전체를 소유하는 유일한 테이블 (entities.md §1)
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("display_name <> ''", name="ck_users_display_name_not_empty"),
        _enum_check("role", USER_ROLES, "ck_users_role"),
    )

    id: Mapped[uuid.UUID] = _uuid_pk()
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False, server_default="USER")
    age_band: Mapped[str | None] = mapped_column(Text, nullable=True)
    language_background: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 동의 여부는 이 한 값이 나타낸다 — 별도 불리언을 두지 않는다. 비어 있으면 아직 동의
    # 전이다.
    consented_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # entities.md §1 의 관계. 둘 다 `lazy="raise"` 라 무심코 따라가면 즉시 터진다.
    conversations: Mapped[list[Conversation]] = related(
        "Conversation", back_populates="user"
    )
    guardian_invitations: Mapped[list[GuardianInvitation]] = related(
        "GuardianInvitation", back_populates="user"
    )


# ---------------------------------------------------------------------------
# account — guardian_invitations (속성 상세 소유: u12-s-guardian-sharing)
# ---------------------------------------------------------------------------
class GuardianInvitation(Base):
    """U1 이 적는 것: 사용자 참조, 초대 코드 유일성."""

    __tablename__ = "guardian_invitations"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    invitation_code: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True
    )

    user: Mapped[User] = related("User", back_populates="guardian_invitations")


# ---------------------------------------------------------------------------
# conversation — conversations / audio_assets / utterances / corrections
# ---------------------------------------------------------------------------
class Conversation(Base):
    """U1 이 적는 것: 사용자 참조, 상태 컬럼 둘과 전사 실패 사유, 전사 버전, 대화 키.

    두 상태 값은 독립적으로 움직인다 (BR7.3). 말이 되지 않는 조합은 아래 검사가 막는다 —
    분석은 전사가 끝난 뒤에만 시작될 수 있다 (BR7.1).
    """

    __tablename__ = "conversations"
    __table_args__ = (
        _enum_check(
            "transcript_status",
            TRANSCRIPT_STATUSES,
            "ck_conversations_transcript_status",
        ),
        CheckConstraint(
            "transcript_failure_reason IS NULL OR transcript_failure_reason IN "
            "('STORAGE', 'TRANSCRIPTION')",
            name="ck_conversations_transcript_failure_reason",
        ),
        # 실패 사유는 전사 실패 상태에서만 값을 가진다 (entities.md §4)
        CheckConstraint(
            "(transcript_status = 'TRANSCRIBE_FAILED') "
            "= (transcript_failure_reason IS NOT NULL)",
            name="ck_conversations_failure_reason_only_when_failed",
        ),
        _enum_check(
            "analysis_status", ANALYSIS_STATUSES, "ck_conversations_analysis_status"
        ),
        # BR7.1 — 전사가 끝나기 전에는 분석이 시작될 수 없다 (functional-spec.md §2
        # SM-B)
        CheckConstraint(
            "analysis_status = 'NOT_ANALYZED' OR transcript_status = 'TRANSCRIBED'",
            name="ck_conversations_analysis_requires_transcript",
        ),
    )

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    transcript_status: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="UPLOADING"
    )
    transcript_failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    analysis_status: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="NOT_ANALYZED"
    )
    transcript_version: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="1"
    )
    conversation_key: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User] = related("User", back_populates="conversations")


class AudioAsset(Base):
    """U1 이 적는 것: 대화 참조.

    **음성 본문을 넣는 컬럼을 두지 않는다** (TC-05, BR8.2). 파일은 파일 저장소에 두고
    이 테이블에는 참조와 메타데이터만 둔다 — 메타데이터 컬럼은 u3-f01-capture 가 더한다.
    """

    __tablename__ = "audio_assets"

    id: Mapped[uuid.UUID] = _uuid_pk()
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )


class Utterance(Base):
    """U1 이 적는 것: 대화 참조, 발화 순번."""

    __tablename__ = "utterances"

    id: Mapped[uuid.UUID] = _uuid_pk()
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    utterance_order: Mapped[int] = mapped_column(Integer, nullable=False)


class Correction(Base):
    """U1 이 적는 것: 발화 참조, 만든 시각."""

    __tablename__ = "corrections"

    id: Mapped[uuid.UUID] = _uuid_pk()
    utterance_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("utterances.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class ContextInfo(Base):
    """U1 이 적는 것: 대화 참조, 값과 상태(확인됨 / 사용자 보고 / 미상).

    네 항목(관계·장소·목적·사용자 목표)은 각각 `{값, 상태}` 짝이다
    (docs/input/04_domain-model.md §2). 그 밖의 세부는 u4-f02-context 가 정한다.
    """

    __tablename__ = "context_infos"
    __table_args__ = tuple(
        _enum_check(
            f"{field}_status", CONTEXT_STATUSES, f"ck_context_infos_{field}_status"
        )
        for field in ("relation", "place", "purpose", "user_goal")
    )

    id: Mapped[uuid.UUID] = _uuid_pk()
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    relation_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    relation_status: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="UNKNOWN"
    )
    place_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    place_status: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="UNKNOWN"
    )
    purpose_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    purpose_status: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="UNKNOWN"
    )
    user_goal_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_goal_status: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="UNKNOWN"
    )


# ---------------------------------------------------------------------------
# assessment — social_events / behavior_judgments / evidences / analysis_feedbacks
# ---------------------------------------------------------------------------
class SocialEvent(Base):
    """U1 이 적는 것: 대화 참조."""

    __tablename__ = "social_events"

    id: Mapped[uuid.UUID] = _uuid_pk()
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )


class BehaviorJudgment(Base):
    """U1 이 적는 것: 출처 네 컬럼 `NOT NULL`, `supersedes_judgment_id`, `needs_review`.

    출처 네 값은 묶어서 다닌다 (TC-10, 계약 C10 `Provenance`). "함께 저장한다"가 사람의
    주의력이 아니라 스키마 제약이 되게 한다. 부모 참조는 `SocialEvent ─<
    BehaviorJudgment`
    (docs/input/04_domain-model.md §1).
    """

    __tablename__ = "behavior_judgments"

    id: Mapped[uuid.UUID] = _uuid_pk()
    social_event_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("social_events.id", ondelete="CASCADE"),
        nullable=False,
    )
    criteria_version: Mapped[str] = mapped_column(Text, nullable=False)
    prompt_version: Mapped[str] = mapped_column(Text, nullable=False)
    model_name: Mapped[str] = mapped_column(Text, nullable=False)
    transcript_version: Mapped[int] = mapped_column(Integer, nullable=False)
    supersedes_judgment_id: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("behavior_judgments.id", ondelete="CASCADE"),
        nullable=True,
    )
    needs_review: Mapped[bool] = mapped_column(nullable=False, server_default="false")


class Evidence(Base):
    """U1 이 적는 것: 판정 참조, 발화 참조."""

    __tablename__ = "evidences"

    id: Mapped[uuid.UUID] = _uuid_pk()
    judgment_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("behavior_judgments.id", ondelete="CASCADE"),
        nullable=False,
    )
    utterance_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("utterances.id", ondelete="CASCADE"),
        nullable=False,
    )


class AnalysisFeedback(Base):
    """U1 이 적는 것: 대화 참조, 남긴 시각."""

    __tablename__ = "analysis_feedbacks"

    id: Mapped[uuid.UUID] = _uuid_pk()
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


# ---------------------------------------------------------------------------
# training — goals / recommendations / scenarios / sessions / attempts / hints
# ---------------------------------------------------------------------------
class TrainingGoal(Base):
    """U1 이 적는 것: 사용자 참조.

    `source_event_id`·`source_judgment_id` 는 **CASCADE 로 지우지 않는다** — 앱이 비운다
    (ADR-006, 계약 C13 의 `goal_disposition="KEEP"`).
    """

    __tablename__ = "training_goals"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    source_event_id: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("social_events.id"), nullable=True
    )
    source_judgment_id: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("behavior_judgments.id"), nullable=True
    )


class Recommendation(Base):
    """U1 이 적는 것: 사용자 참조."""

    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


class ScenarioTemplate(Base):
    """U1 이 적는 것: 시드 원형이 들어갈 자리.

    식별자는 `tpl_repair_person_01` 처럼 사람이 읽는 키다
    (docs/input/05_synthetic-test-data.md).
    제목·상황·상대 역할 등 내용 컬럼은 u7-f05-practice 가 더한다.
    """

    __tablename__ = "scenario_templates"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)


class ScenarioVariant(Base):
    """U1 이 적는 것: 원형 참조. 가변 구조(변형 규칙)는 JSONB 다 (계약 C15)."""

    __tablename__ = "scenario_variants"

    id: Mapped[uuid.UUID] = _uuid_pk()
    template_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("scenario_templates.id", ondelete="CASCADE"),
        nullable=False,
    )
    variation_rules: Mapped[dict] = mapped_column(
        JSONB, nullable=False, server_default="{}"
    )


class PracticeSession(Base):
    """U1 이 적는 것: 사용자 참조, 목표 참조."""

    __tablename__ = "practice_sessions"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    goal_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("training_goals.id", ondelete="CASCADE"),
        nullable=False,
    )


class Attempt(Base):
    """U1 이 적는 것: 세션 참조, 시도 순번."""

    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = _uuid_pk()
    session_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("practice_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    attempt_order: Mapped[int] = mapped_column(Integer, nullable=False)


class HintEvent(Base):
    """U1 이 적는 것: 시도 참조."""

    __tablename__ = "hint_events"

    id: Mapped[uuid.UUID] = _uuid_pk()
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("attempts.id", ondelete="CASCADE"),
        nullable=False,
    )


# ---------------------------------------------------------------------------
# privacy — deletion_requests / sharing_settings
# ---------------------------------------------------------------------------
class DeletionRequest(Base):
    """U1 이 적는 것: 사용자 참조, 지울 파일 경로 목록, 일부 완료 상태 (ADR-006).

    삭제는 지울 파일 경로를 **먼저 기록**하고, 한 트랜잭션에서 DB 행을 지워 커밋한 뒤
    파일을
    지운다. 실패한 파일 경로는 `PARTIAL` 로 남겨 다시 삭제 요청 때 지운다.
    """

    __tablename__ = "deletion_requests"
    __table_args__ = (
        _enum_check("status", DELETION_REQUEST_STATUSES, "ck_deletion_requests_status"),
    )

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    pending_file_paths: Mapped[list] = mapped_column(
        JSONB, nullable=False, server_default="[]"
    )
    status: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="REQUESTED"
    )


class SharingSetting(Base):
    """U1 이 적는 것: 사용자 참조, `level` 허용값 NONE / SUMMARY / FULL, 기본 NONE
    (FR11.2).
    """

    __tablename__ = "sharing_settings"
    __table_args__ = (
        _enum_check("level", SHARING_LEVELS, "ck_sharing_settings_level"),
    )

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    level: Mapped[str] = mapped_column(Text, nullable=False, server_default="NONE")


#: 초기 리비전이 만드는 테이블 20개. 시험이 이 목록을 그대로 대조한다.
INITIAL_TABLES: tuple[str, ...] = (
    "users",
    "guardian_invitations",
    "conversations",
    "audio_assets",
    "utterances",
    "corrections",
    "context_infos",
    "social_events",
    "behavior_judgments",
    "evidences",
    "analysis_feedbacks",
    "training_goals",
    "recommendations",
    "scenario_templates",
    "scenario_variants",
    "practice_sessions",
    "attempts",
    "hint_events",
    "deletion_requests",
    "sharing_settings",
)
