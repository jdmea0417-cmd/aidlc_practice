"""프롬프트 로더 — 파일 이름에서 식별자와 버전을 뽑는다 (team.md § Code Style, TC-10).

코드가 버전 문자열을 따로 들고 있으면 저장하는 값과 어긋난다. 파일 이름이 기준이다.
모듈 기준 상대 경로로 읽고, 한 번 읽어 재사용한다 (performance-design.md §3).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Prompt:
    """프롬프트 하나. 식별자와 버전은 파일 이름에서 나온다."""

    prompt_id: str
    version: str
    text: str


def split_prompt_name(file_stem: str) -> tuple[str, str]:
    """`assess_v1` -> `("assess", "v1")`."""
    prompt_id, separator, version = file_stem.rpartition("_")
    if not separator or not version.startswith("v") or not version[1:].isdigit():
        raise ValueError(
            f"프롬프트 파일 이름이 `<식별자>_v<번호>` 모양이 아니다: {file_stem!r}"
        )
    return prompt_id, version


@cache
def load_prompt(file_stem: str) -> Prompt:
    """프롬프트 파일을 읽는다.

    없는 파일은 오류다 — 조용히 빈 프롬프트를 만들지 않는다.
    """
    path = PROMPT_DIR / f"{file_stem}.md"
    if not path.is_file():
        raise FileNotFoundError(f"프롬프트 파일이 없다: {path}")
    prompt_id, version = split_prompt_name(file_stem)
    return Prompt(
        prompt_id=prompt_id, version=version, text=path.read_text(encoding="utf-8")
    )
