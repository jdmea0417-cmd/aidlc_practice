# Team Allocation — SCD 소통 코칭 MVP

**Stage**: delivery-planning (2.9)
**작성일**: 2026-09-17

## Sources

| 태그 | 출처 |
|---|---|
| `[plan]` | `bolt-plan.md` (같은 디렉터리) |
| `[units]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/unit-of-work.md` |
| `[practices]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/practices-discovery/team-practices.md` |
| `[constraint]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/feasibility/constraint-register.md` |
| `[Q<n>]` | `delivery-planning-questions.md` |

team-formation(1.5)은 범위 밖이다. 팀 구성표가 없는 것은 결손이 아니라 범위 밖이며, 이 문서는 제약 OC-02·OC-03 과 사용자 답에 따른다.

**이 문서에서 쓰는 말**

- **Bolt** — 설계부터 코드·테스트까지 한 번에 지나가는 작업 묶음이다. 작업 단위 하나 이상을 담는다.
- **갈래** — 동시에 진행하는 작업 줄기다. 최대 4개다(D-91).
- **mob(몹)** — 한 작업을 함께 맡는 사람 묶음을 뜻하는 AI-DLC 용어다. 이 프로젝트에서는 "갈래"가 그 자리를 대신한다.

---

## 배정 원칙

- **Bolt 는 갈래에만 배정하고 사람 이름은 적지 않는다.** 누가 어느 갈래를 맡을지는 그 Bolt 를 시작할 때 정한다 `[Q5]` (D-112).
  5인 전원 풀스택이고 고정 역할을 두지 않는다는 제약 OC-03 을 따른다 `[constraint]`.
- **코드는 AI 개발 에이전트(aidlc-developer-agent)가 만든다.** 사람은 계획 승인, 단계 승인, PR 리뷰, 병합을 맡는다. team-formation 이
  범위 밖이므로 AI-DLC 기본값대로 모든 Bolt 의 코드 생성 주체는 이 에이전트다.
- **리뷰는 그 Bolt 를 맡지 않은 사람 1인**이 하고, 필수 확인 항목은 해당 PR 의 GitHub Actions 검사 통과다 `[practices]` Way of Working.
- **계약을 깨는 변경**(필드 이름 변경·삭제 등)은 그 계약을 쓰는 Bolt 담당자의 PR 승인이 추가로 필요하다 (D-100).
- **컬럼을 바꾸는 Bolt** 는 U1 담당(갈래 4 의 시드 작업 담당)을 리뷰어로 넣는다 (D-98).
- **갈래가 작업 단위를 맡아 각자 승인받는다** (D-118). 갈래는 자기 단위의 설계와 코드를 스스로 진행하고, 다른 갈래의 승인을 기다리지
  않는다. 위 배정표의 갈래 열이 곧 그 소유 관계다.
- **승인은 단계마다 받는다** (D-119). 한 갈래가 자기 단위의 기능 설계, 품질 요구, 품질 설계, 인프라 설계, 코드를 지날 때 각 단계가
  끝날 때마다 확인을 받는다. 단위가 다 끝난 뒤 한 번만 보는 방식은 고르지 않았다 — 잘못 든 방향을 다음 단계가 그 위에 쌓기 전에
  잡기 위해서다 `[constraint:OC-04][raid:R1]`.

## 배정표

| Bolt | 담는 단위 | 갈래 | 코드 생성 | 사람의 역할 |
|---|---|---|---|---|
| B1 뼈대 | U1(범위 제한) · U2 · U3 · U4 | 혼자(한 갈래) | aidlc-developer-agent | 담당 1인 이상 + 리뷰 1인. 나머지 인원은 B1 승인 전까지 병렬 Bolt 의 설계 입력(계약·시드 모양) 확인과 `docs/glossary.md` 작성을 돕는다 |
| B2 | U5 | 갈래 1 | aidlc-developer-agent | Bolt 시작 때 정함 |
| B3 | U6 + U7 | 갈래 2 | aidlc-developer-agent | Bolt 시작 때 정함 |
| B4 | U8 | 갈래 3 | aidlc-developer-agent | Bolt 시작 때 정함. SM1 리허설을 맡는다 |
| B5 | U1 뒤쪽 시드 → U9 | 갈래 4 | aidlc-developer-agent | Bolt 시작 때 정함. 시드 작업을 먼저 끝낸다 |
| B6 | U10 | 빈 갈래 | aidlc-developer-agent | Must + SM1 통과 뒤 정함 |
| B7 | U11 + U12 | 빈 갈래 | aidlc-developer-agent | 같음 |
| B8 | U13 | 빈 갈래 | aidlc-developer-agent | 같음 |
| B9 | U14 | 빈 갈래 | aidlc-developer-agent | 같음 |

인원 5명에 갈래 4개이므로 병렬 기간에는 한 사람이 남는다. D-91 에서 고른 대로 그 한 사람은 기반·통합을 맡는다 — 뒤쪽 시드 교체 확인,
갈래 사이 계약 어긋남 조정, SM1 리허설 준비. 이름은 적지 않는다 `[Q5]`.

## 갈래가 비었을 때

Must(B1~B5)가 끝나고 SM1 리허설을 통과하기 전에는 Should Bolt 를 시작하지 않는다. 먼저 끝난 갈래는 Must 통합과 테스트를 돕는다
`[Q6]` (D-113).

## Program Board 에 대하여

Program Board(여러 팀의 작업과 의존을 한 판에 올려 조율하는 보드)는 팀이 둘 이상일 때 쓴다. 이 프로젝트는 한 팀이 갈래로 나눠
일하므로 위 배정표와 `bolt-plan.md` 의 순서 그림이 그 역할을 대신한다.

## Assumptions & Open Questions

- 이름 없는 배정이라, 누가 어느 갈래를 맡는지는 B1 승인 직후 팀이 정하고 `docs/decisions/decision-log.md` 에 남긴다 `[practices]` (OC-05).
