"""계층 경계 — 사람이 아니라 검사가 지킨다 (TC-14, security-design.md §2).

`api` -> `service` -> `repository` 순으로만 내려간다. 역방향은 없다.
기술적 동작이므로 시험 이름은 영어다.
"""

from __future__ import annotations

import ast
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = BACKEND_ROOT / "app"


def _imported_modules(path: Path) -> set[str]:
    """그 파일이 실제로 import 하는 모듈 이름. 주석과 문자열은 세지 않는다."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _offenders(package: str, forbidden: tuple[str, ...]) -> list[str]:
    return [
        f"{path.relative_to(BACKEND_ROOT)} -> {name}"
        for path in (APP_ROOT / package).rglob("*.py")
        for name in _imported_modules(path)
        if any(name == bad or name.startswith(f"{bad}.") for bad in forbidden)
    ]


def test_api_never_imports_repository() -> None:
    """영속성 접근은 반드시 service 를 경유한다.

    건너뛰면 삭제 전파와 권한 검사가 빠진다.
    """
    assert _offenders("api", ("app.repository",)) == []


def test_service_never_imports_fastapi() -> None:
    """특히 `HTTPException` 을 service 에서 던지지 않는다."""
    assert _offenders("service", ("fastapi", "starlette")) == []


def test_providers_never_import_domain_or_http_tools() -> None:
    """어댑터는 도메인을 모르고, HTTP 도구는 감싸기 장치에서 받는다."""
    assert (
        _offenders("providers", ("app.service.account", "app.repository", "httpx"))
        == []
    )

    # 인터페이스와 DTO 만 service 에서 가져온다 — 업무 로직은 가져오지 않는다.
    allowed_service_imports = {"app.service.ports"}
    service_imports = {
        name
        for path in (APP_ROOT / "providers").rglob("*.py")
        for name in _imported_modules(path)
        if name.startswith("app.service")
    }
    assert (
        service_imports <= allowed_service_imports
    ), f"providers 가 업무 모듈을 가져온다: {service_imports - allowed_service_imports}"
