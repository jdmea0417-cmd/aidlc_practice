# Entities — u1-backend-foundation

**Stage**: functional-design (3.1) · **Unit**: u1-backend-foundation (U1 백엔드 기반)
**작성일**: 2026-09-18

## Sources

| 태그 | 출처 |
|---|---|
| `[unit]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/unit-of-work.md` — U1 정의(가지는 것·넘기는 것·경계) |
| `[map]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/unit-of-work-story-map.md` — U1 에 배정된 스토리 US9.1·US9.2 |
| `[req]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/requirements.md` — FR11.1, NFR5, NFR10 |
| `[components]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/domain-design/components.md` — Account, ProviderAdapters 컴포넌트 |
| `[contract]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md` — C1, C14, C15, C16 |
| `[Q<n>]` | `functional-design-questions.md` — 이 단계에서 사용자가 답한 내용 |
| `[spec:04]` | `docs/input/04_domain-model.md` — 기존 명세의 데이터 모델과 상태값 |

**이 문서의 범위** — U1 이 **소유**하는 엔티티는 `User` 하나다 `[contract]` C15. 다만 U1 은 엔티티 20개의 테이블을
초기 리비전 하나로 만들므로(D-102), 나머지 19개에 대해 **이번에 무엇을 적고 무엇을 남기는지**를 아래 §3 에
등록해 둔다. 그 19개의 속성 상세는 각 소유 단위의 기능 설계가 정한다 `[Q1]`.

---

## 1. 엔티티 모델 (U1 소유)

```yaml
entities:
  - name: User
    description: >
      서비스를 쓰는 사람. Must 경로는 시드된 고정 사용자 한 명으로 돌고, 그 사용자는 동의 전 상태로
      시작한다. 보호자도 같은 엔티티에 역할로 구분해 담는다. 사용자 삭제는 이번 범위에 없으므로
      삭제 전파 대상이 아니다.
    attributes:
      - name: id
        type: 식별자
        required: true
        unique: true
        description: 사용자를 가리키는 값. 다른 엔티티가 이 값으로 사용자를 참조한다.
      - name: displayName
        type: 짧은 텍스트
        required: true
        constraints: 빈 문자열 금지
        description: 화면에 보이는 이름. 합성 데이터만 들어간다.
      - name: role
        type: 열거값
        required: true
        allowed_values: [USER, GUARDIAN]
        default: USER
        description: 주 사용자인지 보호자인지. 시드 고정 사용자는 USER 다.
      - name: ageBand
        type: 짧은 텍스트
        required: false
        description: 연령대. 개인 식별에 쓰지 않는 구간 값이며 판정에 쓰이지 않는다.
      - name: languageBackground
        type: 짧은 텍스트
        required: false
        description: 언어 배경. 판정 기준을 바꾸지 않는 참고 값이다.
      - name: consentedAt
        type: 시각
        required: false
        description: >
          첫 방문 서비스 안내에 동의한 시각. 비어 있으면 아직 동의하지 않은 것이다. 이 한 값이
          동의 여부를 나타내며 별도의 불리언을 두지 않는다.
      - name: createdAt
        type: 시각
        required: true
        description: 만들어진 시각.
    constraints:
      - id: 사용자마다 식별자는 하나이고 바뀌지 않는다
      - consent: consentedAt 은 한 번 값이 들어가면 되돌리지 않는다 — 동의 철회는 이번 범위 밖이다
    relationships:
      - target: Conversation
        cardinality: 1..N
        direction: User → Conversation
        note: 각 대화는 사용자 한 명에게 속한다. Conversation 자체는 u3-f01-capture 가 소유한다.
      - target: GuardianInvitation
        cardinality: 1..N
        direction: User → GuardianInvitation
        note: >
          초대는 사용자 한 명이 만들고 보호자 한 명이 수락한다. 초대의 속성 상세는
          u12-s-guardian-sharing 이 정한다. U1 은 테이블과 사용자 참조만 만든다.
```

**요약** — U1 이 정의하는 엔티티는 `User` 하나다. 이 엔티티는 두 가지 일을 한다: 시연이 로그인 없이 돌게 하는
고정 사용자의 자리가 되고(FR11.1, AC9.2.1), 첫 방문 동의 상태를 사용자 단위로 들고 있다. 동의는 별도 불리언
없이 `consentedAt` 한 값으로 나타내며, 비어 있음이 "아직 동의 전"을 뜻한다. 이 모양은 계약 C1 의 `Me` 응답
(`id`, `displayName`, `role`, `consentedAt`)과 그대로 맞물린다.

---

## 2. 저장소가 아닌 값 (엔티티가 아님)

U1 이 다루지만 테이블로 저장하지 않는 것들이다. 혼동을 막기 위해 여기에 적어 둔다.

| 값 | 어디에 사는가 | 왜 엔티티가 아닌가 |
|---|---|---|
| 분석 모드(mock / live) | 환경변수를 기동 시 한 번 읽어 만든 설정 객체 | 실행 환경의 설정이지 사용자 데이터가 아니다. 기동할 때마다 다시 정해진다 |
| 요청 식별자(`request_id`) | 요청·작업의 수명 동안만 존재하고 로그에 남는다 | 조회 대상이 아니라 로그를 잇는 표식이다 `[Q6]` |
| 합성 대화 기대 판정 픽스처 | `backend/app/fixtures/` 의 파일 세 개 | 저장소가 아니라 코드와 테스트가 함께 읽는 고정 입력이다 `[Q5]` |
| 시나리오 원형·변형 | 테이블(`scenario_templates`, `scenario_variants`)에 시드로 들어간다 | 엔티티이긴 하나 소유는 u7-f05-practice 다. U1 은 시드만 넣는다 `[contract]` C16 |

---

## 3. 초기 리비전이 만드는 나머지 19개 테이블

U1 은 엔티티 20개의 테이블을 초기 리비전 하나로 만든다(D-102) `[contract]` C15. 이번 리비전에 **U1 이 적는
것**은 계약과 기존 명세가 이미 글로 확정한 것뿐이고, 그 밖의 세부는 각 소유 단위가 나중에 리비전으로 더한다
`[Q1]`. 아래 표의 "U1 이 지금 적는 것" 칸이 그 경계다.

| 테이블 | 엔티티 | 컴포넌트 | 속성 상세 소유 단위 | U1 이 지금 적는 것 |
|---|---|---|---|---|
| `users` | User | account | **u1-backend-foundation** | §1 전체 |
| `guardian_invitations` | GuardianInvitation | account | u12-s-guardian-sharing | 사용자 참조, 초대 코드 유일성 |
| `conversations` | Conversation | conversation | u3-f01-capture | 사용자 참조, **상태 컬럼 둘과 전사 실패 사유(§4)**, 전사 버전, 대화 키. 내부 값 ↔ API 값 변환의 책임도 이 단위가 진다(§4 대응표) |
| `audio_assets` | AudioAsset | conversation | u3-f01-capture | 대화 참조. **음성 본문을 넣는 컬럼을 두지 않는다**(TC-05) |
| `utterances` | Utterance | conversation | u3-f01-capture | 대화 참조, 발화 순번 |
| `corrections` | Correction | conversation | u3-f01-capture | 발화 참조, 만든 시각 |
| `context_infos` | ContextInfo | conversation | u4-f02-context | 대화 참조, 값과 상태(확인됨 / 사용자 보고 / 미상) `[spec:04]` |
| `social_events` | SocialEvent | assessment | u5-f03-assessment | 대화 참조 |
| `behavior_judgments` | BehaviorJudgment | assessment | u5-f03-assessment | **출처 네 컬럼 NOT NULL**, `supersedes_judgment_id`, `needs_review` `[contract]` C15 |
| `evidences` | Evidence | assessment | u5-f03-assessment | 판정 참조, 발화 참조 |
| `analysis_feedbacks` | AnalysisFeedback | assessment | u5-f03-assessment | 대화 참조, 남긴 시각 |
| `training_goals` | TrainingGoal | training | u6-f04-goal | 사용자 참조. `source_event_id`·`source_judgment_id` 는 **CASCADE 로 지우지 않고 앱이 비운다** `[contract]` C15 |
| `recommendations` | Recommendation | training | u6-f04-goal | 사용자 참조 |
| `scenario_templates` | ScenarioTemplate | training | u7-f05-practice | 시드 6개가 들어갈 자리 `[contract]` C16 |
| `scenario_variants` | ScenarioVariant | training | u7-f05-practice | 원형 참조 |
| `practice_sessions` | PracticeSession | training | u7-f05-practice | 사용자 참조, 목표 참조 |
| `attempts` | Attempt | training | u7-f05-practice | 세션 참조, 시도 순번 |
| `hint_events` | HintEvent | training | u7-f05-practice | 시도 참조 |
| `deletion_requests` | DeletionRequest | privacy | u9-f07-correction-deletion | 사용자 참조, **지울 파일 경로 목록**, 일부 완료 상태 (ADR-006) |
| `sharing_settings` | SharingSetting | privacy | u12-s-guardian-sharing | **`level` 허용값 NONE / SUMMARY / FULL, 기본 NONE** (FR11.2) |

**이 표의 규칙**

- U1 은 위 "지금 적는 것" 밖의 타입·제약·허용값을 **추측해 적지 않는다.** 소유 단위가 자기 기능 설계에서 정하고
  같은 단위의 리비전으로 더한다 `[Q1]`.
- 외래 키의 `ON DELETE CASCADE` 는 **그물로만** 둔다. 실제 삭제 순서는 계약 C13 과 privacy 의 삭제 유스케이스가
  정한다 `[contract]` C15.
- 가변 구조(판정 대안 목록, 변형 규칙)는 구조화된 문서 컬럼으로 둔다 `[contract]` C15.
- 컬럼을 더하는 단위는 같은 PR 에서 U1 담당자에게 시드 갱신을 요청하고, U1 담당자가 리뷰어로 들어간다
  `[contract]` C16.

---

## 4. 대화의 상태를 두 값으로 나눈다

계약 C15 가 "전사 상태와 분석 상태를 컬럼 하나로 둘지 둘로 둘지"를 이 단계로 넘겼고, **둘로 나누기로**
정했다 `[Q2]`. 도메인 설계의 `Conversation` 속성 목록에 적힌 `status` 한 자리가 이 결정으로 두 자리가 된다 —
상위 문서를 뒤집은 것이 아니라 상위 문서가 이 단계에 남겨 둔 자리를 채운 것이다.

| 값 | 무엇을 나타내는가 | 허용값 |
|---|---|---|
| `transcript_status` | 음성을 받아 전사가 준비되기까지 | `UPLOADING` · `TRANSCRIBING` · `TRANSCRIBED` · `TRANSCRIBE_FAILED` |
| `transcript_failure_reason` | 위가 `TRANSCRIBE_FAILED` 일 때 **무엇이** 실패했는가 | `STORAGE` · `TRANSCRIPTION` (그 밖의 상태에서는 비어 있다) |
| `analysis_status` | 전사를 재료로 판정이 만들어지기까지 | `NOT_ANALYZED` · `ANALYZING` · `ANALYZED` · `ANALYZE_FAILED` |

- 두 값은 **독립적으로 움직인다.** 재분석은 `analysis_status` 만 바꾸고 `transcript_status` 를 건드리지 않으므로,
  재분석 중에도 화면은 전사를 계속 보여 줄 수 있다.
- 실패가 어느 쪽 실패인지 값 자체로 갈린다. 화면의 "다시 시도"가 전사 재시도인지 재분석인지 판단할 수 있다.
- **전사 실패는 다시 한 번 갈린다.** 파일이 디스크에 아예 쓰이지 못한 실패(`STORAGE`)와, 파일은 있는데 전사가
  실패한 것(`TRANSCRIPTION`)은 회복 경로가 다르다. 사유 값이 그 둘을 가른다 — 자세한 전이는 `functional-spec.md`
  §2 SM-A, 규칙은 `rules.md` BR7.5 다.
- 조합 규칙은 `rules.md` 의 BR7 이 맡는다(전사가 끝나기 전에는 분석이 시작될 수 없다 등).

### 내부 값과 계약 값의 대응

**여기 적은 값은 저장소 안의 값이고, 계약 C2 가 정한 API 응답 값과 이름이 다르다.** 상위 계약을 바꾸지 않고
내부 이름을 따로 둔 것이므로, 어느 것이 어느 것으로 바뀌는지를 아래에 못박는다. 이 표가 없으면 같은 것을 두
이름으로 부르게 되고, 팀 관행 Code Style 이 경계하는 이름 분기가 바로 여기서 시작된다.

| 내부 저장 값 | API 응답 값 (계약 C2) | 어느 필드 |
|---|---|---|
| `transcript_status = UPLOADING` | `status = UPLOADING` | `status` |
| `transcript_status = TRANSCRIBING` | `status = TRANSCRIBING` | `status` |
| `transcript_status = TRANSCRIBED` | `status = READY` | `status` |
| `transcript_status = TRANSCRIBE_FAILED` | `status = FAILED` | `status` |
| `analysis_status = NOT_ANALYZED` | `analysisStatus = NOT_STARTED` | `analysisStatus` |
| `analysis_status = ANALYZING` | `analysisStatus = ANALYZING` | `analysisStatus` |
| `analysis_status = ANALYZED` | `analysisStatus = ANALYZED` | `analysisStatus` |
| `analysis_status = ANALYZE_FAILED` | `analysisStatus = FAILED` | `analysisStatus` |
| `transcript_failure_reason` | **내보내지 않는다** | — |

- **변환하는 자리**: API 계층의 응답 모델 한 곳이다. 업무 계층과 저장소 계층은 내부 값만 다룬다.
- **변환의 책임 단위**: `conversations` 의 컬럼 상세를 소유하는 **u3-f01-capture** 다(§3 표). U1 은 값의 목록과
  이 대응표를 고정하고, 실제 변환 코드는 그 단위가 쓴다.
- **계약 C16 의 "S1 전사 READY" 표기**는 API 값을 가리킨 것이며, 이 표의 `transcript_status = TRANSCRIBED` 와 같은
  상태를 말한다. 시드 상태 이름과 이 표가 어긋나 보이면 이 표가 기준이다.
- `transcript_failure_reason` 은 내부 회복 경로를 고르기 위한 값이라 응답에 싣지 않는다. 화면이 보여 줄 실패
  안내 문구는 계약 C2 의 오류 봉투가 맡는다.
- 이 경계를 검사 가능한 문장으로 만든 것이 `rules.md` 의 BR7.4 다.
- API 응답은 계약 C2 의 두 필드를 그대로 유지한다 — 이 결정은 저장 모양에 대한 것이고 계약을 바꾸지 않는다.

---

## Assumptions & Open Questions

### 가정

- `User` 의 `ageBand`·`languageBackground` 를 선택 항목으로 둔 것은 도메인 설계의 속성 목록을 그대로 따른 것이며,
  Must 경로의 시드 사용자는 이 값 없이도 성립한다.
- 동의 철회 경로가 없다는 전제로 `consentedAt` 을 되돌리지 않게 했다. 도메인 설계가 사용자 삭제를 범위 밖으로
  둔 것과 같은 결에 있다 `[components]`.

### 열린 질문

| ID | 질문 | 담당 단계 |
|---|---|---|
| OQ-F1 | `users` 의 `displayName` 길이 상한을 둘지. 합성 데이터만 들어오므로 지금은 두지 않았다. 화면 레이아웃이 상한을 요구하면 그때 정한다 | u2-web-foundation 기능 설계 |
| OQ-F2 | 시드 고정 사용자의 식별자를 고정값으로 박을지, 시드가 만들 때마다 새로 만들지. 테스트가 그 값을 직접 쓰는지에 달려 있다 | 이 단위의 code-generation (3.5) |
