# Code Summary — u1-backend-foundation

**Stage**: code-generation (3.5) · **Unit**: u1-backend-foundation (U1 백엔드 기반)
**작성일**: 2026-09-18 · **방법론**: test-after (승인된 Testing Contract
`sha256:00847776538d2675b246a4641aebe46517d03fe33e6024b7b717595a353ff951`)

## Sources

| 태그 | 출처 |
|---|---|
| `[plan]` | `code-generation-plan.md` — 승인된 Step 1~12 |
| `[tests]` | `unit-test-instructions.md` — 시험 범위와 기준 명령 |
| `[spec]` | `../functional-design/functional-spec.md` — W1~W6, SM-A~SM-C |
| `[entities]` | `../functional-design/entities.md` — §1 `User`, §3 경계표, §4 상태 두 컬럼 |
| `[rules]` | `../functional-design/rules.md` — BR1.1~BR8.2 |
| `[design]` | `../nfr-design/` — security·observability·reliability·performance |
| `[nfr]` | `../nfr-requirements/tech-stack-decisions.md` — §1 기술 선택, §3 설정값, §5 NFR14.x |
| `[infra]` | `../infrastructure-design/infrastructure-specification.md` — §1·§2·§2.1·§4 |
| `[contract]` | `.../inception/contract-design/contract-summary.md` — 공통 규칙, C1, C14, C15, C16 |
| `[practices]` | `aidlc/spaces/default/memory/team.md`, `project.md` |

---

## 1. 만든 것 — 무엇이 어디에 있는가

응용 코드는 전부 저장소 루트에 썼다. 전체 경로 목록은 `source-manifest.json` 에 있다
(파일 100개).

| 자리 | 파일 | 무엇 |
|---|---|---|
| 프로젝트 | `backend/pyproject.toml`, `backend/uv.lock` | uv 프로젝트, Ruff·mypy·pytest 설정 한 파일 |
| 실행 | `backend/Dockerfile`, `docker-compose.yml` | uv 로 설치(태그 고정), backend·postgres 두 서비스 |
| 설정 | `backend/app/config.py` | 설정값 전부 + **분석 모드 결정 한 곳** |
| 공통 | `backend/app/common/` | 로그·식별자 문맥·예외·작업 단위 장치·제공자 호출 감싸기·미들웨어·오류 처리기 |
| 포트 | `backend/app/service/ports.py` | `SttProvider`/`LlmProvider` Protocol 과 DTO 7종 (계약 C14) |
| 어댑터 | `backend/app/providers/` | Mock 둘, live 뼈대 둘, factory |
| 픽스처 | `backend/app/fixtures/` | 합성 대화 3건 + 로더 + 시드 사용자 상수 |
| 프롬프트 | `backend/app/prompts/` | `assess_v1.md` + 로더 (버전은 파일 이름에서) |
| 조립기 | `backend/app/service/prompt_builder.py` | 전사를 데이터 블록 안에만 넣는 순수 함수 |
| 저장소 | `backend/app/repository/models.py`, `backend/alembic/` | 테이블 20개, 초기 리비전 하나 |
| 업무 | `backend/app/service/` | `current_user`, `account`, `health` |
| API | `backend/app/api/` | `GET /api/v1/health`, `GET /api/v1/me`, `POST /api/v1/me/consent` |
| 앱 | `backend/app/main.py` | 기동 흐름 W1 조립 |
| 도구 | `backend/scripts/` | `seed.py`, `migrate.sh`, `check.sh`, `check-full.sh` |
| 시험 | `backend/tests/` | 단위 17파일, 통합 6파일 |

`api/`·`service/`·`repository/` 는 **업무 이름 6개**(`conversation`, `assessment`,
`training`, `record`, `account`, `privacy`)로 나눴다 — 팀 관행의 5개가 아니라 도메인 설계
D-83 의 6개다 `[practices]` project.md.

---

## 2. 주요 구현 결정과 근거

### 2.1 전사가 밖으로 나갈 수 없게 하는 구조

| 결정 | 근거 |
|---|---|
| 분석 모드 결정을 `config.py` 한 함수에 모으고, `factory.py` 가 **결정된 모드의 객체만** 만든다. live 구현은 함수 안에서 import 한다 | mock 으로 뜬 프로세스 안에는 외부로 나가는 경로를 가진 객체가 없다. `test_provider_factory.py` 가 **새 프로세스**에서 `*_live` 모듈이 안 불러와졌는지 확인한다 `[design]` security §1.2 |
| 감싸기 장치가 HTTP 클라이언트를 만들어 **어댑터에 인자로 준다** | 어댑터가 HTTP 도구를 직접 import 하지 못한다 → "반드시 이 장치를 거친다"가 검사가 된다. 설계가 린터 규칙으로 표현하려던 것을 구조로 바꿨다 (§5 참고) |
| 프롬프트 조립기가 데이터 블록 안에서 `<`·`>` 를 **이스케이프**한다 | 구분자의 일부만 지우면 조각을 이어 붙여 되살릴 수 있다. 두 문자를 막으면 자료가 어떤 문자열이든 구분자를 흉내 낼 수 없다 (TC-08) |
| 로거가 전사로 읽히는 **필드 이름을 거부**하고 예외 객체를 통째로 받지 않는다 | "남기지 않는다"를 사람의 주의력이 아니라 예외로 만든다. 진단 수준에서도 같다 (BR6.3) |

### 2.2 실패가 사라질 수 없는 구조

`app/common/unit_of_work.py` 가 `[design]` reliability §2 의 순서를 그대로 구현한다 —
성공이면 한 번 확정, 예외면 되돌리고 닫은 뒤 **별도 연결**로 실패를 적고, 그 기록마저 실패하면
로그만 남기고 넘어간다. 작업 함수는 장치가 연 세션만 받는다(요청 세션이 흘러들어올 자리가
없다). 예약 수단은 웹 프레임워크의 기본 배경 작업이다 — 새 의존성 0 `[Q1]`.

### 2.3 스키마 — 확정된 것만 적었다

`users` 만 속성 전체를 적고, 나머지 19개는 `[entities]` §3 의 "U1 이 지금 적는 것" 칸만 적었다
(BR8.1). 추측해 적지 않은 결과로 여러 테이블이 참조 컬럼만 가진다 — 소유 단위가 자기 리비전으로
더한다.

구조로 바꾼 자리 셋:

- `conversations` 에 **검사 제약**을 걸어 `analysis_status` 가 `NOT_ANALYZED` 가 아니면
  `transcript_status` 가 `TRANSCRIBED` 여야 하게 했다 (BR7.1). 말이 되지 않는 조합이 저장될 수
  없다.
- 전사 실패 사유는 `TRANSCRIBE_FAILED` 일 때만 값을 가진다 `[entities]` §4.
- `behavior_judgments` 의 출처 네 컬럼이 `NOT NULL` 이다 (TC-10) — "함께 저장한다"가 스키마
  제약이다.

마이그레이션은 모델에서 뽑은 초안을 사람이 읽고 고쳤다. 초안이 틀렸던 자리 둘: 문자열 기본값이
식별자로 렌더링되는 것과 `now()` 가 문자열 리터럴로 굳는 것. 둘 다 `[practices]` Deployment 가
"autogenerate 는 초안이다"라고 경고한 그 종류다.

### 2.4 이번 단계가 정한 값

| 값 | 정한 것 | 근거 |
|---|---|---|
| 업로드 최대 크기 기본값 | 26,214,400 바이트(25MiB) | `[nfr]` §3 이 "설정값"이라고만 정했다. 5분짜리 webm/opus 에 여유를 둔 값이며 **설정으로만** 산다 — 시험이 값을 바꿔 확인한다 |
| 오류 봉투의 503 | 헬스체크 실패는 `STORAGE_UNAVAILABLE` 코드로 503 을 낸다 | 계약 C1 은 200 만 적었고 컨테이너 확인은 2xx 가 아니어야 실패로 읽는다. 예외 6종을 늘리지 않고 봉투 생성기만 직접 썼다 |
| 검증 실패 사유 문구 | 종류별 한국어 문구 표 | `[design]` security §4.1 이 `reason` 을 한국어로 정했고 문구 자체는 비어 있었다 |

---

## 3. 시험 범위와 실행 결과

**전부 실제로 돌렸다.** 실행 방법은 §4 에 적은 대로다.

| 묶음 | 개수 | 결과 |
|---|---|---|
| 단위 (`-m "not integration and not e2e"`) | 83 | 전부 통과 |
| 통합 (`-m integration`, 실제 PostgreSQL 16) | 21 | 전부 통과 |
| 합계 | **104** | 전부 통과 |

| 품질 목표 | 값 | 결과 |
|---|---|---|
| `backend/app/service/` 라인 커버리지 | 80% 이상 | **99%** (124줄 중 1줄 미도달) |
| 세 엔드포인트 응답 시간 | 200ms (p95) | 통합 시험의 경과 시간 단언 3건 통과 |
| 린터 위반 | 0건 (`E,F,I,UP,B,SIM,TID,RUF,S`) | **0건** (`ruff format --check` 도 통과) |
| 타입 오류 | 0건, `app.service.*` 는 타입 필수 | **0건** (57파일) |

계획이 이름을 적은 시험 파일과 개수를 그대로 만들었다. 추가로 확인한 것 둘:

- **연결 누수 감시** — 시험 세션이 끝난 뒤 저장소에 남은 연결이 풀 크기 5를 넘으면 실패한다
  (`tests/conftest.py`의 `connection_leak_guard`). 계획 Step 10 의 마지막 항목이다.
- **픽스처 중복 감시** — 픽스처의 전사 문장이 코드나 시험에 옮겨 적혀 있으면 실패한다
  (`test_fixture_loader.py`). 실제로 이 검사가 작성 중 옮겨 적은 한 줄을 잡아냈다.

---

## 4. 어떻게 돌렸는가 — 그리고 무엇을 못 돌렸는가

**기준 명령은 컨테이너 안에서 도는 것이다**(`docker compose run --rm backend ...`)
`[tests]` §2. **이 작업 환경에는 Docker 가 없어서 기준 명령을 그대로 돌리지 못했다.**

```
$ docker --version
The command 'docker' could not be found in this WSL 2 distro.
$ docker info      # 데몬 없음
```

그래서 `[tests]` §2 가 함께 적어 둔 **호스트 실행 형태**로 돌렸다. 호스트에는 Python 이 3.14
하나뿐이고 `pip`·`venv` 도 없어서, 팀이 고른 패키지 관리자 `uv` 를 설치해 `uv` 가 Python
3.11.16 을 받아 쓰게 했다(프로젝트가 `requires-python = ">=3.11,<3.12"` 로 고정한 그 버전이다).

```
$ cd backend && uv run pytest -m "not integration and not e2e" <파일 17개>   # 83 passed
$ cd backend && uv run pytest -m integration <파일 6개>                      # 21 passed
$ uv run ruff check . && uv run ruff format --check .                       # All checks passed
$ uv run mypy app scripts                                                   # Success: 57 files
$ uv run pytest --cov=app/service                                           # 99%
```

통합 시험의 저장소도 Testcontainers 를 쓰지 못했다(같은 이유). 대신 **실제 PostgreSQL 16** 을
로컬 소켓으로 띄우고 `TEST_DATABASE_URL` 로 가리켰다 — 이 갈림은 `tests/conftest.py` 가 원래
지원하는 경로이며, 저장소를 만지는 시험이 가짜로 대체되지 않았다는 뜻이다. 실제로 확인된 것:
마이그레이션이 테이블 20개를 만들고, 기동이 마이그레이션을 돌리지 않으며, 세 엔드포인트가
실제 저장소를 상대로 응답한다.

**Docker 위에서 다시 확인해야 하는 것 셋** — 이 환경에서는 검증하지 못했다:

1. `docker compose up --build` 로 두 컨테이너가 뜨고 헬스체크가 통과하는지 (AC9.1.1 의 절반).
2. `backend` 이미지가 `uv sync --frozen` 으로 실제로 빌드되는지.
3. Testcontainers 경로가 도는지.

**직접 돌려 본 것** (실제 저장소 상대):

```
$ DATABASE_URL=... bash scripts/migrate.sh      # 마이그레이션을 적용했다
$ DATABASE_URL=... uv run python scripts/seed.py --state s1-transcribed
$ # GET /health -> 200 {"status":"ok","analysisMode":"mock"}
$ # GET /me -> 고정 사용자, POST /me/consent 두 번 -> 시각 그대로, agreed=false -> 422 + details
```

---

## 5. 계획과 달라진 점

| # | 계획 | 실제 | 왜 |
|---|---|---|---|
| 1 | 단위 시험 "합계 78개" `[tests]` §3 | **83개** | 같은 문서의 구성 요소별 표(6,5,5,5,7,6,7,4,5,6,4,4,5,3,3,3,5)를 더하면 83이다. 파일별 개수는 계획 그대로 만들었고 합계 문장만 어긋나 있었다. 개수를 줄이지 않았다 |
| 2 | 어댑터가 HTTP 도구를 직접 import 하지 못하게 **린터 규칙**으로 막는다 `[design]` security §2 | 규칙 대신 **구조**로 막았다 — 감싸기 장치가 클라이언트를 만들어 어댑터에 넘긴다. 검사는 `test_layer_boundaries.py` 가 한다 | `TID251` 은 전역 금지 뒤 per-file 해제 모양이라 "providers 에서만 금지"를 표현할 수 없다. 설계가 "표현이 어려우면 코드 작성 단계에서 대체 수단을 정한다"고 열어 둔 자리다 |
| 3 | `base` 시드는 시나리오 원형 **6개**와 검토된 변형 `[contract]` C16 | 원형 **1개**(`tpl_repair_person_01`)와 변형 1개만 넣었다 | 기존 명세가 이름을 적은 원형은 이것 하나뿐이고, 나머지 다섯의 식별자·내용은 어디에도 글로 없다. 지어내면 u7-f05-practice 가 확정할 값과 어긋난다 (BR8.1). **u7 이 닫아야 하는 자리다 — §6 에 열린 질문으로 남겼다** |
| 4 | `behavior_judgments` 의 부모 참조 | `social_event_id` 를 넣었다 | `[entities]` §3 이 이 테이블의 참조 컬럼을 적지 않았다. `docs/input/04_domain-model.md` §1 이 `SocialEvent ─< BehaviorJudgment` 로 글로 적은 것을 따랐다 |
| 5 | `context_infos` 의 "값과 상태" | 네 항목(관계·장소·목적·사용자 목표) 각각 값·상태 두 컬럼 | 같은 문서 §2 가 `{value, status}` 짝을 네 항목에 둔다고 글로 적었다 |
| 6 | Ruff `per-file-ignores` | `app/api/**` 에 `B008` 을 더했다 | FastAPI 의 `Depends` 는 기본값 자리에서 부르는 것이 그 프레임워크의 쓰임새다. 품질 목표를 낮춘 것이 아니라 도구가 이 틀을 모르는 자리를 좁혀 해제했다 |
| 7 | `docker-compose.yml` 의 frontend | 넣지 않았다 | 계획 §2 가 이미 정한 경계다. u2-web-foundation 이 자기 서비스를 더한다 |

---

## 6. 다음 단위에 남기는 것

| 항목 | 담당 | 무엇을 해야 하는가 |
|---|---|---|
| 시나리오 원형 5개와 그 시드 | u7-f05-practice | `scenario_templates` 에 내용 컬럼을 더하고 원형 6개를 채운다. 픽스처의 `practice` 절과 `scripts/seed.py::seed_base` 가 그 자리다 |
| `utterances`·`conversations` 의 내용 컬럼 | u3-f01-capture | 화자·본문·순서 컬럼을 리비전으로 더한다. 지금 시드는 순번만 넣는다 |
| 내부 상태값 → 계약 값 변환 | u3-f01-capture | `[entities]` §4 대응표대로 API 계층 응답 모델 한 곳에서 바꾼다 (BR7.4). U1 은 내부 값과 대응표만 고정했다 |
| 전사 실패 사유별 재시도 | u3-f01-capture | BR7.5 의 갈림. U1 은 값의 목록과 제약만 만들었다 |
| live 제공자 두 개 | 제공자 확정 시점 | `stt_live.py`·`llm_live.py` 의 TODO 자리. 타임아웃·재시도·로그는 감싸기 장치가 이미 맡고 있어 **바꾸는 것은 설정값 두 개와 그 파일 하나**다 (OQ-N1) |
| `docs/glossary.md` | 기반·통합 담당 (D-122) | 이 단위가 만들지 않는다 |
| GitHub Actions 워크플로 | ci-pipeline (3.7) | `scripts/check.sh`·`check-full.sh` 가 그 안에서 불릴 수 있게 되어 있다 |
| Docker 위 확인 3건 | build-and-test (3.6) | §4 의 목록 |

---

## 7. 검토 1회차 뒤의 수정

검토 1회차 판정은 **READY** (Critical 0 · Major 0 · Minor 2) 였고, 사용자가 두 Minor 를 먼저 고치기로 했다.
**응용 코드는 한 줄도 바뀌지 않았다** — 고친 것은 기록 문서 두 곳이다.

| 지적 | 무엇이 틀렸나 | 무엇을 고쳤나 |
|---|---|---|
| R-01 (Minor) | `unit-test-instructions.md` §3 의 합계 문장이 "단위 78개"인데 구성 요소별 표를 더하면 83 이다. `build-and-test`(3.6)가 그 합계를 기준으로 대조하면 헛되이 어긋난다 | 합계를 **83** 으로 고치고, 더한 식과 "구성 요소별 개수는 그대로이며 합계 줄만 틀렸다"는 사실을 함께 적었다. 시험 범위를 늘리거나 줄인 것이 아니다 |
| R-02 (Minor) | `traceability.json` 의 `PARTIAL` 다섯 건(BR7.2, BR7.4, BR7.5, NFR6.7, C16)에 이유가 없다. 이 문서로는 근거를 확인할 수 없다 | 각 항목에 `note` 를 더해 **U1 이 무엇까지 만들었고 남은 몫의 담당이 누구인지**를 적었고, 문서 머리에 `notes_on_partial` 로 PARTIAL 의 뜻을 명시했다 |

### 판정 기록이 한 번 막혔던 일

1회차 판정을 기록하려 하자 "검토 요청 이후 작업 공간 소스가 바뀌었다"며 거부되었다. 원인은 검토자가 지시대로
검증 도구(pytest, mypy)를 돌리면서 **Python 바이트코드 캐시(`__pycache__/*.pyc`)와 `.coverage` 가 새로
쓰인 것**이다. 이 파일들은 `.gitignore` 에 있지만 소스 지문 계산에는 들어간다. 같은 회차 재시도와 새 회차
열기가 모두 거부되어, 엔진이 제시한 유일한 경로인 **변경 요청**으로 수정을 열었다. 검토 내용 자체에는 문제가
없었고, 그 회차의 두 Minor 가 실제로 고칠 값이 있어 헛돌지 않았다.

**다음 회차부터는 바이트코드 생성을 끈 채로(`PYTHONDONTWRITEBYTECODE=1`) 검증을 돌린다.**
