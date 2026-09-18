# External Dependency Map — SCD 소통 코칭 MVP

**Stage**: delivery-planning (2.9)
**작성일**: 2026-09-17

## Sources

| 태그 | 출처 |
|---|---|
| `[plan]` | `bolt-plan.md` (같은 디렉터리) |
| `[raid]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/feasibility/raid-log.md` |
| `[brief]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/approval-handoff/initiative-brief.md` |
| `[practices]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/practices-discovery/team-practices.md` |
| `[contract]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md` |
| `[req]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/requirements.md` |

**이 문서에서 쓰는 말** — **Bolt** 는 설계부터 코드·테스트까지 한 번에 지나가는 작업 묶음이다(B1~B9, `bolt-plan.md`).
**외부 의존** 은 팀이 코드를 써서 해결할 수 없고 바깥의 도구·결정·환경에 기대는 항목이다.

이 프로젝트는 로컬 Docker Compose 에서 합성 데이터와 Mock 경로로 도는 시연이라 외부 의존이 적다. 외부 API 를 기본 경로에서 부르지
않고, 외부 팀의 인계나 데이터 제공 창구도 없다 `[req]` NFR5, 제약 SC-02(합성 데이터 전용).

---

## 의존 목록

| # | 의존 항목 | 주인 | 걸리는 시간 | 막는 Bolt | 늦어지거나 막히면 | 근거 |
|---|---|---|---|---|---|---|
| E1 | **원격 저장소(GitHub 등)와 GitHub Actions 사용 가능 여부** (가정 A6) | 팀 (저장소를 만드는 사람) | 1~2일 — 저장소 생성, `.gitignore` 팀 구역 추가, `git init`, 첫 `git add` 순서 | **B1 시작** | 병합 게이트와 ci-pipeline(3.7) 산출물을 다시 짜야 한다. 그동안은 컨테이너 안 `scripts/check.sh` 로 병합 전 확인을 대신하고 decision-log 에 남긴다 | `[raid]` A6, `[practices]` Way of Working |
| E2 | **`localhost` 에서 HTTPS 없이 브라우저 녹음(MediaRecorder)이 동작** (가정 A1) | 브라우저 동작 — 팀이 확인 | B1 안에서 한 번 실행 | **B1 완료** (직접 녹음 US2.2) | 로컬 개발용 HTTPS 인증서 설정이 B1 에 추가된다. 파일 업로드 경로(US2.1)는 막히지 않으므로 뼈대 관통 자체는 계속한다 | `[raid]` A1, `[practices]` Walking Skeleton |
| E3 | **live STT·LLM 제공자 선택** (의존 D2, D-37) | 외부 결정 (팀이 정하지 않음) | 미정 | **없음** — Mock 이 기본 경로 | live 구현체 작성만 늦어진다. SM1·Must Bolt 는 영향이 없다. 타임아웃 값은 nfr-requirements(3.2)에서 정한다 | `[raid]` R4·D2, `[contract]` C14 |
| E4 | **새 의존성 패키지의 실존·이름 확인** (PyPI·npm) | 각 PR 의 리뷰어 | 패키지 이름당 30초 | 의존성을 추가하는 모든 Bolt (주로 B1) | 확인되지 않은 패키지는 병합하지 않는다 | `[practices]` Way of Working |
| E5 | **시연 일자 2026-11-05** | 외부 일정 (과정 운영) | 고정 | B4 의 SM1 리허설, B6~B9 의 범위 | Should 를 줄이고 SM1 까지는 지킨다(D-45). 일정 재계산은 `risk-and-sequencing-rationale.md` §4 | 제약 OC-01 |

## Bolt 별로 본 외부 의존

| Bolt | 기대는 외부 의존 |
|---|---|
| B1 | E1(시작 전), E2(안에서 확인), E4 |
| B2 | 없음 (Mock LLM 픽스처만 사용) |
| B3 | 없음 |
| B4 | E5 (리허설 시점) |
| B5 | 없음 |
| B6~B9 | E5 (남는 기간) |

## Assumptions & Open Questions

- E1 의 주인은 사람 이름 없이 "저장소를 만드는 사람"으로 둔다 — 이름은 B1 시작 때 정한다(D-112).
- 이 목록 밖의 외부 의존이 Construction 중에 드러나면 이 문서에 행을 추가하고 decision-log 에 남긴다.
