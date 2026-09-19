# Functional Design Questions — u1-backend-foundation

**Stage**: functional-design (3.1) · **Unit**: u1-backend-foundation (U1 백엔드 기반)
**작성일**: 2026-09-18

## Sources

| 태그 | 출처 |
|---|---|
| `[unit]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/unit-of-work.md` — U1 정의 |
| `[story]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/user-stories/stories.md` — US9.1, US9.2 |
| `[components]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/domain-design/components.md` — Account, ProviderAdapters |
| `[contract]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md` — 공통 규칙, C1, C14, C15, C16 |
| `[req]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/requirements.md` |
| `[practices]` | `aidlc/spaces/default/memory/team.md`, `project.md` |

## 다시 묻지 않는 것

앞 단계가 이미 닫은 항목입니다. 이 파일에서 다시 묻지 않습니다.

| 항목 | 닫은 결정 |
|---|---|
| 백엔드 도구 — uv, SQLAlchemy 2.0(동기), Alembic, Ruff, mypy | D-54 |
| 계층 경계 `api` → `service` → `repository`, 역방향 금지, 포트는 `service/ports.py` | TC-14, `[practices]` Code Style |
| 분석 모드 판별 — 미설정·빈 값·모르는 값은 mock, live 인데 키 없으면 기동 거부 | SC-04, D-... `[components]` |
| 오류 봉투 모양과 `code` 영어·`message` 한국어 | `[practices]`, `[contract]` 공통 규칙 |
| 초기 리비전을 U1 이 하나로 만든다 (엔티티 20개) | D-102 `[contract]` C15 |
| 시드 상태 9개와 진입점 `scripts/seed.py --state <name>` | D-98 `[contract]` C16 |
| 헬스체크 응답에 분석 모드를 싣는다 | AC9.1.2, AC9.3.4 `[contract]` C1 |
| 오래 걸리는 작업은 `202 Accepted` + 1초 간격 상태 조회 | D-96 `[contract]` 공통 규칙 |

---

## Q1. 초기 스키마 리비전에서 U1 은 각 테이블을 어디까지 적습니까?

U1 이 엔티티 20개의 테이블을 초기 리비전 하나로 만든다는 것은 정해졌습니다(D-102). 아직 안 정해진 것은
**각 테이블의 컬럼을 U1 이 어디까지 적느냐**입니다. 도메인 설계는 엔티티마다 속성 이름 목록만 주고
(예: Conversation 은 `userId, source, status, conversationKey, transcriptVersion, audioAssetId, createdAt`),
타입·제약·허용값은 "functional-design 이 정한다"고 넘겼습니다 `[contract]` C15. 그런데 그 상세를 실제로
아는 쪽은 각 기능 단위입니다. U1 이 지금 얼마나 적느냐에 따라 나중 단위가 추가 리비전을 몇 개 쓰게 될지가
갈립니다.

- A. **속성 이름과 타입만 적고 제약은 최소로 둔다** — NOT NULL 과 FK 만 걸고, 허용값(enum)·기본값·길이 제한·인덱스는
  각 단위가 자기 리비전에서 더한다. U1 이 빨리 닫히고 네 갈래가 일찍 시작하지만, 리비전 수가 늘고 초기 스키마만
  보고는 규칙을 알 수 없다
- B. **도메인 설계와 계약이 이미 적은 것은 전부 반영하고, 적지 않은 것만 최소로 둔다** — 계약이 못박은 것
  (판정 출처 네 컬럼 NOT NULL, 열람 권한 기본 NONE, 가변 구조는 JSONB 등)과 명세 `docs/input/04_domain-model.md` 의
  상태값은 초기 리비전에 넣고, 그 밖의 세부만 각 단위가 더한다
- C. **U1 이 20개 테이블의 컬럼을 전부 확정해 적는다** — U1 담당이 각 기능 명세를 읽어 타입·제약·허용값을 다 정한다.
  나중 리비전이 거의 없어지지만, U1 이 다른 단위의 설계를 앞질러 결정하게 되고 뼈대 기간이 길어진다
- X. Other (please specify)

[Answer]: B. **도메인 설계와 계약이 이미 적은 것은 전부 반영하고, 적지 않은 것만 최소로 둔다** — 계약이 못박은 것(판정 출처 네 컬럼 NOT NULL, 열람 권한 기본 NONE, 가변 구조는 JSONB 등)과 명세 `docs/input/04_domain-model.md` 의 상태값은 초기 리비전에 넣고, 그 밖의 세부만 각 단위가 더한다

## Q2. 대화의 "전사 상태"와 "분석 상태"를 컬럼 하나로 둡니까, 둘로 둡니까?

계약이 이 질문을 이 단계로 명시적으로 넘겼습니다 — "전사 상태와 분석 상태를 컬럼 하나로 둘지 둘로 둘지는
functional-design(3.1). API 는 C2 의 두 필드를 유지" `[contract]` C15. 대화는 업로드 중 → 전사 중 → 전사 완료를
지나고, 그와 별개로 분석 중 / 분석 완료 상태를 가집니다. 분석이 진행 중이면 새 분석 요청을 받지 않아야 합니다
`[components]`. 화면에 나가는 응답은 어느 쪽을 고르든 두 필드 그대로입니다.

- A. **컬럼 두 개** — `transcript_status` 와 `analysis_status` 를 따로 둔다. 전사 재시도와 재분석이 서로를 덮어쓰지
  않고, "전사 완료 + 분석 중"이 자연스럽게 표현된다. 대신 두 컬럼의 조합 중 말이 안 되는 것을 규칙으로 막아야 한다
- B. **컬럼 하나** — 상태 하나에 전 과정을 늘어놓는다(UPLOADING → TRANSCRIBING → TRANSCRIBED → ANALYZING → ANALYZED → FAILED).
  읽기 쉽지만 재분석 중에 전사 완료 정보가 가려지고, 실패가 어느 쪽 실패인지 따로 표시해야 한다
- X. Other (please specify)

[Answer]: A. **컬럼 두 개** — `transcript_status` 와 `analysis_status` 를 따로 둔다. 전사 재시도와 재분석이 서로를 덮어쓰지 않고, "전사 완료 + 분석 중"이 자연스럽게 표현된다. 대신 두 컬럼의 조합 중 말이 안 되는 것을 규칙으로 막아야 한다

## Q3. 백그라운드 작업(전사·분석)의 DB 세션을 어떻게 만듭니까?

계약이 이것도 이 단계로 넘겼습니다 — 백그라운드 작업은 요청 세션을 재사용하지 않고 세션 팩토리로 새 세션을
직접 열며, "세션 팩토리의 위치·주입 방식 세부는 functional-design(3.1)이 정한다" `[contract]` 공통 규칙.
U1 이 `db.py` 를 만들므로 이 모양을 U1 이 정하고 나머지 단위가 따릅니다.

- A. **`db.py` 가 세션 팩토리를 모듈 수준으로 공개하고, 백그라운드 작업 함수가 직접 `with session_factory() as s:` 로 연다** —
  가장 단순하고 Python 이 처음인 사람도 읽는다. 대신 각 작업 함수가 세션 수명을 직접 책임지므로 닫기를 빠뜨릴 여지가 있다
- B. **`db.py` 가 세션을 열고 커밋·롤백·닫기까지 감싸는 컨텍스트 매니저(예: `unit_of_work()`)를 하나 제공하고, 백그라운드 작업은
  그것만 쓴다** — 커밋 위치와 실패 시 롤백이 한 곳에 모이고, 실패 시 별도 세션으로 상태를 `FAILED` 로 적는 경로도 같이 담긴다.
  새 개념 하나를 팀이 익혀야 한다
- C. **백그라운드 작업 함수가 세션을 인자로 받고, 세션을 여는 일은 작업을 예약하는 쪽이 한다** — 테스트에서 세션을 넣기 쉽지만,
  작업을 예약하는 자리가 요청 경로여서 "요청 세션을 재사용하지 않는다"는 규칙을 실수로 깨기 가장 쉬운 모양이다
- X. Other (please specify)

[Answer]: B. **`db.py` 가 세션을 열고 커밋·롤백·닫기까지 감싸는 컨텍스트 매니저(예: `unit_of_work()`)를 하나 제공하고, 백그라운드 작업은 그것만 쓴다** — 커밋 위치와 실패 시 롤백이 한 곳에 모이고, 실패 시 별도 세션으로 상태를 `FAILED` 로 적는 경로도 같이 담긴다. 새 개념 하나를 팀이 익혀야 한다

## Q4. 헬스체크는 어디까지 확인합니까?

`docker compose up --build` 한 번으로 세 컨테이너가 뜨고 헬스체크가 통과해야 합니다(AC9.1.1) `[story]`.
응답에 분석 모드를 싣는 것은 정해졌습니다. 안 정해진 것은 **헬스체크가 DB 연결까지 확인하느냐**입니다.
Compose 가 backend 를 postgres 보다 먼저 띄울 수 있어서, 이 선택이 "떴는데 실은 못 쓰는 상태"를 잡느냐를 가릅니다.

- A. **프로세스만 확인한다** — 앱이 응답하면 `ok`. 빠르고 단순하지만, DB 가 아직 안 뜬 상태에서도 통과해 시연 당일
  첫 요청에서 처음 실패한다
- B. **DB 연결까지 확인한다** — 가벼운 질의(`SELECT 1`) 하나를 걸어 DB 가 응답할 때만 `ok`. 세 컨테이너가 실제로
  붙었는지를 한 번에 알 수 있다. DB 가 잠깐 느리면 헬스체크가 실패로 보일 수 있다
- C. **두 가지를 나눈다** — `/api/v1/health` 는 프로세스만 보고, Compose 의 컨테이너 헬스체크와 리허설 확인은
  DB 까지 보는 별도 경로를 쓴다. 정확하지만 확인할 자리가 둘이 되고 U1 범위가 늘어난다
- X. Other (please specify)

[Answer]: B. **DB 연결까지 확인한다** — 가벼운 질의(`SELECT 1`) 하나를 걸어 DB 가 응답할 때만 `ok`. 세 컨테이너가 실제로 붙었는지를 한 번에 알 수 있다. DB 가 잠깐 느리면 헬스체크가 실패로 보일 수 있다

## Q5. 합성 대화 기대 판정 픽스처를 파일 몇 개로, 어떤 모양으로 둡니까?

`docs/input/05_synthetic-test-data.md` 의 기대 판정을 기계가 읽는 픽스처 한 벌로 고정하고, Mock 제공자·백엔드 단위
테스트·프론트엔드 MSW 핸들러·Playwright 단언이 **전부 같은 한 벌**을 읽습니다 `[practices]` Testing Posture.
자리는 `backend/app/fixtures/` 로 정해졌습니다. 안 정해진 것은 그 안의 파일 구성과 형식이며, U1 이 이 자리를 만듭니다.

- A. **합성 대화 한 건당 파일 하나(JSON)** — `s1_repair.json`, `s2_topic.json`, `s3_unclear.json`. 한 대화의 전사와 기대 판정이
  한 파일에 모여 사람이 표와 대조하기 쉽다. 정정 후 S3 처럼 전사 버전이 다른 경우를 같은 파일 안에 버전별로 담는다
- B. **종류별 파일(JSON)** — `transcripts.json` 과 `expected_judgments.json` 로 나눈다. Mock STT 와 Mock LLM 이 각자 자기
  파일만 읽어 경계가 깔끔하지만, 한 대화를 확인하려면 두 파일을 오간다
- C. **YAML 한 파일** — 세 대화의 전사와 기대 판정을 한 파일에 담는다. 주석을 달 수 있어 기준 문서와 대조하기 좋지만,
  프론트엔드에서 읽으려면 변환이 한 단계 필요하다
- X. Other (please specify)

[Answer]: A. **합성 대화 한 건당 파일 하나(JSON)** — `s1_repair.json`, `s2_topic.json`, `s3_unclear.json`. 한 대화의 전사와 기대 판정이 한 파일에 모여 사람이 표와 대조하기 쉽다. 정정 후 S3 처럼 전사 버전이 다른 경우를 같은 파일 안에 버전별로 담는다

## Q6. 요청 식별자(`request_id`)를 백그라운드 작업까지 이어 붙입니까?

요청마다 `request_id` 를 발급해 로그와 응답에 같은 값을 넣는 것은 정해졌습니다 `[practices]`. 안 정해진 것은
**전사·분석처럼 요청이 끝난 뒤에 도는 작업의 로그에 무엇을 남기느냐**입니다. 이것이 없으면 "S2 업로드가 실패했다"는
신고를 받았을 때 그 업로드를 받은 요청과 그 뒤에 돈 전사 작업의 로그를 이어 볼 수 없습니다.

- A. **요청의 `request_id` 를 작업에 넘겨 그대로 쓴다** — 업로드 요청과 그 전사 작업이 같은 값으로 묶여 한 번에 찾힌다.
  작업이 여러 번 재시도되면 같은 값이 여러 묶음에 걸친다
- B. **작업이 자기 `request_id` 를 새로 발급하고, 로그에 원래 요청의 값을 함께 남긴다** — 작업 한 번이 한 묶음이 되고
  원래 요청으로도 거슬러 갈 수 있다. 로그에 값이 두 개가 된다
- C. **작업은 대화 ID 만 남긴다** — 가장 단순하지만 요청 쪽 로그와 이어 볼 수단이 대화 ID 하나뿐이라, 같은 대화에
  여러 번 작업이 돌면 어느 요청에서 비롯됐는지 알 수 없다
- X. Other (please specify)

[Answer]: B. **작업이 자기 `request_id` 를 새로 발급하고, 로그에 원래 요청의 값을 함께 남긴다** — 작업 한 번이 한 묶음이 되고 원래 요청으로도 거슬러 갈 수 있다. 로그에 값이 두 개가 된다

## Consolidated Summary Confirmation

확정된 답 여섯 가지:

- **Q1 초기 스키마 상세 수준** — 계약과 명세가 이미 글로 확정한 것(판정 출처 네 컬럼 NOT NULL, 열람 권한 기본 NONE,
  가변 구조 JSONB, `docs/input/04_domain-model.md` 의 상태값)은 초기 리비전에 반영하고, 아직 글이 없는 세부는 각 단위가
  나중에 더한다. U1 이 다른 단위의 설계를 앞질러 결정하지 않는다.
- **Q2 대화 상태 컬럼** — `transcript_status` 와 `analysis_status` 두 컬럼으로 나눈다. 재분석이 전사 완료 정보를
  덮어쓰지 않는다. 말이 안 되는 조합은 규칙으로 막는다. API 응답은 계약 C2 의 두 필드 그대로다.
- **Q3 백그라운드 작업 DB 세션** — `db.py` 가 열기·커밋·롤백·닫기와 실패 시 `FAILED` 기록 경로까지 감싼 컨텍스트
  매니저를 하나 제공하고, 전사·분석 작업은 그것만 쓴다. 요청 세션을 재사용하지 않는다.
- **Q4 헬스체크** — 가벼운 질의 하나로 DB 연결까지 확인하고, 응답할 때만 `ok` 를 낸다. 응답에는 계약 C1 대로
  `status` 와 `analysisMode` 를 싣는다.
- **Q5 픽스처 파일** — 합성 대화 한 건당 JSON 파일 하나(`s1_repair.json`, `s2_topic.json`, `s3_unclear.json`)를
  `backend/app/fixtures/` 에 둔다. 전사 버전이 다른 경우(정정 후 S3)는 같은 파일 안에 버전별로 담는다.
  Mock 제공자·백엔드 단위 테스트·프론트엔드 MSW·Playwright 가 모두 이 한 벌을 읽는다.
- **Q6 요청 식별자** — 백그라운드 작업은 자기 `request_id` 를 새로 발급하고, 로그에 원래 요청의 값을 함께 남긴다.

- **검토 반영(변경 요청 뒤 추가)** — R-01: 내부 상태값과 계약 C2 의 API 값 대응표를 `entities.md` §4 에 넣고,
  변환은 API 계층 응답 모델에서 하며 책임은 u3-f01-capture 에 둔다. 계약 C16 의 "전사 READY" 는 API 값을 가리킨
  것임을 밝히고, 규칙 BR7.4 로 "내부 값을 응답에 그대로 내보내지 않는다"를 더한다.
  R-02: 전사 실패에 사유(`STORAGE` / `TRANSCRIPTION`)를 두어, 다시 시도가 저장부터 도는 경로와 전사만 도는
  경로로 갈리게 상태 기계 SM-A 와 규칙 BR7.5 에 적는다. R-03: "말이 되지 않는 조합" 표에 `ANALYZE_FAILED` 를
  포함하고 그 표가 전체 목록임을 밝힌다.

- Looks correct
- Request changes

[Answer]: Looks correct

## Requested Changes Feedback

승인 게이트에서 **Request Changes** 를 고르셨습니다. 검토가 낸 지적은 아래와 같습니다. 무엇을 어떻게 고칠지
알려 주시면 그대로 반영하고 다시 검토받겠습니다.

- **R-01 (Major)** — 이 단위가 정한 내부 상태값(`TRANSCRIBED`, `NOT_ANALYZED` 등)이 확정된 계약 C2 의 API 값
  (`READY`, `NOT_STARTED`)과 다른데, 대응표도 변환 책임자도 어느 문서에도 없다. C16 의 "S1 전사 READY" 표기와도
  어긋나 보인다.
- **R-02 (Major)** — 상태 기계 SM-A 가 파일 저장 실패와 전사 실패를 `TRANSCRIBE_FAILED` 하나로 합쳤는데,
  계약 C2 의 다시 시도는 전사만 가리킨다. 파일이 디스크에 없는 저장 실패의 회복 경로가 정의되지 않았다.
- **R-03 (Minor)** — SM-B 의 "말이 되지 않는 조합" 표에 `ANALYZE_FAILED` 행이 빠졌다.

**리드가 제시한 반영 방안** (사용자의 답 "그대로 진행" 이 가리키는 내용):

- R-01 — `entities.md` §4 에 내부 값 ↔ API 값 대응표를 넣는다: `TRANSCRIBED` → `READY`,
  `TRANSCRIBE_FAILED` → `FAILED`, `NOT_ANALYZED` → `NOT_STARTED`, `ANALYZE_FAILED` → `FAILED`.
  변환은 API 계층 응답 모델에서 하고 책임은 `conversations` 컬럼 소유 단위인 u3-f01-capture 에 둔다.
  계약 C16 의 "전사 READY" 는 API 값을 가리킨 것임을 밝힌다. 규칙 BR7.4 로 "내부 값을 API 응답에
  그대로 내보내지 않는다"를 더한다.
- R-02 — `TRANSCRIBE_FAILED` 에 실패 사유를 두어 저장 실패와 전사 실패를 구분하고, 다시 시도가 사유에 따라
  저장부터 도는 경로와 전사만 도는 경로로 갈리게 상태 기계와 규칙에 적는다.
- R-03 — "말이 되지 않는 조합" 표에 `ANALYZE_FAILED` 행을 더한다.

[Answer]: 그대로 진행
