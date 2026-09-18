# Unit of Work Story Map — SCD 소통 코칭 MVP

**Stage**: units-generation (2.7)
**작성일**: 2026-09-17

## Sources

| 태그 | 출처 |
|---|---|
| `[stories]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/user-stories/stories.md` — 스토리 37개와 의존 |
| `[requirements]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/requirements.md` — 스토리가 가리키는 FR |
| `[unit-of-work]` | `unit-of-work.md` — 단위 정의(같은 디렉터리) |
| `[Q<n>]` | `units-generation-questions.md` |
| `[log]` | `docs/decisions/decision-log.md` (D-94) |

스토리의 요구사항 연결(FR·NFR)은 `stories.md` 에 있고 이 문서는 되풀이하지 않는다. 이 문서는 스토리 → 단위
대응만 적는다.

---

## 스토리 → 단위

| 스토리 | 제목 | 등급 | Unit ID | Directory |
|---|---|---|---|---|
| US1.1 | 첫 방문 서비스 안내에 동의하기 | Must | U2 | `u2-web-foundation` |
| US1.2 | 홈에서 무엇을 할지 고르기 | Must | U2 | `u2-web-foundation` |
| US2.1 | 음성 파일을 올려 대화 가져오기 | Must | U3 | `u3-f01-capture` |
| US2.2 | 브라우저에서 직접 녹음해 가져오기 | Must | U3 | `u3-f01-capture` |
| US2.3 | 대화의 맥락 입력하기 | Must | U4 | `u4-f02-context` |
| US3.1 | 전사와 맥락 확인하기 | Must | U3 | `u3-f01-capture` |
| US3.2 | 발화 고치기와 분석에서 빼기 | Must | U3 | `u3-f01-capture` |
| US3.3 | 고친 뒤 재검토 안내를 보고 다시 분석하기 | Must | U9 | `u9-f07-correction-deletion` |
| US4.1 | 잘한 장면과 어려움이 보인 장면을 근거와 함께 보기 | Must | U5 | `u5-f03-assessment` |
| US4.2 | 분석을 보류한 부분의 이유 보기 | Must | U5 | `u5-f03-assessment` |
| US4.3 | 근거 발화로 이동하고 맥락 고치기 | Must | U5 | `u5-f03-assessment` |
| US4.4 | 분석이 이상하다고 알리기 | Must | U5 | `u5-f03-assessment` |
| US5.1 | 추천 목표를 보고 고르기 | Must | U6 | `u6-f04-goal` |
| US5.2 | 고른 목표를 그대로 연습으로 잇기 | Must | U6 | `u6-f04-goal` |
| US6.1 | 연습 목록에서 고르고 상황 준비하기 | Must | U7 | `u7-f05-practice` |
| US6.2 | 도움 없이 첫 시도하기 | Must | U7 | `u7-f05-practice` |
| US6.3 | 단계별 힌트를 받고 다시 시도하기 | Must | U7 | `u7-f05-practice` |
| US6.4 | 멈추거나 모르겠다고 말하기 | Must | U7 | `u7-f05-practice` |
| US6.5 | 첫 시도와 다시 시도를 나란히 보기 | Must | U7 | `u7-f05-practice` |
| US7.1 | 실제 대화와 모의 대화 기록 목록 보기 | Must | U8 | `u8-f06-record` |
| US7.2 | 목표별 추이를 독립·도움 후로 나눠 보기 | Must | U8 | `u8-f06-record` |
| US7.3 | 다음 코칭 추천 보기 | Must | U8 | `u8-f06-record` |
| US8.1 | 대화 기록을 연결 항목까지 확인하고 삭제하기 | Must | U9 | `u9-f07-correction-deletion` |
| US8.2 | 삭제하는 대화에서 나온 목표와 추천 처리 고르기 | Must | U9 | `u9-f07-correction-deletion` |
| US8.3 | 원음만 삭제하기 | Must | U9 | `u9-f07-correction-deletion` |
| US9.1 | 한 명령으로 환경을 띄우고 분석 모드 확인하기 | Must | U1 | `u1-backend-foundation` |
| US9.2 | 합성 대화 파일로 로그인 없이 시작하기 | Must | U1 | `u1-backend-foundation` |
| US9.3 | 성공 기준 SM1 종단 리허설 | Must | U8 | `u8-f06-record` |
| US10.1 | 목표 상세와 시도 이력 보기 | Should | U10 | `u10-s-detail-views` |
| US10.2 | 연습 기록 상세 보기 | Should | U10 | `u10-s-detail-views` |
| US10.3 | 실제 대화 기록 상세와 정정 이력 보기 | Should | U10 | `u10-s-detail-views` |
| US11.1 | 내 계정 만들고 로그인하기 | Should | U11 | `u11-s-account-auth` |
| US12.1 | 보호자를 초대하고 열람 권한 정하기 | Should | U12 | `u12-s-guardian-sharing` |
| US12.2 | 보호자로서 허락된 범위만 열람하기 | Should | U12 | `u12-s-guardian-sharing` |
| US12.3 | 원음 보관 기간 정하고 서비스 안내 다시 보기 | Should | U12 | `u12-s-guardian-sharing` |
| US13.1 | 노트북 브라우저에서도 제대로 보기 | Should | U13 | `u13-s-laptop-layout` |
| US14.1 | 쌓인 기록을 반영한 다음 코칭 추천 받기 | Should | U14 | `u14-s-recommendation-plus` |

배치 기준은 기능 F01~F07 이다 `[Q1]`. 사용자가 직접 답하지 않은 배치(US1 → U2, US9.1·US9.2 → U1, US9.3 → U8,
US3.2 → U3, US3.3 → U9)는 리드가 정했고 요약 확인에서 승인되었다 (D-94).

---

## 여러 단위에 걸친 스토리

스토리는 한 단위에만 배정한다. 아래는 배정된 단위 밖의 코드나 데이터에 기대는 스토리다. 기대는 쪽이 아직
없으면 계약(2.8)과 시드로 대신한다 `[Q5]`.

| 스토리 | 배정 단위 | 기대는 단위 | 걸치는 내용 |
|---|---|---|---|
| US1.2 | U2 | U3, U7, U8 | 홈의 진입 버튼이 가져오기·연습·기록 화면으로 이동한다(화면 이동이라 의존은 아니다 `[stories]`) |
| US2.1 | U3 | U1 | 걷는 뼈대 관통 경로 — US9.1·AC9.2.1·AC9.2.3 에 기댄다 |
| US3.1 | U3 | U4 | 전사 확인 화면이 맥락 네 항목을 함께 보여 준다 |
| US3.3 | U9 | U3, U5, U6 | 정정 사건(U3) → 재검토 표시·재분석(U5 의 판정) → 추천 재계산 대기(U6) |
| US4.3 | U5 | U4, U6 | 맥락 수정 화면(U4)과 목표 선택 화면(U6)으로 이동한다 |
| US5.2 | U6 | U7 | 고른 목표로 연습이 시작되는 쪽은 U7 이 받는다(AC6.5.5) |
| US6.2·US6.3 | U7 | U5 | 시도 판정을 Assessment 저장 규칙으로 저장한다(ADR-004) |
| US7.1·US7.2 | U8 | U3, U5, U7 | 실제 대화·판정·연습 기록을 읽어 집계한다 |
| US7.2 | U8 | U9 | 재분석 뒤 대체된 판정을 분모에서 뺀다(D-74) |
| US8.1·US8.2 | U9 | U3, U5, U6, U7 | 각 컴포넌트의 데이터 정리 인터페이스를 한 트랜잭션에서 부른다(ADR-006) |
| US9.3 | U8 | U2~U7 | SM1 종단 리허설 — 동의부터 기록까지의 흐름이 통합되어야 통과한다(AC9.3.1). 정정·삭제(U9)는 이 흐름에 없다 (OQ-U3) |
| US10.3 | U10 | U9 | 정정 이력과 삭제 뒤 상태 |
| US12.1·US12.2 | U12 | U11, U8 | 로그인한 보호자(U11), 열람 데이터 모양(U8 의 Record 응답) |
| US12.3 | U12 | U2 | 서비스 안내 다시 보기는 U2 의 첫 방문 안내를 재사용한다 |
| US13.1 | U13 | U2~U12 의 화면 | 넓은 화면에서 모든 Must 화면을 다시 점검한다 |
| US14.1 | U14 | U8 | U8 의 다음 코칭 추천 Must 규칙을 넓힌다 |

---

## 단위 안의 구현 순서

`stories.md` 의 스토리 의존을 단위 안으로 좁힌 순서다. 단위 사이의 순서와 갈래 배정은 delivery-planning(2.9)이
정한다.

| Unit | 순서 | 근거 |
|---|---|---|
| U1 | US9.1 → US9.2 | US9.2 는 US9.1 에 의존 |
| U2 | US1.1 → US1.2 | US1.2 는 US1.1 에 의존(화면 이동) |
| U3 | US2.1 → US2.2 → US3.1 → US3.2 | US2.2·US3.1 은 US2.1, US3.2 는 US3.1 에 의존. US3.1 의 맥락 표시는 U4 계약으로 대신 |
| U4 | US2.3 | 단일 스토리 |
| U5 | US4.1 → US4.2 → US4.4 → US4.3 | US4.2·US4.4 는 US4.1 에 의존. US4.3 은 U4·U6 화면으로의 이동을 담아 마지막 |
| U6 | US5.1 → US5.2 | US5.2 는 US5.1 에 의존 |
| U7 | US6.1 → US6.2 → US6.3 → US6.4 → US6.5 | US6.2 는 US6.1, US6.3·US6.4 는 US6.2, US6.5 는 US6.3 에 의존 |
| U8 | US7.1 → US7.2 → US7.3 → US9.3 | US7.2 는 US7.1, US7.3 은 US7.2, US9.3 은 US7.2 에 의존 |
| U9 | US3.3 → US8.1 → US8.2 → US8.3 | US8.1 의 AC8.1.3 은 US3.3, US8.2 는 US8.1 에 의존. US8.3 은 단위 안 의존이 없어 마지막에 둔다 |
| U10 | US10.1 → US10.2 → US10.3 | 단위 안 의존은 없다. US10.3 이 U9 결과에 가장 많이 기대어 마지막 |
| U11 | US11.1 | 단일 스토리 |
| U12 | US12.1 → US12.2 → US12.3 | US12.2 는 US12.1 에 의존. US12.3 은 단위 안 의존이 없다 |
| U13 | US13.1 | 단일 스토리 |
| U14 | US14.1 | 단일 스토리 |

---

## 누락 점검

| 점검 | 결과 |
|---|---|
| 모든 스토리가 단위에 배정되었는가 | 예 — 37/37 (Must 28, Should 9) |
| 모든 단위에 스토리가 있는가 | 예 — U1~U14 모두 1개 이상 |
| 한 스토리가 두 단위에 배정되었는가 | 아니오 — 걸치는 스토리는 위 표에 따로 적었다 |
| Must 스토리가 Should 단위에 들어갔는가 | 아니오 `[Q3]` |
| Should 스토리가 Must 단위에 들어갔는가 | 아니오 `[Q3]` |

단위별 스토리 수: U1 2 · U2 2 · U3 4 · U4 1 · U5 4 · U6 2 · U7 5 · U8 4 · U9 4 · U10 3 · U11 1 · U12 3 · U13 1 · U14 1.
