# Feasibility Assessment — SCD 소통 코칭

## Sources

이 문서의 모든 서술은 아래 출처를 가진다. 출처가 없는 서술은 쓰지 않는다.

| 태그 | 출처 |
|---|---|
| `[intent]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/intent-capture/intent-statement.md` — 승인된 의도 서술 |
| `[Q<n>]`, `[F<n>]` | `feasibility-questions.md` — 이 단계에서 사용자가 답한 내용 |
| `[spec:01]` | `docs/input/01_vision.md` (기존 명세) |
| `[spec:02]` | `docs/input/02_tech-environment.md` (기존 명세) |
| `[spec:04]` | `docs/input/04_domain-model.md` (기존 명세) |
| `[spec:05]` | `docs/input/05_synthetic-test-data.md` (기존 명세) |
| `[spec:07]` | `docs/input/07_decision-log.md` (기존 명세: 결정·가정 기록) |

market-research(1.2)는 이번 범위에서 실행하지 않으므로 선택 입력인
`competitive-analysis`, `market-trends`, `build-vs-buy`는 존재하지 않는다. 시장
근거가 필요한 판단은 이 문서에 넣지 않았다.

---

## 1. 판정 요약

**기술적으로 실현 가능하다.** 단, 아래 두 가지가 일정 안에서 관리되어야 한다.

| # | 판정 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | MVP 범위 F01~F07 을 로컬 환경에서 구현할 수 있는가 | 가능 | 외부 의존이 Mock 으로 대체되고 클라우드 배포가 없다 `[intent][Q3]` |
| 2 | 성공 기준 SM1(합성 대화 3건 종단 실행)을 검증할 수 있는가 | 가능 | Mock 이 기대 판정을 고정 반환하므로 결정적으로 재현된다 `[spec:02][F2]` |
| 3 | 선택한 기술 스택을 팀이 다룰 수 있는가 | **조건부** | 백엔드를 Python 으로 확정했으나 팀 배경은 React+Java 이고 Python 경험은 일부다 `[F1][F5][spec:07]` |
| 4 | 마감(2026-11-05) 안에 끝낼 수 있는가 | **조건부** | 약 7주, 5인 전원 풀스택. 스택 학습과 범위가 동시에 압박한다 `[F4][F6]` |

3번과 4번은 진행을 막는 사유가 아니라 **관리 대상 위험**이다. RAID 로그 R1, R2 로
기록했다.

---

## 2. 목표 아키텍처 (이번 단계에서 확정된 범위)

```
+---------------------------+       +------------------------------+
| React 18 + TS 5 + Vite 5  | REST  | Python 3.11 + FastAPI        |
| (모바일 웹, 375px 기준)    |------>| 단일 백엔드                   |
+---------------------------+ JSON  |  - 인증, 대화/전사/맥락        |
                                    |  - 목표/연습/기록/정정/삭제    |
                                    |  - 규칙 기반 집계             |
                                    |  - SttProvider/LlmProvider    |
                                    +---------------+--------------+
                                                    |
                                    +---------------+--------------+
                                    | PostgreSQL 16 | 로컬 파일 저장소 |
                                    | (JSONB 활용)   | (음성 원본)     |
                                    +---------------+--------------+
```

<!-- Text fallback: React 모바일 웹 프론트엔드가 REST/JSON 으로 Python FastAPI 단일 백엔드를 호출하고, 그 백엔드가 PostgreSQL 16 과 로컬 파일 저장소를 소유한다. STT·LLM 은 백엔드 안의 Provider 인터페이스 뒤에 있다. -->

Docker Compose 컨테이너는 **frontend, backend, postgres 3개**다 `[Q3][F1]`.

### 2.1 원래 명세에서 바뀐 것

결정 D-01 은 "React + Java(Spring Boot) 기반, 분석 기능은 Python 서비스로 연동.
연동 불가 시 React + FastAPI 로 전환"이라는 분기를 확정 상태로 두고 있었다
`[spec:07]`. 사용자는 이 단계에서 **대체안(단일 백엔드)** 을 선택했다 `[Q1][F1]`.

| 무효가 되는 확정 항목 | 대체 |
|---|---|
| D-01 의 Java 경로 (상태: 확정) `[spec:07]` | 상태를 "변경됨 → D-xx"로 바꾸고 새 항목 추가 |
| Backend(core) = Java 21, Spring Boot 3.3, Spring Web, Spring Data JPA, Bean Validation, Flyway `[spec:02]` | Python 3.11 + FastAPI + Pydantic v2 + ORM/마이그레이션 도구 |
| Build = Gradle (Kotlin DSL) `[spec:02]` | Python 패키지 관리 도구 |
| API 문서 = springdoc-openapi `[spec:02]` | FastAPI 내장 OpenAPI |
| core 테스트 = JUnit 5, AssertJ, Mockito, Spring Boot Test, MockMvc, Testcontainers `[spec:02]` | pytest, httpx TestClient, Testcontainers(Python) |
| 금지사항 "analysis 서비스의 DB 직접 접근" `[spec:02]` | 서비스 분리 자체가 사라져 무의미. 대신 계층 경계 규칙으로 다시 씀 |
| 금지사항 "JPA 엔티티를 API 응답으로 반환" `[spec:02]` | Pydantic 응답 모델 규칙으로 다시 씀 |
| 패키지 구조 `core/src/main/java/kr/scdcoach/**` `[spec:02]` | Python 패키지 구조로 다시 씀 |
| Java 코드 예시 3건 `[spec:02]` | Python 예시로 다시 씀 |
| 컨테이너 4개 `[spec:02]` | 3개 |

이 표는 **후속 단계에서 기존 명세를 고칠 때의 작업 목록**이기도 하다. 구체적인
대체 기술(ORM, 마이그레이션 도구, 패키지 관리자)은 이 단계에서 확정하지 않았고,
domain-design(2.6) 또는 practices-discovery(2.2)에서 정한다.

### 2.2 바뀌지 않은 것

- 프론트엔드 스택과 모바일 웹 전제 `[spec:02]`
- PostgreSQL 16 과 JSONB 로 가변 구조를 담는 방식 `[spec:02]`
- STT·LLM 을 `SttProvider` / `LlmProvider` 인터페이스 뒤에 두는 구조 `[spec:02]`
- 전사 텍스트를 LLM 시스템 명령이 아닌 데이터 블록으로만 전달하는 규칙 `[spec:01][spec:02]`
- 클라우드 배포 없음, 로컬 Docker Compose 전용 `[intent][Q3]`
- MVP 범위 F01~F07 과 제외 항목 9건 `[intent]`

---

## 3. 항목별 타당성

### 3.1 F01 녹음·전사 — 가능

브라우저 MediaRecorder API 로 녹음하고 multipart 로 업로드한다 `[spec:02]`.
MediaRecorder 는 보안 컨텍스트를 요구하지만 `localhost` 는 보안 컨텍스트로 취급되어
로컬 개발에서 HTTPS 없이 동작한다. 전사는 Mock 이 고정 fixture 를 반환하므로
STT 정확도가 이번 검증의 변수가 되지 않는다 `[spec:02][F2]`.

### 3.2 F02 맥락 구조화 / F04 목표·프로필 — 가능

입력 폼과 저장이 전부이며 외부 의존이 없다. "미상" 저장과 확인/미확인 구분은
데이터 모델 수준의 문제다 `[spec:01]`.

### 3.3 F03 수행 평가 — 가능, 단 규칙 엔진이 핵심

3개 행동 묶음에 대해 기회 판정 → 행동 판정 → 근거·보류 사유를 낸다 `[spec:01]`.
판정 후보 검출은 Mock LLM 이 담당하고, **집계 규칙은 백엔드의 결정적 코드**다
`[spec:02]`. 보류·기회없음을 분모에서 제외하는 규칙이 `[spec:02]` 7.2 에 Java 예시로
있는데, 단일 백엔드 전환에 따라 Python 으로 다시 써야 한다. 로직 자체는 언어
중립적이라 이식 위험은 낮다.

### 3.4 F05 모의 대화 — 가능

시나리오 원형 + 제한적 변형, 3단계 힌트, 첫 시도·재시도 분리 기록 `[spec:01]`.
시나리오 원형 6개는 대상 연령 변경(13–18세)에 맞춰 중·고등학교 생활 배경으로
새로 작성하기로 이미 확정되어 있다 `[intent]`. 이 재작성은 이 단계의 범위가 아니다.

### 3.5 F06 기록·다음 추천 — 가능

"비교 불충분" 기준(유효 기회 3회 미만)은 확정하지 않고 설정값으로 둔다 `[Q6]`.
설정값이므로 구현은 임계값을 하드코딩하지 않아야 한다.

### 3.6 F07 정정·삭제 — 가능, 전파 범위가 설계 난점

전사 정정 시 관련 판정에 "재검토 필요"를 표시하고, 삭제 시 연결 기록을 함께
처리해야 한다 `[spec:01][intent]`. 단일 백엔드 전환은 이 기능에 **유리하다**:
원래 구조에서는 데이터 소유권이 core 에 있고 analysis 가 상태를 갖지 않는다는
규칙으로 삭제 누락을 막았는데 `[spec:02]`, 단일 백엔드에서는 그 분산 자체가 없다.

### 3.7 STT·LLM live 어댑터 — 가능, 선택 경로로 한정

live 구현체를 만들되 기본 실행과 SM1 검증은 Mock 을 쓴다. live 는
`ANALYSIS_MODE=live` 로만 켜진다 `[Q7][F2]`. 제공자는 아직 정하지 않았다 `[F3]`.

이 결정은 승인된 의도 서술의 "실제 STT·LLM 연동은 이 목적에 필요하지 않다"와
표면적으로 충돌했으나, **기본 실행 경로를 Mock 으로 유지**함으로써 의도 서술의
취지(합성 데이터로 흐름 전체가 성립하는지 확인)는 보존된다 `[intent][F2]`.
다만 의도 서술의 해당 문장은 "live 어댑터는 선택 경로로 만든다"는 취지를 담도록
approval-handoff(1.7) 또는 requirements-analysis(2.3)에서 갱신되어야 한다.

제공자가 미정이므로 live 어댑터의 **비용·응답시간·요청 실패 처리**는 이 단계에서
평가할 수 없다. RAID 로그 A3, D2 로 기록했다.

---

## 4. 일정 타당성

- 기간: 2026-09-16 → 2026-11-05, 약 7주 `[F4]`
- 인원: 5인, 전원 풀스택, 작업 단위별 분담 `[F4][F6]`
- 역량: 전원 AI 의 도움을 받으며 진행, Python 경험은 일부 `[F5]`

**보수적 평가**: 7주·5인은 F01~F07 을 로컬 Mock 기반으로 완성하기에 부족하지
않다. 단 아래 두 가지가 동시에 압박한다.

1. **스택 학습**. 팀의 학습 배경은 React+Java 인데 백엔드를 Python 으로 확정했다
   `[spec:07][F1][F5]`. 전원 풀스택 배정이므로 학습 부담이 특정인에게 쏠리지 않고
   분산되는데, 이는 위험 완화인 동시에 전원이 동시에 학습 곡선을 탄다는 뜻이기도
   하다.
2. **기존 명세 재작성**. 2.1 표의 9개 항목과, 대상 연령 변경에 따른 시나리오
   원형 6개·UI 문구 재작성 `[intent]` 이 구현 전에 선행되어야 한다.

여기에 세 번째 압박이 더해졌다. **실행 단계 수가 두 번 늘었다** — approval-handoff
에서 user-stories(2.4)가 추가되어 19 → 20 이 되었고, practices-discovery 후속으로
ci-pipeline(3.7)을 다시 넣어 20 → 21 이 되었다. 두 추가 모두 어느 단계도 맡지 않은
공백을 메우는 것이지만, 마감 2026-11-05 은 그대로다 `[F7]`.

이 평가는 추정이며 실측이 아니다. delivery-planning(2.9)에서 작업 단위가 나온 뒤
다시 검증해야 하며, 그 재검증에는 위 두 증가분을 모두 넣어야 한다 `[F7]`.

---

## 5. 이 단계에서 평가하지 않은 것

- **시장·경쟁 타당성** — market-research(1.2)가 범위 밖이라 입력이 없다
- **live 제공자별 비용·성능** — 제공자 미정 `[F3]`
- **실사용 확장 시의 규제 대응** — 사용자가 이번 범위의 제약으로 기록하지
  않기로 결정했다 `[Q5]`. 이는 규제가 없다는 판단이 **아니라**, 합성 데이터
  전용 테스트라 이번 범위에서 다루지 않는다는 결정이다
- ~~**구체적 ORM·마이그레이션·패키지 관리 도구 선택**~~ — **해소됨(2026-09-17)**: practices-discovery(2.2)에서 SQLAlchemy 2.0(동기) / Alembic / uv 로 확정되었다. 제약 TC-15 를 보라 `[F7]`

## Assumptions & Open Questions

None.
