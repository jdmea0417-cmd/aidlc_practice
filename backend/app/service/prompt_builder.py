"""프롬프트 조립 — 전사를 데이터 블록 안에만 넣는다 (TC-08, security-design.md §3.1).

TC-08 은 Mock 경로에서 살아남는 유일한 보안 속성이다. Mock 은 전사를 읽지 않으므로
시연이
통과해도 이 속성이 지켜졌다는 증거가 되지 않는다. 그래서 **구조와 시험 둘 다로** 지킨다.

구조:
- 전사는 구분자로 감싼 데이터 블록 **안에만** 들어간다.
- 넣기 전에 구분자를 만들 수 있는 문자(`<`, `>`)를 이스케이프한다. 데이터가 구분자를
포함할
  수 있으면 그 구분자는 경계가 아니다.
- 지시문 영역은 **하나뿐**이고 데이터 블록 뒤에 다시 열리지 않는다.
- 조립 함수는 전사를 인자로 받는 **순수 함수**다 — 외부 호출 없이 결과만 검사할 수 있다.
"""

from __future__ import annotations

from app.service.ports import ContextView, TranscriptBlock

#: 데이터 블록 구분자. 이 문자열은 조립 결과에 각각 정확히 한 번씩만 나타난다.
DATA_BLOCK_BEGIN = "<<<TRANSCRIPT_DATA_BEGIN>>>"
DATA_BLOCK_END = "<<<TRANSCRIPT_DATA_END>>>"

#: 프롬프트 파일에서 데이터 블록이 들어갈 자리
DATA_BLOCK_PLACEHOLDER = "{{TRANSCRIPT_DATA_BLOCK}}"


def escape_for_data_block(text: str) -> str:
    """구분자를 만들 수 있는 문자를 이스케이프한다.

    `<` 와 `>` 를 막으면 자료가 어떤 문자열이든 구분자를 흉내 낼 수 없다. 구분자의
    일부만
    지우는 방식은 조각을 이어 붙여 되살릴 수 있어 쓰지 않는다.
    """
    return text.replace("\\", "\\\\").replace("<", "\\<").replace(">", "\\>")


def render_data_block(
    transcript_block: TranscriptBlock, context: ContextView | None = None
) -> str:
    """맥락과 전사를 데이터 블록 하나로 만든다. 둘 다 신뢰하지 않는 자료다."""
    lines: list[str] = [DATA_BLOCK_BEGIN]

    if context is not None:
        lines.append("[맥락]")
        for label, value in (
            ("관계", context.relation),
            ("장소", context.place),
            ("목적", context.purpose),
            ("사용자 목표", context.user_goal),
        ):
            rendered = escape_for_data_block(value) if value else "미상"
            lines.append(f"{label}: {rendered}")

    lines.append("[발화]")
    for utterance in transcript_block.utterances:
        unclear_mark = " (불명확)" if utterance.unclear else ""
        lines.append(
            f"{escape_for_data_block(utterance.id)} | "
            f"{escape_for_data_block(utterance.speaker)} | "
            f"{escape_for_data_block(utterance.text)}{unclear_mark}"
        )

    lines.append(DATA_BLOCK_END)
    return "\n".join(lines)


def build_assessment_prompt(
    *,
    prompt_text: str,
    transcript_block: TranscriptBlock,
    context: ContextView | None = None,
) -> str:
    """지시문 하나 + 데이터 블록 하나. 그 뒤에는 아무것도 열리지 않는다."""
    if DATA_BLOCK_PLACEHOLDER not in prompt_text:
        raise ValueError(
            f"프롬프트에 데이터 블록 자리가 없다: {DATA_BLOCK_PLACEHOLDER}"
        )
    if prompt_text.count(DATA_BLOCK_PLACEHOLDER) > 1:
        raise ValueError(
            "데이터 블록 자리가 둘 이상이다 — 지시문 영역은 하나뿐이어야 한다"
        )

    rendered = prompt_text.replace(
        DATA_BLOCK_PLACEHOLDER, render_data_block(transcript_block, context)
    )
    return rendered.rstrip() + "\n"
