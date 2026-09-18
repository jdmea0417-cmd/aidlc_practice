#!/usr/bin/env bash
# 스키마 적용 — **기동 흐름 밖의 별도 단계**다 (functional-spec.md W1).
# 기동마다 적용하면 컨테이너가 동시에 뜰 때 경쟁이 생기고, 전진 방향만 쓰기로 한 관행과도
# 결이 맞지 않는다.
#
#   docker compose run --rm backend scripts/migrate.sh
set -euo pipefail
cd "$(dirname "$0")/.."
uv run alembic upgrade head
echo "마이그레이션을 적용했다"
