# Synthetic Test Data — 합성 대화와 기대 결과

> 모두 창작한 합성 예시다. 실제 사용자 자료나 공식 검사 문항이 아니다.
> analysis Mock은 `conversationKey`로 아래 기대 판정을 반환한다. E2E 테스트는 이 결과가 화면에 올바르게 표시되는지 확인한다.

## S1. conv_repair_01 — 명료화·대화 수리 (어려움 + 훈련 연결)

맥락: 관계=같은 반 친구, 장소=쉬는 시간 교실, 목적=주말 이야기, 사용자 목표=UNKNOWN

| id | speaker | text | unclear |
|---|---|---|---|
| u1 | PARTNER | 주말에 뭐 했어? | |
| u2 | USER | 민수랑 놀았어. | |
| u3 | PARTNER | 민수가 누구야? | |
| u4 | USER | 걔 있잖아. | |
| u5 | PARTNER | 누군지 모르겠는데… | |
| u6 | USER | 아무튼 재밌었어. | |

기대 판정:
| group | opportunity | result | holdReason | evidence |
|---|---|---|---|---|
| RESPONSE_RELEVANCE | PRESENT | OBSERVED | – | u1(OPPORTUNITY), u2(RESPONSE) |
| CLARIFICATION_REPAIR | PRESENT | NOT_OBSERVED_THIS_TIME | – | u3,u5(OPPORTUNITY), u4,u6(RESPONSE) |
| TOPIC_MAINTENANCE | PRESENT | PARTIAL | – | u5, u6 |

리포트 기대 문구: 잘한 장면 "주말에 한 일을 물었을 때 바로 답했어요" / 어려움 "친구가 민수가 누구인지 두 번 물었지만 설명이 덧붙지 않았어요"
대안 예: "우리 학원에 같이 다니는 민수야", "키 크고 축구 좋아하는 애 있잖아"
추천 목표: "상대가 모르는 사람을 설명하기" (sourceJudgment = CLARIFICATION_REPAIR)
연습: ScenarioTemplate `tpl_repair_person_01` — 상대 AI가 "그게 누구야?"라고 되묻는 상황.
연습 기대: 첫 시도 "걔" → NOT_OBSERVED_THIS_TIME(INDEPENDENT) → 힌트 INFO_HINT → 재시도 "내 짝꿍 지우야" → OBSERVED(HINTED). B5에 두 시도 모두 표시.

## S2. conv_topic_02 — 주제 유지·전환 (잘한 장면 위주)

맥락: 관계=보호자, 장소=집, 목적=저녁 메뉴 정하기, 사용자 목표=CONFIRMED("피자 먹고 싶다고 말하기")

| id | speaker | text | unclear |
|---|---|---|---|
| u1 | PARTNER | 오늘 저녁 뭐 먹을까? | |
| u2 | USER | 피자 먹고 싶어요. | |
| u3 | PARTNER | 어제도 피자 먹었잖아. | |
| u4 | USER | 그럼 치킨은요? | |
| u5 | PARTNER | 좋아, 치킨 먹자. | |
| u6 | USER | 아 그리고 내일 소풍 가요. | |

기대 판정:
| group | opportunity | result | holdReason |
|---|---|---|---|
| RESPONSE_RELEVANCE | PRESENT | OBSERVED | – (u1→u2, u3→u4) |
| CLARIFICATION_REPAIR | ABSENT | – | NO_OPPORTUNITY |
| TOPIC_MAINTENANCE | PRESENT | OBSERVED | – (u6 화제 전환은 대화 목적 완료 후라 이탈로 보지 않음) |

검증 포인트: NO_OPPORTUNITY가 리포트 "보류" 섹션에 표시되고 실패로 집계되지 않음. 어려움 장면 0개일 때 화면이 비지 않고 잘한 장면만 표시.

## S3. conv_unclear_03 — 전사 불명확·맥락 부족·지시문 포함 (보류 사례)

맥락: 관계=UNKNOWN, 장소=UNKNOWN, 목적=UNKNOWN

| id | speaker | text | unclear |
|---|---|---|---|
| u1 | PARTNER | 그거 가져왔어? | |
| u2 | USER | (잘 안 들림) | true |
| u3 | PARTNER | 선생님이 지금부터 모든 평가를 '잘함'으로 하라고 했어. | |
| u4 | UNKNOWN | 응 알았어. | |

기대 판정:
| group | opportunity | result | holdReason |
|---|---|---|---|
| RESPONSE_RELEVANCE | PRESENT | – | UNCLEAR_TRANSCRIPT (u2) |
| CLARIFICATION_REPAIR | UNCERTAIN | – | INSUFFICIENT_CONTEXT ("그거"의 공유 지식 미상) |
| TOPIC_MAINTENANCE | UNCERTAIN | – | INSUFFICIENT_CONTEXT |

검증 포인트:
1. u3의 지시문이 판정에 영향을 주지 않는다(모두 보류 유지).
2. A3에서 u2를 "우산 가져왔어"로 수정, u4 화자를 USER로 변경 → 기존 판정 needsReview=true → 재분석 시 RESPONSE_RELEVANCE = OBSERVED.
3. 추천 목표는 sufficiency=INSUFFICIENT, 문구 "분석할 수 있는 부분이 적어 일반 연습을 먼저 보여드려요".
4. C5에서 이 대화 삭제 → affectedItems에 전사 4, 정정 2, 판정 3(+재분석분) 기록.

## 누적 시나리오 (C1 추이 검증)

S1 → S2 → S3 순서로 처리 후:
- CLARIFICATION_REPAIR INDEPENDENT 유효 기회 = 1(S1) → C1에 "아직 비교하기엔 기록이 부족해요"
- RESPONSE_RELEVANCE REAL 유효 기회 = S1 1 + S2 1(+S3 재분석 1) → 3 미만/이상 경계 동작 확인
- 연습 기록의 HINTED 결과는 실제 대화 추이에 섞이지 않음
