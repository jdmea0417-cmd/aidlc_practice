# uv 버전을 태그로 고정한다 — 컨테이너와 로컬이 같은 방식으로 설치되게 한다 (team.md Code Style)
FROM ghcr.io/astral-sh/uv:0.5.11-python3.11-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 잠금 파일에서만 설치한다. 매니페스트와 잠금이 같은 커밋에 들어간다.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen

EXPOSE 8000

# 스키마 적용은 기동 흐름에 넣지 않는다 — scripts/migrate.sh 가 별도 단계로 돌린다 (functional-spec W1)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
