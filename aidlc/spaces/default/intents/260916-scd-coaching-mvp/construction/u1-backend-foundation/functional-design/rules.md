# Business Rules — u1-backend-foundation

**Stage**: functional-design (3.1) · **Unit**: u1-backend-foundation (U1 백엔드 기반)
**작성일**: 2026-09-18

## Sources

| 태그 | 출처 |
|---|---|
| `[unit]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/unit-of-work.md` — U1 정의 |
| `[map]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/unit-of-work-story-map.md` — U1 에 배정된 스토리 US9.1·US9.2 |
| `[req]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/requirements.md` — FR11.1, NFR5, NFR10, NFR12 |
| `[components]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/domain-design/components.md` — Account, ProviderAdapters |
| `[contract]` | `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md` — 공통 규칙, C1, C14, C15, C16 |
| `[Q<n>]` | `functional-design-questions.md` |
| `[spec:05]` | `docs/input/05_synthetic-test-data.md` — 합성 대화 3건과 기대 판정 |

**읽는 법** — `BR{묶음}.{순번}` 이 규칙 번호다. "무엇에 적용되는가"는 규칙이 지키는 대상, "어길 때"는 규칙이
깨졌을 때 시스템이 하는 일이다. 이 문서는 기술 선택이 아니라 지켜야 할 것을 적는다.

---

```yaml
rules:
  - id: BR1.1
    statement: 분석 모드가 미설정이거나 빈 값이거나 모르는 값이면 mock 으로 동작한다
    category: policy
    applies_to: 기동 시 설정 해석
    trigger: 프로세스가 기동하며 분석 모드 설정을 읽을 때
    logic: >
      IF 분석 모드 설정이 없거나 / 빈 값이거나 / 정해진 값(mock, live) 중 어느 것도 아니면
      THEN 분석 모드를 mock 으로 정하고 Mock 제공자를 쓴다. 절대 live 로 흘러가지 않는다.
    violation: 해당 없음 — 이 규칙 자체가 안전한 쪽으로 닫는 규칙이다. 다만 모르는 값이었다는 사실은 로그에 남긴다
    source: SC-04, AC9.1.2, `[components]` ProviderAdapters

  - id: BR1.2
    statement: 분석 모드가 live 인데 필요한 키가 없으면 기동을 거부한다
    category: constraint
    applies_to: 기동 시 설정 해석
    trigger: 분석 모드가 live 로 확인된 직후
    logic: >
      IF 분석 모드가 live 이고 AND 필요한 제공자 키 중 하나라도 없으면
      THEN 기동을 중단하고 어떤 키가 없는지를 로그에 남긴다.
      조용히 mock 으로 되돌아가지 않고, 첫 사용자 요청까지 미루지도 않는다.
    violation: 프로세스가 뜨지 않는다. 컨테이너가 실패 상태로 남아 사람이 바로 알아챈다
    source: SC-04, AC9.1.3, `[components]` ProviderAdapters

  - id: BR1.3
    statement: 분석 모드는 기동할 때 한 번 정해지고 실행 중에 바뀌지 않는다
    category: constraint
    applies_to: 설정 객체
    trigger: 기동 이후의 모든 요청
    logic: >
      IF 코드의 어느 자리에서든 분석 모드를 알아야 하면
      THEN 기동 시 만들어진 설정 객체 하나를 통해 읽는다. 환경변수를 다시 읽지 않는다.
    violation: 같은 실행 안에서 모드가 갈려 헬스체크가 알린 값과 실제 동작이 어긋난다
    source: `[contract]` 공통 규칙, 팀 관행 Code Style

  - id: BR2.1
    statement: 시드 고정 사용자는 동의 전 상태로 시작한다
    category: constraint
    applies_to: User
    trigger: 시드 상태 base 를 적재할 때
    logic: >
      IF 시드가 고정 사용자를 만들면
      THEN 동의 시각을 비운 채로 만든다. 종단 시험은 동의 화면부터 시작해야 한다.
    violation: 동의 화면이 종단 흐름에서 건너뛰어져 첫 방문 동의가 시험되지 않는다
    source: AC9.2.1, `[contract]` C16, `[components]` Account

  - id: BR2.2
    statement: 동의는 사용자 단위로 서버에 저장하고, 한 번 저장되면 되돌리지 않는다
    category: constraint
    applies_to: User
    trigger: 첫 방문 안내에 동의를 보낼 때
    logic: >
      IF 동의 요청이 들어오면 THEN 그 사용자의 동의 시각을 지금으로 적는다.
      IF 이미 동의한 사용자가 다시 동의를 보내면 THEN 처음 동의 시각을 유지하고 성공으로 답한다.
    violation: 같은 동의를 여러 번 보내면 시각이 계속 갱신되어 언제 동의했는지가 사라진다
    source: FR9.2, `[contract]` C1, `[components]` Account

  - id: BR2.3
    statement: Must 경로는 인증 없이 고정 사용자 한 명으로 처리한다
    category: authorization
    applies_to: 모든 백엔드 요청
    trigger: 요청이 들어올 때
    logic: >
      IF 요청에 사용자 정보가 없으면 THEN 서버가 시드 고정 사용자로 처리한다.
      계정·로그인이 들어오면(u11) 이 자리가 세션 확인으로 바뀐다.
    violation: 시연이 로그인 화면에서 막힌다
    source: FR11.1, AC9.2.1, `[contract]` 공통 규칙

  - id: BR3.1
    statement: 헬스체크는 저장소가 실제로 응답할 때만 정상이라고 답한다
    category: validation
    applies_to: 헬스체크 응답
    trigger: 헬스체크를 조회할 때
    logic: >
      IF 프로세스가 살아 있고 AND 저장소에 가벼운 확인 질의를 보내 응답을 받으면 THEN 정상이라고 답한다.
      ELSE 정상이 아니라고 답한다.
    violation: 컨테이너는 떴는데 저장소에 못 붙은 상태가 통과로 보여, 첫 사용자 요청에서 처음 드러난다
    source: AC9.1.1, `[Q4]`

  - id: BR3.2
    statement: 헬스체크 응답은 현재 분석 모드를 함께 알린다
    category: constraint
    applies_to: 헬스체크 응답
    trigger: 헬스체크를 조회할 때
    logic: IF 헬스체크에 답하면 THEN 지금 쓰고 있는 분석 모드 값을 응답에 포함한다
    violation: 시연 리허설이 mock 임을 기계적으로 단언할 수 없어 눈으로 확인하게 된다
    source: AC9.3.4, `[contract]` C1

  - id: BR4.1
    statement: Mock 전사와 Mock 판정은 파일 이름의 대화 키로 합성 대화를 고른다
    category: calculation
    applies_to: Mock 제공자
    trigger: mock 모드에서 전사 또는 판정을 요청받을 때
    logic: >
      IF 파일 이름에 알려진 대화 키가 들어 있으면 THEN 그 키의 합성 대화 자료를 쓴다
      (`conv_repair_01` → S1, `conv_topic_02` → S2, `conv_unclear_03` → S3).
    violation: 같은 파일을 올려도 매번 다른 결과가 나와 시연이 재현되지 않는다
    source: AC9.2.2, FR1.5, `[spec:05]`

  - id: BR4.2
    statement: 대화 키가 없거나 모르는 키이거나 브라우저 녹음이면 S1 으로 처리한다
    category: policy
    applies_to: Mock 제공자
    trigger: mock 모드에서 대화 키를 찾지 못했을 때
    logic: >
      IF 파일 이름에 대화 키가 없거나 / 키처럼 생겼지만 모르는 값이거나 / 브라우저 녹음이면
      THEN S1(`conv_repair_01`)의 자료로 처리한다. 실패로 만들지 않는다.
    violation: 시연 중 이름이 다른 파일을 올리면 흐름이 끊긴다
    source: AC9.2.3, FR1.5

  - id: BR4.3
    statement: 합성 대화 자료는 파일 한 벌이 단일 출처이며, 기대 판정을 코드나 테스트에 옮겨 적지 않는다
    category: constraint
    applies_to: Mock 제공자, 백엔드 단위 테스트, 프론트엔드 모의 응답, 종단 시험
    trigger: 합성 대화의 전사나 기대 판정이 필요할 때
    logic: >
      IF 어느 자리든 합성 대화의 전사나 기대 판정이 필요하면
      THEN `backend/app/fixtures/` 의 대화별 파일(`s1_repair`, `s2_topic`, `s3_unclear`)을 읽는다.
      값을 따로 적어 두지 않는다. 전사 버전이 다른 경우는 같은 파일 안에서 버전으로 고른다.
    violation: >
      손으로 옮긴 사본이 한 칸 어긋나도 각자 초록이라 아무도 모른 채 전 구간이 일관되게 거짓말한다
    source: `[Q5]`, 팀 관행 Testing Posture, `[spec:05]`

  - id: BR5.1
    statement: 요청이 끝난 뒤 도는 작업은 요청의 저장소 연결을 재사용하지 않는다
    category: constraint
    applies_to: 전사·분석처럼 응답 이후에 도는 작업
    trigger: 작업이 시작될 때
    logic: >
      IF 요청 이후에 도는 작업이 저장소를 써야 하면
      THEN 자기 연결을 새로 열고, 끝날 때 닫는다. 요청에 주입된 연결은 이미 닫혀 있다.
    violation: 작업이 이미 닫힌 연결을 만져 실패하고, 실패 원인이 기능과 무관한 자리에서 나온다
    source: `[contract]` 공통 규칙, `[Q3]`

  - id: BR5.2
    statement: 작업의 저장소 연결은 열기·확정·되돌리기·닫기를 한 장치가 맡는다
    category: constraint
    applies_to: 전사·분석처럼 응답 이후에 도는 작업
    trigger: 작업이 저장소를 쓸 때
    logic: >
      IF 작업이 저장소를 쓰면 THEN 공통 작업 단위 장치를 통해서만 연결을 얻는다.
      그 장치가 성공 시 한 번 확정하고, 예외가 나면 되돌린 뒤 별도 연결로 실패 상태를 적고, 어느 경우든 닫는다.
    violation: 작업마다 닫기와 되돌리기가 흩어져, 하나라도 빠지면 연결이 새거나 부분 저장이 남는다
    source: `[Q3]`, `[contract]` 공통 규칙

  - id: BR5.3
    statement: 확정은 업무 계층의 경계에서 한 번만 한다
    category: constraint
    applies_to: 모든 저장 경로
    trigger: 저장 작업이 끝날 때
    logic: IF 저장을 마치면 THEN 업무 계층 경계에서 한 번 확정한다. 저장소 계층은 확정하지 않는다
    violation: 부분 저장이 생기고, 그것이 삭제 누수와 같은 계열의 사고가 된다
    source: 팀 관행 Code Style, TC-14

  - id: BR6.1
    statement: 요청마다 요청 식별자를 발급해 로그와 응답에 같은 값을 넣는다
    category: constraint
    applies_to: 모든 요청
    trigger: 요청이 들어올 때
    logic: IF 요청이 들어오면 THEN 식별자를 하나 발급해 그 요청의 모든 로그와 오류 응답에 싣는다
    violation: 사용자가 본 오류와 로그를 이어 볼 수단이 없다
    source: NFR12, 팀 관행 Code Style

  - id: BR6.2
    statement: 응답 이후에 도는 작업은 자기 식별자를 새로 발급하고 원래 요청의 식별자를 함께 남긴다
    category: constraint
    applies_to: 전사·분석처럼 응답 이후에 도는 작업
    trigger: 작업이 시작될 때
    logic: >
      IF 작업이 시작되면 THEN 작업 자신의 식별자를 새로 발급하고,
      그 작업을 낳은 요청의 식별자를 로그에 함께 남긴다. 재시도는 새 작업 식별자를 받는다.
    violation: 한 대화에 작업이 여러 번 돌면 어느 요청에서 비롯됐는지 갈라 볼 수 없다
    source: `[Q6]`

  - id: BR6.3
    statement: 로그에 전사 본문을 남기지 않는다
    category: constraint
    applies_to: 모든 로그
    trigger: 전사나 판정을 다루는 자리에서 로그를 남길 때
    logic: >
      IF 로그를 남기면 THEN 모델 이름·프롬프트 버전·소요 시간·식별자를 남기고 전사 본문은 남기지 않는다
    violation: 합성 데이터라도 대화 내용이 로그 파일로 새어 나가는 경로가 생긴다
    source: `[components]` ProviderAdapters, 팀 관행 Code Style

  - id: BR6.4
    statement: 비밀값과 키는 환경변수로만 다루고 저장소에 커밋하지 않는다
    category: constraint
    applies_to: 저장소 트리
    trigger: 저장소를 새로 받아 확인할 때
    logic: >
      IF 새로 받은 저장소 트리를 확인하면 THEN 실제 값이 든 환경 파일이 없어야 한다.
      예시 파일만 있고, 그 값 자리는 비워 두거나 설명 문구로 둔다. 실제 키를 닮은 더미를 넣지 않는다.
    violation: 한 번 커밋에 들어간 키는 무시 규칙으로 지워지지 않는다
    source: AC9.1.4, `[req]` NFR6, 팀 관행 Way of Working

  - id: BR7.1
    statement: 전사가 끝나기 전에는 분석이 시작될 수 없다
    category: validation
    applies_to: Conversation 의 두 상태 값
    trigger: 분석을 시작하려 할 때
    logic: >
      IF 전사 상태가 `TRANSCRIBED` 가 아니면 THEN 분석 시작을 거부한다
    violation: 재료 없이 분석이 돌아 빈 판정이 저장된다
    source: `[Q2]`, `[components]` Conversation

  - id: BR7.2
    statement: 분석이 진행 중이면 새 분석 요청을 받지 않는다
    category: validation
    applies_to: Conversation 의 분석 상태
    trigger: 분석 또는 재분석을 요청할 때
    logic: IF 분석 상태가 `ANALYZING` 이면 THEN 새 요청을 거부하고 진행 중임을 알린다
    violation: 같은 대화에 판정이 두 벌 만들어져 어느 것이 최신인지 갈린다
    source: AC3.3.4, `[components]` Conversation

  - id: BR7.3
    statement: 재분석은 전사 상태를 되돌리지 않는다
    category: constraint
    applies_to: Conversation 의 두 상태 값
    trigger: 재분석이 시작될 때
    logic: >
      IF 재분석이 시작되면 THEN 분석 상태만 `ANALYZING` 으로 바꾸고 전사 상태는 `TRANSCRIBED` 로 둔다.
      화면은 재분석 중에도 전사를 계속 보여 준다.
    violation: 재분석 중에 전사가 사라진 것처럼 보인다
    source: `[Q2]`, F07 재검토 흐름

  - id: BR7.4
    statement: 저장소 안의 상태값을 API 응답에 그대로 내보내지 않는다
    category: constraint
    applies_to: 대화 상태를 담은 모든 응답
    trigger: 대화 상태를 응답으로 만들 때
    logic: >
      IF 대화 상태를 응답에 실으면 THEN `entities.md` §4 의 대응표대로 계약 값으로 바꿔서 내보낸다
      (`TRANSCRIBED` → `READY`, `TRANSCRIBE_FAILED` → `FAILED`, `NOT_ANALYZED` → `NOT_STARTED`,
      `ANALYZE_FAILED` → `FAILED`). 전사 실패 사유는 내보내지 않는다.
      변환은 API 계층의 응답 모델 한 곳에서만 하고, 업무 계층과 저장소 계층은 내부 값만 다룬다.
    violation: >
      같은 것을 두 이름으로 부르게 되고, 프론트엔드가 계약에 없는 값을 받아 분기가 깨진다.
      팀 관행이 경계하는 이름 분기가 여기서 시작된다
    source: `[contract]` C2, `entities.md` §4, 팀 관행 Code Style

  - id: BR7.5
    statement: 전사 실패의 다시 시도는 실패 사유에 따라 시작점이 다르다
    category: policy
    applies_to: Conversation 의 전사 상태와 실패 사유
    trigger: 전사 실패 상태에서 다시 시도를 요청할 때
    logic: >
      IF 실패 사유가 `STORAGE` 이면 THEN 파일 저장부터 다시 한다 — 디스크에 파일이 없으므로 전사만
      다시 돌릴 수 없다. 상태는 `UPLOADING` 으로 돌아간다.
      IF 실패 사유가 `TRANSCRIPTION` 이면 THEN 이미 저장된 파일로 전사만 다시 돈다. 상태는
      `TRANSCRIBING` 으로 간다.
    violation: >
      없는 파일을 전사하려는 시도가 되어 같은 실패가 반복되고, 사용자는 원인을 알 수 없는 채로
      다시 시도 버튼만 누르게 된다
    source: 검토 R-02, `[contract]` C2 재시도 경로

  - id: BR8.1
    statement: 초기 스키마는 이미 글로 확정된 것만 담고, 정해지지 않은 세부는 소유 단위에 남긴다
    category: policy
    applies_to: 초기 스키마 리비전
    trigger: U1 이 20개 테이블을 만들 때
    logic: >
      IF 어떤 컬럼의 타입·제약·허용값이 계약이나 기존 명세에 글로 적혀 있으면 THEN 초기 리비전에 반영한다.
      ELSE 참조 관계와 이름만 두고, 그 테이블의 소유 단위가 자기 기능 설계 뒤에 리비전으로 더한다.
    violation: >
      U1 담당이 다른 단위의 설계를 앞질러 결정하게 되고, 그 단위가 나중에 확정한 값과 어긋나면
      병합된 리비전을 고치게 된다
    source: `[Q1]`, `[contract]` C15

  - id: BR8.2
    statement: 음성 본문은 저장소 안에 넣지 않는다
    category: constraint
    applies_to: 초기 스키마 리비전
    trigger: 음성 관련 테이블을 만들 때
    logic: IF 음성 자료를 다루면 THEN 파일은 파일 저장소에 두고 테이블에는 참조와 메타데이터만 둔다
    violation: 저장소가 비대해지고 삭제 경로가 둘로 갈린다
    source: TC-05, `[contract]` C15
```

---

## 규칙 요약

| 묶음 | 무엇을 지키는가 | 규칙 |
|---|---|---|
| BR1 | 분석 모드가 안전한 쪽으로만 닫힌다 | BR1.1 미설정·모르는 값은 mock · BR1.2 키 없는 live 는 기동 거부 · BR1.3 기동 시 한 번 결정 |
| BR2 | 동의와 고정 사용자 | BR2.1 시드 사용자는 동의 전 · BR2.2 동의는 되돌리지 않음 · BR2.3 인증 없이 고정 사용자 |
| BR3 | 헬스체크가 진실을 말한다 | BR3.1 저장소까지 확인 · BR3.2 분석 모드 노출 |
| BR4 | 시연이 매번 같은 결과로 재현된다 | BR4.1 대화 키로 선택 · BR4.2 모르면 S1 · BR4.3 픽스처가 단일 출처 |
| BR5 | 응답 이후 작업의 저장소 사용 | BR5.1 요청 연결 재사용 금지 · BR5.2 한 장치가 수명 관리 · BR5.3 확정은 한 번 |
| BR6 | 무슨 일이 있었는지 되짚을 수 있다 | BR6.1 요청 식별자 · BR6.2 작업 식별자와 원래 값 · BR6.3 전사 본문 제외 · BR6.4 비밀값 커밋 금지 |
| BR7 | 두 상태 값의 조합이 말이 되고, 안과 밖의 이름이 섞이지 않는다 | BR7.1 전사 먼저 · BR7.2 분석 중 중복 금지 · BR7.3 재분석이 전사를 되돌리지 않음 · BR7.4 내부 값을 응답에 그대로 내보내지 않음 · BR7.5 실패 사유에 따라 다시 시도의 시작점이 다름 |
| BR8 | 초기 스키마의 경계 | BR8.1 확정된 것만 담는다 · BR8.2 음성 본문 제외 |
