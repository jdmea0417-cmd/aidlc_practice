# Discovered Rules — SCD 소통 코칭 MVP

확인 게이트에서 승인되면 이 문서의 `## Mandated` / `## Forbidden` 항목이
`aidlc/spaces/default/memory/project.md` 의 같은 이름 절에 도장이 찍혀 올라간다.

항목을 적게 유지했다. 여기 올린 것은 앞 단계에서 이미 닫힌 **확정 제약**과 인터뷰에서
사람이 직접 고른 **하드 제약**을 코드 작성 규칙의 말로 옮긴 것뿐이고, 취향이나 권고는
`team-practices.md` 에 남겼다. 어겼을 때 무엇이 깨지는지가 분명하지 않은 항목은 올리지
않았다.

**각 항목은 정확히 한 줄이다.** 승격 도구가 절 안의 비어 있지 않은 줄을 각각 하나의
규칙으로 취급하므로, 한 규칙을 여러 줄로 나누면 `project.md` 에 조각나 들어간다.

## Sources

| 태그 | 출처 |
|---|---|
| `[constraint]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/feasibility/constraint-register.md` |
| `[raid]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/feasibility/raid-log.md` |
| `[Q<n>]` / `[FU<n>]` | `practices-discovery-questions.md` — 사람이 확정한 인터뷰 답변 |
| `[spec:02]` | `docs/input/02_tech-environment.md` |
| `[spec:05]` | `docs/input/05_synthetic-test-data.md` |
| `[org]` | `aidlc/spaces/default/memory/org.md` |
| `[phase]` | `aidlc/spaces/default/memory/phases/construction.md` |
| `[devsecops]` | `contributions/aidlc-devsecops-agent.md` |
| `[log]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/approval-handoff/decision-log.md` — 결정 ID 와 결정이 바뀐 이력 |

## Mandated

- ALWAYS `api` → `service` → `repository` 순서로만 호출하고 영속성 접근은 반드시 `service` 를 경유한다. 건너뛰면 삭제 전파와 권한 검사가 누락된다 `[constraint:TC-14][spec:02 §5][raid:R3]`
- ALWAYS STT·LLM 은 `SttProvider` / `LlmProvider` 인터페이스 뒤에서만 호출하고 기본 실행 경로는 `ANALYSIS_MODE=mock` 으로 둔다 `[constraint:TC-06][constraint:SC-04]`
- ALWAYS `ANALYSIS_MODE` 가 미설정·빈 값·모르는 값이면 `mock` 으로 동작하고 `live` 인데 키가 없으면 기동을 거부한다. 조용히 `mock` 으로 되돌아가거나 첫 요청에서 터지게 두지 않는다 `[constraint:SC-04][raid:A3][devsecops §5]`
- ALWAYS 전사 텍스트는 프롬프트에서 구분자로 감싼 데이터 블록으로만 전달하고, 넣기 전에 전사에서 구분자 시퀀스를 제거하거나 이스케이프한다. 데이터가 구분자를 포함할 수 있으면 그 구분자는 경계가 아니다 `[constraint:TC-08][devsecops §4]`
- ALWAYS LLM 판정 결과를 저장할 때 모델명·프롬프트 버전·기준 버전을 함께 저장하고, 응답 모델 검증에 실패한 출력은 강제 변환하지 않고 거부한다 `[constraint:TC-10][devsecops §4]`
- ALWAYS 비밀값과 API 키는 backend 환경변수로만 다루고 저장소에 커밋하지 않는다 `[spec:02 §4][phase]`
- ALWAYS `docs/input/05_synthetic-test-data.md` 의 기대 판정을 픽스처 파일로 고정하고 판정 관련 단위 테스트가 그 파일을 읽는다. 기대값을 테스트 코드에 직접 적지 않는다 `[FU2][spec:05]`
- ALWAYS `backend/app/service/` 의 라인 커버리지를 80% 이상으로 유지한다. 통과시키려고 이 바닥을 낮추지 않는다 `[Q4][org]`
- ALWAYS 병합 전에 GitHub Actions 검사를 통과한다. 검사가 통과하지 않은 PR 은 `main` 에 병합하지 않는다 `[Q1][FU3]`
- ALWAYS 사람이 읽는 것 — 산출물, 질문, UI 문구, 커밋 메시지 — 은 한국어로 쓴다 `[constraint:OC-06]`

## Forbidden

- NEVER 프론트엔드에서 STT·LLM API 를 직접 호출한다. 키가 노출되고 호출 기록이 누락된다 `[constraint:TC-07]`
- NEVER ORM 모델을 API 응답으로 그대로 반환한다. Pydantic 응답 모델로 바꿔 내보낸다 `[constraint:TC-14][spec:02 §5]`
- NEVER 음성 파일을 DB BLOB 으로 저장한다. 파일 저장소 + 메타데이터 테이블로 관리한다 `[constraint:TC-05]`
- NEVER 종합점수·백분위를 계산하는 코드를 만든다. 행동별 상태와 기회 수 집계까지만 한다 `[constraint:TC-13]`
- NEVER 이번 범위에서 LangChain 류 오케스트레이션 프레임워크, Neo4j·벡터DB, Redux 류 전역 상태 관리 라이브러리를 도입한다 `[constraint:TC-11][constraint:TC-12][spec:02 §5]`
- NEVER 실제 사용자 데이터를 수집하거나 저장소·픽스처에 넣는다. 모든 데이터는 합성 데이터다 `[constraint:SC-02]`
- NEVER `ANALYSIS_MODE=live` 를 합성 데이터가 아닌 대화에 대해 켠다. live 는 전사 텍스트를 제3자에게 보내는 경로이고, 한 번이라도 SC-02 가 깨지면 규제 항목을 기록하지 않기로 한 결정이 함께 무효가 된다 `[constraint:SC-02][raid:A2][devsecops §7]`
- NEVER 전사 텍스트나 LLM 출력을 `dangerouslySetInnerHTML` 로 렌더링한다. LLM 출력발 저장형 XSS 가 된다 `[constraint:TC-08][devsecops §4]`

## 여기 올리지 않은 것

아래는 규칙으로 굳히지 않고 다른 자리에 두기로 판단한 항목이다. 판단 근거는
`evidence.md` 의 "통합하지 않은 반대 의견과 그 이유"에 있다.

ORM(SQLAlchemy 2.0 동기)·마이그레이션(Alembic)·패키지 관리자(uv)는 인터뷰에서 확정되었고
`[Q6][constraint:TC-15][raid:D3]`, 도구 선택이므로 `team-practices.md` 의 `## Code Style`
이 단일 출처다. 규칙 절에는 올리지 않는다.

| 후보 | 왜 여기 두지 않았는가 |
|---|---|
| 잠금 파일 커밋, Ruff 규칙 집합, mypy 설정, 계층 역방향 import 금지, 제공자 예외 변환 | 확정 제약에서 파생된 **도구 설정과 코드 규약**이다. `team-practices.md` `## Code Style` 이 단일 출처이고, 같은 내용을 규칙 절에 복제하면 어느 쪽이 기준인지 흐려진다 |
| 삭제 전파의 단일 진입점과 파일·행 순서 | 최종 경계 정의는 domain-design(2.6)이 닫기로 되어 있다 `[constraint:TC-14][raid:R3]`. 그때까지 코드가 따를 **잠정 규칙**으로 `team-practices.md` `## Code Style` 에 두었다. **domain-design(2.6)이 계층 경계를 닫은 뒤 이 항목의 규칙 승격 여부를 다시 판단한다** — 판단 시점은 2.6 완료 직후이고, 미루면 그 사이에 쌓인 코드가 잠정 규칙에 고착된다. **그 재판단의 중요도는 이번 회차에 올라갔다**: F07(정정·삭제)이 Should 에서 Must 로 올라가면서 `[log §5-2]`(D-59), 삭제 전파는 이제 Must 경로 위에 있다. Should 였을 때는 경계 정의가 늦어도 감당할 수 있었지만, Must 가 된 지금은 경계가 늦게 닫히면 시연 필수선이 직접 흔들린다 `[FU4]` |
| `LlmProvider` 가 프롬프트 식별자와 데이터를 분리해 받는 인터페이스 모양 | 인터페이스 시그니처는 contract-design(2.8)과 domain-design(2.6)이 닫는 자리다. 요구 자체는 위 TC-08 규칙이 이미 담고 있다 |
| 테스트 함수명 한국어 허용 | 허용이지 의무가 아니다. 허용 경계(함수 이름에만, 판정 규칙 검증은 한국어·기술 동작 검증은 영어)는 `team-practices.md` `## Code Style` 에 있다 |
| squash-merge, 브랜치 수명, PR 리뷰 | `org.md` 의 `## Way of Working` 이 이미 담고 있고 `team-practices.md` 가 구체화한다. 중복 규칙을 만들지 않는다. 실제로 막는 장치는 위 `## Mandated` 의 GitHub Actions 항목이다 |
| 분기 커버리지 바닥 | 사람이 `[Q4]` 에서 라인 80% 하나만 두기로 선택했다. 두지 않기로 한 결정이며 빠뜨린 것이 아니다 |

**이번 되돌리기 회차(2026-09-17)가 이 문서에 남긴 것** `[FU4][log §5-2]` — 규칙 18건
(`## Mandated` 10건, `## Forbidden` 8건) 자체는 **한 건도 바뀌지 않았다**. 항목도 문구도
근거 태그도 그대로다. 이번 회차가 바꾼 것은 위 표의 **재판단 대상이 명확해졌다는 것
하나**다 — 삭제 전파 항목이 어느 단계가 닫은 뒤(domain-design 2.6) 무엇을 다시 판단하는지,
그리고 왜 그 판단이 전보다 더 중요해졌는지(F07 의 Must 승격, D-59)가 표에 적혔다. 승격
대상 목록은 이전 회차와 동일하므로, 확인 게이트가 승인하는 규칙 집합도 동일하다.
