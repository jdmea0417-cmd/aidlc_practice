"""프롬프트 로더 — 파일 이름이 식별자와 버전의 기준이다 (TC-10).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.prompts.loader import PROMPT_DIR, load_prompt, split_prompt_name


def test_id_and_version_come_from_the_file_name() -> None:
    assert split_prompt_name("assess_v1") == ("assess", "v1")

    prompt = load_prompt("assess_v1")
    assert (prompt.prompt_id, prompt.version) == ("assess", "v1")
    assert prompt.text.strip(), "프롬프트 본문이 비어 있다"


def test_prompt_dir_is_resolved_relative_to_the_module() -> None:
    """작업 디렉터리가 어디든 같은 파일을 읽는다."""
    assert Path(__file__).resolve().parents[2] / "app" / "prompts" == PROMPT_DIR
    assert (PROMPT_DIR / "assess_v1.md").is_file()


def test_missing_prompt_file_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_prompt("does_not_exist_v9")


def test_prompt_file_is_read_only_once() -> None:
    first = load_prompt("assess_v1")
    second = load_prompt("assess_v1")
    assert first is second, "호출마다 디스크를 읽고 있다"
