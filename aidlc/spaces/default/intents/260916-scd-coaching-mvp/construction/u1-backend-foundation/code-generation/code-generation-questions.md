# Code Generation Questions — u1-backend-foundation

**Stage**: code-generation (3.5) · **Unit**: u1-backend-foundation (U1 백엔드 기반)
**작성일**: 2026-09-18

## Sources

| 태그 | 출처 |
|---|---|
| `[spec]` | `../functional-design/functional-spec.md` — 흐름 W1~W6, 열린 질문 OQ-F2·OQ-F5 |
| `[entities]` | `../functional-design/entities.md` — 열린 질문 OQ-F2 |
| `[nfr]` | `../nfr-requirements/tech-stack-decisions.md` — 열린 질문 OQ-N1, §3 설정값 |
| `[design]` | `../nfr-design/` — reliability-design.md §2·§3, performance-design.md §2 |
| `[infra]` | `../infrastructure-design/infrastructure-specification.md` — §2·§2.1 연결 풀 |
| `[contract]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md` — 공통 규칙, C14, C16 |
| `[practices]` | `aidlc/spaces/default/memory/team.md`, `project.md` |

**이 단계가 닫아야 할 것** — 상위 산출물이 이 단계를 담당으로 지정한 열린 질문은 정확히 세 건이고, 아래 세
질문이 그 셋이다. 다시 묻지 않는 것은 이미 닫힌 결정이다 — 기술 선택(D-54), 설정값과 타임아웃(§3), 계층
경계(TC-14), 오류 봉투, 로그 여섯 필드, 연결 풀 5, 헬스체크 주기, 초기 리비전의 경계(BR8.1).

---

## Q1

`[spec]` OQ-F5 — **응답 이후에 도는 작업(전사·분석·재분석)을 무엇으로 예약하는가.**

U1 은 그 작업들의 *모양*(W5, 작업 단위 장치)을 만들고 실제 작업 내용은 u3·u5·u9 가 채운다. 예약 수단은 U1 이
정해서 넘겨야 하는 것이고, `functional-spec.md` 는 어느 쪽이든 성립하게 써 두었다.

작업 큐·메시지 브로커는 선택지가 아니다 — `[nfr]` §4 가 이번 범위에서 도입하지 않기로 못박았다.

- **A. 웹 프레임워크의 기본 배경 작업 수단을 쓴다** — 응답을 보낸 뒤 같은 프로세스에서 함수를 돌린다.
  새 의존성이 0 이고 코드가 가장 적다. 대신 **동시에 도는 작업 수를 제한할 수단이 없다** — `[infra]` §2.1 이
  연결 풀 5 를 "동시에 도는 작업 2개"라는 보수적 전제로 계산했는데, 그 전제를 강제하는 장치가 생기지 않는다.
  프로세스가 죽으면 진행 중 작업이 사라진다(상태는 진행 중으로 남는다).
- **B. 앱이 소유하는 작은 스레드 실행자를 둔다** — 동시 실행 수를 설정값으로 **제한한다**. `[infra]` §2.1 의
  전제가 계산이 아니라 강제가 되고, 연결 풀 5 와의 관계가 값으로 이어진다. 대신 종료 처리와 실행자 수명을
  U1 이 직접 다뤄야 하고, Python 이 처음인 팀에게 읽을 코드가 한 겹 늘어난다 `[constraint:OC-04]`.
- X. Other (please specify)

[Answer]: A

---

## Q2

`[entities]` OQ-F2 — **시드 고정 사용자의 식별자를 고정값으로 박을지, 시드가 만들 때마다 새로 만들지.**

시드 상태는 누적이고(`[contract]` C16) 개발 중 여러 번 다시 넣게 된다. 모든 데이터가 합성이므로
`[constraint:SC-02]` 고정값이 노출 위험이 되지는 않는다.

- **A. 고정 식별자를 상수로 박는다** — 시드를 몇 번을 다시 넣어도 같은 값이다. 픽스처·통합 테스트·프론트엔드
  모의 응답이 그 값을 직접 쓸 수 있고, 시연 중 화면과 로그를 대조하기 쉽다. 대신 그 상수가 코드와 시드 양쪽에
  있게 되므로 한 자리(픽스처)에서만 읽도록 해야 한다.
- **B. 시드가 만들 때마다 새로 만든다** — 테스트는 사용자 조회 API 로 값을 얻어 쓴다. 상수가 늘지 않는 대신,
  값을 미리 아는 것을 전제로 한 픽스처(예: 미리 만들어 둔 대화의 사용자 참조)를 쓸 수 없다.
- X. Other (please specify)

[Answer]: A

---

## Q3

`[nfr]` OQ-N1 — **STT·LLM 제공자가 정해졌는가. 정해졌다면 타임아웃 두 값을 실측으로 조정한다.**

`[nfr]` §3 이 연결 5초 / 읽기 60초를 **제공자 미정 상태의 안전한 출발점**으로 정했고, OQ-N1 은 "제공자가
정해지면 실측으로 조정하되 늦어도 이 단계 착수 전"이라고 적었다. 지금이 그 시점이다.

- **A. 아직 정해지지 않았다 — 5초 / 60초를 그대로 둔다** — 두 값은 설정값이므로 제공자가 정해지면 코드가
  아니라 값만 바꾼다. `live` 구현체는 인터페이스를 지키는 뼈대로 만들고 키 없이 둔다 `[practices]`.
  OQ-N1 은 닫히지 않고 "제공자 확정 시점"으로 그대로 남는다.
- **B. 정해졌다 — 제공자 이름과 조정할 값을 알려 준다** — 그 값으로 기본값을 바꾸고, `live` 어댑터가 실제
  엔드포인트를 향하게 쓴다. 네트워크를 타는 시험은 기본 실행에서 여전히 제외한다 `[practices]`.
- X. Other (please specify)

[Answer]: A

---

## Plan Approval

**무엇을 승인하는가** — 두 문서다.

| 문서 | 내용 |
|---|---|
| `code-generation-plan.md` | 실행 계획 12단계, 이 단계가 닫은 열린 질문 3건, 만들지 않는 것의 경계, 그리고 §3 에 박힌 **Testing Contract** |
| `unit-test-instructions.md` | 시험 도구·표시·정확한 실행 명령, 구성 요소 23벌의 시험 범위(단위 78 · 통합 21), 커버리지 바닥 80%, 대역·데이터·이름 규칙 |

승인 뒤에는 이 계획대로 코드가 생성된다. 계획이나 시험 지침을 한 글자라도 고치면 이 승인은 무효가 되고 다시
받아야 한다.

[Approval Fingerprint]: sha256:v3:1c64450fcb4f04b0d8267af79c82798f2ffffd887bb91b92cc904f19cb7f8b67
[Planned Source]: 218ea40388bf44abce2a1b30a9ddf32fbb5837cef472b3b2d206c42fc2059aee

- "Approve Plan" — proceed to code generation
- "Request Changes" — revise the plan

[Answer]: Approve Plan
