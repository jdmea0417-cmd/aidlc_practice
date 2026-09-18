# Approval & Handoff — 확인 질문

**Stage**: approval-handoff (1.7)
**Depth**: Standard
**작성일**: 2026-09-16

## Sources

| 태그 | 출처 |
|---|---|
| `[intent]` | `.../ideation/intent-capture/intent-statement.md` |
| `[stake]` | `.../ideation/intent-capture/stakeholder-map.md` |
| `[scope]` | `.../ideation/scope-definition/scope-document.md` |
| `[backlog]` | `.../ideation/scope-definition/intent-backlog.md` |
| `[feas]` | `.../ideation/feasibility/feasibility-assessment.md` |
| `[constraint]` | `.../ideation/feasibility/constraint-register.md` |
| `[raid]` | `.../ideation/feasibility/raid-log.md` |
| `[spec:02]` | `docs/input/02_tech-environment.md` (기존 명세) |
| `[log]` | `docs/decisions/decision-log.md` |

market-research(1.2), team-formation(1.5), rough-mockups(1.6)은 이번 범위에서
실행하지 않는다. 따라서 `competitive-analysis`, `team-assessment`, `wireframes`는
입력으로 존재하지 않으며, 그 부재는 결손이 아니라 범위 밖이다.

**이미 확정되어 다시 묻지 않는 것**: 의도와 범위에 대한 이해관계자 합의(결정권자는
사용자 본인 단독) `[stake]`, 인력과 일정 확보(5인·2026-11-05) `[constraint]`,
위험 인지와 완화 방안(R1~R6) `[raid]`, 워크플로 단계 구성(D-08) `[log]`.

이 단계가 묻는 것은 **Inception 으로 넘기기 전에 닫아야 할 미결 사항**이다.

---

## Q1. 의도 서술의 STT·LLM 문장을 어떻게 갱신합니까?

승인된 의도 서술에는 "실제 사용자 데이터 수집, 클라우드 배포, **실제 STT·LLM
연동은 이 목적에 필요하지 않다**"고 적혀 있습니다 `[intent]`. 그런데 Feasibility
단계의 결정 D-36 은 live 어댑터를 선택 경로로 만들기로 했습니다. 이 어긋남이
`[raid]` 의 현안 I2 로 남아 있습니다.

- A. 지금 고친다 — 이 단계에서 `intent-statement.md` 의 해당 문장을 갱신하고 초안 요약서에도 갱신된 내용을 싣는다
- B. requirements-analysis(2.3)에서 고친다 — 여기서는 현안으로만 넘긴다
- C. 고치지 않는다 — 의도 서술은 승인 당시 기록으로 그대로 두고, 범위 문서의 SC-04(기본 실행은 Mock, live 는 선택 경로)가 실질 기준이 된다
- D. 의도 서술은 그대로 두되 초안 요약서에 "이 문장은 D-36 으로 대체되었다"를 명시한다
- X. Other (please specify)

[Answer]: A. 지금 고친다 — 이 단계에서 `intent-statement.md` 의 해당 문장을 갱신하고 초안 요약서에도 갱신된 내용을 싣는다

---

## Q2. 기존 명세 `02_tech-environment.md` 재작성을 언제 합니까?

`[spec:02]` 는 Java·Spring Boot 전제로 쓰여 있는데 결정 D-30 으로 백엔드가 Python
FastAPI 단일 서비스로 바뀌었습니다. 재작성 대상 9개 항목은 `[feas]` §2.1 표에
정리되어 있고, `[raid]` 의 현안 I3 와 위험 R2 가 이 표를 가리킵니다. 이 문서가
Inception 의 입력으로 쓰이므로 언제 고치는지가 하위 단계의 정확도를 좌우합니다.

- A. Inception 진입 전에 지금 — 핸드오프의 일부로 먼저 고친다
- B. practices-discovery(2.2)에서 — 개발 관행을 정하면서 기술 문서도 함께 손본다
- C. requirements-analysis(2.3) 진입 전에 — `[raid]` I3 에 적힌 대로
- D. domain-design(2.6)에서 — 실제로 설계에 쓸 때 고친다
- X. Other (please specify)

[Answer]: A. Inception 진입 전에 지금 — 핸드오프의 일부로 먼저 고친다

---

## Q3. 수용 기준(Given/When/Then)을 어디서 만듭니까?

user-stories(2.4)는 이번 워크플로에서 실행하지 않습니다 `[log]` D-08. 그런데
Inception 단계 지침은 수용 기준을 Given/When/Then 형식으로 쓰도록 요구합니다.
user-stories 가 없으면 그 일을 맡을 단계를 정해야 합니다.

- A. requirements-analysis(2.3)가 맡는다 — 요구사항마다 Given/When/Then 수용 기준을 함께 쓴다
- B. user-stories(2.4)를 다시 넣는다 — 승인 게이트에서 이 단계를 추가한다
- C. functional-design(3.1)이 맡는다 — 작업 단위별 상세 설계에서 함께 쓴다
- D. build-and-test(3.6)가 맡는다 — 테스트 설계와 함께 만든다
- X. Other (please specify)

[Answer]: B. user-stories(2.4)를 다시 넣는다 — 승인 게이트에서 이 단계를 추가한다

---

## Q4. 이데이션 종합 판정을 무엇으로 합니까?

초안 요약서에 실을 진행 권고입니다. 타당성 판정은 "실현 가능, 단 조건부 2건"이었고
`[feas]`, 그 두 건은 팀의 Python 역량(R1)과 7주 일정(R5)입니다 `[raid]`.

- A. 진행(Go) — 조건 없이 Inception 으로 넘어간다
- B. 조건부 진행 — 넘어가되, R1 과 R5 의 완화 조치가 Inception 초반에 실제로 잡히는지 확인한다는 조건을 명시한다
- C. 보류 — 스택 전환(D-30) 결정을 한 번 더 검토한 뒤 판단한다
- D. 중단 — 이 계획으로는 진행하지 않는다
- X. Other (please specify)

[Answer]: A. 진행(Go) — 조건 없이 Inception 으로 넘어간다

---

## Q5. 이번 회차에 부담이 더 늘었습니다. 종합 판정을 유지합니까?

Q4 에서 "진행(Go) — 조건 없이 Inception 으로 넘어간다"로 판정했습니다. 그 뒤
practices-discovery(2.2)와 이번 회차의 되돌리기에서 사실이 여러 개 달라졌고, 그중
셋은 부담을 늘리는 쪽입니다. 판정을 다시 확인할 자리입니다.

**부담을 늘린 것 세 가지**

| # | 변경 | 이전 | 지금 |
|---|---|---|---|
| 1 | F07(정정·삭제)이 Should 에서 Must 로 올라갔다 | Must 7 / Should 4 | Must 8 / Should 3 |
| 2 | Must 비율이 프레임워크 권고 60% 를 더 크게 넘었다 | 64% | 73% |
| 3 | ci-pipeline(3.7)을 계획에 다시 넣어 EXECUTE 단계가 한 번 더 늘었다 | 19 → 20 | 19 → 20 → 21 |

마감 **2026-11-05**, 인원 **5인**, 위험 R1(Python 학습)과 R5(7주 일정)는 그대로입니다.

**부담을 줄이거나 없앤 것 두 가지**

| # | 변경 | 효과 |
|---|---|---|
| 4 | ORM·마이그레이션 도구·패키지 관리자가 확정되었다 (SQLAlchemy 2.0 동기 / Alembic / uv) | 의존 D3 해소. 첫 작업 단위가 바로 실제 스택을 관통할 수 있다 |
| 5 | 테스트 방침과 배포 성공 판정이 확정되었다 (test-after, `service/` 라인 80%, 기대 판정 픽스처 고정) | 방법론이 하나로 단순해져 Python 이 처음인 팀에 얹히는 비용이 줄었다 |

**새로 들어온 전제 하나**

원격 저장소(GitHub 등)를 만들 수 있고 GitHub Actions 를 쓸 수 있어야 합니다(가정 A6).
막히면 병합 게이트와 ci-pipeline(3.7)의 산출물을 다시 짜야 합니다.

- A. 진행(Go) 을 유지한다 — 늘어난 부담은 관리 대상이며 판정을 바꾸지 않는다
- B. 조건부 진행으로 내린다 — delivery-planning(2.9)의 일정 재검증 결과를 조건으로 단다
- C. 진행하되 지금 범위를 줄인다 — Must 8개 중 무엇을 뺄지 여기서 정한다
- D. 보류한다 — 일정과 범위를 다시 보기 전에는 Inception 으로 넘어가지 않는다
- X. Other (please specify)

[Answer]: A. 진행(Go) 을 유지한다 — 늘어난 부담은 관리 대상이며 판정을 바꾸지 않는다

---

## Consolidated Summary Confirmation

이번 Modify 회차에서 확정된 내용입니다.

**판정** — 조건 없이 Inception 으로 진행(Go)을 유지한다. 늘어난 부담은 관리 대상으로 기록한다 [Q5]

**`initiative-brief.md` 에서 고치는 것**

- §5 범위 경계: F07 을 Should 에서 Must 로. 화면 항목을 C2~C5 에서 "C2~C4 와 C5 의 삭제 부분을 뺀 나머지"로. proto-Unit 을 Must 7/Should 4 에서 Must 8/Should 3 으로 바꾸고, Must 비율 73% 와 그 초과가 의도된 것임을 함께 적는다 [Q5]
- §6 확정된 기술 구성: SQLAlchemy 2.0(동기) / Alembic / uv 를 추가한다 [Q5]
- §8 위험: R3(삭제 전파)의 중요도가 올라갔음을 명시한다 — Must 경로 위로 옮겨갔다. R6 의 대응 방안을 확정된 테스트 방침으로 재작성한다. R7 을 19 → 20 → 21 로 갱신한다 [Q5]
- §9 계획 변경 기록: ci-pipeline(3.7) 재삽입을 두 번째 행으로 추가한다 [Q5]
- §10 Inception 첫 단계에서 이어질 일: 2.2 항목의 "ORM 선택이 여기 또는 2.6 에서 닫힌다"를 "이미 닫혔다"로 갱신한다 [Q5]
- §11 남은 미결 항목: 가정 A6(원격 저장소와 GitHub Actions 사용 가능)을 추가한다 [Q5]

**`decision-log.md` 에 추가하는 것** — 이번 회차의 결정: F07 승격과 C5 분할, Python 도구 3종 확정, ci-pipeline 재삽입, 테스트 방침과 배포 성공 판정, 종합 판정 유지 [Q5]

**단계 경계 검증** — `phase-check-ideation.md` 를 다시 실행한다. 산출물이 바뀌었으므로 이전 결과는 유효하지 않다

**고치지 않는 것 (앞서 확정된 그대로 유지)**

- 문제 정의, 대상 고객, 성공 기준 SM1 [Q1 of intent-capture]
- 제외 항목 9건, 인력과 일정(5인 / 2026-11-05) [Q4 of feasibility]
- 위험 R1·R2·R4·R5 의 서술과 대응
- Q1~Q4 의 확정 답변 — 의도 서술 갱신, 기술 명세 재작성, user-stories 추가, 진행(Go) 판정
- 세 산출물의 `## Assumptions & Open Questions`: None.

- Looks correct
- Request changes

[Answer]: Looks correct
