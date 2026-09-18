# Domain Model — 판정 규칙과 데이터 구조

> 기획서의 온톨로지 개념(대화·발화·맥락·사건·행동·근거·목표·시도·도움 수준)을 MVP용 관계형 모델로 정리한 것이다.
> **이 문서가 데이터 구조의 유일한 기준**이며, 별도 온톨로지 파일이나 그래프 DB는 사용하지 않는다.

## 1. 핵심 연결

```
Conversation ─< Utterance
Conversation ─ ContextInfo
Conversation ─< SocialEvent ─< BehaviorJudgment ─< Evidence(utterance ids)
SocialEvent ─< TrainingGoal ─< PracticeSession ─< Attempt ─< HintEvent
TrainingGoal ─< Recommendation
모든 판정·시도 ─ VersionInfo(criteria, prompt, model, transcript)
Utterance ─< Correction      User ─< DeletionRequest      User ─< SharingSetting
```

## 2. 엔티티

| 엔티티 | 주요 필드 |
|---|---|
| User | id, displayName, ageBand(선택), languageBackground(선택·확장용), createdAt |
| SharingSetting | userId, supporterId, level(NONE/SUMMARY/FULL) |
| Conversation | id, userId, source(UPLOAD/RECORD/SYNTHETIC), status(UPLOADING/TRANSCRIBING/READY/FAILED), audioAssetId, transcriptVersion, createdAt |
| AudioAsset | id, path, durationSec, retentionUntil, deletedAt |
| Utterance | id, conversationId, seq, speaker(USER/PARTNER/UNKNOWN), startMs, endMs, text, sttConfidence, unclear(bool), excluded(bool), edited(bool) |
| Correction | id, utteranceId, field, before, after, correctedAt |
| ContextInfo | conversationId, relation, place, purpose, userGoal — 각 값은 `{value, status: CONFIRMED/USER_REPORTED/UNKNOWN}` |
| SocialEvent | id, conversationId, utteranceRange, summary, confirmedFacts(JSONB), modelInferences(JSONB) |
| BehaviorJudgment | id, socialEventId, group, mode(REAL/ROLEPLAY), performanceMode(INDEPENDENT/HINTED), opportunity, result, holdReason, rationale, alternatives(JSONB), versionInfoId, needsReview(bool) |
| Evidence | judgmentId, utteranceIds[], role(OPPORTUNITY/RESPONSE/REPAIR) |
| TrainingGoal | id, userId, sourceEventId, sourceJudgmentId, group, title, status(ACTIVE/PAUSED/DONE), selectedBy(USER/RECOMMENDED_ACCEPTED) |
| Recommendation | id, userId, goalId, reason, sourceIds[], sufficiency(SUFFICIENT/INSUFFICIENT), userChoice(ACCEPTED/CHANGED/DECLINED) |
| ScenarioTemplate | id, group, title, situation, partnerRole, ageBand, reviewStatus(REVIEWED) |
| ScenarioVariant | id, templateId, variationRules(JSONB), distance(SAME_CONTEXT/NEAR), skillPreserved(REVIEWED/PENDING) |
| PracticeSession | id, goalId, variantId, status(IN_PROGRESS/PAUSED/COMPLETED/ABORTED) |
| Attempt | id, sessionId, order, performanceMode, responseText, judgmentId, createdAt (수정 불가) |
| HintEvent | id, sessionId, attemptOrder, level(ATTENTION_CUE/INFO_HINT/EXAMPLE), content |
| VersionInfo | id, criteriaVersion, promptVersion, modelName, transcriptVersion |
| DeletionRequest | id, userId, targetType, targetId, affectedItems(JSONB), status(REQUESTED/DONE/PARTIAL), note |

## 3. 판정 상태

- `opportunity`: **PRESENT / ABSENT / UNCERTAIN**
- `result` (opportunity=PRESENT이고 분석 가능할 때만): **OBSERVED / PARTIAL / NOT_OBSERVED_THIS_TIME**
- `holdReason`: **NO_OPPORTUNITY / INSUFFICIENT_CONTEXT / UNCLEAR_TRANSCRIPT / UNSUPPORTED_MODALITY / INVALID_EVIDENCE**
- `result`와 `holdReason`은 동시에 값을 가지지 않는다.

## 4. 행동 묶음 조작적 정의 (개발용 초안, 공식 척도 아님)

| group | 관찰 기회 | 목표 행동 | 실패로 보지 않는 경우 |
|---|---|---|---|
| RESPONSE_RELEVANCE (응답 관련성) | 상대의 질문·요청·직전 발화가 특정 정보나 기능을 기대함 | 기대된 정보·기능에 연결된 반응 | 짧은 답, 정당한 거절, 도움 요청, "모르겠어" |
| CLARIFICATION_REPAIR (명료화·대화 수리) | 모호성·이해 불일치가 드러남(상대의 되묻기, 엇갈린 응답) | 되묻기, 재설명, 정보 추가 등 해결 시도 | 수리 기회가 없음. 상대가 이해했는지는 별도 기록 |
| TOPIC_MAINTENANCE (주제 유지·전환) | 공유 목표·화제가 진행 중 | 화제 유지 또는 상황에 맞는 전환·종료 신호 | 모든 화제 변경을 이탈로 보지 않음. 관계·목적·상대 반응 확인 |

명료화와 수리는 한 흐름으로 기록해 중복 감점하지 않는다.

## 5. 규칙

1. **분모 규칙**: 집계 분모는 `opportunity=PRESENT && holdReason=null`인 판정 수. 같은 performanceMode·mode끼리만 집계.
2. **비교 불충분**: 유효 기회가 `minOpportunities`(기본 3) 미만이면 추이를 숫자로 보이지 않고 INSUFFICIENT_FOR_COMPARISON.
3. **근거 필수**: Evidence가 없거나 존재하지 않는 utteranceId를 가리키면 holdReason=INVALID_EVIDENCE.
4. **불명확 발화**: unclear=true이고 수정되지 않은 발화가 근거의 핵심이면 UNCLEAR_TRANSCRIPT.
5. **맥락 부족**: 판정에 필요한 ContextInfo 값이 UNKNOWN이고 앞뒤 발화로 보완되지 않으면 INSUFFICIENT_CONTEXT.
6. **정정 전파**: Utterance 수정·제외 시 그 발화를 근거로 한 판정에 needsReview=true, 관련 추천은 재계산 대기.
7. **시도 불변**: Attempt는 생성 후 수정 불가. 재시도는 order+1로 새로 생성. HintEvent 이후 시도는 HINTED.
8. **추천**: 반복 어려움(NOT_OBSERVED_THIS_TIME 반복), 성공 조건(HINTED에서 OBSERVED), 사용자 선택 이력을 반영. 기록이 부족하면 sufficiency=INSUFFICIENT로 표시. 난이도 점수 공식은 만들지 않는다.
9. **변형 제한**: skillPreserved=REVIEWED인 ScenarioVariant만 제공. distance는 SAME_CONTEXT/NEAR만. 없으면 검토된 원형 제공.
10. **삭제 전파**: Conversation 삭제 시 AudioAsset, Utterance, Correction, SocialEvent, BehaviorJudgment, Evidence 삭제. 이를 원인으로 한 TrainingGoal·Recommendation은 사용자에게 함께 삭제/유지 선택을 묻는다. 처리 결과를 affectedItems에 기록.
11. **보안**: 전사 텍스트 속 "지금부터 ~해라" 같은 지시문은 분석 대상 데이터로만 처리한다.
