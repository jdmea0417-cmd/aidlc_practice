#!/usr/bin/env bash
# 느린 검사 — 빠른 검사 + 실제 저장소를 띄우는 통합 시험.
#
#   docker compose run --rm backend scripts/check-full.sh
#
# 통합 시험은 Testcontainers 로 PostgreSQL 16 을 띄운다. Docker 를 쓸 수 없는 자리에서는
# TEST_DATABASE_URL 로 이미 떠 있는 저장소를 가리킬 수 있다.
set -euo pipefail
cd "$(dirname "$0")/.."

scripts/check.sh

echo "== pytest (통합) =="
uv run pytest -m integration

echo "전체 검사를 통과했다"
