# Contract Summary — SCD 소통 코칭 MVP

**Stage**: contract-design (2.8)
**작성일**: 2026-09-17
**기준 문서 선언**: 이 문서가 단위 사이 계약의 기준이다. 구현이 이 문서와 어긋나면 구현을 고치고, 계약을 바꾸려면
이 문서를 먼저(같은 PR 에서) 고친다 `[Q4]` (D-99). FastAPI 가 생성하는 `openapi.json` 과 프론트엔드 생성 타입은 이
문서를 따르는 결과물이다.

## Sources

| 태그 | 출처 |
|---|---|
| `[units]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/unit-of-work.md`, `unit-of-work-dependency.md` |
| `[components]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/domain-design/components.md`, `decisions.md` (ADR-001~010) |
| `[req]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/requirements.md` |
| `[practices]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/practices-discovery/team-practices.md` |
| `[spec:02]`, `[spec:04]`, `[spec:05]`, `[spec:06]` | `docs/input/02_tech-environment.md`, `04_domain-model.md`, `05_synthetic-test-data.md`, `06_seed-scenarios.md` |
| `[Q<n>]` | `contract-design-questions.md` — 이 단계에서 사용자가 답한 내용 |
| `[log]` | `docs/decisions/decision-log.md` (D-96~D-105) |

reverse-engineering(2.1)과 refined-mockups(2.5)는 범위 밖이다. 기존 API 나 고충실도 화면 설계가 입력에 없는 것은
결손이 아니라 범위 밖이다. `[spec:02]` §7 의 `/api/conversations`, `/api/assess` 경로는 명세 예시 코드이며, 이 문서의
`/api/v1` 경로가 대체한다.

**외부 공개 API 는 없다** — 로컬 시연용 단일 서비스이고 소비자는 우리 프론트엔드뿐이다. 모든 계약은 시스템 안의
경계다. 외부로 나가는 호출은 STT·LLM 제공자(live, 미정 D-37)뿐이며, 그 경계는 포트 계약(C14)이 감싼다.

---

## 공통 규칙 (모든 REST 계약에 적용)

| 항목 | 규칙 | 근거 |
|---|---|---|
| 경로 | 모두 `/api/v1` 아래. 버전을 여러 개 동시에 유지하지 않는다 | `[Q4]` 리드 해석 (D-99) |
| 오류 응답 | `{"error": {"code": "<ENGLISH_TOKEN>", "message": "<한국어>", "details": [...], "request_id": "..."}}` 하나로 고정. 404 `NOT_FOUND`, 403 `PERMISSION_DENIED`, 409 `CONFLICT`, 413 `PAYLOAD_TOO_LARGE`, 422 `VALIDATION_ERROR`, 502 `PROVIDER_ERROR`, 504 `PROVIDER_TIMEOUT`, 500 `INTERNAL_ERROR` | `[practices]` Code Style, `[req]` NFR12 |
| 필드 이름 | JSON 은 camelCase, Python 은 snake_case 로 두고 Pydantic alias 로 바꾼다 | `[practices]` Code Style |
| 변경 | 필드 추가는 자유 — 받는 쪽은 모르는 필드를 무시한다. 이름 변경·삭제는 소비 단위 담당자의 PR 승인 + 같은 PR 에서 이 문서 수정 | `[Q5]` (D-100) |
| 오래 걸리는 작업 | 업로드·전사·분석·재분석은 `202 Accepted` + 상태 조회. 화면은 1초 간격으로 상태를 조회하고 `FAILED` 면 다시 시도 버튼을 보인다 | `[Q1]` (D-96) |
| 백그라운드 작업의 DB 세션 | 전사·분석·재분석 백그라운드 작업은 요청에 `Depends` 로 주입된 세션을 재사용하지 않는다 — 그 세션은 응답이 나갈 때 이미 닫혀 있다. 작업은 ID 만 넘겨받아 세션 팩토리로 **새 세션을 직접 열고**, 작업 단위의 `service` 경계에서 한 번 커밋하고 닫는다. 예외가 나면 롤백한 뒤 별도 세션으로 상태를 `FAILED` 로 기록한다. 요청 경로의 "요청당 세션 하나, 커밋은 service 경계에서 한 번" 관행은 그대로이며, 이 행은 요청 밖에서 도는 작업에만 적용하는 구분선이다. 세션 팩토리의 위치·주입 방식 세부는 functional-design(3.1)이 정한다 | `[practices]` Code Style, 검토 R-02 반영 |
| 재시도 | 프론트엔드는 비멱등 호출(POST)을 자동 재시도하지 않는다. 제공자 호출은 백엔드 어댑터에서 타임아웃·연결 실패에만 1회 재시도 | `[practices]`, `[req]` NFR13 |
| 금지 필드 | 리포트·추이 응답에 점수·등급·백분위 필드가 없다 | `[req]` FR5.5, TC-13 |
| 사용자 | Must 경로는 시드 고정 사용자 하나. 인증 헤더 없이 서버가 고정 사용자로 처리한다(Should U11 이 들어오면 세션 쿠키로 바뀐다 — C11-S 참고) | `[req]` FR11.1 |

**Mock 분석 시간 기준 (NFR3 보완)** — Mock 모드에서 분석 접수 응답(`202`)은 **1초 이내**, 접수부터 대화 상태가
완료로 바뀔 때까지는 **PM-02(기본 3초) 이내**다. 분석 API 통합 테스트가 두 경과 시간을 모두 단언한다 `[Q8]` (D-103).
이 해석은 `requirements.md` 의 NFR3 문장을 보완하며, 두 문서가 어긋나 보이면 이 문단이 기준이다. 접수 응답 1초는
이 단계에서 새로 생긴 목표다.

---

## 계약 목록

| # | Provider Unit | Consumer | Mechanism | Owner |
|---|---|---|---|---|
| C1 | U1 백엔드 기반 | U2 화면 기반 | REST — 헬스체크·고정 사용자·첫 방문 동의 | U1 |
| C2 | U3 F01 녹음·전사 | U3 화면, U4, U8, U9 화면 | REST — 대화 가져오기·처리 상태·전사·발화 정정·대화 목록 | U3 |
| C3 | U4 F02 맥락 | U4 화면, U5 화면(맥락 수정 이동) | REST — 맥락 네 항목 저장·조회 | U4 |
| C4 | U5 F03 수행 평가 | U5 화면, U6 화면(이 목표 연습) | REST — 분석 요청·리포트·분석 수정 요청 | U5 |
| C5 | U6 F04 목표·추천 | U6 화면, U7 화면 | REST — 목표 추천·선택 | U6 |
| C6 | U7 F05 모의 대화 | U7 화면, U8 화면 | REST — 연습 목록·세션·시도·힌트·결과 | U7 |
| C7 | U8 F06 기록 | U8 화면, U2 홈(최근 기록) | REST — 기록 목록·목표별 추이·다음 코칭 추천 | U8 |
| C8 | U9 F07 정정·삭제 | U9 화면(A3 레이아웃, C5) | REST — 재분석·재검토 요약·삭제 미리보기·삭제·원음 삭제 | U9 |
| C9 | U3·U4 | U5 | 프로세스 안 인터페이스 — 분석 입력(발화·맥락) 조회, 분석 중 상태 전환 | U3 (발화), U4 (맥락) |
| C10 | U5 | U6, U7, U8, U9 | 프로세스 안 인터페이스 — 판정 조회·판정 저장(연습 시도 포함)·판정 대체 | U5 |
| C11 | U6·U7 | U8, U14 | 프로세스 안 인터페이스 — 목표·연습 기록·추천 조회 | U6 (목표·추천), U7 (연습) |
| C12 | U3 → U5, U5 → U6 | U5, U6 (구독자) | 프로세스 안 사건 — "발화 정정됨", "판정 재검토 필요" | 발행 단위 (U3, U5), 구독 처리는 U9 |
| C13 | U3·U5·U6·U7 | U9 | 프로세스 안 인터페이스 — 삭제 정리 인터페이스 | 각 제공 단위, 호출 순서는 U9 |
| C14 | U1 | U3, U5, U7 | 포트 — `SttProvider`, `LlmProvider` | U1 |
| C15 | U1 | 모든 백엔드 단위 | 공유 스키마 — PostgreSQL 초기 스키마(엔티티 20개) | U1 (이후 컬럼 변경은 해당 단위) |
| C16 | U1 | 모든 단위(개발·테스트) | 공유 스키마 — 시드 상태 목록 | U1 |
| C17 | U2 | U3~U14 화면 | 프론트엔드 공통 — 라우트 트리·API 클라이언트·화면 상태 | U2 (각 구역 라우트는 해당 단위) |
| C18-S | U10·U11·U12·U14 | 해당 Should 화면 | REST — 상세 조회·계정·보호자·추천 고도화 (Should) | 각 Should 단위 |

---

## C1. 헬스체크·고정 사용자·동의 (U1)

```yaml
openapi: 3.1.0
info: { title: C1 foundation, version: "1" }
paths:
  /api/v1/health:
    get:
      summary: 기동 확인과 분석 모드 노출 (시연 리허설이 mock 을 단언한다 — AC9.3.4)
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [status, analysisMode]
                properties:
                  status: { type: string, enum: [ok] }
                  analysisMode: { type: string, enum: [mock, live] }
  /api/v1/me:
    get:
      summary: 현재 사용자(Must 는 시드 고정 사용자)
      responses:
        "200":
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Me" }
  /api/v1/me/consent:
    post:
      summary: 첫 방문 서비스 안내 동의 (FR9.2)
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [agreed]
              properties:
                agreed: { type: boolean, const: true }
      responses:
        "200":
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Me" }
components:
  schemas:
    Me:
      type: object
      required: [id, displayName, role, consentedAt]
      properties:
        id: { type: string, format: uuid }
        displayName: { type: string }
        role: { type: string, enum: [USER, GUARDIAN] }
        consentedAt: { type: [string, "null"], format: date-time }
```

## C2. 대화 가져오기·전사·정정 (U3)

```yaml
openapi: 3.1.0
info: { title: C2 conversation, version: "1" }
paths:
  /api/v1/conversations:
    post:
      summary: 음성 업로드(파일 또는 브라우저 녹음). 녹음 알림 확인 필수 (FR1.1~FR1.2)
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              required: [file, source, recordingNoticeConfirmed]
              properties:
                file: { type: string, format: binary, description: "webm/opus 등 허용 형식, MAX_UPLOAD_BYTES 이하, 빈 파일 거부" }
                source: { type: string, enum: [UPLOAD, RECORDING] }
                recordingNoticeConfirmed: { type: boolean, const: true }
      responses:
        "202":
          description: 접수됨. 전사는 백그라운드에서 진행 (D-96)
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ConversationStatus" }
        "413": { description: PAYLOAD_TOO_LARGE }
        "422": { description: VALIDATION_ERROR — 형식·빈 파일·알림 미확인 }
    get:
      summary: 실제 대화 목록 (대화 돌아보기 탭)
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items: { $ref: "#/components/schemas/ConversationStatus" }
  /api/v1/conversations/{conversationId}/status:
    get:
      summary: 처리 상태 조회 (화면이 1초 간격으로 부른다)
      responses:
        "200":
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ConversationStatus" }
  /api/v1/conversations/{conversationId}/transcription/retry:
    post:
      summary: FAILED 에서 전사 다시 시도 (FR1.3)
      responses:
        "202": { content: { application/json: { schema: { $ref: "#/components/schemas/ConversationStatus" } } } }
        "409": { description: CONFLICT — FAILED 가 아닌 상태 }
  /api/v1/conversations/{conversationId}/transcript:
    get:
      summary: 전사 확인 (A3). 맥락 요약은 C3 를 따로 부른다
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [conversationId, transcriptVersion, utterances]
                properties:
                  conversationId: { type: string, format: uuid }
                  transcriptVersion: { type: integer, minimum: 1 }
                  utterances:
                    type: array
                    items: { $ref: "#/components/schemas/Utterance" }
  /api/v1/conversations/{conversationId}/utterances/{utteranceId}:
    patch:
      summary: 발화 정정 — 텍스트·화자·분석에서 빼기/되돌리기 (FR3.1~FR3.3). 정정 이력 저장, 전사 버전 +1, "발화 정정됨" 사건 발행(C12)
      requestBody:
        content:
          application/json:
            schema:
              type: object
              minProperties: 1
              properties:
                text: { type: string, minLength: 1 }
                speaker: { type: string, enum: [USER, PARTNER, UNKNOWN] }
                excluded: { type: boolean }
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [utterance, transcriptVersion, affectedJudgmentCount]
                properties:
                  utterance: { $ref: "#/components/schemas/Utterance" }
                  transcriptVersion: { type: integer }
                  affectedJudgmentCount: { type: integer, minimum: 0, description: "같은 트랜잭션에서 재검토 필요로 표시된 판정 수 (ADR-009, FR3.4)" }
        "409": { description: CONFLICT — 분석 중인 대화 }
components:
  schemas:
    ConversationStatus:
      type: object
      required: [id, status, analysisStatus, source, createdAt]
      properties:
        id: { type: string, format: uuid }
        status: { type: string, enum: [UPLOADING, TRANSCRIBING, READY, FAILED] }
        analysisStatus: { type: string, enum: [NOT_STARTED, ANALYZING, ANALYZED, FAILED] }
        source: { type: string, enum: [UPLOAD, RECORDING] }
        conversationKey: { type: [string, "null"], description: "Mock 픽스처 키, 예: conv_repair_01" }
        failureMessage: { type: [string, "null"] }
        audioDeleted: { type: boolean }
        createdAt: { type: string, format: date-time }
    Utterance:
      type: object
      required: [id, seq, speaker, startMs, endMs, text, unclear, excluded, edited]
      properties:
        id: { type: string, format: uuid }
        seq: { type: integer }
        speaker: { type: string, enum: [USER, PARTNER, UNKNOWN] }
        startMs: { type: integer }
        endMs: { type: integer }
        text: { type: string }
        unclear: { type: boolean }
        excluded: { type: boolean }
        edited: { type: boolean }
```

**`status` / `analysisStatus` 두 필드** — 도메인 설계(`components.md`)는 대화의 `status` 속성 하나에 "분석 중" 상태를 더하는
것으로 적었다. 이 계약은 API 응답을 전사 처리 상태(`status`)와 분석 상태(`analysisStatus`) 두 필드로 나눠 노출한다 — 화면이
전사 실패와 분석 실패를 따로 다시 시도해야 하기 때문이다. **이것은 API 모양의 결정이며, 내부 컬럼을 하나로 둘지 둘로 둘지는
functional-design(3.1)이 정한다.** 어느 쪽이든 API 응답은 이 두 필드를 유지한다 (검토 R-03 반영).

## C3. 맥락 (U4)

```yaml
openapi: 3.1.0
info: { title: C3 context, version: "1" }
paths:
  /api/v1/conversations/{conversationId}/context:
    get:
      responses:
        "200": { content: { application/json: { schema: { $ref: "#/components/schemas/ContextInfo" } } } }
    put:
      summary: 맥락 네 항목 저장. 모두 UNKNOWN 이어도 거부하지 않는다 (FR2.1, AC2.3.3)
      requestBody:
        content:
          application/json:
            schema: { $ref: "#/components/schemas/ContextInfo" }
      responses:
        "200": { content: { application/json: { schema: { $ref: "#/components/schemas/ContextInfo" } } } }
components:
  schemas:
    ContextField:
      type: object
      required: [value, status]
      properties:
        value: { type: [string, "null"] }
        status: { type: string, enum: [CONFIRMED, USER_REPORTED, UNKNOWN], description: "UNKNOWN 이면 value 는 null" }
    ContextInfo:
      type: object
      required: [relation, place, purpose, userGoal]
      properties:
        relation: { $ref: "#/components/schemas/ContextField" }
        place: { $ref: "#/components/schemas/ContextField" }
        purpose: { $ref: "#/components/schemas/ContextField" }
        userGoal: { $ref: "#/components/schemas/ContextField" }
```

`CONFIRMED` / `USER_REPORTED` 를 가르는 조건은 functional-design(3.1)이 정한다 — 값 이름만 여기서 고정한다.

## C4. 분석·리포트·분석 수정 요청 (U5)

```yaml
openapi: 3.1.0
info: { title: C4 assessment, version: "1" }
paths:
  /api/v1/conversations/{conversationId}/analysis:
    post:
      summary: 첫 분석 요청("이대로 분석하기"). 접수 1초 이내, 완료 3초 이내 (Mock, D-103)
      responses:
        "202": { content: { application/json: { schema: { $ref: "C2#/components/schemas/ConversationStatus" } } } }
        "409": { description: CONFLICT — 전사 미완료 또는 이미 ANALYZING }
  /api/v1/conversations/{conversationId}/report:
    get:
      summary: 리포트 (A4). 대체된 판정은 제외하고 최신 판정만 (ADR-007 — 조회 조건은 U9 가 더한다)
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [conversationId, situation, analyzableScope, wellDoneScenes, difficultScenes, heldParts, needsReview]
                properties:
                  conversationId: { type: string, format: uuid }
                  situation: { type: object, description: "관계·장소·목적 요약 (FR5.1)" }
                  analyzableScope: { type: string }
                  wellDoneScenes: { type: array, items: { $ref: "#/components/schemas/Scene" } }
                  difficultScenes: { type: array, items: { $ref: "#/components/schemas/Scene" } }
                  heldParts: { type: array, items: { $ref: "#/components/schemas/Scene" } }
                  needsReview: { type: boolean }
        "409": { description: CONFLICT — 아직 ANALYZED 가 아님 }
  /api/v1/conversations/{conversationId}/analysis-feedback:
    post:
      summary: '"분석이 이상해요" (FR5.6). 판정은 바뀌지 않는다'
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [socialEventId, reasonType]
              properties:
                socialEventId: { type: string, format: uuid }
                judgmentId: { type: [string, "null"], format: uuid }
                reasonType: { type: string, enum: [TRANSCRIPT_WRONG, CONTEXT_WRONG, JUDGMENT_ODD] }
                description: { type: string, maxLength: 500 }
      responses:
        "201":
          content:
            application/json:
              schema:
                type: object
                required: [id, redirectTo]
                properties:
                  id: { type: string, format: uuid }
                  redirectTo: { type: [string, "null"], enum: [TRANSCRIPT, CONTEXT, null] }
components:
  schemas:
    Judgment:
      type: object
      required: [id, group, opportunity, result, holdReason, rationale, evidence, needsReview]
      properties:
        id: { type: string, format: uuid }
        group: { type: string, enum: [RESPONSE_RELEVANCE, CLARIFICATION_REPAIR, TOPIC_MAINTENANCE] }
        opportunity: { type: string, enum: [PRESENT, ABSENT, UNCERTAIN] }
        result: { type: [string, "null"], enum: [OBSERVED, PARTIAL, NOT_OBSERVED_THIS_TIME, null] }
        holdReason: { type: [string, "null"], enum: [NO_OPPORTUNITY, INSUFFICIENT_CONTEXT, UNCLEAR_TRANSCRIPT, UNSUPPORTED_MODALITY, INVALID_EVIDENCE, null] }
        rationale: { type: string }
        alternatives: { type: array, items: { type: string } }
        evidence:
          type: array
          items:
            type: object
            required: [utteranceIds, role]
            properties:
              utteranceIds: { type: array, items: { type: string, format: uuid } }
              role: { type: string, enum: [OPPORTUNITY, RESPONSE, REPAIR] }
              excludedAfterAnalysis: { type: boolean, description: "근거 발화가 분석 뒤 빠졌으면 true (AC4.3.4)" }
        needsReview: { type: boolean }
    Scene:
      type: object
      required: [socialEventId, summary, utteranceRange, judgments]
      properties:
        socialEventId: { type: string, format: uuid }
        summary: { type: string }
        utteranceRange: { type: array, items: { type: integer }, minItems: 2, maxItems: 2 }
        judgments: { type: array, items: { $ref: "#/components/schemas/Judgment" } }
```

- `result` 와 `holdReason` 은 동시에 값을 가지지 않는다(FR4.2). 한 판정의 PARTIAL 은 잘한 장면과 어려움 장면 두 곳에 같은
  `socialEventId` 로 나타날 수 있다(D-76).
- 응답에는 점수·등급·백분위가 없다. 버전 값 객체(기준·프롬프트·모델·전사 버전)는 저장만 하고 Must 리포트 응답에는
  싣지 않는다 — 화면 표시는 C4 상세(Should, FR8.6)에서 한다.
- 리포트 화면 안에서의 이동(근거 보기, 맥락 수정, 이 목표 연습)은 API 가 아니라 C17 의 라우트 매개변수다.

## C5. 목표 추천·선택 (U6)

```yaml
openapi: 3.1.0
info: { title: C5 goal, version: "1" }
paths:
  /api/v1/conversations/{conversationId}/goal-recommendations:
    get:
      summary: 목표 추천 1~3개 또는 충분성 부족 (FR6.1, FR6.4)
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [recommendationId, sufficiency, goals]
                properties:
                  recommendationId: { type: string, format: uuid }
                  sufficiency: { type: string, enum: [SUFFICIENT, INSUFFICIENT] }
                  goals:
                    type: array
                    maxItems: 3
                    items:
                      type: object
                      required: [group, title, reason, sourceEventId, sourceJudgmentId]
                      properties:
                        group: { type: string, enum: [RESPONSE_RELEVANCE, CLARIFICATION_REPAIR, TOPIC_MAINTENANCE] }
                        title: { type: string }
                        reason: { type: string }
                        sourceEventId: { type: string, format: uuid }
                        sourceJudgmentId: { type: string, format: uuid }
  /api/v1/goals:
    post:
      summary: 추천 받아들이기·바꾸기 (FR6.2~FR6.3). 일반 연습 선택은 C6 에서 목표 없이 시작
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [recommendationId, userChoice]
              properties:
                recommendationId: { type: string, format: uuid }
                userChoice: { type: string, enum: [ACCEPTED, CHANGED, DECLINED] }
                group: { type: string, enum: [RESPONSE_RELEVANCE, CLARIFICATION_REPAIR, TOPIC_MAINTENANCE] }
                sourceEventId: { type: [string, "null"], format: uuid }
                sourceJudgmentId: { type: [string, "null"], format: uuid }
      responses:
        "201":
          content:
            application/json:
              schema:
                type: object
                required: [goal]
                properties:
                  goal: { $ref: "#/components/schemas/Goal" }
        "200": { description: "DECLINED — goal 없이 선택만 저장" }
    get:
      summary: 진행 중인 목표 (홈 카드)
      responses:
        "200": { content: { application/json: { schema: { type: object, properties: { items: { type: array, items: { $ref: "#/components/schemas/Goal" } } } } } } }
components:
  schemas:
    Goal:
      type: object
      required: [id, group, title, status, sourceEventId, sourceJudgmentId]
      properties:
        id: { type: string, format: uuid }
        group: { type: string, enum: [RESPONSE_RELEVANCE, CLARIFICATION_REPAIR, TOPIC_MAINTENANCE] }
        title: { type: string }
        status: { type: string, enum: [ACTIVE, STOPPED] }
        sourceEventId: { type: [string, "null"], format: uuid, description: "원본 삭제 후 유지하면 null" }
        sourceJudgmentId: { type: [string, "null"], format: uuid }
```

## C6. 모의 대화 연습 (U7)

```yaml
openapi: 3.1.0
info: { title: C6 practice, version: "1" }
paths:
  /api/v1/practice/scenarios:
    get:
      summary: 연습 목록 — 목표 연결 장면 카드, 같은 목표의 다른 상황, 검토된 일반 연습 (FR7.1)
      parameters:
        - { name: goalId, in: query, required: false, schema: { type: string, format: uuid } }
        - { name: group, in: query, required: false, schema: { type: string, enum: [RESPONSE_RELEVANCE, CLARIFICATION_REPAIR, TOPIC_MAINTENANCE] } }
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [linkedScene, scenarios]
                properties:
                  linkedScene: { type: [object, "null"], description: "목표의 원본 장면 요약" }
                  scenarios:
                    type: array
                    items:
                      type: object
                      required: [templateId, variantId, title, situation, partnerRole, isGeneralPractice]
                      properties:
                        templateId: { type: string, format: uuid }
                        variantId: { type: [string, "null"], format: uuid }
                        title: { type: string }
                        situation: { type: string }
                        partnerRole: { type: string }
                        isGeneralPractice: { type: boolean }
  /api/v1/practice/sessions:
    post:
      summary: 세션 시작. goalId 없으면 일반 연습(행동 묶음만)
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [templateId, group]
              properties:
                goalId: { type: [string, "null"], format: uuid }
                templateId: { type: string, format: uuid }
                variantId: { type: [string, "null"], format: uuid }
                group: { type: string, enum: [RESPONSE_RELEVANCE, CLARIFICATION_REPAIR, TOPIC_MAINTENANCE] }
      responses:
        "201": { content: { application/json: { schema: { $ref: "#/components/schemas/Session" } } } }
  /api/v1/practice/sessions/{sessionId}:
    get:
      responses:
        "200": { content: { application/json: { schema: { $ref: "#/components/schemas/Session" } } } }
  /api/v1/practice/sessions/{sessionId}/attempts:
    post:
      summary: 시도 제출. 빈 입력·"그만" → 일시정지, "몰라"·"도와줘" → 힌트 제안(판정 없음) (FR7.4, FR7.7). 판정은 동기(Mock 규칙)
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [responseText]
              properties:
                responseText: { type: string }
      responses:
        "201":
          content:
            application/json:
              schema:
                type: object
                required: [outcome]
                properties:
                  outcome: { type: string, enum: [JUDGED, PAUSED, HINT_SUGGESTED] }
                  attempt: { $ref: "#/components/schemas/Attempt" }
                  partnerReply: { type: [string, "null"] }
  /api/v1/practice/sessions/{sessionId}/hints:
    post:
      summary: 다음 단계 힌트 (ATTENTION_CUE → INFO_HINT → EXAMPLE). 이후 시도는 HINTED (FR7.5)
      responses:
        "201":
          content:
            application/json:
              schema:
                type: object
                required: [level, content, attemptOrder]
                properties:
                  level: { type: string, enum: [ATTENTION_CUE, INFO_HINT, EXAMPLE] }
                  content: { type: string }
                  attemptOrder: { type: integer }
        "409": { description: CONFLICT — 이미 마지막 단계 }
  /api/v1/practice/sessions/{sessionId}/resume:
    post:
      responses:
        "200": { content: { application/json: { schema: { $ref: "#/components/schemas/Session" } } } }
components:
  schemas:
    Attempt:
      type: object
      required: [id, order, performanceMode, responseText, judgment, createdAt]
      properties:
        id: { type: string, format: uuid }
        order: { type: integer, minimum: 1 }
        performanceMode: { type: string, enum: [INDEPENDENT, HINTED] }
        responseText: { type: string }
        judgment: { $ref: "C4#/components/schemas/Judgment" }
        createdAt: { type: string, format: date-time }
    Session:
      type: object
      required: [id, goalId, group, status, attempts, hints]
      properties:
        id: { type: string, format: uuid }
        goalId: { type: [string, "null"], format: uuid }
        group: { type: string, enum: [RESPONSE_RELEVANCE, CLARIFICATION_REPAIR, TOPIC_MAINTENANCE] }
        status: { type: string, enum: [IN_PROGRESS, PAUSED, COMPLETED] }
        attempts: { type: array, items: { $ref: "#/components/schemas/Attempt" } }
        hints: { type: array, items: { type: object } }
```

시도 판정은 Mock 규칙으로 짧게 끝나므로 202 가 아니라 동기로 둔다 — D-96 은 업로드·전사·대화 분석·재분석에 적용한다.
시도는 생성 후 수정 API 가 없다(FR7.6).

## C7. 기록·추이·다음 코칭 추천 (U8)

```yaml
openapi: 3.1.0
info: { title: C7 record, version: "1" }
paths:
  /api/v1/records:
    get:
      parameters:
        - { name: type, in: query, schema: { type: string, enum: [ALL, REAL, ROLEPLAY], default: ALL } }
        - { name: limit, in: query, schema: { type: integer, minimum: 1, maximum: 50 } }
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items:
                      type: object
                      required: [id, type, date, summary]
                      properties:
                        id: { type: string, format: uuid }
                        type: { type: string, enum: [REAL, ROLEPLAY] }
                        date: { type: string, format: date-time }
                        goalTitle: { type: [string, "null"] }
                        summary: { type: string }
  /api/v1/records/trends:
    get:
      summary: 목표별 추이 — mode 와 performanceMode 를 섞지 않는다 (FR8.2~FR8.4)
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items:
                      type: object
                      required: [goalId, group, mode, performanceMode, status]
                      properties:
                        goalId: { type: string, format: uuid }
                        group: { type: string, enum: [RESPONSE_RELEVANCE, CLARIFICATION_REPAIR, TOPIC_MAINTENANCE] }
                        mode: { type: string, enum: [REAL, ROLEPLAY] }
                        performanceMode: { type: string, enum: [INDEPENDENT, HINTED] }
                        status: { type: string, enum: [AVAILABLE, INSUFFICIENT_FOR_COMPARISON] }
                        observedCount: { type: [integer, "null"], description: "status=AVAILABLE 일 때만" }
                        notObservedCount: { type: [integer, "null"] }
  /api/v1/records/next-coaching:
    get:
      summary: 다음 코칭 추천 — Must 는 최근 어려움 장면 하나, 없으면 추천 없음 (D-78)
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [recommendation]
                properties:
                  recommendation:
                    type: [object, "null"]
                    required: [goalGroup, reason, sourceRecordId]
                    properties:
                      goalGroup: { type: string }
                      reason: { type: string }
                      sourceRecordId: { type: string, format: uuid }
                      recalculationPending: { type: boolean }
```

응답 라벨에 "유효 기회", "분모" 같은 내부 용어를 쓰지 않는다. 화면 문구는 프론트엔드가 `status` 로 고른다.

## C8. 재분석·재검토 요약·삭제 (U9)

```yaml
openapi: 3.1.0
info: { title: C8 correction-deletion, version: "1" }
paths:
  /api/v1/conversations/{conversationId}/review-summary:
    get:
      summary: A3 부모 레이아웃의 재검토 안내 (FR3.4, D-104)
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [needsReview, affectedJudgmentCount]
                properties:
                  needsReview: { type: boolean }
                  affectedJudgmentCount: { type: integer, minimum: 0 }
  /api/v1/conversations/{conversationId}/reanalysis:
    post:
      summary: 정정 후 다시 분석 (FR3.5). 새 판정이 이전 판정을 supersedes 로 가리킨다 (ADR-007)
      responses:
        "202": { content: { application/json: { schema: { $ref: "C2#/components/schemas/ConversationStatus" } } } }
        "409": { description: CONFLICT — 이미 ANALYZING (AC3.3.4) }
  /api/v1/conversations/{conversationId}/deletion-preview:
    get:
      summary: 삭제 전 연결 항목 미리보기. 아무것도 지우지 않는다 (FR10.1)
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [transcriptCount, judgmentCount, practiceSessionCount, goals, recommendationCount]
                properties:
                  transcriptCount: { type: integer }
                  judgmentCount: { type: integer }
                  practiceSessionCount: { type: integer }
                  recommendationCount: { type: integer }
                  goals: { type: array, items: { type: object, required: [id, title], properties: { id: { type: string, format: uuid }, title: { type: string } } } }
  /api/v1/deletion-requests:
    post:
      summary: 대화 삭제 확정 (FR10.2~FR10.4, ADR-006)
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [targetType, targetId, goalDisposition]
              properties:
                targetType: { type: string, enum: [CONVERSATION] }
                targetId: { type: string, format: uuid }
                goalDisposition: { type: string, enum: [DELETE, KEEP] }
      responses:
        "201": { content: { application/json: { schema: { $ref: "#/components/schemas/DeletionRequest" } } } }
  /api/v1/deletion-requests/{deletionRequestId}:
    get:
      responses:
        "200": { content: { application/json: { schema: { $ref: "#/components/schemas/DeletionRequest" } } } }
  /api/v1/deletion-requests/{deletionRequestId}/retry:
    post:
      summary: PARTIAL 일 때 남은 파일만 다시 지운다 (D-84)
      responses:
        "200": { content: { application/json: { schema: { $ref: "#/components/schemas/DeletionRequest" } } } }
  /api/v1/conversations/{conversationId}/audio:
    delete:
      summary: 원음만 삭제 — 전사·판정은 남고 음성 메타데이터에 삭제 시각 (FR10.5)
      responses:
        "204": { description: 삭제됨 }
components:
  schemas:
    DeletionRequest:
      type: object
      required: [id, status, affectedItems, pendingFileCount]
      properties:
        id: { type: string, format: uuid }
        status: { type: string, enum: [REQUESTED, COMPLETED, PARTIAL] }
        affectedItems: { type: object, description: "지운 항목 종류별 수" }
        pendingFileCount: { type: integer, minimum: 0, description: "파일 경로 자체는 응답에 싣지 않는다" }
```

삭제는 커밋 전까지 한 트랜잭션이라 요청 응답 시점에 DB 행은 이미 지워져 있다. 커밋 후 파일 삭제는 같은 요청 안에서
실행하고, 실패한 경로가 있으면 `PARTIAL` 로 돌아온다 — 삭제는 202 가 아니라 동기다.

## C9. 분석 입력 조회 (U3·U4 → U5, 프로세스 안)

```python
# app/service/conversation/ports_for_assessment.py — 제공: U3(발화, 상태), U4(맥락)
class AnalysisInputReader(Protocol):
    def get_analysis_input(self, conversation_id: UUID) -> AnalysisInput: ...
        # 분석에서 뺀 발화(excluded=True)는 포함하지 않는다. 전사 미완료면 ConflictError.
    def mark_analyzing(self, conversation_id: UUID) -> None: ...     # 이미 ANALYZING 이면 ConflictError
    def mark_analyzed(self, conversation_id: UUID) -> None: ...
    def mark_analysis_failed(self, conversation_id: UUID, message: str) -> None: ...

@dataclass(frozen=True)
class AnalysisInput:
    conversation_id: UUID
    conversation_key: str | None
    transcript_version: int
    utterances: tuple[UtteranceView, ...]   # id, seq, speaker, text, unclear
    context: ContextView                     # 네 항목의 value, status
```

## C10. 판정 조회·저장·대체 (U5 → U6·U7·U8·U9, 프로세스 안)

```python
# app/service/assessment/api.py — 제공: U5. 판정 저장 규칙(근거 검증, 보류, 배타성, 버전)은 이 입구만 지난다.
class JudgmentService(Protocol):
    def save_conversation_judgments(self, conversation_id: UUID, candidates: Sequence[JudgmentCandidate],
                                    provenance: Provenance) -> Sequence[JudgmentView]: ...
    def save_attempt_judgment(self, session_id: UUID, attempt_order: int, candidate: JudgmentCandidate,
                              provenance: Provenance) -> JudgmentView: ...          # ADR-004, 사용: U7
    def supersede(self, conversation_id: UUID, candidates: Sequence[JudgmentCandidate],
                  provenance: Provenance) -> Sequence[JudgmentView]: ...             # ADR-007, 사용: U9
    def list_current_judgments(self, conversation_id: UUID) -> Sequence[JudgmentView]: ...   # 대체된 판정 제외
    def list_judgments_for_trends(self, user_id: UUID) -> Sequence[JudgmentView]: ...        # 사용: U8
    def count_needs_review(self, conversation_id: UUID) -> int: ...                          # 사용: U9

@dataclass(frozen=True)
class Provenance:          # ADR-003 값 객체. 네 값 모두 필수(NOT NULL)
    criteria_version: str
    prompt_version: str
    model_name: str
    transcript_version: int
```

`JudgmentCandidate` 는 LLM·Mock 이 낸 후보다. 없는 발화 ID·뺀 발화를 가리키면 저장 규칙이 `INVALID_EVIDENCE` 로 바꾸고
500 이 되지 않는다(D-86, TC-10).

## C11. 목표·연습·추천 조회 (U6·U7 → U8·U14, 프로세스 안)

```python
class GoalReader(Protocol):          # 제공: U6
    def list_goals(self, user_id: UUID) -> Sequence[GoalView]: ...
    def get_latest_next_coaching(self, user_id: UUID) -> NextCoachingView | None: ...   # U8 이 Must 규칙을 쓰고, U14 가 확장
class PracticeReader(Protocol):      # 제공: U7
    def list_sessions(self, user_id: UUID) -> Sequence[SessionView]: ...                # 시도·힌트·판정 ID 포함
```

## C12. 프로세스 안 사건 (ADR-009)

```yaml
asyncapi: 3.0.0
info: { title: C12 in-process events, version: "1" }
defaultContentType: application/python-dataclass
channels:
  utteranceCorrected:
    description: 발화 텍스트·화자 수정, 분석에서 빼기·되돌리기 직후. 같은 요청 트랜잭션에서 동기 전달
    messages:
      UtteranceCorrected:
        payload:
          type: object
          required: [conversationId, utteranceIds, transcriptVersion]
          properties:
            conversationId: { type: string, format: uuid }
            utteranceIds: { type: array, items: { type: string, format: uuid } }
            transcriptVersion: { type: integer }
  judgmentReviewRequired:
    description: 판정에 재검토 필요를 표시한 직후. 같은 트랜잭션에서 동기 전달
    messages:
      JudgmentReviewRequired:
        payload:
          type: object
          required: [conversationId, judgmentIds]
          properties:
            conversationId: { type: string, format: uuid }
            judgmentIds: { type: array, items: { type: string, format: uuid } }
operations:
  publishUtteranceCorrected: { action: send, channel: { $ref: "#/channels/utteranceCorrected" } }       # 발행: U3
  onUtteranceCorrected: { action: receive, channel: { $ref: "#/channels/utteranceCorrected" } }        # 구독: Assessment (U9 구현)
  publishJudgmentReviewRequired: { action: send, channel: { $ref: "#/channels/judgmentReviewRequired" } } # 발행: Assessment (U9 구현)
  onJudgmentReviewRequired: { action: receive, channel: { $ref: "#/channels/judgmentReviewRequired" } }   # 구독: Training (U9 구현)
```

- 사건에는 식별자만 싣고 전사 본문을 싣지 않는다(ADR-009 보안 영향).
- 구독 처리에서 예외가 나면 같은 트랜잭션이 롤백되어 정정도 저장되지 않는다. 사용자는 정정 실패 오류를 받는다.
- 발행 코드(U3)는 U9 보다 먼저 만들어질 수 있다. 구독자가 없으면 발행은 아무 일도 하지 않는다 — 계약 기준 병렬 시작(D-92)을 지킨다.

## C13. 삭제 정리 인터페이스 (U3·U5·U6·U7 → U9, 프로세스 안)

```python
class ConversationCleanup(Protocol):     # 제공: U3
    def collect_file_paths(self, conversation_id: UUID) -> Sequence[str]: ...
    def delete_rows(self, conversation_id: UUID) -> Mapping[str, int]: ...     # 대화·음성 메타·발화·정정·맥락. 커밋하지 않는다
    def delete_file(self, path: str) -> None: ...                              # 커밋 후 호출. 실패 시 예외
    def delete_audio_only(self, conversation_id: UUID) -> None: ...            # 파일 삭제 + deletedAt 기록
class AssessmentCleanup(Protocol):       # 제공: U5
    def delete_for_conversation(self, conversation_id: UUID) -> Mapping[str, int]: ...   # 사건·판정·근거·분석 수정 요청
class TrainingCleanup(Protocol):         # 제공: U6(목표·추천), U7(연습)
    def preview_for_conversation(self, conversation_id: UUID) -> TrainingDeletionPreview: ...
    def delete_for_conversation(self, conversation_id: UUID, goal_disposition: Literal["DELETE", "KEEP"]) -> Mapping[str, int]: ...
        # KEEP 이면 목표의 sourceEventId·sourceJudgmentId 를 비운다(연쇄 삭제가 아니다)
```

호출 순서와 트랜잭션은 U9 의 삭제 유스케이스가 소유한다: 파일 경로를 삭제 요청에 먼저 기록 → Training → Assessment →
Conversation 행 삭제 → 커밋 → 파일 삭제 → 실패 경로는 `pendingFilePaths` 에 남기고 `PARTIAL` (ADR-006, D-84).
정리 인터페이스는 `commit` 하지 않는다.

## C14. STT·LLM 포트 (U1 → U3·U5·U7)

```python
# app/service/ports.py — 팀 관행: 인터페이스는 providers/ 가 아니라 service/ports.py
class SttProvider(Protocol):
    model_name: str
    def transcribe(self, audio_path: str, *, file_name: str) -> TranscriptionResult: ...
        # Mock: file_name 의 conversationKey 로 합성 전사 선택, 없거나 녹음이면 S1 (FR1.5)

class LlmProvider(Protocol):
    model_name: str
    def assess_conversation(self, *, prompt_id: str, prompt_version: str, criteria_version: str,
                            transcript_block: TranscriptBlock, context: ContextView,
                            conversation_key: str | None,
                            transcript_version: int) -> Sequence[JudgmentCandidate]: ...
        # Mock: conversation_key 와 transcript_version 으로 기대 판정 픽스처를 고른다 — 정정 후 S3 포함 (components.md ProviderAdapters)
    def coach_turn(self, *, prompt_id: str, prompt_version: str, scenario: ScenarioView,
                   attempt_text_block: TranscriptBlock, attempt_order: int) -> CoachTurnResult: ...
        # 상대 발화와 시도 판정 후보를 함께 돌려준다

@dataclass(frozen=True)
class TranscriptBlock:     # 지시문과 데이터를 섞지 않는다(TC-08). 구분자 시퀀스는 만들 때 이스케이프한다
    utterances: tuple[UtteranceView, ...]
```

- **전사 버전 전달 경로** — U5 는 C9 의 `AnalysisInput.transcript_version` 을 그대로 `assess_conversation(transcript_version=...)` 에 넘기고,
  같은 값을 C10 의 `Provenance.transcript_version` 으로 저장한다. 재분석(C8)도 같은 경로를 쓴다. 이 값이 빠지면 Mock 이 정정 전·후
  S3 를 구분하지 못해 재분석 시연 경로가 재현되지 않는다 (검토 R-01 반영).
- 프롬프트 식별자·버전은 프롬프트 파일 이름에서 뽑는다(`assess_v1.md` → `assess`, `v1`) `[practices]` Code Style.
- 제공자 예외는 어댑터 경계에서 `ProviderError`(502) / `ProviderTimeoutError`(504)로 바꾼다. 연결·읽기 타임아웃을 따로 두고
  타임아웃·연결 실패에만 1회 재시도한다(NFR13). live 타임아웃 값은 nfr-requirements(3.2)가 정한다(OQ5).

## C15. 공유 DB 스키마 (U1)

```yaml
shared-schema: postgresql-initial
owner: u1-backend-foundation
decision: D-102   # OQ-U1 닫음
migration:
  initial_revision: "U1 이 엔티티 20개 테이블 전체를 초기 리비전 하나로 만든다"
  later_changes: "컬럼 추가·변경은 그 엔티티를 쓰는 단위가 새 리비전으로. 병합된 리비전은 수정하지 않는다"
  branch_conflict: "down_revision 이 갈라지면 새 파일을 만들지 말고 alembic merge"
  downgrade: "쓰지 않는다 (전진 방향만)"
tables:              # 엔티티 → 테이블, 컬럼 주인(나중 변경을 맡는 단위)
  users:                  { entity: User, component: account, column_owner: u1-backend-foundation }
  guardian_invitations:   { entity: GuardianInvitation, component: account, column_owner: u12-s-guardian-sharing }
  conversations:          { entity: Conversation, component: conversation, column_owner: u3-f01-capture,
                            notes: "전사 상태와 분석 상태를 컬럼 하나로 둘지 둘로 둘지는 functional-design(3.1). API 는 C2 의 두 필드를 유지" }
  audio_assets:           { entity: AudioAsset, component: conversation, column_owner: u3-f01-capture }
  utterances:             { entity: Utterance, component: conversation, column_owner: u3-f01-capture }
  corrections:            { entity: Correction, component: conversation, column_owner: u3-f01-capture }
  context_infos:          { entity: ContextInfo, component: conversation, column_owner: u4-f02-context }
  social_events:          { entity: SocialEvent, component: assessment, column_owner: u5-f03-assessment }
  behavior_judgments:     { entity: BehaviorJudgment, component: assessment, column_owner: u5-f03-assessment,
                            notes: "provenance 네 컬럼 NOT NULL, supersedes_judgment_id, needs_review" }
  evidences:              { entity: Evidence, component: assessment, column_owner: u5-f03-assessment }
  analysis_feedbacks:     { entity: AnalysisFeedback, component: assessment, column_owner: u5-f03-assessment }
  training_goals:         { entity: TrainingGoal, component: training, column_owner: u6-f04-goal,
                            notes: "source_event_id·source_judgment_id 는 ON DELETE SET NULL 이 아니라 앱이 비운다(ADR-006)" }
  recommendations:        { entity: Recommendation, component: training, column_owner: u6-f04-goal }
  scenario_templates:     { entity: ScenarioTemplate, component: training, column_owner: u7-f05-practice }
  scenario_variants:      { entity: ScenarioVariant, component: training, column_owner: u7-f05-practice }
  practice_sessions:      { entity: PracticeSession, component: training, column_owner: u7-f05-practice }
  attempts:               { entity: Attempt, component: training, column_owner: u7-f05-practice }
  hint_events:            { entity: HintEvent, component: training, column_owner: u7-f05-practice }
  deletion_requests:      { entity: DeletionRequest, component: privacy, column_owner: u9-f07-correction-deletion }
  sharing_settings:       { entity: SharingSetting, component: privacy, column_owner: u12-s-guardian-sharing,
                            notes: "level NONE/SUMMARY/FULL, 기본 NONE (FR11.2)" }
rules:
  - "음성 본문은 DB BLOB 에 넣지 않는다 (TC-05)"
  - "FK 의 ON DELETE CASCADE 는 그물로만 둔다. 삭제 순서는 C13 이 정한다"
  - "가변 구조(판정 alternatives, 변형 규칙)는 JSONB"
  - "데이터 타입·제약·허용값의 세부는 functional-design(3.1)이 정하고, 바뀌면 column_owner 단위가 리비전을 추가한다"
```

## C16. 시드 상태 (U1)

```yaml
shared-schema: seed-states
owner: u1-backend-foundation
decision: D-98   # OQ-U2 닫음
entrypoint: "scripts/seed.py --state <name>  (상태는 누적: 뒤 상태는 앞 상태를 포함한다)"
source_of_truth: "docs/input/05_synthetic-test-data.md 의 기대 판정 픽스처 (backend/app/fixtures/) — 시드는 픽스처를 읽고 값을 다시 적지 않는다"
states:
  base:                     { contains: "고정 사용자 1명(동의 전), 시나리오 원형 6개·검토된 변형", used_by: [U2, U7] }
  consented:                { contains: "base + 동의 완료", used_by: [U3, U4, U8] }
  s1-transcribed:           { contains: "consented + S1(conv_repair_01) 전사 READY, 맥락 입력", used_by: [U4, U5, U9] }
  s1-analyzed:              { contains: "s1-transcribed + S1 기대 판정 저장(ANALYZED)", used_by: [U5, U6, U9] }
  s1-goal-selected:         { contains: "s1-analyzed + 추천 수락, 목표 ACTIVE", used_by: [U7] }
  s1-practiced:             { contains: "s1-goal-selected + 연습 세션 1개(독립 시도 1, 힌트 후 시도 1)", used_by: [U8, U10] }
  records-sufficient:       { contains: "s1-practiced + 같은 목표 유효 기회 3회 이상이 되게 판정·시도 누적", used_by: [U8, U14] }
  s1-corrected-needs-review: { contains: "s1-analyzed + 근거 발화 1건 정정, 해당 판정 needs_review", used_by: [U9, U10] }
  s2-s3-analyzed:           { contains: "consented + S2(conv_topic_02)·S3(conv_unclear_03) 분석 완료", used_by: [U5, U8] }
rules:
  - "시드가 계약(C2~C8 응답 모양, C15 테이블)과 어긋나면 시드를 고친다 — 계약이 기준 (D-99)"
  - "단위가 컬럼을 추가하면 같은 PR 에서 U1 담당자에게 시드 갱신을 요청하고, U1 담당자가 리뷰어로 들어간다"
  - "실제 사용자 데이터는 넣지 않는다 — 전부 합성 (SC-02)"
```

## C17. 프론트엔드 라우트 트리와 공통 (U2)

```yaml
shared-schema: frontend-routes
owner: u2-web-foundation
decision: [D-101, D-104]
common:
  apiClient: "src/api/client.ts — 오류 봉투 → 타입 있는 오류. 생성 타입은 src/api/generated/ (openapi-typescript, 손으로 고치지 않음)"
  statusPolling: "src/hooks/useStatusPolling.ts — 1초 간격, READY/ANALYZED/FAILED 에서 멈춤 (D-96)"
  screenStates: "로딩 / 성공 / 실패(다시 시도) / 비어 있음 (NFR9)"
  comingSoon: "아직 없는 Should 화면 버튼 → 공통 안내 (D-73)"
routes:
  - { path: "/",                                   screen: A1 홈,          owner: u2-web-foundation }
  - { path: "/consent",                            screen: 첫 방문 동의,    owner: u2-web-foundation }
  - { path: "/conversations",                      screen: 대화 돌아보기 목록, owner: u3-f01-capture }
  - { path: "/conversations/new",                  screen: A2 업로드,      owner: u3-f01-capture }
  - { path: "/conversations/new/record",           screen: A2-R 직접 녹음, owner: u3-f01-capture }
  - { path: "/conversations/:id/context",          screen: 맥락 입력,      owner: u4-f02-context }
  - { path: "/conversations/:id/transcript",       screen: A3 레이아웃(재검토 안내), owner: u9-f07-correction-deletion,
      children: [ { path: "",                      screen: A3 전사 확인·정정, owner: u3-f01-capture } ] }
  - { path: "/conversations/:id/report",           screen: A4 리포트,      owner: u5-f03-assessment,
      params: "?focusUtterance=<id> 는 A3 로 이동해 강조할 때 사용" }
  - { path: "/conversations/:id/goals",            screen: A5 목표 선택,   owner: u6-f04-goal, params: "?group=&sourceEventId= (이 목표 연습)" }
  - { path: "/practice",                           screen: B1 연습 목록,   owner: u7-f05-practice, params: "?goalId=" }
  - { path: "/practice/sessions/:sessionId",       screen: B2~B5 준비·대화·힌트·결과, owner: u7-f05-practice }
  - { path: "/records",                            screen: C1 기록,        owner: u8-f06-record }
  - { path: "/conversations/:id/delete",           screen: C5 삭제(Must 부분), owner: u9-f07-correction-deletion }
  - { path: "/records/goals/:goalId",              screen: C2 목표 상세,   owner: u10-s-detail-views, grade: Should }
  - { path: "/records/practice/:sessionId",        screen: C3 연습 기록 상세, owner: u10-s-detail-views, grade: Should }
  - { path: "/records/conversations/:id",          screen: C4 실제 대화 상세, owner: u10-s-detail-views, grade: Should }
  - { path: "/login",                              screen: 로그인·가입,    owner: u11-s-account-auth, grade: Should }
  - { path: "/settings/sharing",                   screen: C5 보호자·보관 기간(Should 부분), owner: u12-s-guardian-sharing, grade: Should }
  - { path: "/guardian",                           screen: 보호자 읽기 화면, owner: u12-s-guardian-sharing, grade: Should }
rules:
  - "페이지 컴포넌트 이름은 화면 ID + 영어 역할 (예: A3TranscriptPage.tsx, A3ReviewLayout.tsx)"
  - "부모 레이아웃은 <Outlet /> 자리만 두고 자식의 내부를 알지 않는다"
  - "노트북 레이아웃(U13)은 라우트를 추가하지 않고 공통 스타일만 바꾼다"
```

## C18-S. Should 계약 (U10·U11·U12·U14)

Should 단위는 Must 가 선 뒤 만든다. 경로와 응답의 뼈대만 고정하고, 세부 필드는 해당 단위 착수 전에 이 문서에 추가한다
(추가는 자유 — D-100). 만드는 시점만 뒤로 간 것이며 확정된 Should 기능을 취소한 것이 아니다.

```yaml
openapi: 3.1.0
info: { title: C18-S should contracts, version: "1" }
paths:
  /api/v1/records/goals/{goalId}:            { get: { summary: "C2 목표 상세 (U10, FR12.1)" } }
  /api/v1/records/practice/{sessionId}:      { get: { summary: "C3 연습 기록 상세 (U10, FR12.2)" } }
  /api/v1/records/conversations/{id}:        { get: { summary: "C4 실제 대화 상세 — 정정 이력·버전 값 객체 포함 (U10, FR12.3, FR8.6)" } }
  /api/v1/auth/signup:                       { post: { summary: "사용자 스스로 가입 (U11, FR13.1). 보호자가 대신 만들지 않는다" } }
  /api/v1/auth/login:                        { post: { summary: "세션 쿠키 발급 (U11)" } }
  /api/v1/auth/logout:                       { post: { summary: "(U11)" } }
  /api/v1/guardian-invitations:              { post: { summary: "초대 코드 생성 (U12, FR14.2)" } }
  /api/v1/guardian-invitations/accept:       { post: { summary: "보호자가 코드 수락 (U12)" } }
  /api/v1/sharing-settings:                  { get: { summary: "(U12)" }, put: { summary: "NONE/SUMMARY/FULL, 사용자만 변경 (U12, FR14.1)" } }
  /api/v1/guardian/view:                     { get: { summary: "권한 범위 데이터 — 전사 원문·원음 없음 (U12, FR14.4)" } }
  /api/v1/me/audio-retention:                { put: { summary: "원음 보관 기간 (U12, FR14.5, PM-04)" } }
```

U14 는 새 경로를 만들지 않고 C7 의 `/api/v1/records/next-coaching` 응답 모양을 그대로 쓴다. U11 이 들어오면 모든 경로가
세션의 사용자로 동작하고, Must 시연 경로의 고정 사용자(로그인 없음, US9.2)는 설정으로 유지한다.

---

## 계약 소유 규칙

- **소유** — 각 계약의 Owner 단위가 스펙과 구현을 책임진다. 프로세스 안 인터페이스(C9~C13)는 제공 단위가 Protocol 을
  만들고, 소비 단위는 Protocol 에만 의존한다(구현 모듈을 직접 import 하지 않는다).
- **기준** — 이 문서가 기준이다. 구현·생성 스키마·시드가 어긋나면 그쪽을 고친다 `[Q4]` (D-99).
- **추가 변경** — 필드·경로·선택 매개변수 추가는 소유 단위가 자유롭게 한다. 같은 PR 에서 이 문서에도 추가한다.
  받는 쪽은 모르는 필드를 무시한다 `[Q5]` (D-100).
- **깨는 변경** — 필드 이름 변경·삭제, 필수 여부 강화, enum 값 삭제, 상태 코드 변경은 그 계약의 모든 소비 단위 담당자의
  PR 리뷰 승인이 있어야 병합한다. 이 문서를 같은 PR 에서 고친다 `[Q5]` (D-100).
- **스키마** — 초기 스키마는 U1, 이후 컬럼 변경은 `column_owner` 단위의 새 리비전 `[Q7]` (D-102).
- **시드** — 시드 상태는 U1 이 소유한다. 컬럼을 바꾸는 단위는 U1 담당자를 리뷰어로 넣는다 `[Q3]` (D-98).
- **화면** — 라우트 트리의 각 경로는 표의 owner 단위만 고친다. 부모 레이아웃과 자식은 서로의 내부를 모른다 `[Q6][Q9]` (D-101, D-104).
- **Change Control** — 이 문서는 승인 뒤에도 구현 중에 고쳐진다. 이 워크플로의 Change Control 은 relaxed 라, 고칠 때
  바뀐 사실이 기록·안내되고 이후 단계가 멈추지는 않는다.

---

## Open questions

| Contract | Question | Blocks |
|---|---|---|
| C14 | live STT·LLM 제공자와 타임아웃 값, live 응답시간 목표(D-37, OQ5) | 없음 — Mock 기본 경로는 막지 않는다. live 구현(U1)만 nfr-requirements(3.2) 뒤로 |
| C3 | 맥락 `CONFIRMED` / `USER_REPORTED` 를 가르는 조건 | U4 (functional-design 3.1 에서 닫음) |
| C4 | `analyzableScope` 문구와 보류 장면의 표시 단위(장면 전체인지 판정 하나인지) | U5 (functional-design 3.1) |
| C5 | 목표 `STOPPED` 로 바꾸는 경로(그만하기)는 Should C2(FR12.1) 뿐인지, Must 에도 필요한지 | U6·U10 (functional-design 3.1) |
| C16 | `records-sufficient` 시드의 정확한 판정·시도 수 — 비교 불충분 기준 PM-03(기본 3)의 경계 테스트와 맞춘다 | U8 (functional-design 3.1) |
| C17 | 분석 완료 뒤 A3 → A4 로 자동 이동할지, 버튼으로 이동할지 | U3·U5 화면 (functional-design 3.1) |

## Assumptions & Open Questions

- **리드가 정하고 요약 확인에서 승인된 것** — 계약 목록 구성, `/api/v1` 경로, 1초 간격 상태 조회와 FastAPI 요청 후 작업
  (별도 큐 없음), 서버 재시작 시 진행 중 상태를 실패로 바꿈, LLM 포트가 프롬프트 식별자·버전과 전사 블록을 따로 받음,
  A2·A4 라우트 소유, 계약 요약 위치 (D-105).
- **이 문서를 쓰며 리드가 정한 기술 세부 (승인 게이트에서 확인)** — 연습 시도 판정과 삭제는 202 가 아니라 동기(짧게 끝나는
  작업이고 삭제는 ADR-006 의 트랜잭션 순서를 한 요청에 담는다), 사건 구독 실패 시 정정까지 롤백, 시드 상태 9개의 이름과 누적
  구조, JSON camelCase, 열거값 이름(맥락 상태 `CONFIRMED`/`USER_REPORTED`/`UNKNOWN`, 분석 수정 이유
  `TRANSCRIPT_WRONG`/`CONTEXT_WRONG`/`JUDGMENT_ODD`, 근거 역할 `OPPORTUNITY`/`RESPONSE`/`REPAIR`). 판정 관련 열거값은
  `[spec:04]` 의 이름을 그대로 쓴다. 새 영어 이름은 팀 관행대로 `docs/glossary.md` 에 먼저 올린다.
- 위 Open questions 표의 항목은 모두 Must 흐름의 계약 모양을 바꾸지 않는 세부라 functional-design(3.1)으로 넘긴다.
