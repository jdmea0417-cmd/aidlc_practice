# Feasibility & Constraints — 확인 질문

**Stage**: feasibility (1.3)
**Depth**: Standard
**작성일**: 2026-09-16

## Sources

- `[intent]` — `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/intent-capture/intent-statement.md` (확정된 의도 서술)
- `[desc]` — 워크플로 시작 시 사용자가 입력한 프로젝트 설명
- `[spec:02]` — `docs/input/02_tech-environment.md` (기존 명세: 기술 환경)
- `[spec:01]` — `docs/input/01_vision.md` (기존 명세: 비전·MVP 범위·미결정 기본값)
- `[spec:07]` — `docs/input/07_decision-log.md` (기존 명세: 결정 기록 D-01~D-06, 가정 A-01~A-12)

market-research(1.2)는 이번 범위에서 실행하지 않으므로 `competitive-analysis`,
`market-trends`, `build-vs-buy`는 입력으로 존재하지 않는다.

---

## Q1. Java core + Python analysis 2-서비스 구성을 그대로 갑니까?

기존 명세 `[spec:02]`는 core(Java 21 / Spring Boot 3.3)와 analysis(Python 3.11 /
FastAPI)를 나누고, 결정 D-01은 "Java–Python 연동이 불가능하다고 판단되면 React +
FastAPI + PostgreSQL 단일 백엔드로 전환한다"는 분기를 남겨 두었습니다 `[spec:07]`.
이 분기를 지금 닫아야 이후 단계(도메인 설계, 단위 분해, 계약 설계)가 갈라지지 않습니다.

- A. 2-서비스 구성을 유지한다 (core=Java, analysis=Python, 그 사이는 REST/JSON)
- B. 대체안으로 전환한다 (React + Python FastAPI + PostgreSQL 단일 백엔드)
- C. core=Java 단일로 시작하고, analysis는 Java 안의 Mock 구현으로 두었다가 나중에 분리한다
- D. 아직 판단할 근거가 부족하다 — 이번 단계에서 양쪽 난이도를 먼저 비교해 달라
- X. Other (please specify)

[Answer]: B. 대체안으로 전환한다 (React + Python FastAPI + PostgreSQL 단일 백엔드)

---

## Q2. 기존 명세가 적어 둔 버전 조합을 그대로 확정합니까?

`[spec:02]`의 Java 21 / Spring Boot 3.3 / React 18 + TypeScript 5 + Vite 5 /
PostgreSQL 16 / Python 3.11 + FastAPI 조합은 AI가 "일반적 최신 안정 조합"으로 적어 둔
값이고, 아직 사용자가 확인하지 않은 가정(A-09)으로 남아 있습니다 `[spec:07]`.

- A. 그대로 확정한다
- B. 확정하되 Java 버전만 바꾼다 (사용 중인 버전을 함께 적어 주세요)
- C. 확정하되 Node/React 계열만 바꾼다 (사용 중인 버전을 함께 적어 주세요)
- D. 지금 개발 머신에 설치된 버전을 먼저 확인한 뒤 맞춘다
- X. Other (please specify)

[Answer]: A. 그대로 확정한다

---

## Q3. 로컬 실행 환경에 제약이 있습니까?

`[desc]`와 `[spec:02]`는 클라우드 배포 없이 Docker Compose(frontend, core, analysis,
postgres 네 컨테이너)로만 돌리기로 정해 두었습니다. 컨테이너 네 개와 Gradle·Vite 빌드가
동시에 도는 환경이라, 실제로 그렇게 돌릴 수 있는지가 이후 설계의 전제가 됩니다.

- A. 제약 없다 — Docker Desktop(또는 동등한 런타임)이 있고 컨테이너 4개를 돌릴 수 있다
- B. Docker는 쓸 수 있지만 메모리·성능이 빠듯하다 — 컨테이너 수를 줄이는 방향을 고려해 달라
- C. Docker를 쓸 수 없다 — 각 서비스를 호스트에서 직접 실행하는 방식이 필요하다
- D. WSL2 환경이라 파일 I/O·포트 관련 제약을 함께 고려해야 한다
- X. Other (please specify)

[Answer]: A. 제약 없다 — Docker Desktop(또는 동등한 런타임)이 있고 컨테이너 4개를 돌릴 수 있다

---

## Q4. 일정과 투입 인원은 어떻게 됩니까?

의도 서술은 이 작업을 "AI-DLC 워크플로 검증을 겸한 테스트 MVP"로 규정합니다 `[intent]`.
남은 단계의 깊이(문서 분량, 테스트 분량, 단위 분해 수)를 정하려면 쓸 수 있는 시간과
사람이 몇인지가 필요합니다.

- A. 1인(사용자 본인) + AI, 기한 없음 — 끝까지 가는 것이 목적이다
- B. 1인 + AI, 기한 있음 (기한을 함께 적어 주세요)
- C. 여러 명이 나눠 작업한다 (인원과 역할을 함께 적어 주세요)
- D. 시연·제출 등 외부 마감이 있다 (일자를 함께 적어 주세요)
- X. Other (please specify)

[Answer]: D. 시연·제출 등 외부 마감이 있다

---

## Q5. 개인정보·규제 제약을 이번 MVP에서 어느 수준까지 다룹니까?

이번 테스트는 합성 데이터만 쓰므로 실제 규제 적용 대상이 아닙니다 `[intent]`. 다만 주
사용자가 13–18세 전원 미성년자이고, 보호자 열람 권한(NONE/SUMMARY/FULL)과 정정·삭제
기능(F07)이 MVP 범위 안에 있습니다 `[intent]`. 이 둘을 "설계 제약으로 기록만 할지",
"이번 구현에서 실제로 동작시킬지"가 갈립니다.

- A. 제약으로 기록만 한다 — 개인정보보호법·아동청소년 관련 요건은 constraint register에 적고, 이번 구현은 합성 데이터 전제로 최소한만 만든다
- B. 기록하고 핵심은 구현한다 — 보관기한·삭제 전파·권한 제어가 합성 데이터 위에서 실제로 동작하게 만든다
- C. 기록하지 않는다 — 합성 데이터 전용 테스트이므로 규제 항목은 이번 범위에서 제외한다
- D. 기록하고 구현하되, 암호화·감사로그까지 포함한다
- X. Other (please specify)

[Answer]: C. 기록하지 않는다 — 합성 데이터 전용 테스트이므로 규제 항목은 이번 범위에서 제외한다

---

## Q6. 운영 파라미터의 기본값을 확정합니까?

`[spec:01]`이 "사용자가 확정한 값이 아니다"라고 명시한 테스트용 기본값들입니다
(A-05, A-06, A-07, A-08) `[spec:07]`. 이 값들은 이후 NFR과 도메인 설계에 그대로
들어가므로 지금 확정하거나 바꿔야 합니다.

현재 값: 녹음 최대 5분 / Mock 분석 응답 3초 이내 / "비교 불충분" 기준은 유효 기회 3회 미만 / 원음 보관 기본 30일.

- A. 네 값을 모두 그대로 확정한다
- B. 모두 확정하되 원음 보관 기간만 바꾼다 (원하는 값을 함께 적어 주세요)
- C. 모두 확정하되 녹음 최대 길이만 바꾼다 (원하는 값을 함께 적어 주세요)
- D. 설정값으로만 두고 지금은 확정하지 않는다 — 기본값은 유지하되 언제든 바꿀 수 있게 한다
- X. Other (please specify)

[Answer]: D. 설정값으로만 두고 지금은 확정하지 않는다 — 기본값은 유지하되 언제든 바꿀 수 있게 한다

---

## Q7. STT·LLM의 실제 연동 어댑터를 이번 범위에서 어디까지 만듭니까?

`[spec:02]`는 `SttProvider` / `LlmProvider` 인터페이스를 두고 기본 구현은 Mock,
실제 제공자 연결은 `ANALYSIS_MODE=mock|live` 환경변수로 전환한다고 적었습니다.
`[spec:01]`은 "실제 연동 어댑터는 설정으로 교체 가능하게 설계만 한다"고 적었습니다.
"설계만"의 범위가 인터페이스까지인지 빈 구현체까지인지가 코드 생성 단계에서 갈립니다.

- A. 인터페이스와 Mock 구현만 만든다 — live 구현체는 만들지 않는다
- B. 인터페이스 + Mock + live 구현체의 골격(미구현 스텁)까지 만든다 — 실제 호출은 하지 않는다
- C. live 구현체를 실제로 동작하게 만든다 (사용할 제공자를 함께 적어 주세요)
- D. Mock만 만들고 인터페이스 분리도 하지 않는다 — 나중에 리팩터링한다
- X. Other (please specify)

[Answer]: C. live 구현체를 실제로 동작하게 만든다

---

## 후속 질문 (모순 해소 및 미기재 값)

Q1~Q7 답변을 교차 검토한 결과 두 건의 모순과 두 건의 미기재 값이 발견되어 후속 질문을 추가한다.

---

## F1. Q1(대체안 전환)과 Q2(버전 조합 그대로 확정)가 충돌합니다. 어느 쪽을 살립니까?

Q1 에서 **B. React + Python FastAPI + PostgreSQL 단일 백엔드로 전환**을 고르셨는데,
Q2 에서는 Java 21 / Spring Boot 3.3 이 포함된 조합을 **A. 그대로 확정**으로 고르셨습니다.
단일 백엔드로 가면 Java 쪽 항목은 성립하지 않습니다.

Q1=B 가 무효로 만드는 **이미 확정된 항목**은 다음과 같습니다.

| 대상 | 확정 내용 | 전환 시 |
|---|---|---|
| `[spec:07]` D-01 | "React + Java(Spring Boot) 기반, 분석은 Python 서비스로 연동" (상태: 확정) | 상태를 "변경됨 → D-xx"로 바꾸고 새 항목 추가 |
| `[spec:02]` 2장 | Backend(core) = Java 21, Spring Boot 3.3, Spring Web, Spring Data JPA, Bean Validation, Flyway / Build = Gradle(Kotlin DSL) | 전부 무효. FastAPI + SQLAlchemy(또는 동등) + Alembic 으로 대체 |
| `[spec:02]` 2장 | API 문서 = springdoc-openapi | FastAPI 내장 OpenAPI 로 대체 |
| `[spec:02]` 3장 | core 단위 = JUnit 5·AssertJ·Mockito / core API = Spring Boot Test·MockMvc·Testcontainers | pytest 계열로 대체 |
| `[spec:02]` 5장 | 금지사항 "analysis 서비스의 DB 직접 접근 금지" | 단일 백엔드에서는 분리 자체가 사라져 무의미해짐 |
| `[spec:02]` 5장 | 금지사항 "JPA 엔티티를 API 응답으로 반환 금지" | Pydantic 응답 모델 규칙으로 다시 씀 |
| `[spec:02]` 6장 | 패키지 구조 `core/src/main/java/kr/scdcoach/**` 전체 | Python 패키지 구조로 다시 씀 |
| `[spec:02]` 7장 | Java 코드 예시 3건(ReportController, BehaviorSummary, BehaviorSummaryTest) | Python 예시로 다시 씀 |
| Q3 답 | 컨테이너 4개(frontend, core, analysis, postgres) | 3개(frontend, backend, postgres)로 줄어듦 |

- A. 전환을 확정한다 — 위 표의 Java 항목을 모두 무효로 하고, 버전 확정은 React 18 / TypeScript 5 / Vite 5 / PostgreSQL 16 / Python 3.11 + FastAPI 에만 적용한다. 컨테이너는 3개로 줄인다
- B. 전환을 확정하되 Python 버전을 올린다 (원하는 버전을 함께 적어 주세요)
- C. 전환을 취소한다 — Q1 을 A(2-서비스 유지)로 되돌리고 Q2 의 "그대로 확정"을 그대로 살린다
- D. 지금 정하지 않는다 — 두 안의 작업량·난이도 비교를 먼저 보고 결정하겠다
- X. Other (please specify)

[Answer]: A. 전환을 확정한다 — Java 항목을 모두 무효로 하고, 버전 확정은 React 18 / TypeScript 5 / Vite 5 / PostgreSQL 16 / Python 3.11 + FastAPI 에만 적용한다. 컨테이너는 3개로 줄인다

---

## F2. Q7(live 실제 구현)이 확정된 의도 서술과 충돌합니다. 어떻게 정리합니까?

Q7 에서 **C. live 구현체를 실제로 동작하게 만든다**를 고르셨습니다. 그런데 승인된 의도
서술은 실제 연동을 명시적으로 범위 밖에 두고 있습니다.

Q7=C 가 건드리는 **이미 확정된 항목**은 다음과 같습니다.

| 대상 | 확정 내용 | live 구현 시 |
|---|---|---|
| `[intent]` Initiative Trigger | "실제 사용자 데이터 수집, 클라우드 배포, 실제 STT·LLM 연동은 이 목적에 필요하지 않다" | 이 문장을 고쳐야 함 |
| `[spec:01]` 4장 테스트 조건 | "STT·LLM은 Mock 구현을 기본값으로 하고, 실제 연동 어댑터는 설정으로 교체 가능하게 설계만 한다" | "설계만"이 깨짐 |
| `[intent]` 성공 기준 SM1 | 합성 대화 3건의 종단 실행이 성공하면 통과 | live 결과는 `05_synthetic-test-data.md` 의 기대 판정과 일치한다는 보장이 없어, SM1 을 무엇으로 검증할지 다시 정해야 함 |
| Q6 답 | "Mock 기준 분석 3초 이내"를 설정값으로 유지 | live 응답시간에는 적용할 수 없어 별도 목표가 필요함 |
| `[spec:02]` 4장 | "API 키는 analysis 서비스 환경변수에만 둔다" | F1 에서 단일 백엔드로 가면 키 보관 위치를 다시 정해야 함 |
| 새로 생기는 제약 | — | API 키 발급·비용·네트워크 의존·요청 실패 처리 |

- A. live 를 만들되 기본 실행과 SM1 검증은 Mock 으로 유지한다 — live 는 `ANALYSIS_MODE=live` 로만 켜지는 선택 경로
- B. live 를 기본값으로 올린다 — 성공 기준 SM1 도 live 결과 기준으로 다시 정의한다
- C. live 확정을 취소한다 — Q7 을 B(인터페이스 + Mock + live 스텁)로 내린다
- D. live 확정을 취소한다 — Q7 을 A(인터페이스 + Mock 만)로 내린다
- X. Other (please specify)

[Answer]: A. live 를 만들되 기본 실행과 SM1 검증은 Mock 으로 유지한다 — live 는 `ANALYSIS_MODE=live` 로만 켜지는 선택 경로

---

## F3. live 어댑터를 만든다면 어느 제공자를 씁니까?

Q7 의 선택지 C 는 "사용할 제공자를 함께 적어 주세요"였는데 제공자가 비어 있습니다.
STT 와 LLM 은 서로 다른 제공자를 쓸 수 있습니다. (F2 에서 live 를 취소하면 이 질문은
무효가 됩니다.)

- A. STT·LLM 모두 OpenAI (Whisper + GPT)
- B. STT 는 OpenAI Whisper, LLM 은 Anthropic Claude
- C. 로컬 오픈소스 (faster-whisper + 로컬 LLM) — API 키·비용 없음
- D. 아직 정하지 않았다 — 인터페이스만 맞춰 두고 제공자는 나중에 고른다
- X. Other (please specify)

[Answer]: D. 아직 정하지 않았다 — 인터페이스만 맞춰 두고 제공자는 나중에 고른다

---

## F4. 외부 마감은 언제입니까?

Q4 에서 **D. 시연·제출 등 외부 마감이 있다**를 고르셨는데 일자가 비어 있습니다. 남은
단계의 문서 분량과 테스트 분량을 이 값에 맞춰 조절합니다.

- A. 1주 이내
- B. 2주 이내
- C. 1개월 이내
- D. 1개월 초과
- X. Other (please specify)

[Answer]: X. 11월 5일까지, 개발 인원 5인

---

## 추가 후속 질문 (F4 답변에서 새로 드러난 사실)

F4 답변으로 **마감 2026-11-05, 개발 인원 5인**이 확인되었다. Q4 에서는 인원 정보가 없었고
team-formation(1.5)은 이번 범위에서 실행하지 않으므로, 인원과 역량은 이 단계에서 확정한다.

---

## F5. 5인의 Python·FastAPI 경험은 어느 정도입니까?

결정 D-01 의 원래 근거는 사용자 답변 원문 "현재 배운 것은 React+Java" 였습니다 `[spec:07]`.
그런데 F1 에서 백엔드를 Python 단일로 확정했으므로, 팀이 실제로 Python 으로 백엔드를
작성할 수 있는지가 이번 일정(7주) 안에서 가장 큰 기술 위험이 됩니다.

- A. 대부분 Python·FastAPI 경험이 있다 — 위험 낮음
- B. 일부만 경험이 있다 — 경험자가 백엔드를 맡고 나머지는 프론트로 배치한다
- C. 거의 없다 (React+Java 배경) — 학습 시간을 일정에 포함해야 한다
- D. 개인차를 아직 모른다 — 일단 위험으로 기록하고 진행한다
- X. Other (please specify)

[Answer]: X. 전원 AI의 도움을 받으며 진행, 일부 Python 경험

---

## F6. 5인의 역할을 어떻게 나눕니까?

team-formation(1.5)이 이번 범위에서 실행되지 않으므로 여기서 확정합니다. 이후
delivery-planning(2.9)의 작업 단위 병렬화와 소유권 배정에 그대로 쓰입니다.

- A. 프론트엔드 2 / 백엔드 3
- B. 프론트엔드 1 / 백엔드 3 / QA 1
- C. 전원 풀스택 — 작업 단위별로 그때그때 나눈다
- D. 아직 나누지 않았다 — 제안해 달라
- X. Other (please specify)

[Answer]: C. 전원 풀스택 — 작업 단위별로 그때그때 나눈다

---


## F7. 이번에 무엇을 고칩니까? (해당하는 것 모두 선택)

이 단계가 끝난 뒤 practices-discovery(2.2)와 계획 변경에서 사실이 달라졌다. 아래는
그 대조 결과이며, 어디까지 반영할지 정한다.

**달라진 것 1 — 미확정이던 도구 3종이 확정되었다.** practices-discovery 에서
**SQLAlchemy 2.0(동기) / Alembic / uv** 로 확정되었다. 지금 문서는 제약 TC-15 를
"아직 정하지 않았다(미확정)"로, 의존 D3 를 "practices-discovery(2.2) 또는
domain-design(2.6)에서 확정"으로 열어 둔 채다. 둘 다 닫혔다.

**달라진 것 2 — 원격 저장소와 GitHub Actions 가 전제로 들어왔다.** 병합 전 검사를
GitHub Actions 로 강제하기로 했고, CI 파이프라인 단계(3.7)가 계획에 다시 들어가
그 워크플로를 만든다. 지금 문서에는 원격 저장소·GitHub 계정이 있어야 한다는 전제가
어디에도 없다. 이 전제가 막히면 병합 게이트와 작업 분기 흐름을 다시 짜야 한다.
범위 제약 SC-01(클라우드 배포 없음)과는 충돌하지 않는다 — Actions 는 배포가 아니라
검사다.

**달라진 것 3 — 실행 단계가 20 에서 21 로 늘었다.** 위험 R7 은 19 → 20 증가만
기록하고 있다. ci-pipeline(3.7) 재삽입으로 한 번 더 늘었고, 마감 2026-11-05 과
위험 R5 는 그대로다.

**달라진 것 4 — 판정 정확성을 지키는 수단이 좁아졌다.** 위험 R6 의 대응 방안은
"집계 규칙을 별도 단위 테스트로 직접 검증한다"였다. practices-discovery 에서 테스트는
전부 구현 후에 쓰고(test-after), 커버리지 바닥은 `service/` 라인 80% 하나만 걸며,
종단 실행은 기대 판정과 대조하지 않기로 확정되었다. 그 단위 테스트에 분기 바닥이
없으므로, 집계 함수가 한 갈래만 타도 바닥을 통과한다. 대신 기대 판정을 픽스처 파일로
고정하는 의무가 새로 들어왔다.

- A. TC-15 와 D3 를 확정 상태로 바꾼다 — SQLAlchemy 2.0(동기) / Alembic / uv
- B. 원격 저장소·GitHub Actions 전제를 가정으로 추가한다 — 막혔을 때 무엇이 깨지는지 함께 적는다
- C. 위험 R7 을 20 → 21 로 갱신한다
- D. 위험 R6 의 대응 방안을 확정된 테스트 방침에 맞게 다시 쓴다 — 픽스처 고정이 들어오고 분기 바닥은 없다는 사실을 함께 적는다
- E. 고칠 것이 없다 — 현재 내용 그대로 검토와 승인으로 넘어간다
- X. Other (please specify)

[Answer]: A, B, C, D

---

## Consolidated Summary Confirmation

이번 Modify 회차에서 확정된 내용입니다.

**이번에 고치는 것 (F7 = A, B, C, D)**

- 제약 TC-15: "미확정"에서 "확정"으로. ORM 은 SQLAlchemy 2.0(동기), 마이그레이션은 Alembic, 패키지 관리자는 uv [F7]
- 의존 D3: 해소됨으로 표기. practices-discovery(2.2)에서 닫혔고 더 이상 백엔드 코드 생성을 차단하지 않는다 [F7]
- 새 가정 추가: 원격 저장소(GitHub 등)를 만들 수 있고 GitHub Actions 를 쓸 수 있다. 막히면 병합 게이트와 작업 분기 흐름을 다시 짜야 한다. 확인 방법은 저장소 생성 시점에 실제로 만들어 보는 것 [F7]
- 새 기술 제약 추가: 병합 전 검사는 GitHub Actions 가 강제하며 그 워크플로는 ci-pipeline(3.7)이 만든다. SC-01(클라우드 배포 없음)과 충돌하지 않음을 함께 적는다 [F7]
- 위험 R7: 19 → 20 에서 19 → 20 → 21 로 갱신. ci-pipeline 재삽입분을 더하고, delivery-planning(2.9)의 일정 재검증에 두 증가분을 모두 넣는다 [F7]
- 위험 R6: 대응 방안을 확정된 테스트 방침에 맞게 다시 쓴다. 테스트는 구현 후에 쓰고, 커버리지 바닥은 `service/` 라인 80% 하나뿐이라 집계 함수의 분기를 강제하지 않으며, 대신 기대 판정을 픽스처 파일로 고정하는 의무가 새로 들어왔다 [F7]

**이번에 고치지 않는 것 (앞 회차 확정 그대로 유지)**

- 타당성 판정 자체(진행 가능), 스택 확정 TC-01~TC-03, 컨테이너 3개 TC-04
- 범위 제약 SC-01~SC-08. F07 이 Must 로 올라간 것은 등급 변경이며 `scope-document.md` 소관이다. SC-03 은 F01~F07 을 등급 없이 나열하므로 충돌하지 않는다
- 조직·일정 제약 OC-01~OC-06, 규제 제약(없음 — Q5 결정), 운영 파라미터 PM-01~PM-04
- 위험 R1~R5, 가정 A1~A5, 현안 I1~I4, 의존 D1·D2·D4·D5
- 세 산출물의 `## Assumptions & Open Questions`: None.

- Looks correct
- Request changes

[Answer]: Looks correct
