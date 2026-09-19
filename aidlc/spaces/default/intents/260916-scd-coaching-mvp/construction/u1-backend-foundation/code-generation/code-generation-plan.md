# Code Generation Plan — u1-backend-foundation

**Stage**: code-generation (3.5) · **Unit**: u1-backend-foundation (U1 백엔드 기반)
**작성일**: 2026-09-18 · **담당**: 양성민 (D-123)

## Sources

| 태그 | 출처 |
|---|---|
| `[spec]` | `../functional-design/functional-spec.md` — 흐름 W1~W6, 상태 기계 SM-A~SM-C |
| `[entities]` | `../functional-design/entities.md` — `User`, 20개 테이블 경계표, 내부↔API 대응표 |
| `[rules]` | `../functional-design/rules.md` — BR1.1~BR8.2 |
| `[design]` | `../nfr-design/` — security·observability·reliability·performance·scalability·logical-components |
| `[nfr]` | `../nfr-requirements/` — tech-stack-decisions.md §3 설정값, §5 NFR14.x |
| `[infra]` | `../infrastructure-design/infrastructure-specification.md` — §1·§2·§2.1·§4 |
| `[contract]` | `.../inception/contract-design/contract-summary.md` — 공통 규칙, C1, C14, C15, C16 |
| `[unit]` | `.../inception/units-generation/unit-of-work.md` — U1 정의 |
| `[map]` | `.../inception/units-generation/unit-of-work-story-map.md` — US9.1, US9.2 |
| `[req]` | `.../inception/requirements-analysis/requirements.md` — FR11.1, NFR3~NFR14 |
| `[Q<n>]` | `code-generation-questions.md` — 이 단계에서 사용자가 답한 내용 |
| `[practices]` | `aidlc/spaces/default/memory/team.md`, `project.md` |

---

## 1. 이 단계가 닫은 열린 질문

| ID | 질문 | 답 | 계획에 미치는 영향 |
|---|---|---|---|
| OQ-F5 | 응답 이후 작업의 예약 수단 | **A. 웹 프레임워크의 기본 배경 작업 수단** `[Q1]` | Step 7 의 작업 단위 장치가 그 수단 위에 올라간다. 새 의존성 0 |
| OQ-F2 | 시드 고정 사용자의 식별자 | **A. 고정 식별자를 상수로** `[Q2]` | Step 3·Step 11. 상수는 픽스처 한 자리에서만 읽는다 |
| OQ-N1 | 제공자 확정 여부와 타임아웃 | **A. 아직 미정 — 5초 / 60초 유지** `[Q3]` | Step 7 의 감싸기 장치는 설정값을 읽는다. `live` 는 인터페이스를 지키는 뼈대로 두고 키 없이 둔다 |

**OQ-N1 은 닫히지 않는다.** 제공자가 정해지는 시점까지 열린 채로 남으며, 그때 바꾸는 것은 코드가 아니라
설정값 두 개다 `[Q3]`.

### Q1 의 답이 남기는 대가 — 계획이 이것을 어떻게 다루는가

`[infra]` §2.1 은 연결 풀 5 를 "동시에 도는 작업 2개"라는 보수적 전제로 계산했는데, A 안은 그 전제를
**강제하지 않는다**. 이 계획은 두 가지로 대응한다.

1. 작업 단위 장치가 여는 연결 수를 **로그로 드러낸다**(작업 시작·종료에 작업 식별자가 붙으므로 겹침이 로그에서
   보인다) — Step 7.
2. 통합 시험이 **반복 실행 후 연결 수가 늘지 않는지** 확인한다 — Step 10, `[design]` performance-design.md §5.

동시 작업이 실제로 3개를 넘는 상황이 생기면 그때 실행자를 두는 쪽(Q1 의 B)으로 바꾼다. 지금 그렇게 하지 않는
근거는 사용자 5명 로컬이라는 전제와 `[nfr]` §4 의 "작업 큐·브로커 비도입"이다.

---

## 2. 무엇을 만드는가 — 경계

**만든다** `[unit]`: FastAPI 앱 골격, 업무 이름 6개 × 3계층 패키지 틀, 설정과 분석 모드 판별, DB 연결과
SQLAlchemy 세션, Alembic 초기 리비전(테이블 20개), 오류 봉투와 요청 식별자, 로그 여섯 필드, 작업 단위 장치,
제공자 호출 감싸기, `SttProvider`/`LlmProvider` 인터페이스와 Mock 구현, 합성 대화 픽스처, 프롬프트 로더와
조립기, 시드 고정 사용자와 동의 API, 헬스체크, Docker Compose 기동.

**만들지 않는다** `[unit]`: 기능별 업무 규칙(판정 저장 규칙, 추천, 삭제 전파), 다른 19개 테이블의 타입·제약·
허용값 중 계약과 기존 명세가 글로 확정하지 않은 것(BR8.1), 프론트엔드.

**이 계획이 명시적으로 정하는 경계 두 가지**

| 항목 | 이 단계의 처리 | 근거 |
|---|---|---|
| `docker-compose.yml` 의 frontend 서비스 | **정의하지 않는다.** backend·postgres 둘만 둔다. u2-web-foundation 이 자기 서비스를 더한다 | `[infra]` §2 — "frontend 는 u2 가 소유한다. 이 문서는 자리만 표시한다". AC9.1.1(세 컨테이너)은 **B1 완료 기준**이지 U1 완료 기준이 아니다 |
| `docs/glossary.md` | **이 단위가 만들지 않는다.** 기반·통합 담당이 맡는다 | D-122 배정. `[unit]` U1 의 "가지는 것"에 없다 |

---

## 3. Testing Contract

아래 블록은 `aidlc engine testing-posture render` 의 출력을 **그대로** 옮긴 것이다. 이 단계의 시험 순서는 이
계약이 정하며, 계획의 단계 배열이 그 `plan_profile.steps` 를 따른다.

**적용하지 않는 계층 하나** — `plan_profile.steps` 의 `Frontend behavior` 두 줄은 이 단위에 해당하지 않는다.
U1 은 `kind: service` 인 백엔드 단위이고 화면은 u2-web-foundation 이 소유한다 `[unit]`. 방법론(`test-after`)과
나머지 계층의 순서는 바꾸지 않았다.

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "모든 계층(`api`, `service`, `repository`, `providers`, frontend)을 구현한",
  "scope": "scd-coach-mvp",
  "test_strategy": "standard",
  "project_type": "greenfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: test-after\n- **Ordering**: 모든 계층(`api`, `service`, `repository`, `providers`, frontend)을 구현한\n  뒤 그 계층의 테스트를 쓰고 실행한다. 어느 계층도 테스트를 먼저 쓰지 않는다 `[Q3]`.\n\n방법론을 하나로 둔 이유는 헷갈리지 않기 위해서다 `[Q3]`. 초안이 제안했던 `custom`(규칙\n모듈만 테스트 선행)은 채택되지 않았다.\n\n- **기대 판정은 픽스처 파일로 고정한다** `[FU2]`. 테스트 시점은 위 `Ordering` 그대로지만,\n  `docs/input/05_synthetic-test-data.md` 의 기대 판정을 기계가 읽는 픽스처 파일 한 벌로\n  두고, 판정 관련 단위 테스트가 그 파일을 읽는다. **기대값을 테스트 코드에 직접 적지\n  않는다.** 이 의무는 위 `Methodology` / `Ordering` 두 줄을 대체하지 않는다.\n- 픽스처는 **단일 출처**다. Mock provider, backend 단위 테스트, frontend MSW 핸들러,\n  Playwright 단언이 전부 같은 한 벌을 읽는다 `[quality §9(a)]`. 사람이 같은 표를 두 번\n  적는 자리를 0 으로 만든다 — 손으로 옮긴 사본은 반드시 어긋나고, 어긋나도 각자 초록이라\n  아무도 모른다. 위치는 `backend/app/fixtures/` 로 두되 `[spec:02 §6]`, Mock 이 런타임에\n  반환하는 고정 응답(시연 경로의 일부다 `[constraint:SC-04]`)과 테스트 기대값을 같은 벌로\n  다룬다는 점을 파일 머리에 적어 둔다.\n- **Test Strategy 는 Standard** 다. 구성 요소마다 5–8개, 단위 테스트와 주요 경계의 통합\n  테스트를 쓴다 `[state][spec:02 §3]`.\n- 도구는 `docs/input/02_tech-environment.md` §3 에서 이미 정해졌다. backend 단위는 pytest,\n  backend API 는 pytest + httpx TestClient, DB 연동은 Testcontainers(PostgreSQL), frontend\n  는 Vitest + React Testing Library + MSW, E2E 는 Playwright 로 합성 대화 3건을 돌린다.\n- **커버리지 바닥은 `backend/app/service/` 전체의 라인 커버리지 80% 하나다** `[Q4]`.\n  저장소 전체 바닥은 없고, 분기 커버리지 바닥도 두지 않는다. 활성 스코프\n  `scd-coach-mvp` 는 `org.md` 가 80% 바닥을 주는 목록에 없으므로 이건 무언가를 좁힌 것이\n  아니라 **없던 자리에 바닥을 새로 세운 것**이다 `[quality §3(c)]`. 이 선택이 판정\n  정확성에 남기는 위험은 `evidence.md` 에 기록했다.\n- **병합 전 강제 수단은 GitHub Actions** 다 `[Q1][FU3]`. 로컬 `scripts/check.sh` 는\n  개발자 편의 수단으로 남길 수 있으나 게이트가 아니다. 워크플로 안에서 기계적으로 검증하는\n  지점은 하나 더 있다 — `build-and-test`(3.6)는 EXECUTE 이고, 정의된 커버리지 바닥과 확정\n  품질 목표를 검증한다 `[quality §8][state]`. 통과시키려고 목표를 낮추는 것은 `org.md` 가\n  금지한다.\n- `scripts/check.sh` 를 두는 경우 **컨테이너 안에서 돌린다**(`docker compose run --rm\n  backend ...`) `[devsecops §2][quality §8]`. 5인의 로컬 Python·Node 버전이 제각각인데\n  호스트에서 돌리면 \"내 자리에선 통과했다\"가 분쟁이 된다. 빠른 것과 느린 것을 나눈다 —\n  `check.sh` = ruff + mypy + `pytest -m \"not integration and not e2e\"` + vitest(목표 2분\n  이내), `check-full.sh` = 여기에 Testcontainers 통합 + Playwright.\n- pytest 마커 `integration`, `e2e` 를 **지금** 정한다 `[quality §9(b)]`. 나중에 정하면\n  전부 한 덩어리가 되어 있고 되돌리는 비용이 크다.\n- 수용 기준 추적은 이름이 아니라 마커로 단다: `@pytest.mark.ac(\"AC1.3.2\")`\n  `[quality §9(f)]`. user-stories(2.4)가 만들 수용 기준 ID 를 `build-and-test`(3.6)가\n  기계적으로 대조할 수 있게 된다.\n- **Testcontainers 격리 규약** `[quality §9(c)]`: 컨테이너는 세션당 1개, 스키마는 세션\n  시작 시 `alembic upgrade head` 로 한 번 만든다(`Base.metadata.create_all()` 을 쓰지\n  않는다 — 그래야 마이그레이션이 실제로 한 번은 실행된다 `[developer §2.3]`), 테스트마다\n  트랜잭션 후 롤백으로 격리한다. 테스트 독립성은 타협 대상이 아니다.\n- 어떤 구현이 와도 통과하는 테스트(`assert True` 류)는 쓰지 않는다. 테스트는 행복 경로와\n  최소 2개의 오류·경계 경우를 덮는다 `[phase:construction]`.\n- **Mock 픽스처 대조 테스트를 둔다** `[quality §4]`. `MockLlmProvider` 가 각\n  `conversationKey` 에 대해 픽스처와 정확히 같은 `group / opportunity / result /\n  holdReason / evidence` 를 반환하는지 검증한다. 이게 없으면 Mock 픽스처가 기대 판정표에서\n  한 칸 어긋났을 때 SM1 도 E2E 도 단위 테스트도 전부 초록인 채로 전 구간이 일관되게\n  거짓말한다.\n- **프롬프트 빌더 단위 테스트를 둔다** `[quality §4][devsecops §4]`. TC-08 은 Mock 경로에서\n  살아남는 유일한 보안 속성인데, Mock 은 전사를 읽지 않으므로 SM1 통과가 이 속성을 전혀\n  증명하지 않는다. LLM 없이 지금 쓸 수 있는 테스트 2건: (a) 전사에 주입 문구가 들어간 경우\n  렌더 결과에서 그 문장이 데이터 블록 **안**에 있고 지시문 영역이 하나뿐임을 단언한다,\n  (b) 전사에 구분자 문자열 자체가 들어간 경우 렌더 결과에 구분자가 여는 것/닫는 것 각 1회만\n  남거나 이스케이프된 형태로만 남는다.\n- frontend 에는 수치 바닥을 걸지 않는다. 빠뜨린 것이 아니라 뺀 것이고, 대신 비수치 의무를\n  하나 둔다 — SM1 경로의 A/B/C 화면은 정상 표시가 아니라 **빈·부족·보류 상태**에 최소\n  1개의 RTL 테스트를 둔다 `[quality §3(d)]`. `05_synthetic-test-data.md` 가 직접 요구하는\n  것들이다: S2 의 \"어려움 장면 0개일 때 화면이 비지 않고 잘한 장면만 표시\", S3 의 보류\n  표시, C1 의 \"아직 비교하기엔 기록이 부족해요\". Mock 행복 경로 E2E 가 절대 못 잡는다.\n- **Playwright 주기와 범위** `[quality §7]`: 빠른 루프(병합 전)는 S1 만, 3건 전체는 Bolt\n  완료 시점과 주 1회 고정 시각, 태그·리허설 전에는 반드시 전체. E2E 개수는 3건에서 늘리지\n  않는다 — 새 동작은 통합·단위로 내린다. S2 는 보류 표시와 목적 완료 판정이 들어오는\n  Bolt 에, S3 는 보류 사유가 들어오는 Bolt 에 붙인다. **S3 의 검증 항목 2·4(전사 정정 후\n  재검토 표시, 삭제 시 연결 항목 처리)는 F07 이 Must 로 올라가면서 이번 범위 안에 들어왔다**\n  `[Q7][FU1]`.\n- `live` 경로는 인터페이스 준수 계약 테스트만 두고, **네트워크를 타는 테스트는 기본\n  실행에서 제외한다** `[quality §9(g)]`. 제공자가 미정인 동안 `[raid:D2]` 누군가 API 키가\n  필요한 테스트를 쓰면 기본 스위트가 실행 불가능해진다.\n- 결함은 고치기 전에 **재현 테스트를 먼저 쓴다** `[quality §9(e)]`. 이슈 트래커가 없으므로\n  기록 자리는 `docs/decisions/decision-log.md` 다 `[constraint:OC-05]`.\n\n**규칙마다 강제 테스트** — `discovered-rules.md` 의 항목 중 무엇이 테스트로 지켜지는지를\n여기에 고정한다 `[quality §5]`. 테스트 없는 규칙은 7주 안에 조용히 썩는다.\n\n| 규칙 | 강제하는 테스트 |\n|---|---|\n| TC-08 전사는 데이터 블록으로만 | 프롬프트 빌더 단위 테스트 2건 |\n| TC-10 모델명·프롬프트 버전·기준 버전 저장 | 판정 저장 후 세 필드 존재를 단언하는 통합 테스트 |\n| TC-13 종합점수·백분위 금지 | 리포트 응답 스키마에 해당 필드가 없음을 단언 |\n| TC-14 `api` → `service` → `repository` | `api` 모듈이 `repository` 를 import 하지 않음을 검사하는 테스트 + Ruff `TID251` |\n| TC-05 음성 BLOB 금지 | 스키마 검사 |\n| SC-04 `ANALYSIS_MODE` fail closed | 미설정·모르는 값에서 mock 으로 뜨고, 키 없는 `live` 에서 기동이 거부되는지 단위 테스트 |\n| F07 삭제 전파 | 대화 1건을 만들고 삭제한 뒤 관련 테이블 전부와 파일 경로가 비었는지 확인하는 검사 |\n| TC-07 프론트에서 STT·LLM 직접 호출 금지 | 테스트로 잡기 어려움 — 규칙만 |\n\n**운영 파라미터 검증** — `performance-validation`(4.6)이 SKIP 이라 PM-01~PM-04 를 확인할\n단계가 계획에 없다. 부하 시험을 하자는 것이 아니라 기존 테스트 안의 단언 한 줄씩이다\n`[quality §9(d)]`.\n\n| 항목 | 값 | 어디서 확인 |\n|---|---|---|\n| PM-01 녹음 최대 길이 | 5분 | 업로드 검증 경계 단위 테스트(4:59 / 5:01) |\n| PM-02 Mock 분석 응답 시간 | 3초 이내 | 분석 API 통합 테스트에 경과 시간 단언 추가 |\n| PM-03 \"비교 불충분\" 기준 | 유효 기회 3회 미만 | 경계 단위 테스트 2 / 3 / 4 |\n| PM-04 원음 보관 기간 | 30일 | 설정값이 노출되고 기본값이 30일인지만 확인한다. 경과 시간에 따른 만료 삭제 동작은 7주 안에 실측할 수 없으므로 이번 범위에서 검증하지 않는다 |\n\n\n**이 절의 근거 결정: D-57** (`decision-log.md` §5-2) `[log §5-2][FU4]`. 방법론은\n**test-after** 하나, 커버리지 바닥은 `service/` **라인 80%** 하나, 기대 판정은 **픽스처\n파일로 고정**하고 단위 테스트가 그것을 읽는다 — 위 세 항목이 그 결정의 세 갈래다."
    }
  ],
  "obligations": {
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:f7a662778c51563563aca6034458b07c7976455325ede1b9040a88c4e8a7cb0c",
  "contract_sha256": "sha256:00847776538d2675b246a4641aebe46517d03fe33e6024b7b717595a353ff951"
}
```

---

## 4. 실행 계획

번호는 실행 순서다. 각 구현 단계 바로 뒤에 그 계층의 시험 단계가 온다 — **test-after**, 계약이 정한 순서다.

### Step 1 — 프로젝트 구조와 운영 설정 뼈대

- [x] `backend/pyproject.toml` — uv 프로젝트, 의존성(`fastapi`, `uvicorn`, `sqlalchemy>=2`, `alembic`,
      `psycopg[binary]`, `pydantic-settings`, `python-multipart`, `httpx`), 개발 의존성(`pytest`,
      `pytest-cov`, `testcontainers[postgres]`, `ruff`, `mypy`)
- [x] Ruff 설정 — 규칙 집합 `E, F, I, UP, B, SIM, TID, RUF, S`, 줄 길이 88, `tests/` 에 `S101`
      per-file-ignore, `TID251` 로 `app.repository` 전역 import 금지 + `app/service/**`·
      `app/repository/**`·`tests/**` 해제 `[practices]`
- [x] mypy 설정 — 전역 `check_untyped_defs`·`warn_unused_ignores`, 서드파티 `ignore_missing_imports`,
      `plugins = ["pydantic.mypy"]`, **`app.service.*` 에만 `disallow_untyped_defs`** `[practices]`
- [x] `backend/Dockerfile` — uv 로 설치, uv 버전을 태그로 고정 `[practices]`
- [x] `docker-compose.yml` — backend·postgres 두 서비스. 헬스체크 **5초 간격 12회, 한 번당 3초, 시작 유예
      0초**, 자동 재시작 없음, 자원 한도 없음, 이름 있는 볼륨 둘(데이터·업로드) `[infra]` §1·§2
- [x] `backend/.env.example` — 값 자리를 비우거나 `<발급받은-키>`. **실제 키를 닮은 더미를 넣지 않는다**
      `[design]` security-design.md §5
- [x] `backend/app/` 패키지 틀 — `api/`·`service/`·`repository/` 각각에 업무 이름 6개
      (`conversation`, `assessment`, `training`, `record`, `account`, `privacy`) `[practices]` project.md,
      그리고 `common/`, `providers/`, `fixtures/`, `prompts/`
- [x] `uv.lock` 생성·커밋. 설치는 잠금에서만 `[practices]`

**스토리**: US9.1 (기동) · **수용 기준**: AC9.1.1 의 전제

### Step 2 — 시험 실행기 준비

계약이 **첫 시험보다 먼저**라고 정한 자리다.

- [x] `pyproject.toml` 의 pytest 설정 — 표시 `integration`, `e2e`, `ac(...)` 등록, `testpaths`
- [x] `backend/tests/conftest.py` — Testcontainers 세션당 1개, 세션 시작 시 `alembic upgrade head`
      (`Base.metadata.create_all()` **금지**), 시험마다 트랜잭션 후 되돌림 `[practices]`
- [x] `unit-test-instructions.md` §2 의 정확한 단위 범위 명령이 **실제로 도는지** 확인한다(시험 0건이어도
      수집이 성공해야 한다)

**요구사항**: NFR14.3

### Step 3 — 데이터 모델·데이터베이스 동작 구현

- [x] `app/repository/models.py` — 테이블 20개. `users` 는 `[entities]` §1 전체, 나머지 19개는
      `[entities]` §3 의 "U1 이 지금 적는 것" 칸만. **추측해 적지 않는다** (BR8.1)
- [x] `conversations` — `transcript_status`·`transcript_failure_reason`·`analysis_status` 세 컬럼,
      허용값은 `[entities]` §4 의 내부 값 `[Q2 of 3.1]`
- [x] `behavior_judgments` — 출처 네 컬럼 `NOT NULL` (TC-10)
- [x] `audio_assets` — **음성 본문 컬럼을 두지 않는다** (TC-05, BR8.2)
- [x] `sharing_settings.level` — `NONE`/`SUMMARY`/`FULL`, 기본 `NONE` (FR11.2)
- [x] FK 에 `ON DELETE CASCADE` 를 **그물로만**. 가변 구조는 JSONB `[contract]` C15
- [x] 관계 기본값을 `lazy="raise"` 로 `[practices]` — 조용한 N+1 대신 즉시 예외 `[design]`
      performance-design.md §2
- [x] `alembic/` + `alembic.ini` (`backend/` 아래, `app/` 밖), 초기 리비전 하나. `--autogenerate` 결과는
      **초안**이므로 사람이 읽고 고친 뒤 커밋 `[practices]`
- [x] 시드 고정 사용자 식별자 상수 — `app/fixtures/` 한 자리에서만 읽는다 `[Q2]`

**스토리**: US9.2 (고정 사용자) · **요구사항**: `[contract]` C15, NFR10.7

### Step 4 — 데이터 모델 시험 (구현 뒤)

- [x] `tests/unit/test_schema_no_audio_blob.py` (3건)
- [x] `tests/integration/test_migration_applied.py` (3건)

### Step 5 — 저장소 계층 구현

- [x] `app/db.py` — 동기 엔진, **연결 풀 크기 5** `[infra]` §2, `Depends` 로 주입하는 요청당 세션 하나,
      그리고 응답 이후 작업이 쓸 **세션 팩토리** `[contract]` 공통 규칙
- [x] `app/repository/account/` — 사용자 조회·동의 시각 갱신. **확정하지 않는다** (BR5.3)
- [x] `repository` 에서 예외를 잡아 `None` 을 반환하지 않는다 — "없음"과 "실패"는 다른 값이다 `[practices]`

**요구사항**: NFR10.3, NFR3.x

### Step 6 — 저장소 계층 시험 (구현 뒤)

- [x] `tests/integration/test_user_repository.py` (3건)

### Step 7 — 업무 계층 구현

이 단위의 무게중심이다. `[design]` 이 정한 장치들이 전부 여기 있다.

- [x] `app/config.py` — pydantic-settings. 기동 시 **한 번** 파싱 (BR1.3). `[nfr]` §3 의 설정값 전부:
      분석 모드, 연결 타임아웃 5초, 읽기 타임아웃 60초, 재시도 1회, 업로드 최대 크기, 업로드 저장 경로,
      원음 보관 30일, 녹음 최대 5분, 비교 불충분 기준 3, Mock 분석 목표 3초, 로그 기본 수준 정보,
      헬스체크 확인 질의 제한 1초. 평면 구조 + 접두사 규칙 `[design]` nfr-design Q3
- [x] 분석 모드 결정 — `[design]` security-design.md §1.1 의 흐름 그대로. 미설정·빈 값·모르는 값 → mock
      (+로그), `live` + 키 없음 → **기동 중단** (BR1.1, BR1.2)
- [x] `app/common/logging.py` — `get_logger(component=...)`, 여섯 필드, 허용값 8개 고정
      `[design]` observability-design.md §1
- [x] `app/common/request_context.py` — 요청 식별자·작업 식별자 문맥. 로그가 **자동으로** 읽는다 (BR6.1, BR6.2)
- [x] `app/common/exceptions.py` — `AppError(code, message, http_status)` 와 하위 예외 6종
      (`NotFoundError` 404, `PermissionDeniedError` 403, `ValidationError` 422, `ConflictError` 409,
      `ProviderError` 502, `ProviderTimeoutError` 504)
- [x] `app/common/unit_of_work.py` — **작업 단위 장치**. 자기 연결을 직접 연다(작업 함수가 연결을 인자로 받지
      않는다). 성공 → 한 번 확정 → 닫기. 예외 → 되돌리기 → 닫기 → **별도 연결**로 실패 상태 기록 → 확정 →
      닫기. 실패 기록마저 실패하면 로그만 남기고 넘어간다 `[design]` reliability-design.md §2
      (BR5.1~BR5.3)
- [x] `app/common/provider_call.py` — **공용 호출 감싸기**. 시간 측정, 연결·읽기 타임아웃 분리, 타임아웃·연결
      실패에만 1회 재시도, 4xx 재시도 안 함, 제공자 예외를 앱 오류로 변환, 모델명·프롬프트 버전·소요 시간·
      식별자만 로그(요청 본문을 받지 않는다) `[design]` security-design.md §2
- [x] `app/service/ports.py` — `SttProvider`, `LlmProvider` Protocol 과 DTO
      (`TranscriptionResult`, `TranscriptBlock`, `UtteranceView`, `ContextView`, `JudgmentCandidate`,
      `CoachTurnResult`, `ScenarioView`) `[contract]` C14. **`providers/` 에 두지 않는다** `[practices]`
- [x] `app/providers/` — `stt_mock.py`, `llm_mock.py`, `stt_live.py`, `llm_live.py`(인터페이스를 지키는
      뼈대, 키 없음 `[Q3]`), `factory.py`. **결정된 모드의 객체만 만든다** (NFR5.3)
- [x] `app/fixtures/` — `s1_repair`, `s2_topic`, `s3_unclear` 와 로더. 파일 머리에 **단일 출처**임을 적는다
      (BR4.3, NFR14.1). 대화 키 선택과 모르면 S1 규칙 (BR4.1, BR4.2)
- [x] `app/prompts/assess_v1.md` 와 로더 — **파일 이름에서 식별자·버전을 뽑는다** `[practices]`
- [x] 프롬프트 조립기 — 전사를 **구분자로 감싼 데이터 블록 안에만** 넣고, 넣기 전에 구분자 시퀀스를
      이스케이프한다. 지시문 영역은 하나뿐이고 데이터 블록 뒤에 다시 열리지 않는다. **전사를 인자로 받는 순수
      함수** `[design]` security-design.md §3.1 (TC-08)
- [x] `app/service/current_user.py` — **현재 사용자 결정 지점 하나**. 클라이언트가 보낸 식별자를 읽지 않는다
      `[design]` security-design.md §6 (BR2.3)
- [x] `app/service/account/` — 사용자 조회, 동의 저장(이미 동의했으면 처음 시각 유지). **`fastapi` 를
      import 하지 않는다** (TC-14, BR2.2)

**스토리**: US9.1, US9.2 · **요구사항**: NFR5.x, NFR6.x, NFR12.x, NFR13.x

### Step 8 — 업무 계층 시험 (구현 뒤)

- [x] `test_config_analysis_mode.py`(6) · `test_config_values.py`(5) · `test_logging_fields.py`(5) ·
      `test_request_context.py`(5) · `test_unit_of_work.py`(6) · `test_provider_call.py`(7) ·
      `test_provider_factory.py`(4) · `test_mock_stt_provider.py`(5) · `test_mock_llm_provider.py`(6) ·
      `test_fixture_loader.py`(4) · `test_prompt_loader.py`(4) · **`test_prompt_builder.py`(5)** ·
      `test_current_user.py`(3) · `test_account_service.py`(5)
- [x] `test_prompt_builder.py` 의 앞 두 건은 팀 관행이 못박은 필수 2건이다 — 주입 문구가 데이터 블록 안에
      있는지, 구분자 문자열이 이스케이프되는지 `[practices]`

### Step 9 — API 계층 구현

- [x] `app/common/middleware.py` — 요청마다 식별자 발급, 요청 수신·완료 로그
      `[design]` observability-design.md §3
- [x] `app/common/error_handlers.py` — 오류 봉투 하나로 고정. `code` 영어 토큰, `message` 한국어,
      `details` 는 **검증 실패에만**, 그 밖에는 빈 배열. 500 은 내부 메시지를 노출하지 않고 스택은 로그에만
      `[design]` security-design.md §4.1 `[contract]` 공통 규칙
- [x] `app/api/common/health.py` — `GET /api/v1/health`. 저장소에 **1초 제한**을 건 확인 질의, 현재 분석
      모드를 설정 객체에서 읽어 함께 응답. **헬스체크 자체의 로그는 실패할 때만** `[design]`
      observability-design.md §4 (BR3.1, BR3.2)
- [x] `app/api/account/` — `GET /api/v1/me`, `POST /api/v1/me/consent`, `schemas.py`.
      응답은 계약 C1 의 `Me` 모양 그대로
- [x] **모든 라우트에 `response_model` 선언** — ORM 객체가 응답으로 새는 일을 구조적으로 막는다 `[practices]`
- [x] 라우트는 동기 `def` `[practices]` (D-54)
- [x] `app/main.py` — 앱 조립, 예외 처리기 등록, 미들웨어 등록, 라우터 등록, 기동 완료 로그.
      **스키마 적용을 기동 흐름에 넣지 않는다** `[spec]` W1

**스토리**: US9.1, US9.2 · **수용 기준**: AC9.1.1, AC9.1.2, AC9.1.3, AC9.2.1, AC9.3.4

### Step 10 — API 계층 시험 (구현 뒤)

- [x] `test_error_envelope.py`(7) · `test_layer_boundaries.py`(3)
- [x] `tests/integration/test_health_endpoint.py`(4) · `test_me_endpoint.py`(3) ·
      `test_consent_endpoint.py`(4) — 각각 **경과 시간 200ms 단언 한 줄** `[design]` performance-design.md §5
- [x] 연결이 새지 않는지 — 통합 시험 반복 실행 후 연결 수가 늘지 않는지 확인 (§1 의 Q1 대가 대응 2)

> **`Frontend behavior` 두 단계는 이 단위에 해당하지 않아 생략한다** (§3 참고). 빠뜨린 것이 아니다.

### Step 11 — 실행 환경과 시드

- [x] `backend/scripts/seed.py --state <name>` — `base`·`consented`·`s1-transcribed` 세 상태. 누적이며
      값은 **픽스처에서 읽는다** `[contract]` C16 (BR2.1, BR4.3). 나머지 여섯 상태는 갈래 4 가 더한다
- [x] `backend/scripts/check.sh` — ruff + mypy + `pytest -m "not integration and not e2e"`.
      **컨테이너 안에서 돈다** `[practices]`
- [x] `backend/scripts/check-full.sh` — 위 + Testcontainers 통합
- [x] `backend/scripts/migrate.sh` — `alembic upgrade head`. **기동 흐름 밖의 별도 단계** `[spec]` W1
- [x] `tests/integration/test_seed_states.py`(4)
- [x] 새로 받은 트리에 실제 값이 든 환경 파일이 **없는지** 확인 (AC9.1.4, BR6.4)

**수용 기준**: AC9.1.4, AC9.2.1

### Step 12 — 문서와 추적

- [x] 각 모듈의 사람이 읽는 주석은 **한국어** `[constraint:OC-06]`
- [x] `code-summary.md` — 만든 파일, 주요 구현 결정, 시험 범위, 계획과 달라진 점
- [x] `source-manifest.json` — 이 단위가 만들거나 고친 **모든** 응용 소스 경로
- [x] `traceability.json` — 배정된 AC 7개와 인용한 `NFRx.y`·`BRx.y` 전부. **본문이 근거로 인용한 항목도
      넣는다** `[practices]` project.md (검토 R-02·R-06 이 두 번 지적한 자리다)

---

## 5. 스토리 ↔ 단계 대응

| 스토리 | 수용 기준 | 어느 단계가 만드는가 |
|---|---|---|
| US9.1 기동과 분석 모드 | AC9.1.1 | Step 1(컨테이너·헬스체크 설정), Step 9(헬스체크 라우트), Step 10 |
| | AC9.1.2 | Step 7(분석 모드 결정), Step 8 |
| | AC9.1.3 | Step 7(기동 거부), Step 8 |
| | AC9.1.4 | Step 1(예시 환경 파일), Step 11(확인) |
| US9.2 고정 사용자와 동의 | AC9.2.1 | Step 3(사용자 테이블·상수), Step 7(동의 업무), Step 9(두 라우트), Step 11(시드) |
| | AC9.2.2 | Step 7(Mock 대화 키 선택), Step 8 |
| | AC9.2.3 | Step 7(모르면 S1), Step 8 |
| 시연 리허설 | AC9.3.4 | Step 9(헬스체크가 분석 모드를 알린다), Step 10 |

---

## 6. 품질 목표 — 낮추지 않는다

| 목표 | 값 | 어디서 확인 |
|---|---|---|
| `backend/app/service/` 라인 커버리지 | **80% 이상** | Step 8·10 의 시험, 검증은 `build-and-test`(3.6) |
| 세 엔드포인트 응답 시간 | **200ms (p95)** | Step 10 의 경과 시간 단언 |
| 린터 위반 | **0건** (`E, F, I, UP, B, SIM, TID, RUF, S`) | Step 1 설정, `check.sh` |
| 타입 오류 | **0건**, `app.service.*` 는 타입 필수 | 같음 |
| 시험 통과 | 단위 78 · 통합 21 전부 | `unit-test-instructions.md` §3 |

**통과시키려고 이 값들을 낮추거나 검사 설정을 끄지 않는다.** 못 맞추면 그 사실을 드러낸다 `[practices]`.

---

## 7. 이 계획이 지키는 금지 규칙

| 금지 | 이 계획의 어디가 지키는가 |
|---|---|
| 음성 파일을 DB BLOB 으로 저장 | Step 3 — `audio_assets` 에 본문 컬럼 없음, Step 4 시험 |
| ORM 모델을 API 응답으로 반환 | Step 9 — 모든 라우트에 `response_model` |
| `api` → `repository` 직접 호출 | Step 1 — Ruff `TID251`, Step 10 — 경계 시험 |
| 종합점수·백분위 계산 | Step 4 — 응답 모델에 해당 필드 없음을 단언 |
| 오케스트레이션 프레임워크·벡터DB 도입 | Step 1 의 의존성 목록이 전부다 |
| 실제 사용자 데이터 | Step 7·11 — 픽스처와 시드가 전부 합성 |
| 비밀값 커밋 | Step 1 — 예시 파일만, Step 11 — 확인 |

## Assumptions & Open Questions

### 가정

- Step 1 의 의존성 목록이 첫 실행에 충분하다는 것은 `[nfr]` §2 가 "빠뜨리면 첫 주에 막히는" 셋
  (`python-multipart`, `pydantic-settings`, `httpx`)을 이미 짚어 둔 것에 기댄다. 새 이름을 추가할 때는
  리뷰어가 공식 문서와 배포 페이지에서 확인한다 `[practices]`.
- 시험 개수(단위 78 · 통합 21)는 Standard 전략의 "구성 요소마다 5~8개"를 구성 요소 17개에 적용한 결과다.
  구현 중 한 구성 요소가 더 갈라지면 개수는 늘 수 있으나 줄지 않는다.
- `docker-compose.yml` 에 frontend 를 두지 않아도 `docker compose up --build` 가 성립한다는 전제다.
  u2 가 들어오면 세 컨테이너가 된다.

### 열린 질문

| ID | 질문 | 담당 |
|---|---|---|
| OQ-N1 | live 제공자가 정해지면 타임아웃 두 값을 실측으로 조정한다 | 제공자 확정 시점 (`[Q3]` 이 이 단계에서 닫지 않기로 확인했다) |

**승인은 `code-generation-questions.md` 의 `## Plan Approval` 에서 받는다.** 그 승인은 이 문서와
`unit-test-instructions.md` 두 벌을 함께 묶는다.
