"""초기 스키마가 구조로 지키는 것들.

기술적·배관 동작을 검증하므로 시험 이름은 영어다 (team.md § Code Style).
"""

from __future__ import annotations

import importlib
import pkgutil

import pytest
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.types import _Binary

from app.repository.models import Base

#: 종합점수·백분위를 뜻하는 이름 조각 (TC-13)
FORBIDDEN_FIELD_FRAGMENTS = ("score", "percentile", "grade", "ranking")


@pytest.mark.ac("AC9.2.1")
def test_no_table_stores_audio_bytes() -> None:
    """TC-05·BR8.2 — 음성 본문을 넣을 수 있는 컬럼이 어느 테이블에도 없다."""
    binary_columns = [
        f"{table.name}.{column.name}"
        for table in Base.metadata.tables.values()
        for column in table.columns
        if isinstance(column.type, LargeBinary | BYTEA | _Binary)
    ]
    assert binary_columns == [], f"음성 본문이 들어갈 수 있는 컬럼: {binary_columns}"

    audio = Base.metadata.tables["audio_assets"]
    assert set(audio.columns.keys()) == {
        "id",
        "conversation_id",
    }, "audio_assets 는 대화 참조만 가진다 — 메타데이터 컬럼은 u3-f01-capture 가 더한다"


def test_judgment_provenance_columns_are_not_nullable() -> None:
    """TC-10 — 출처 네 값은 스키마 제약으로 함께 저장된다."""
    judgments = Base.metadata.tables["behavior_judgments"]
    provenance = (
        "criteria_version",
        "prompt_version",
        "model_name",
        "transcript_version",
    )

    for name in provenance:
        assert name in judgments.columns, f"출처 컬럼 {name} 이 없다"
        assert (
            judgments.columns[name].nullable is False
        ), f"출처 컬럼 {name} 이 NULL 을 허용한다 — 스키마 제약이 되어 있지 않다"


def test_no_score_or_percentile_field_anywhere() -> None:
    """TC-13 — 저장 컬럼에도 API 응답 모델에도 종합점수·백분위 자리가 없다."""
    offenders = [
        f"{table.name}.{column.name}"
        for table in Base.metadata.tables.values()
        for column in table.columns
        if any(
            fragment in column.name.lower() for fragment in FORBIDDEN_FIELD_FRAGMENTS
        )
    ]

    from pydantic import BaseModel

    import app.api

    for module_info in pkgutil.walk_packages(app.api.__path__, "app.api."):
        module = importlib.import_module(module_info.name)
        for attribute in vars(module).values():
            if isinstance(attribute, type) and issubclass(attribute, BaseModel):
                offenders += [
                    f"{attribute.__name__}.{field}"
                    for field in attribute.model_fields
                    if any(f in field.lower() for f in FORBIDDEN_FIELD_FRAGMENTS)
                ]

    assert offenders == [], f"종합점수·백분위로 읽히는 자리: {offenders}"
