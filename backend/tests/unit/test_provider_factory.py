"""제공자 선택 — 결정된 모드의 객체만 만든다 (NFR5.3, security-design.md §1.2).

기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from app.config import Settings
from app.providers.factory import build_providers
from app.providers.llm_mock import MockLlmProvider
from app.providers.stt_mock import MockSttProvider

BACKEND_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.ac("AC9.1.2")
def test_mock_mode_builds_only_mock_providers() -> None:
    providers = build_providers("mock", Settings())

    assert isinstance(providers.stt, MockSttProvider)
    assert isinstance(providers.llm, MockLlmProvider)
    assert providers.mode == "mock"


def test_live_mode_builds_live_providers() -> None:
    settings = Settings(analysis_mode="live", stt_api_key="키1", llm_api_key="키2")

    providers = build_providers("live", settings)

    assert type(providers.stt).__name__ == "LiveSttProvider"
    assert type(providers.llm).__name__ == "LiveLlmProvider"


@pytest.mark.ac("AC9.1.2")
def test_mock_mode_never_imports_live_modules() -> None:
    """mock 으로 뜬 프로세스 안에는 외부로 나가는 경로를 가진 객체가 없다.

    같은 프로세스에서는 다른 시험이 이미 live 를 불러왔을 수 있으므로 새 프로세스에서
    본다.
    """
    script = (
        "import sys;"
        "from app.config import Settings;"
        "from app.providers.factory import build_providers;"
        "build_providers('mock', Settings());"
        "print([m for m in sys.modules if m.endswith('_live')])"
    )
    completed = subprocess.run(  # noqa: S603 - 인자를 고정한 자기 해석기 호출이다
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        cwd=BACKEND_ROOT,
        check=True,
    )

    assert (
        completed.stdout.strip() == "[]"
    ), f"mock 모드인데 live 구현이 불러와졌다: {completed.stdout.strip()}"


def test_ports_live_in_the_service_layer_not_in_providers() -> None:
    """인터페이스가 구현체와 같은 패키지에 있으면 service 가
    providers 를 import 하게 된다.
    """
    assert (BACKEND_ROOT / "app" / "service" / "ports.py").is_file()
    assert not (BACKEND_ROOT / "app" / "providers" / "ports.py").exists()

    providers_init = (BACKEND_ROOT / "app" / "providers" / "__init__.py").read_text(
        encoding="utf-8"
    )
    assert (
        "import" not in providers_init
    ), "providers 패키지가 구현체를 재노출하면 mock 모드에서 live 가 딸려 들어온다"
