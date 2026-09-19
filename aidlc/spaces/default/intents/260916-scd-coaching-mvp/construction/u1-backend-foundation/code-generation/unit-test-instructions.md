# Unit Test Instructions — u1-backend-foundation

**Stage**: code-generation (3.5) · **Unit**: u1-backend-foundation (U1 백엔드 기반)
**작성일**: 2026-09-18

## Sources

| 태그 | 출처 |
|---|---|
| `[practices]` | `aidlc/spaces/default/memory/team.md` — Testing Posture, Code Style, Deployment |
| `[contract]` | 이 단계의 승인된 `## Testing Contract` (`code-generation-plan.md`) |
| `[design]` | `../nfr-design/` — security-design.md §2·§3, reliability-design.md §2, observability-design.md §1, performance-design.md §5 |
| `[rules]` | `../functional-design/rules.md` — BR1~BR8 |
| `[spec]` | `../functional-design/functional-spec.md` — §4 수용 기준 대조표 |
| `[nfr]` | `../nfr-requirements/tech-stack-decisions.md` §5 — NFR14.1~14.3 |

---

## 1. 시험 도구와 설정

| 항목 | 값 | 근거 |
|---|---|---|
| 단위·API 시험 | `pytest` | `[practices]` Testing Posture |
| API 호출 | `httpx` 테스트 클라이언트 | 같음 |
| 저장소 연동 | Testcontainers (PostgreSQL 16) | 같음 |
| 실행기 | `uv run` — 가상환경 활성화 개념이 없다 | `[practices]` Code Style (D-54) |
| 설정 위치 | `backend/pyproject.toml` 한 파일 | 같음 |

**표시(marker)를 지금 정한다** `[practices]`. 나중에 정하면 전부 한 덩어리가 되어 있고 되돌리는 비용이 크다.

| 표시 | 뜻 | 기본 실행 |
|---|---|---|
| `integration` | 실제 저장소를 띄워 도는 시험 | 빠른 루프에서 제외 |
| `e2e` | 브라우저 종단 시험 | 제외 (이 단위에는 없다) |
| `ac("<수용기준 ID>")` | 그 시험이 덮는 수용 기준 | 표시일 뿐 실행에 영향 없음 |

`ac` 표시는 `build-and-test`(3.6)가 수용 기준을 기계적으로 대조할 수 있게 한다 `[practices]`.

---

## 2. 이 단위의 시험을 어떻게 돌리는가

**기준 명령 — 컨테이너 안에서 돈다** `[practices]`. 5인의 로컬 Python 버전이 제각각인데 호스트에서 돌리면
"내 자리에선 통과했다"가 분쟁이 된다.

빠른 루프 (표시 없는 것만, 이 단위의 파일만):

```
docker compose run --rm backend uv run pytest -m "not integration and not e2e" \
  tests/unit/test_config_analysis_mode.py \
  tests/unit/test_config_values.py \
  tests/unit/test_logging_fields.py \
  tests/unit/test_request_context.py \
  tests/unit/test_error_envelope.py \
  tests/unit/test_unit_of_work.py \
  tests/unit/test_provider_call.py \
  tests/unit/test_provider_factory.py \
  tests/unit/test_mock_stt_provider.py \
  tests/unit/test_mock_llm_provider.py \
  tests/unit/test_fixture_loader.py \
  tests/unit/test_prompt_loader.py \
  tests/unit/test_prompt_builder.py \
  tests/unit/test_current_user.py \
  tests/unit/test_layer_boundaries.py \
  tests/unit/test_schema_no_audio_blob.py \
  tests/unit/test_account_service.py
```

저장소를 띄우는 것까지 (이 단위의 파일만):

```
docker compose run --rm backend uv run pytest -m integration \
  tests/integration/test_health_endpoint.py \
  tests/integration/test_me_endpoint.py \
  tests/integration/test_consent_endpoint.py \
  tests/integration/test_migration_applied.py \
  tests/integration/test_user_repository.py \
  tests/integration/test_seed_states.py
```

**두 명령 모두 이 단위의 파일만 지목한다.** 저장소 전체를 도는 `pytest` 한 줄을 쓰지 않는 이유는,
`build-and-test`(3.6)가 단위마다 그 단위의 명령을 실행하기 때문이다 — 범위 없는 명령이면 전체 스위트가
단위 수만큼 반복된다.

**호스트에서 도는 형태(개발 중 편의용, 게이트 아님)**: `cd backend && uv run pytest ...` 로 같은 인자를 쓴다.

**시험 실행기 준비가 첫 시험보다 먼저다** `[contract]`. `pyproject.toml` 의 `pytest` 설정과 `uv.lock` 이
있어야 위 명령이 실제로 돈다. 계획의 Step 2 가 그 자리다.

---

## 3. 구성 요소별 시험 범위

Test Strategy 는 **Standard** — 구성 요소마다 5~8개, 단위 시험과 주요 경계의 통합 시험이다 `[contract]`.
행복 경로 하나와 오류·경계 **최소 2개**를 반드시 덮는다 `[phase:construction]`.

| # | 구성 요소 | 시험 파일 | 개수 | 무엇을 덮는가 |
|---|---|---|---|---|
| 1 | 분석 모드 해석 | `test_config_analysis_mode.py` | 6 | 미설정 → mock · 빈 값 → mock · 모르는 값 → mock(+로그) · `mock` → mock · `live`+키 있음 → live · `live`+키 없음 → **기동 거부** (BR1.1, BR1.2, AC9.1.2, AC9.1.3) |
| 2 | 설정값 노출 | `test_config_values.py` | 5 | 타임아웃 5초·60초 기본값 · 재시도 1회 · 업로드 최대 크기가 설정값 · 원음 보관 30일 · 로그 기본 수준 정보 (NFR4.1, PM-04) |
| 3 | 로그 구조 | `test_logging_fields.py` | 5 | 여섯 필드가 모두 있다 · 컴포넌트가 로거 생성 시 붙는다 · 허용값 밖 컴포넌트 거부 · 예외를 통째로 넘기지 않는다 · 진단 수준에서도 전사 본문이 없다 (NFR12.3, NFR12.8, BR6.3) |
| 4 | 식별자 문맥 | `test_request_context.py` | 5 | 요청 식별자 자동 부착 · 작업 식별자 자동 부착 · 작업이 요청 식별자를 함께 담는다 · 요청 경로에서 작업 식별자는 비어 있다 · 문맥 밖에서 읽으면 비어 있다 (NFR12.5, NFR12.6, BR6.1, BR6.2) |
| 5 | 오류 봉투 | `test_error_envelope.py` | 7 | 네 필드 고정 · `code` 는 영어 토큰, `message` 는 한국어 · 검증 실패만 `details` 를 채운다 · 그 밖은 빈 배열 · 500 이 내부 메시지를 노출하지 않는다 · `request_id` 가 로그 값과 같다 · 각 예외의 상태 코드 대응 (NFR6.9, NFR7.1, NFR8.1, `[design]` §4.1) |
| 6 | 작업 단위 장치 | `test_unit_of_work.py` | 6 | 성공 시 한 번 확정 · 예외 시 되돌림 · 되돌림 뒤 **별도 연결**로 실패 기록 · 실패 기록마저 실패하면 로그 남기고 넘어감 · 어느 경로에서든 닫힘 · 요청 연결을 받지 않는다 (BR5.1~BR5.3, NFR10.13, NFR10.14) |
| 7 | 제공자 호출 감싸기 | `test_provider_call.py` | 7 | 연결 5초·읽기 60초를 건다 · 타임아웃에 1회 재시도 · 연결 실패에 1회 재시도 · 4xx 는 재시도 안 함 · 제공자 예외를 앱 오류로 변환 · 소요 시간·모델명·프롬프트 버전 로그 · 요청 본문을 로그에 넘기지 않음 (NFR13.3~13.5, NFR12.7, NFR12.1) |
| 8 | 제공자 선택 | `test_provider_factory.py` | 4 | mock 모드에서 mock 객체만 생성 · live 모드에서 live 객체 생성 · mock 모드에서 live 구현이 불러와지지 않음 · 인터페이스가 `service/ports.py` 에 있다 (NFR5.3, `[contract]` C14) |
| 9 | Mock 전사 | `test_mock_stt_provider.py` | 5 | 대화 키 세 개가 각각 맞는 전사 · 키 없음 → S1 · 모르는 키 → S1 · 녹음 → S1 · 픽스처와 값이 정확히 같다 (BR4.1, BR4.2, AC9.2.2, AC9.2.3) |
| 10 | Mock 판정 | `test_mock_llm_provider.py` | 6 | 대화 키별 기대 판정이 픽스처와 **정확히 일치**(`group`/`opportunity`/`result`/`holdReason`/`evidence`) · 전사 버전으로 정정 전·후 S3 구분 · 모르는 키 → S1 (BR4.1~BR4.3, NFR14.1) |
| 11 | 픽스처 단일 출처 | `test_fixture_loader.py` | 4 | 세 파일이 로드된다 · 없는 키는 오류 · 값이 코드에 중복되어 있지 않다 · 파일 머리에 단일 출처 표기가 있다 (NFR14.1, BR4.3) |
| 12 | 프롬프트 로더 | `test_prompt_loader.py` | 4 | 파일 이름에서 식별자·버전을 뽑는다 · 모듈 기준 상대 경로로 읽는다 · 없는 파일은 오류 · 한 번만 읽는다 (`[contract]` C14) |
| 13 | 프롬프트 조립 | `test_prompt_builder.py` | 5 | **주입 문구가 데이터 블록 안에 있고 지시문 영역이 하나뿐** · **구분자 문자열이 이스케이프되거나 각 1회만** · 빈 전사 · 발화 순서 유지 · 순수 함수라 외부 호출이 없다 (TC-08, NFR6.6, `[design]` §3.2 — 앞의 두 건이 팀 관행이 못박은 필수 2건) |
| 14 | 현재 사용자 결정 지점 | `test_current_user.py` | 3 | 고정 사용자를 돌려준다 · **클라이언트가 보낸 식별자를 읽지 않는다** · 결정 지점이 코드에서 한 곳이다 (BR2.3, NFR6.1, NFR6.2) |
| 15 | 계층 경계 | `test_layer_boundaries.py` | 3 | `api` 가 `repository` 를 import 하지 않음 · `service` 가 `fastapi` 를 import 하지 않음 · `providers` 가 `service`·`repository` 를 import 하지 않음 (TC-14) |
| 16 | 스키마 제약 | `test_schema_no_audio_blob.py` | 3 | 음성 본문 컬럼이 없다 · 판정 출처 네 컬럼이 `NOT NULL` · 리포트 응답 모델에 점수·백분위 필드가 없다 (TC-05, TC-10, TC-13) |
| 17 | 동의 업무 로직 | `test_account_service.py` | 5 | 동의 전 사용자 조회 · 동의 저장 · **같은 동의를 다시 보내도 처음 시각 유지** · 동의는 되돌아가지 않는다 · `service` 가 `HTTPException` 을 던지지 않는다 (BR2.1, BR2.2, SM-C) |

### 통합 시험 (표시 `integration`)

| # | 파일 | 개수 | 무엇을 덮는가 |
|---|---|---|---|
| 18 | `test_health_endpoint.py` | 4 | `status: ok` 와 `analysisMode` 를 함께 준다 · **저장소가 응답하지 않으면 정상이 아니다** · 확인 질의에 1초 제한 · **경과 시간 200ms 이내** (BR3.1, BR3.2, AC9.1.1, AC9.3.4, NFR3.1, NFR10.15) |
| 19 | `test_me_endpoint.py` | 3 | 인증 없이 고정 사용자 · 동의 전에는 동의 시각이 비어 있다 · **경과 시간 200ms 이내** (AC9.2.1, NFR3.2) |
| 20 | `test_consent_endpoint.py` | 4 | 첫 동의 저장 · 두 번째 동의가 시각을 갱신하지 않음 · 잘못된 본문은 422 + `details` · **경과 시간 200ms 이내** (BR2.2, NFR3.3) |
| 21 | `test_migration_applied.py` | 3 | 스키마가 **마이그레이션으로** 만들어졌다(모델에서 직접 만들지 않았다) · 테이블 20개가 존재한다 · 기동 흐름이 마이그레이션을 돌리지 않는다 (NFR14.3, NFR10.7) |
| 22 | `test_user_repository.py` | 3 | 사용자 조회 · 없는 사용자는 `None` 이 아니라 조회 결과 없음으로 구분 · `repository` 가 확정하지 않는다 (BR5.3) |
| 23 | `test_seed_states.py` | 4 | `base` 가 동의 전 사용자와 시나리오 원형을 넣는다 · `consented` 가 그 위에 쌓인다 · `s1-transcribed` 가 그 위에 쌓인다 · 값을 픽스처에서 읽는다 (BR2.1, BR4.3, `[contract]` C16) |

**합계**: 단위 **83개** · 통합 21개 — 모두 **104개**.

§3 의 구성 요소별 개수를 더한 값이다(6+5+5+5+7+6+7+4+5+6+4+4+5+3+3+3+5 = 83). 승인 시점의 이 줄은
**78** 로 적혀 있었고 그것은 산술 오류였다 — 구성 요소별 개수는 그대로이고 합계 줄만 틀렸으므로, 이 정정은
시험 범위를 늘리거나 줄인 것이 아니라 더한 값을 바로잡은 것이다 (검토 지적 R-01).

---

## 4. 커버리지 목표

| 대상 | 바닥 | 근거 |
|---|---|---|
| `backend/app/service/` 라인 커버리지 | **80% 이상** | `[practices]` Testing Posture (D-57), NFR14.2 |
| 저장소 전체 | 바닥 없음 | 같음 — 없던 자리에 바닥을 새로 세운 것이지 무언가를 좁힌 것이 아니다 |
| 분기 커버리지 | 바닥 없음 | 같음 |

**통과시키려고 이 바닥을 낮추지 않는다.** 바닥 자체의 검증은 `build-and-test`(3.6)가 하고, 이 단위는 자기
코드가 그 바닥을 넘게 유지한다 `[nfr]` NFR14.2.

---

## 5. 대역(mock)과 가짜 만들기 지침

| 무엇을 | 어떻게 | 왜 |
|---|---|---|
| STT·LLM 제공자 | **대역을 만들지 않는다.** 실제 `MockSttProvider` / `MockLlmProvider` 를 쓴다 | 그것들이 이미 고정 응답이다. 그 위에 또 대역을 쌓으면 픽스처 대조가 무의미해진다 |
| 저장소 | 통합 시험은 Testcontainers 로 **실제 PostgreSQL** | 인메모리 대체물은 방언 차이를 숨긴다 |
| 단위 시험의 저장소 | 저장소를 만지지 않는 코드만 단위로 시험한다 | 저장소가 필요하면 그 시험은 `integration` 이다 |
| 제공자 호출 감싸기의 외부 호출 | 호출 대상만 가짜로 둔다(타임아웃·4xx·성공을 흉내) | 감싸기 장치 자체를 시험하려면 그 아래가 통제 가능해야 한다 |
| 시각 | 동의 시각처럼 시간이 결과를 가르는 곳은 시각을 주입한다 | 시계에 기대면 간헐적으로 깨진다 |

**어떤 구현이 와도 통과하는 시험(`assert True` 류)을 쓰지 않는다** `[practices]`.

---

## 6. 시험 데이터 관리

| 항목 | 규약 |
|---|---|
| 기대 판정·전사 | `backend/app/fixtures/` 의 세 파일이 **단일 출처**. 시험 코드에 값을 옮겨 적지 않는다 `[practices]` NFR14.1 |
| 격리 | 컨테이너는 **세션당 1개**, 스키마는 세션 시작 시 `alembic upgrade head` 로 **한 번**, 시험마다 트랜잭션 후 되돌림 `[practices]` |
| `Base.metadata.create_all()` | **쓰지 않는다** — 그래야 마이그레이션이 실제로 한 번은 실행된다 `[practices]`, NFR14.3 |
| 시드 | 시험이 `scripts/seed.py` 의 상태 함수를 직접 부른다(별도 프로세스를 띄우지 않는다) |
| 실제 사용자 데이터 | **없다.** 전부 합성이다 `[constraint:SC-02]`, NFR11.1 |

---

## 7. 이름 규칙

`[practices]` Code Style 이 정한 경계를 그대로 쓴다.

- 판정 규칙 자체를 검증하는 시험 이름은 **한국어**(`def test_모르는_값이면_mock_으로_뜬다`).
- 기술적·배관 동작(상태 코드, 직렬화, 권한, 마이그레이션)을 검증하는 시험 이름은 **영어**.
- 파일 이름, 픽스처 이름, 클래스 이름, 표시, 파라미터화 id 는 **전부 영어**. 픽스처 이름은 다른 시험의 매개변수
  이름이 되므로 여기에 한국어가 들어오면 규칙이 바로 깨진다.
