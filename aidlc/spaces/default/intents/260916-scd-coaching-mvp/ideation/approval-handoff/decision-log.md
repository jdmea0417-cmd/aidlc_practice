# Decision Log — Ideation 단계 결정 기록

> Ideation 네 단계(Intent Capture, Feasibility, Scope Definition, Approval & Handoff)
> 에서 내려진 결정을 한곳에 모은 요약이다.
>
> **원본은 `docs/decisions/decision-log.md` 다.** 이 문서는 Ideation 구간만 잘라
> 정리한 사본이며, 두 문서가 어긋나면 원본이 기준이다. 결정 ID(D-xx)는 원본과 같다.

## Sources

| 태그 | 출처 |
|---|---|
| `[log]` | `docs/decisions/decision-log.md` — 원본 결정 기록 |
| `[intent]` | `.../ideation/intent-capture/intent-statement.md` |
| `[stake]` | `.../ideation/intent-capture/stakeholder-map.md` |
| `[feas]` | `.../ideation/feasibility/feasibility-assessment.md` |
| `[constraint]` | `.../ideation/feasibility/constraint-register.md` |
| `[backlog]` | `.../ideation/scope-definition/intent-backlog.md` |
| `[scope]` | `.../ideation/scope-definition/scope-document.md` |

---

## 1. 입력 문서 준비 단계 (AI-DLC 실행 전)

| ID | 결정 | 상태 |
|---|---|---|
| D-01 | 기술 스택: React + Java(Spring Boot), 분석은 Python 서비스로 연동. 연동 불가 시 React + FastAPI 로 전환 | **변경됨 → D-30** |
| D-02 | 테스트 범위: UI 의 A·B·C 흐름 전체를 합성 데이터와 Mock STT·LLM 으로 구현·테스트 | 확정 |
| D-03 | 기획 방향 유지: 기획서와 UI 시안의 흐름을 유지 | 확정 |
| D-04 | 외부 자료 없이 자체 완결형으로 진행 | 확정 |
| D-05 | 모든 질문과 선택을 결정 기록 문서에 남긴다 | 확정 |
| D-06 | 대상 정의 확대안(화용언어 어려움 전반) — 이번 테스트에는 미반영 | 미결정 |

## 2. Intent Capture (1.1)

| ID | 결정 | 상태 |
|---|---|---|
| D-07 | 워크플로 진행 방식 선택 | 확정 |
| D-08 | 워크플로 단계 구성(`scd-coach-mvp`) 승인 | 확정 (D-49 로 일부 변경) |
| D-09 | 문제 정의: 실제 대화를 근거와 함께 돌아볼 방법이 없고, 그 결과가 연습으로 이어지지 않는다 | 확정 |
| D-12 | 대상 연령을 13–18세로 확정 (가정 A-01 을 뒤집음) | 확정 |
| D-21 | 시나리오 원형과 UI 문구를 중·고등학교 생활 배경으로 재작성 | 확정 |
| D-22 | 합성 테스트 대화 3건은 그대로 둔다 | 확정 |
| D-23 | 이해관계자 목록은 제품을 쓰는 사람만. 결정권자는 별도 항목 | 확정 |
| D-24 | 보호자 열람 권한 초기 기본값은 NONE, 사용자 본인이 켠다 | 확정 |
| D-25 | 보호자 역할은 열람만. 계정은 사용자가 생성 | 확정 |
| D-26 | Intent Capture 가정 처리 방식 | 확정 |
| D-27 | Intent Capture 산출물 수정 요청 (승인 게이트 반려) | 확정 |
| D-28 | 결정 기록 갱신 시점과 변경 표기 규칙 | 확정 |
| D-29 | 보호자 열람 권한은 NONE / SUMMARY / FULL 세 단계 유지 | 확정 |

성공 기준은 SM1 하나로 확정되었고, MVP 범위 F01~F07 과 제외 9건도 이 단계에서
확정되었다 `[intent]`.

## 3. Feasibility & Constraints (1.3)

| ID | 결정 | 상태 |
|---|---|---|
| **D-30** | **기술 스택 전환: 백엔드를 Python 3.11 + FastAPI 단일 서비스로. Java·Spring Boot 를 쓰지 않는다. 컨테이너 3개** | 확정 (D-01 대체) |
| D-31 | 버전 확정: React 18 / TypeScript 5 / Vite 5 / PostgreSQL 16 / Python 3.11 + FastAPI | 확정 |
| D-32 | 로컬 실행 환경에 자원 제약 없음. 클라우드 배포 없음 유지 | 확정 |
| D-33 | 마감 2026-11-05(약 7주), 개발 인원 5인 | 확정 |
| D-34 | 개인정보·규제 항목은 이번 범위의 제약으로 기록하지 않는다. 제품 기능 F07 과 보호자 권한은 유지 | 확정 |
| D-35 | 운영 파라미터(녹음 5분 / 분석 3초 / 비교 불충분 3회 / 원음 30일)는 확정하지 않고 설정값으로 둔다 | 확정 |
| D-36 | live STT·LLM 구현체를 만들되 기본 실행과 SM1 검증은 Mock 유지. live 는 선택 경로 | 확정 |
| D-37 | live 제공자 선택 | **미결정 (의도적 보류)** |
| D-38 | 팀은 전원 AI 지원을 받으며 진행, Python 경험은 일부 | 확정 |
| D-39 | 5인 전원 풀스택, 작업 단위별 분담 | 확정 |
| D-40 | Feasibility 산출물 승인 | 확정 |

판정은 "실현 가능, 단 조건부 2건"이었고 그 둘은 팀의 Python 역량(R1)과 7주
일정(R5)이다 `[feas]`.

## 4. Scope Definition (1.4)

| ID | 결정 | 상태 |
|---|---|---|
| D-41 | F01~F06 은 Must, F07 정정·삭제는 Should | 확정 |
| D-42 | 화면 A1~A5 · B1~B5 · C1 은 Must, C2~C5 는 Should | 확정 |
| D-43 | 파일 업로드와 브라우저 직접 녹음 두 경로 모두 Must | 확정 |
| D-44 | 회원가입·로그인과 보호자 권한 동작을 Should 로 내린다. Must 경로는 고정 사용자 하나로 돈다. **권한 3단계 결정은 취소되지 않았고 시점만 뒤로 갔다** | 확정 |
| D-45 | 시연 필수선은 SM1 그대로 | 확정 |
| D-46 | 제작 순서는 얇은 종단 슬라이스 먼저 | 확정 |
| D-47 | 병렬 작업 갈래 수 | **미결정 (2.7 로 이월)** |
| D-48 | Scope Definition 산출물 승인 | 확정 |

proto-Unit 11개(Must 7 / Should 4)가 정리되었고, 임계 경로는 SM1 의 여섯 단계와
일치한다 `[backlog]`.

## 5. Approval & Handoff (1.7)

| ID | 결정 | 상태 |
|---|---|---|
| D-49 | 의도 서술의 STT·LLM 문장을 이 단계에서 갱신. 현안 I2 해소 | 확정 |
| D-50 | `docs/input/02_tech-environment.md` 를 Python·FastAPI 전제로 재작성. 현안 I3 해소 | 확정 |
| D-51 | **user-stories(2.4)를 다시 넣는다. EXECUTE 단계 19 → 20.** 수용 기준(Given/When/Then)은 이 단계가 맡는다 | 확정 (D-08 의 단계 구성을 일부 변경) |
| D-52 | 이데이션 종합 판정은 진행(Go) — 조건 없음 | 변경됨 → D-61 (내용은 유지, 재확인됨) |

## 5-2. 이데이션 되돌리기 회차 (2026-09-17)

practices-discovery(2.2)를 실행하던 중 F07 의 등급 문제가 드러나, 이데이션
네 단계를 intent-capture 부터 다시 열어 반영했다. 그 회차의 결정이다.

| ID | 결정 | 상태 |
|---|---|---|
| D-54 | Python 도구 확정 — ORM **SQLAlchemy 2.0(동기)**, 마이그레이션 **Alembic**, 패키지 관리자 **uv**. 제약 TC-15 와 의존 D3 가 닫혔다 | 확정 |
| D-55 | 저장소는 원격(GitHub 등)을 쓰고 PR 로 병합한다. 병합 전 검사는 **GitHub Actions** 가 강제한다(제약 TC-16). 저장소 생성 전에 `.gitignore` 를 먼저 고친다 | 확정 |
| D-56 | **ci-pipeline(3.7)을 다시 넣는다. EXECUTE 단계 20 → 21.** Actions 워크플로와 품질 게이트는 이 단계가 만든다 | 확정 (D-08·D-51 의 단계 구성을 다시 변경) |
| D-57 | 테스트 방침 — 방법론은 **test-after** 하나. 커버리지 바닥은 `service/` **라인 80%** 하나. 기대 판정은 **픽스처 파일로 고정**하고 단위 테스트가 그것을 읽는다 | 확정 |
| D-58 | "배포 성공"은 `docker compose up --build` 후 헬스체크 통과 + 합성 대화 3건의 종단 통과. 기대 판정 대조는 종단 실행의 성공 조건이 아니다 | 확정 |
| D-59 | **F07(정정·삭제)을 Should 에서 Must 로 올린다.** 근거는 합성 대화 S3 의 검증 항목 2·4 가 F07 에 걸려 있다는 것 | 확정 (D-13 의 F07 등급을 변경) |
| D-60 | **화면 C5 를 쪼갠다.** 삭제 관련 요소만 Must, 보호자 권한 전환·원음 보관 기간·서비스 안내는 Should 유지. F07 은 만드는 순서 3단계(Must 잔여)에 놓는다 | 확정 |
| D-61 | 이데이션 종합 판정을 **진행(Go)으로 유지**한다. 늘어난 부담(Must 73%, 단계 21개)은 관리 대상으로 기록한다 | 확정 (D-52 재확인) |

## 6. 결정이 바뀐 이력

이 워크플로에서 이미 확정된 결정이 뒤집힌 경우는 세 건이다. 모두 영향받는 확정
항목을 먼저 열거해 확인받은 뒤 반영했다.

| 원래 결정 | 바뀐 내용 | 대체한 결정 | 무엇이 함께 무효가 되었나 |
|---|---|---|---|
| D-01 기술 스택 (React + Java) | Python FastAPI 단일 백엔드 | D-30 | Spring Boot, Gradle, JPA·Flyway, JUnit·Mockito·Testcontainers, springdoc-openapi, core 패키지 구조, Java 코드 예시 3건, "analysis 의 DB 직접 접근 금지" 규칙, 컨테이너 4개 — 총 9개 항목 `[feas]` §2.1 |
| 가정 A-01 대상 연령 (8–12세) | 13–18세 | D-12 | 시나리오 원형 6개와 UI 문구의 아동 전용 내용 |
| D-08 단계 구성 (user-stories SKIP) | user-stories EXECUTE | D-51 | 없음 — 단계 추가이며 기존 단계를 무효화하지 않는다 |
| D-51 단계 구성 (EXECUTE 20개) | ci-pipeline 도 EXECUTE, 21개 | D-56 | 없음 — 단계 추가다. 다만 위험 R7 의 부담 수치가 갱신되었다 |
| D-13 범위 등급 (F07 = Should) | F07 = Must | D-59 | `scope-document.md` 의 확정 항목 6건: Should 목록 S1, S1 의 근거, 추적 지도 §7 의 F07 서술, 만드는 순서 4단계, 시연 필수선의 버리는 대상, Should 목록의 화면 C5 항목. 모두 반영 완료 |
| F1 답변 (C5 전체를 Should 로 두고 보호자 권한도 뒤로) | C5 를 쪼개 삭제 부분만 Must | D-60 | 없음 — 쪼개는 방식을 고른 덕분에 F1 의 취지(보호자 권한은 Should)가 유지되었다. C5 전체를 Must 로 올리는 안은 보호자 권한(Must)이 정식 인증(Should)에 의존하게 만들어 철회되었다 |

## 7. 이 시점의 미결 항목

| 항목 | 내용 | 닫힐 단계 |
|---|---|---|
| D-37 | live STT·LLM 제공자 | 3.2 NFR Requirements, 늦어도 3.5 착수 전 (판단) |
| D-47 | 병렬 작업 갈래 수 | 2.7 Units Generation (확정 이월) |
| A-03 | 플랫폼 = 모바일 웹 375px | 2.3 Requirements Analysis (판단) |
| A-04 | 모의 대화 매체 = 텍스트 채팅 | 2.3 Requirements Analysis (판단) |
| A-10 | 행동 묶음 조작적 정의 | 2.3 확정 → 2.6 모델링 (판단) |
| A-11 | UI 세부 문구 재작성 | 3.1 Functional Design 진입 전 (판단) |
| A-12 | Mock 판정 규칙·시나리오 원형 6개 재작성 | 3.5 Code Generation 착수 전 |
| D-06 | 대상 정의 확대안 | 이 워크플로에서 닫지 않는다 |
| A6 | 원격 저장소와 GitHub Actions 사용 가능 여부 | 저장소를 실제로 만드는 시점 (Construction 진입 전) |

A-02(보호자 역할)는 D-25 로 확정되었고, A-05~A-08 은 D-35 로 설정값이 되었으며,
A-09 는 D-31·D-30 으로 정리되었다. 원본 `[log]` 의 미확인 요약표는 A-02 에 대해
갱신이 늦어진 상태다.

## Assumptions & Open Questions

None.
