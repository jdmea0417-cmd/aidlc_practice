#!/usr/bin/env bash
# 빠른 검사 — **컨테이너 안에서 돈다**. 5인의 로컬 Python 버전이 제각각인데 호스트에서
# 돌리면 "내 자리에선 통과했다"가 분쟁이 된다 (team.md § Testing Posture).
#
#   docker compose run --rm backend scripts/check.sh
#
# 이것은 개발자 편의 수단이지 병합 게이트가 아니다. 병합 전 강제 수단은 GitHub Actions 이고,
# 그 워크플로는 ci-pipeline(3.7)이 만든다.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== ruff =="
uv run ruff check .
uv run ruff format --check .

echo "== mypy =="
uv run mypy app scripts

echo "== pytest (단위) =="
uv run pytest -m "not integration and not e2e"

echo "빠른 검사를 통과했다"
