# Risk and Sequencing Rationale — SCD 소통 코칭 MVP

**Stage**: delivery-planning (2.9)
**작성일**: 2026-09-17

## Sources

| 태그 | 출처 |
|---|---|
| `[plan]` | `bolt-plan.md` (같은 디렉터리) |
| `[units]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/unit-of-work.md`, `unit-of-work-dependency.md`, `unit-of-work-story-map.md` |
| `[contract]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md` |
| `[components]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/domain-design/components.md` |
| `[req]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/requirements.md` |
| `[stories]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/user-stories/stories.md` |
| `[practices]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/practices-discovery/team-practices.md` |
| `[scope]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/scope-definition/scope-document.md` |
| `[raid]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/feasibility/raid-log.md` |
| `[Q<n>]` | `delivery-planning-questions.md` |
| `[log]` | `docs/decisions/decision-log.md` |

refined-mockups(2.5, mockups)와 team-formation(1.5)은 범위 밖이다. 입력에 없는 것은 결손이 아니라 범위 밖이다.

**이 문서에서 쓰는 말**

- **Bolt** — 설계부터 코드·테스트까지 한 번에 지나가는 작업 묶음이다. 작업 단위 하나 이상을 담는다.
- **걷는 뼈대(walking skeleton)** — 첫 Bolt 로 만드는, 실제 기능 하나로 모든 층을 얇게 관통하는 경로다(Cockburn, *Crystal Clear*).
- **WSJF** — (가치 + 급한 정도 + 위험 감소) ÷ 크기로 순서를 매기는 점수 방식이다(Reinertsen, SAFe). 이 계획은 쓰지 않았다.
- **위상 순서** — 작업 단위 의존 그래프가 허락하는 순서다. 이 계획은 그 안에서 사람이 고른 경제적 순서다.

---

## 1. 쓴 방식: 걷는 뼈대 먼저 + 시연 흐름 순서

| 단계 | 방식 | 근거 |
|---|---|---|
| B1 | **걷는 뼈대 먼저** (Cockburn) — 업로드 하나로 화면부터 DB·Mock 까지 관통 | 팀 관행 Walking Skeleton `[practices]`, 스코프 `skeleton: on`, 사용자 답 `[Q7][Q9]` (D-114, D-116) |
| B2~B5 | **시연 흐름 순서** — SM1 경로(평가 → 목표·연습 → 기록)를 먼저 네 갈래에 | `[Q4]` (D-111), 시연 필수선 D-45 |
| B6~B9 | **보호선 뒤 Should** — Must 완료와 SM1 리허설 통과 전에는 시작하지 않음 | `[Q6]` (D-113) |

WSJF 같은 점수 모델은 쓰지 않았다 `[Q4]`. 순서를 가르는 기준이 이미 하나(시연 필수선 SM1)로 좁혀져 있고(D-45), 점수를 매겨도 SM1
경로 단위가 맨 앞에 오는 결론이 바뀌지 않기 때문이다.

## 2. 만드는 순서 원칙(D-46)의 표현이 바뀐 이유

Scope Definition 에서 확정한 원칙은 "업로드부터 기록까지 여섯 단계를 최소 형태로 한 번 이은 뒤 깊이를 채운다"였다 `[scope]` §5 (D-46).
이 원칙의 목적은 둘이다 — Python 역량 위험(R1)을 스택 관통으로 일찍 드러내기, 7주 일정 위험(R5)에 대비해 종단 경로가 언제 서는지
일찍 알기 `[raid]`.

작업 단위는 기능 하나씩 잘랐고(D-88) 한 단위는 Construction 을 한 번 지나가므로, "모든 단계를 최소로 먼저"를 단위 경계에서 나눌 수
없었다. 뼈대 Bolt 를 여섯 단계까지 넓히는 안(Q1 B)은 팀 관행의 뼈대 정의(화면·엔드포인트 하나, 업로드로 관통)와 부딪히고 네
갈래의 대기를 늘려 R5 를 키웠다. 사용자는 **Q7 에서 표현을 바꾸기로** 했다 (D-114):

- R1 은 **뼈대 Bolt(B1)** 가 맡는다 — 팀 관행 그대로 업로드로 전 층 관통
- R5 는 **SM1 흐름 단위를 먼저 병렬로 완성**해 B4 의 SM1 리허설로 확인한다

잃는 것: 여섯 단계가 "최소 형태로 한 번" 이어지는 시점이 병렬 기간 끝(B4 리허설)까지 없다. 대신 B2·B3 가 병합되기 전에도 시드와
계약으로 각 갈래가 흐름의 앞뒤를 흉내 내며 일한다(D-92). 이 위험은 아래 R-D1 로 관리한다.

## 3. 위상 순서에서 벗어난 곳

`unit-of-work-dependency.md` 의 그래프는 U1·U2 뒤에 기능 단위 11개가 모두 동시에 시작할 수 있다고 말한다 `[units]`. 이 계획이
그보다 늦추거나 당긴 곳과 이유:

| 벗어난 곳 | 위상 순서 | 이 계획 | 이유 |
|---|---|---|---|
| U3·U4 | U1·U2 뒤 병렬 | **뼈대 B1 안에서 U1·U2 와 함께** | 팀 관행의 뼈대는 실제 첫 기능(업로드, U3 소속)으로 관통해야 하고, 단위는 두 Bolt 에 나눌 수 없다. U4 는 A2 화면 묶음(Q3)으로 함께 들어갔다 `[Q9]` (D-116) |
| U1 의 완료 시점 | U1 전체가 기능 단위보다 먼저 | **테이블 20개 + 앞쪽 시드 3개만 B1 에서**, 뒤쪽 시드 6개는 기능 단위 시작 뒤 병렬 첫 주 | 뼈대가 커질수록 네 갈래가 기다린다. D-92 의 "U1 구현 완료"를 이 범위로 좁혔다 `[Q2][Q8]` (D-115) |
| U9 | U1·U2 뒤 병렬 | **갈래 4 에서 뒤쪽 시드 작업 뒤** | 사용자가 고른 흐름 순서에서 U9 는 SM1 흐름 뒤다 `[Q4]`. 갈래 4 의 첫 주는 U1 시드에 쓴다 |
| U10~U14 | U1·U2 뒤 병렬 (U12 는 U11 뒤) | **Must 완료 + SM1 리허설 통과 뒤** | 일정 보호선 `[Q6]` (D-113). 그래프에는 없는 경제적 조건이다 |
| U8 의 닫는 시점 | 의존 없음 | **B2·B3 병합 뒤** | US9.3(SM1 리허설)의 수용 기준 AC9.3.1 이 U2~U7 통합을 요구한다(OQ-U3). 간선을 추가하지 않고 완료 기준으로 둔다 (D-111) |

그래프에 없는 새 의존을 만들지 않았다 — 위 조건은 모두 "시작·마감 조건"으로 `bolt-plan.md` 에 적었고 `unit-of-work-dependency.md` 는
바뀌지 않는다.

## 4. 일정 재검증 (R5, R7)

마감 2026-11-05 까지 약 7주다(제약 OC-01). 아래는 **가설**이다 — 실제 속도는 B1 이 끝나야 처음 측정된다.

| 구간 | 가설 기간 | 가정 |
|---|---|---|
| 준비(저장소·Actions 확인, `.gitignore`) | 1~2일 | A6 이 막히지 않는다 |
| B1 뼈대 (U1 범위 제한·U2·U3·U4) | 약 1.5주 | 팀이 Python·FastAPI 조립 지점을 처음 넘는 기간 포함(R1) |
| B2~B5 병렬 (네 갈래) | 약 2.5~3주 | 가장 큰 U5(XL)가 갈래 하나를 끝까지 쓴다. 뒤쪽 시드는 첫 주 안 |
| B4 SM1 리허설과 Must 통합 수정 | 약 0.5~1주 | B2·B3 병합 뒤 |
| B6~B9 Should | 남는 기간 | 보호선 통과 뒤에만. 시간이 모자라면 여기서 줄인다(D-45: SM1 까지는 지킨다) |

합계 가설은 Must 까지 약 5~5.5주로, Should 에 1.5~2주가 남는다. 단계 수가 두 번 늘어난 부담(R7 — user-stories 추가, ci-pipeline
재삽입)은 Construction 안의 설계·CI 단계로 이 구간들에 이미 포함된 것으로 본다. **B1 이 2주를 넘기면 이 표를 다시 계산하고 Should
범위를 줄이는 결정을 decision-log 에 남긴다.**

## 5. 위험과 순서의 연결

| ID | 위험 | 가능성 | 영향 | 순서로 대응한 방법 |
|---|---|---|---|---|
| R1 | 팀의 Python 경험이 일부뿐 `[raid]` | 높음 | 높음 | B1 뼈대가 FastAPI 의존성 주입, 동기 세션, Alembic, 컨테이너 연결, 백그라운드 작업의 새 세션을 가장 먼저 한 번 관통한다 |
| R3 | 단일 백엔드에서 삭제 전파가 샌다 `[raid]` | 중간 | 높음 | U9 를 Must 병렬 기간 안(B5)에 두어 Should 전에 확인한다. 삭제 후 테이블·파일 비었는지 검사가 완료 기준이다 |
| R5 | 7주 일정 `[raid]` | 중간 | 높음 | SM1 흐름 단위를 먼저, Should 는 보호선 뒤. B1 기간으로 일정표를 재계산한다(§4) |
| R4 | live 제공자 미정 `[raid]` | 중간 | 중간 | 순서에 넣지 않는다. Mock 이 기본 경로이고 live 구현은 SM1 을 막지 않는다 |
| R-D1 | 여섯 단계가 병렬 기간 끝까지 한 번에 이어지지 않아, 갈래 사이 어긋남이 B4 리허설에서 늦게 드러난다 (D-114 로 새로 생김) | 중간 | 중간 | 계약 요약이 기준(D-99), 시드가 계약과 같은 모양(C16), 기반·통합 담당 1인이 병렬 기간에 계약 어긋남을 조정, B1 의 S1 Playwright 를 매 병합마다 초록으로 유지 |
| R-D2 | 뒤쪽 시드가 첫 주를 넘겨 갈래 1~3 이 임시 데이터로 오래 일한다 (D-115 로 새로 생김) | 중간 | 중간 | 갈래 4 의 첫 작업으로 고정. 시드와 실제 분석 결과가 같은 모양인지 B2 완료 기준에서 교차 확인 |
| R-D3 | B1 뼈대가 U3·U4 까지 담아 커지고, 혼자 진행하는 동안 네 사람이 기다린다 (D-116) | 중간 | 중간 | 기다리는 인원은 계약·시드 모양 확인과 용어집을 맡는다(`team-allocation.md`). B1 이 2주를 넘기면 §4 재계산 |

## 6. 계약 요약을 고치는 흐름

계약 요약(`contract-summary.md`)은 구현 중에도 고쳐지는 기준 문서다(D-99). 고치는 흐름은 이렇게 둔다: 계약을 바꾸는 PR 이 같은 PR 에서
계약 요약을 고치고, 깨는 변경이면 소비 Bolt 담당의 승인을 받는다(D-100). 이 워크플로의 Change Control 은 relaxed 라서, 이후 단계가
바뀐 입력을 기록·안내하고 멈추지는 않는다.

## Assumptions & Open Questions

- §4 의 기간은 가설이며 확정값이 아니다. B1 완료 시점에 실측으로 바꾼다.
- R-D1~R-D3 은 이 단계의 결정(D-114~D-116)에서 새로 생긴 위험이라 RAID 로그에는 아직 없다. 승인 게이트에서 짚는다.
