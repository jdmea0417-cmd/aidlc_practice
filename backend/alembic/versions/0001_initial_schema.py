"""초기 스키마 — 엔티티 20개 테이블 (계약 C15, D-102).

이 리비전은 모델 정의에서 뽑은 초안을 사람이 읽고 고친 것이다. `--autogenerate` 가
놓치는
자리를 두 군데 고쳤다 — 문자열 기본값이 식별자로 렌더링되는 것과 `now()` 가 문자열
리터럴로
굳는 것이다 (team.md § Deployment).

전진 방향만 쓴다. `downgrade` 스크립트를 두지 않는다 — 로컬 초기화(`docker compose down
-v`)가
더 싸고, 쓰지 않을 코드에 시험을 붙이게 되기 때문이다.

Revision ID: 0001_initial_schema
Revises:
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scenario_templates",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=False),
        sa.Column("role", sa.Text(), server_default="USER", nullable=False),
        sa.Column("age_band", sa.Text(), nullable=True),
        sa.Column("language_background", sa.Text(), nullable=True),
        sa.Column("consented_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "display_name <> ''",
            name="ck_users_display_name_not_empty",
        ),
        sa.CheckConstraint(
            "role IN ('USER', 'GUARDIAN')",
            name="ck_users_role",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "conversations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "transcript_status", sa.Text(), server_default="UPLOADING", nullable=False
        ),
        sa.Column("transcript_failure_reason", sa.Text(), nullable=True),
        sa.Column(
            "analysis_status", sa.Text(), server_default="NOT_ANALYZED", nullable=False
        ),
        sa.Column(
            "transcript_version", sa.Integer(), server_default="1", nullable=False
        ),
        sa.Column("conversation_key", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "analysis_status = 'NOT_ANALYZED' OR transcript_status = 'TRANSCRIBED'",
            name="ck_conversations_analysis_requires_transcript",
        ),
        sa.CheckConstraint(
            "analysis_status IN "
            "('NOT_ANALYZED', 'ANALYZING', 'ANALYZED', 'ANALYZE_FAILED')",
            name="ck_conversations_analysis_status",
        ),
        sa.CheckConstraint(
            "(transcript_status = 'TRANSCRIBE_FAILED') = "
            "(transcript_failure_reason IS NOT NULL)",
            name="ck_conversations_failure_reason_only_when_failed",
        ),
        sa.CheckConstraint(
            "transcript_failure_reason IS NULL OR "
            "transcript_failure_reason IN ('STORAGE', 'TRANSCRIPTION')",
            name="ck_conversations_transcript_failure_reason",
        ),
        sa.CheckConstraint(
            "transcript_status IN "
            "('UPLOADING', 'TRANSCRIBING', 'TRANSCRIBED', 'TRANSCRIBE_FAILED')",
            name="ck_conversations_transcript_status",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "deletion_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "pending_file_paths",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default="[]",
            nullable=False,
        ),
        sa.Column("status", sa.Text(), server_default="REQUESTED", nullable=False),
        sa.CheckConstraint(
            "status IN ('REQUESTED', 'DONE', 'PARTIAL')",
            name="ck_deletion_requests_status",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "guardian_invitations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("invitation_code", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("invitation_code"),
    )
    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "scenario_variants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("template_id", sa.String(length=64), nullable=False),
        sa.Column(
            "variation_rules",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["template_id"], ["scenario_templates.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sharing_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("level", sa.Text(), server_default="NONE", nullable=False),
        sa.CheckConstraint(
            "level IN ('NONE', 'SUMMARY', 'FULL')",
            name="ck_sharing_settings_level",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "analysis_feedbacks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["conversation_id"], ["conversations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "audio_assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversation_id"], ["conversations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "context_infos",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("relation_value", sa.Text(), nullable=True),
        sa.Column(
            "relation_status", sa.Text(), server_default="UNKNOWN", nullable=False
        ),
        sa.Column("place_value", sa.Text(), nullable=True),
        sa.Column("place_status", sa.Text(), server_default="UNKNOWN", nullable=False),
        sa.Column("purpose_value", sa.Text(), nullable=True),
        sa.Column(
            "purpose_status", sa.Text(), server_default="UNKNOWN", nullable=False
        ),
        sa.Column("user_goal_value", sa.Text(), nullable=True),
        sa.Column(
            "user_goal_status", sa.Text(), server_default="UNKNOWN", nullable=False
        ),
        sa.CheckConstraint(
            "place_status IN ('CONFIRMED', 'USER_REPORTED', 'UNKNOWN')",
            name="ck_context_infos_place_status",
        ),
        sa.CheckConstraint(
            "purpose_status IN ('CONFIRMED', 'USER_REPORTED', 'UNKNOWN')",
            name="ck_context_infos_purpose_status",
        ),
        sa.CheckConstraint(
            "relation_status IN ('CONFIRMED', 'USER_REPORTED', 'UNKNOWN')",
            name="ck_context_infos_relation_status",
        ),
        sa.CheckConstraint(
            "user_goal_status IN ('CONFIRMED', 'USER_REPORTED', 'UNKNOWN')",
            name="ck_context_infos_user_goal_status",
        ),
        sa.ForeignKeyConstraint(
            ["conversation_id"], ["conversations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("conversation_id"),
    )
    op.create_table(
        "social_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversation_id"], ["conversations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "utterances",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("utterance_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversation_id"], ["conversations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "behavior_judgments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("social_event_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("criteria_version", sa.Text(), nullable=False),
        sa.Column("prompt_version", sa.Text(), nullable=False),
        sa.Column("model_name", sa.Text(), nullable=False),
        sa.Column("transcript_version", sa.Integer(), nullable=False),
        sa.Column(
            "supersedes_judgment_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column("needs_review", sa.Boolean(), server_default="false", nullable=False),
        sa.ForeignKeyConstraint(
            ["social_event_id"], ["social_events.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["supersedes_judgment_id"], ["behavior_judgments.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "corrections",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("utterance_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["utterance_id"], ["utterances.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "evidences",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("judgment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("utterance_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["judgment_id"], ["behavior_judgments.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["utterance_id"], ["utterances.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "training_goals",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_event_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source_judgment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["source_event_id"], ["social_events.id"]),
        sa.ForeignKeyConstraint(["source_judgment_id"], ["behavior_judgments.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "practice_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("goal_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["goal_id"], ["training_goals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("attempt_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"], ["practice_sessions.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "hint_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["attempt_id"], ["attempts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # 전진 방향만 쓴다 (team.md § Deployment). 초기화는 볼륨을 비우는 것으로 한다.
    raise NotImplementedError("이 프로젝트는 되돌리기 마이그레이션을 쓰지 않는다")
