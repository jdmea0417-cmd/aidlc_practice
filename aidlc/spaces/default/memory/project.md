# Project-Level Rules

> Project-specific specialisation and corrections. Loaded after `org.md` and
> `team.md` as strict-additive guidance; contradictions with broader policy
> are rejected. Populated by practices-discovery and the self-learning loop.
>
> Use sparingly: most teams don't need a project layer. Reach for it
> only when this specific project needs stable, durable guidance beyond the
> team practice (for example, package-specific release checks or an additional
> regression suite for a legacy component).

## Way of Working

<!-- Project-specific specialisation. Example: -->
<!-- This monorepo requires package-scoped branch names and a package owner -->
<!-- review in addition to the team's normal merge policy. -->

## Walking Skeleton

<!-- Project-specific specialisation. Example: -->
<!-- The walking skeleton must exercise the legacy service adapter as well -->
<!-- as the new service boundary. -->

- 걷는 뼈대 Bolt 는 화면 하나를 두 Bolt 로 가르지 않는다. 한 화면이 걸친 작업 단위는 뼈대에 통째로 담아, 뼈대가 커지더라도 화면이 나뉘지 않게 한다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:delivery-planning:2f8aa0b4da73f8660f6b8c83ee57489c7f3db412bd26a634bb0dff71ddc42d93 -->

## Testing Posture

<!-- Project-specific specialisation. -->

## Change Control

<!-- Project-specific. Mode: strict or relaxed. Strict here holds for every intent and cannot be changed from chat. -->

## Deployment

<!-- Project-specific specialisation. -->

- 스키마 마이그레이션 적용은 애플리케이션 기동 흐름에 넣지 않고 별도 단계로 둔다. 기동할 때마다 적용하는 모양은 컨테이너가 동시에 뜰 때 경쟁이 생기고, 전진 방향만 쓰기로 한 관행과도 결이 맞지 않는다. 테스트도 같은 마이그레이션으로 스키마를 만들어 마이그레이션이 실제로 한 번은 실행되게 한다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:functional-design:5a8a9023614c7c0784cd3a7b332a464c12e5758925577f9cb9bdf7c522368c85 -->

- 헬스체크는 프로세스 생존만 보지 않고 저장소에 가벼운 확인 질의를 보내 응답할 때만 정상이라고 답한다. 프로세스만 보는 확인은 컨테이너는 떴는데 저장소에 못 붙은 상태를 통과시켜, 시연 당일 첫 요청에서야 드러나게 한다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:functional-design:d458ab397c24a738126d14f071ec6ec35806085d08dcec2081b50e15273ab3de -->

## Code Style

<!-- Project-specific specialisation. -->

- 백엔드의 api·service·repository 는 팀 관행의 5개 이름이 아니라 도메인 설계(D-83)의 6개 업무 이름 conversation, assessment, training, record, account, privacy 로 나눈다. 추천은 training, 사용자·동의·보호자 초대는 account 에 둔다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:domain-design:207b9cc14f70b2965e15b40c6415b7727c05aa785f5fb0322da02dc225f825a6 -->

- 대화 삭제는 privacy 의 삭제 유스케이스 하나에서 시작해 지울 파일 경로를 삭제 요청에 먼저 기록하고, 한 트랜잭션에서 각 컴포넌트 정리 인터페이스로 DB 행을 지워 커밋한 뒤 파일을 지운다. 실패한 파일 경로는 일부 완료로 남겨 다시 삭제 요청 때 지운다. 팀 관행의 파일 → DB 행 잠정 순서는 이 규칙(도메인 설계 ADR-006, D-84)이 대체한다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:domain-design:d3f695313f9ae6b61d13186ddaa37e174a0ef557e8babc2848e30bdad032b62e -->

## Tech Stack

<!-- Technology choices locked for this project. -->

## Decided

<!-- Decisions made in earlier stages that should not be re-asked. -->
<!-- Format: DECIDED: [decision] (Stage [slug], [date]) -->

## Scope Overrides

<!-- Custom scope rules for this project. -->

## Forbidden

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: NEVER [behavior] (affirmed [date]) -->
<!-- Example: NEVER throw exceptions across service layer boundaries (affirmed 2026-05-17) -->

- NEVER 프론트엔드에서 STT·LLM API 를 직접 호출한다. 키가 노출되고 호출 기록이 누락된다 `[constraint:TC-07]` (affirmed 2026-09-17)

- NEVER ORM 모델을 API 응답으로 그대로 반환한다. Pydantic 응답 모델로 바꿔 내보낸다 `[constraint:TC-14][spec:02 §5]` (affirmed 2026-09-17)

- NEVER 음성 파일을 DB BLOB 으로 저장한다. 파일 저장소 + 메타데이터 테이블로 관리한다 `[constraint:TC-05]` (affirmed 2026-09-17)

- NEVER 종합점수·백분위를 계산하는 코드를 만든다. 행동별 상태와 기회 수 집계까지만 한다 `[constraint:TC-13]` (affirmed 2026-09-17)

- NEVER 이번 범위에서 LangChain 류 오케스트레이션 프레임워크, Neo4j·벡터DB, Redux 류 전역 상태 관리 라이브러리를 도입한다 `[constraint:TC-11][constraint:TC-12][spec:02 §5]` (affirmed 2026-09-17)

- NEVER 실제 사용자 데이터를 수집하거나 저장소·픽스처에 넣는다. 모든 데이터는 합성 데이터다 `[constraint:SC-02]` (affirmed 2026-09-17)

- NEVER `ANALYSIS_MODE=live` 를 합성 데이터가 아닌 대화에 대해 켠다. live 는 전사 텍스트를 제3자에게 보내는 경로이고, 한 번이라도 SC-02 가 깨지면 규제 항목을 기록하지 않기로 한 결정이 함께 무효가 된다 `[constraint:SC-02][raid:A2][devsecops §7]` (affirmed 2026-09-17)

- NEVER 전사 텍스트나 LLM 출력을 `dangerouslySetInnerHTML` 로 렌더링한다. LLM 출력발 저장형 XSS 가 된다 `[constraint:TC-08][devsecops §4]` (affirmed 2026-09-17)

## Mandated

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: ALWAYS [behavior] (affirmed [date]) -->
<!-- Example: ALWAYS use Result<T,E> for fallible operations in service layer (affirmed 2026-05-17) -->

- ALWAYS `api` → `service` → `repository` 순서로만 호출하고 영속성 접근은 반드시 `service` 를 경유한다. 건너뛰면 삭제 전파와 권한 검사가 누락된다 `[constraint:TC-14][spec:02 §5][raid:R3]` (affirmed 2026-09-17)

- ALWAYS STT·LLM 은 `SttProvider` / `LlmProvider` 인터페이스 뒤에서만 호출하고 기본 실행 경로는 `ANALYSIS_MODE=mock` 으로 둔다 `[constraint:TC-06][constraint:SC-04]` (affirmed 2026-09-17)

- ALWAYS `ANALYSIS_MODE` 가 미설정·빈 값·모르는 값이면 `mock` 으로 동작하고 `live` 인데 키가 없으면 기동을 거부한다. 조용히 `mock` 으로 되돌아가거나 첫 요청에서 터지게 두지 않는다 `[constraint:SC-04][raid:A3][devsecops §5]` (affirmed 2026-09-17)

- ALWAYS 전사 텍스트는 프롬프트에서 구분자로 감싼 데이터 블록으로만 전달하고, 넣기 전에 전사에서 구분자 시퀀스를 제거하거나 이스케이프한다. 데이터가 구분자를 포함할 수 있으면 그 구분자는 경계가 아니다 `[constraint:TC-08][devsecops §4]` (affirmed 2026-09-17)

- ALWAYS LLM 판정 결과를 저장할 때 모델명·프롬프트 버전·기준 버전을 함께 저장하고, 응답 모델 검증에 실패한 출력은 강제 변환하지 않고 거부한다 `[constraint:TC-10][devsecops §4]` (affirmed 2026-09-17)

- ALWAYS 비밀값과 API 키는 backend 환경변수로만 다루고 저장소에 커밋하지 않는다 `[spec:02 §4][phase]` (affirmed 2026-09-17)

- ALWAYS `docs/input/05_synthetic-test-data.md` 의 기대 판정을 픽스처 파일로 고정하고 판정 관련 단위 테스트가 그 파일을 읽는다. 기대값을 테스트 코드에 직접 적지 않는다 `[FU2][spec:05]` (affirmed 2026-09-17)

- ALWAYS `backend/app/service/` 의 라인 커버리지를 80% 이상으로 유지한다. 통과시키려고 이 바닥을 낮추지 않는다 `[Q4][org]` (affirmed 2026-09-17)

- ALWAYS 병합 전에 GitHub Actions 검사를 통과한다. 검사가 통과하지 않은 PR 은 `main` 에 병합하지 않는다 `[Q1][FU3]` (affirmed 2026-09-17)

- ALWAYS 사람이 읽는 것 — 산출물, 질문, UI 문구, 커밋 메시지 — 은 한국어로 쓴다 `[constraint:OC-06]` (affirmed 2026-09-17)

## Corrections

<!-- Project-specific corrections from human feedback. -->
<!-- Format: NEVER/ALWAYS [behavior] (learned [date]) -->
- 프로젝트 설명이 근거 문서를 여러 개 지목하면 임의로 하나를 고르지 말고, 어느 파일을 근거 문서로 등록할지 사용자에게 물어 확정한다. 나머지 파일은 이후 단계에서 기존 명세로 다룬다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:intent-capture:b3ffe45f22d13ca279a4b7dce563da979de552749615c9396936e582007c41f5 -->
- 검토가 근거 없는 서술을 지적하면, 내용이 실제로 틀린 것인지 근거만 없는 것인지 먼저 구분한다. 근거만 없다면 그 서술을 문서에서 지우지 말고 후속 질문으로 사용자에게 확정을 받아 근거를 만든다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:intent-capture:e07a58c02f333fc00acf1ecc97ef811be009aa0e9e21ff62e13a407dcbbbdfe8 -->
- 사용자가 이미 확정된 결정을 바꾸겠다고 하면 그대로 반영하지 말고, 그 변경이 건드리는 다른 확정 항목을 먼저 열거해 함께 확인한 뒤 반영한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:intent-capture:5c05ae8fe22ee1915ad37ef3689eaa0b6c7bb19fa6c862444251e6577eca041f -->
- 질문을 만들 때 앞 단계가 이미 닫은 영역은 다시 묻지 말고, 기존 명세에 "확인 필요"로 남아 있는 가정과 아직 열려 있는 분기에만 질문을 집중한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:feasibility:fe09dad16c4617c5dbe114526b5ba7414c4913445c89dd7b989a2d1008e6da5c -->
- 건너뛴 단계 때문에 없는 입력은 결손이 아니라 범위 밖이므로, 산출물의 출처 절에 그 부재와 이유를 적어 하위 단계가 누락으로 오해하지 않게 한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:feasibility:a470ec8ffede10fdb1b2ec857f4558e1d7929cf23a05c0004cada442eee2836c -->
- 답변이 이미 확정된 항목을 뒤집으면 바로 반영하지 말고, 그 변경이 무효화하는 확정 항목을 표로 열거한 뒤 후속 질문으로 함께 확인받고 반영한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:feasibility:76cfc2e3be2761d5388d3c819e2d4dcdef7f010e7f9d0247fb4aa1b98096da88 -->
- 규제·컴플라이언스 항목을 이번 범위에서 다루지 않기로 한 결정은 이미 확정된 제품 기능의 범위를 줄이는 결정이 아니다. 두 가지를 구분해 기록하고, 해석이 갈릴 수 있으면 통합 요약 확인 단계에서 다시 확인받는다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:feasibility:8c24ecda01556110b0c064a33326770882c7a602cd4364c3e9ad1064e3e1e7c5 -->
- 답변 도중 어느 단계도 묻지 않는 값(건너뛴 단계가 담당했을 값)이 드러나면, 나중으로 미루지 말고 그 자리에서 후속 질문으로 확정한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:feasibility:3787daab1469a83e14ec1fb2136caae14afb9e0f8cd7a49b27bccc409ff525eb -->
- 어떤 결정이 기존 확정 항목을 무효화하면, 무효화된 항목 목록을 판정 근거이자 후속 재작성 작업 목록으로 쓸 수 있게 한 표에 모으고 다른 문서는 그 표를 가리키게 한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:feasibility:f35561ffbd1195114d07ade9edac9afafeab6d6646709d5152d4b73422bf05b1 -->
- 기능 목록이 이미 확정된 단계에서는 무엇을 만드느냐를 다시 묻지 말고, 확정된 목록 안에서 무엇을 먼저 만들고 무엇을 뒤로 미루는가만 묻는다. 다시 묻지 않는 항목을 질문 파일 서두에 열거해 중복 질문으로 오해받지 않게 한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:scope-definition:824ed753805612234be224276e2508da6c51c25606b37a9333845846c1e59b77 -->
- 우선순위를 물을 때는 확정된 성공 기준이 열거한 단계들과 기능 목록을 대조해, 성공 기준의 경로 밖에 있는 기능을 먼저 찾아낸다. 그 기능이 우선순위 논의의 첫 경계선이 된다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:scope-definition:658a9efaf1f61d147e82acb49b28a99116452e74cd3593080c7898bcbd8dbeab -->
- 화면 단위 우선순위와 기능 단위 우선순위를 함께 정할 때는 한 화면이 등급이 다른 기능을 동시에 담고 있는지 교차 검토한다. 필수 기능을 켜는 유일한 화면이 후순위로 내려가면 그 기능은 쓸 수 없게 된다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:scope-definition:16911180eb53dfa42ad343568c7ac067a309f32334c2e1099c930518f10a6e7c -->
- 프레임워크의 권고 수치를 넘겨야 할 근거가 있으면 수치를 맞추려고 내용을 줄이지 말고, 초과했다는 사실과 그 이유를 산출물에 의도된 것으로 명시한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:scope-definition:e83cc640f9c96a0805b62c9504472b55a2da48102bdd5e9b846ec163db720d49 -->
- 이미 확정된 결정의 우선순위를 후순위로 내릴 때는 그 결정이 취소된 것이 아니라 만드는 시점만 뒤로 갔다는 문장을 산출물에 함께 적는다. 그렇지 않으면 하위 단계가 확정 취소로 읽는다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:scope-definition:3d790e6cc838d9b3fddac6dc359dd0cba439a192b5be058740ea1b825599c3eb -->
- 질문은 실제로 열려 있는 미결 사항으로만 구성한다. 앞 단계가 닫았거나 건너뛴 단계에 속한 질문은 빼고, 그 결과 질문 수가 깊이 권고의 하한에 못 미쳐도 없는 질문을 만들어 채우지 않는다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:approval-handoff:d4ad7eb8b425331700e97be46b80310cc02e2d564560da88a866f2cdb7a931c5 -->
- 건너뛴 단계가 있으면 그 단계가 담당하던 일을 어느 단계도 맡지 않은 채 남아 있는지 단계 지침과 대조해 확인한다. 공백이 있으면 담당 단계를 지정하거나 건너뛴 단계를 다시 넣는다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:approval-handoff:3b007304d3b78b44b668fc9cfacdc7b833d67b416796700ffc2d1ed1d18bc754 -->
- 워크플로 단계를 추가하거나 빼는 계획 변경은 단계 승인 게이트에 옵션으로 얹지 말고 별도의 승인 절차로 먼저 처리한다. 계획이 확정된 뒤에 산출물을 써야 산출물이 실제 계획을 정확히 서술한다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:approval-handoff:df80063a7f476b95de04bad7c43aaf2d9b59916e0b200ea303b8769183298d4d -->
- 기존 문서의 일부를 사본으로 옮겨 적을 때는 어느 쪽이 기준인지를 사본 머리에 명시한다. 기준을 정해 두지 않으면 두 문서가 어긋났을 때 사본이 혼란을 만든다. (learned 2026-09-16) <!-- cid:260916-scd-coaching-mvp:approval-handoff:b3261be35335ae4d3ff10ef7408f3670719e69cb297c8f53fe3b7b45835a56c8 -->
- 되돌아와 다시 여는 단계에서는 무엇을 고칠지 열린 채로 묻지 말고, 그 단계가 끝난 뒤 하위 단계가 실제로 바꾼 사실을 먼저 대조해 질문을 좁힌다. 대조의 축은 네 가지다: 미확정으로 열어 둔 항목이 닫혔는가, 새 전제가 들어왔는가, 수치를 적은 항목의 수치가 변했는가, 대응 방안이 기대던 수단의 조건이 달라졌는가. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:feasibility:b615517ba2f7c1cc9f26b464d5cdc30674f627ac4d30abbcf4ba33ac36af7ee1 -->
- 새로 추가하는 제약이 기존 제약과 모순으로 읽힐 수 있으면, 충돌하지 않는다는 구분선을 같은 문서 안에 함께 적는다. 구분선을 두지 않으면 하위 단계가 두 항목을 모순으로 읽는다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:feasibility:d7ff915f976b6b01477c23649350d10404b33ccc74c9e936dc39ba3c33c4585d -->
- 무효화되는 확정 항목을 표로 열거할 때, 그중 의존 관계가 깨지는 항목을 따로 짚어 말한다. 필수 항목이 후순위 항목에 의존하게 되는 자리가 사람이 선택을 다시 볼 때 가장 먼저 보아야 할 것이며, 그 자리를 짚지 않으면 의존 문제가 하위 단계까지 내려간다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:scope-definition:492c152684fa0d8188fcbcf38959e24fbdc898f06fd21ef0b346d2a5f2b05ef1 -->
- 답변이 바뀌면 이전 답변을 지우지 않고 "변경됨 → <새 질문 번호>" 표기와 함께 질문 파일에 남긴다. 무엇이 왜 바뀌었는지가 파일 안에서 읽혀야 하위 단계가 최종 답만 보고 맥락을 잃지 않는다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:scope-definition:3bd9a85767f031aba8ea2c5cced4475ce4c67b0ddfc4cceb340dc562fb494fca -->
- 되돌려 다시 여는 단계에서는 그 단계가 실제로 소유한 결정만 다시 묻고, 앞 단계의 결과를 모아 적는 부분은 묻지 말고 기계적으로 갱신한다. 소유한 결정이라도 그 판단의 근거가 실제로 달라졌을 때만 다시 묻되, 물을 때는 유리해진 변경과 불리해진 변경을 함께 대조해 보여 준다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:approval-handoff:2070e481a974188b569ea6539c8d0d2888df284ec2a94f76f5c5fa258e816b34 -->
- 앞 단계 산출물이 바뀌면 단계 경계 검증을 부분 갱신이 아니라 재실행으로 다루고, 재실행 사유와 이전 검증 시점을 문서 머리에 함께 적는다. 그래야 두 검증 결과가 언제 것인지 나중에 구분된다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:approval-handoff:b02d27d8af47709b7b4279d099af361fbcce71be123c0b82a4b46c4accf92568 -->
- 검토자의 반대 의견을 사람에게 올릴 것과 통합 단계에서 고칠 것으로 나눈다. 사실관계 오류, 누락 보완, 강제 수단 제안은 리드가 반영할 내용이므로 올리지 않고, 사람의 판단이 필요한 것만 인터뷰 질문으로 만든다. 올리지 않기로 한 의견과 그 이유는 근거 문서에 표로 남긴다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:practices-discovery:387b04373acf676f4599906316b2ae1638c44577087603a5c70fcd3fdfb48a32 -->
- 단계 지침이 질문 문장을 그대로 지정하더라도, 앞 단계가 이미 닫은 영역이면 그 문장을 그대로 묻지 않는다. 영역은 덮되 아직 열려 있는 부분만 묻도록 질문을 바꿔 쓴다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:practices-discovery:c52d069d6cc2a399187664e11567d9ca1e43e195da6ae20423dac3888eb7b05d -->

- 요구사항 단계의 질문은 앞 단계가 이 단계로 넘긴 가정과, 확정된 기능·화면을 요구사항 문장으로 옮기다 드러난 미정 동작 두 갈래로만 구성한다. 이미 닫힌 영역은 묻지 않고 질문 파일 서두에 결정 ID 와 함께 열거한다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:requirements-analysis:4339e221c4136edfd1636f02a384d61e44edc583c0519249a77b64be2acfa08b -->

- 통합 요약 확인이 끝난 뒤 산출물을 쓰다가 빈자리를 발견하면 질문 파일을 다시 열지 않는다. 산출물의 열린 질문에 담당 단계를 지정해 적고, 승인 게이트에서 사용자에게 그 자리를 짚어 지금 정할지 고를 수 있게 한다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:requirements-analysis:6ee86a5c4ee8ce6042a9739f42b843211d728a8a17cad69ff4d9f9bdd5f2d8dc -->

- 요약 확인 뒤에 드러난 빈자리라도, 전문가 검토가 낸 판단 문제가 Must 흐름의 수용 기준을 쓸 수 없게 만든다면 열린 질문으로 넘기지 않고 그 자리에서 사람에게 묻는다. 열린 질문으로 넘기는 것은 Must 흐름을 막지 않는 빈자리에만 쓴다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:user-stories:6c8b90608f029319dc0eaff800115a2dae7beddc9a02f2202f3a63a991cece02 -->

- 요약 확인 뒤에 질문을 더할 때는 질문 파일의 H2 를 FU 가 아니라 다음 Q 번호로 붙이고, 확인된 요약을 갱신해 다시 확인받은 뒤에 산출물을 쓴다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:user-stories:37e1c7a9106a984565ba3e1f7e2f774ac7d8b164fc52dae46e592b0617223de7 -->

- 몹 검토에서 전문가 의견끼리 부딪히지 않고 모두 지식 문제로 리드가 받아들일 수 있으면 2라운드를 돌리지 않는다. 반영한 내역과 사람에게 올리지 않은 이유는 평가 문서에 표로 남긴다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:user-stories:231c7ffcdc2eebc71bbecbbd4ef5aa7ce6d59c6f21e9c6f12a49961b7aff2630 -->

- 작업 단위를 나누는 기준과 병렬 갈래 수를 물을 때는 단위 사이 의존을 구현 완료로 볼지 계약 합의로 볼지도 같은 회차에 함께 묻는다. 기능 단위에 구현 완료 의존을 두면 흐름이 한 줄이 되어 정한 병렬 수를 채울 수 없게 되고, 이 충돌은 두 답을 모두 받은 뒤에야 드러난다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:units-generation:35091886e65af5481fece0de505655144e6cb3cf6b8eedb38d42407c1d111abf -->

- 작업 단위 의존 문서의 yaml 간선 블록에는 단위 이름을 짧은 이름이 아니라 construction 디렉터리 이름(u1-backend-foundation 형태)으로 쓴다. Construction 단계들이 단위를 디렉터리 이름으로 가리키므로 둘이 달라지면 연결이 깨진다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:units-generation:427bd96690c976348b19fdaefe860ca91dae9ece62d53153a97a44a46abd4744 -->

- 단위 사이 의존을 계약 기준으로 정했으면, 여러 단위가 통합되어야 통과하는 수용 기준(종단 리허설 등)을 이유로 확정 결정을 넘어서는 간선을 더하지 않는다. 그 조건은 필요한 단위를 수용 기준에서 직접 확인해 적은 열린 질문으로 만들고 담당 단계를 지정해 넘긴다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:units-generation:59c1e6074bb4a4198a5b4614336004ac8dbad029ec82027b22d7457a9c819819 -->

- 테이블을 만드는 사람, 그 테이블에 시드를 넣는 사람, 외래 키가 만드는 순서처럼 서로 묶인 결정은 따로 묻지 않는다. 한 질문 안에서 선택지마다 조합의 결과(어떤 확정 결정이 유지되거나 깨지는지)를 보여 주고 묻는다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:contract-design:b337ea5ada7a873fb4cccdbe92d18129f0f332ea14398a8307c018bc699dd8d8 -->

- 응답 방식을 바꾸는 답이 확정된 시간 기준 요구사항의 측정 대상을 바꾸면, 요구사항 문서는 고치지 않고 그 단계 산출물에 보완 기준을 적으며 두 문서가 어긋나 보이면 산출물의 그 문단이 기준이라고 명시한다. (learned 2026-09-17) <!-- cid:260916-scd-coaching-mvp:contract-design:03ce74c2b46c02dc06ebe2a430d1cca4ed80f20b2e2fd50c1edd3d104a8ce470 -->

- 팀 구성 단계가 범위 밖이어서 팀 구성표가 없으면 Bolt 를 사람 이름이 아니라 동시 진행 갈래에만 배정하고, 누가 어느 갈래를 맡는지는 그 Bolt 를 시작할 때 정해 결정 기록에 남긴다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:delivery-planning:a5da80a6d48283abcbd0d17c1e42c1cf83c85b5eab37dc3f8afccba9c1430857 -->

- Bolt 순서는 의존 관계의 위상 정렬을 그대로 쓰지 않고 시연 필수선의 흐름 순서로 잡는다. 의존 관계가 허용하는 경로 안에서 고르되, 위상 순서에서 벗어난 자리는 순서 근거 문서에 따로 적는다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:delivery-planning:d3e083fe654c25194bfd9fe56e08923b9f06a05177a0b17c73fb82c4a41f4a67 -->

- 요약 확인이 끝나고 산출물을 쓴 뒤에 그 단계의 남은 질문에 답이 나오면, 산출물을 다시 쓰지 않고 해당 절에만 덧붙여 갱신한다. 앞 절의 확정된 내용은 그대로 둔다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:delivery-planning:bcf680ba63d538ccdd609c88fc597b8457d3473be37c2302bf789596d93c989b -->

- 기반 단위가 다른 단위 소유의 테이블까지 한 리비전으로 만들 때는, 소유하지 않는 테이블마다 "이번에 적는 것 / 소유 단위에 남기는 것"을 경계표로 등록한다. 상위 문서가 글로 확정한 것만 적고, 정해지지 않은 타입·제약·허용값은 추측해 적지 않는다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:functional-design:96a5045dc806ab7dcbe88055d231e571dcd637181cf378960cbe25ffa5558dff -->

- 대화의 전사 상태와 분석 상태는 컬럼 하나로 합치지 않고 두 값으로 나눠 둔다. 재분석이 전사 완료 정보를 덮어쓰지 않아 재분석 중에도 화면이 전사를 계속 보여 줄 수 있다. 대신 말이 되지 않는 조합을 막는 규칙을 함께 둔다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:functional-design:fe6bd45ee6e514352daea99f2300aabf6f642c0566aa89b8592c18c6cf888d5d -->

- 설치된 실행 파일이 "알 수 없는 명령"으로 실패해도 그것만으로 기능이 지원되지 않는다고 판단하지 않는다. 저장소가 함께 들여온 도구에 그 명령이 있는지, 버전 기록이 무엇인지, 대체 호출 경로가 되는지를 먼저 확인한다. 버전 번호가 같아도 실행 파일이 뒤처진 빌드일 수 있다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:functional-design:07fb555911f8c228ffa6f5dfc240f5bd6634f5d9928a74e15c1d1a0b341a8f2c -->

- 도구가 실패했을 때, 위 확인을 마치기 전에는 사용자가 이미 확정한 결정을 되돌리자고 제안하지 않는다. 확인 비용은 명령 몇 줄이고, 제안의 비용은 이미 내린 결정 하나다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:functional-design:50eec866a392757a96d1d1729d599d7c8198d1ac6df07e1c02f0447652b2c71c -->

- 단계 질문을 만들기 전에 상위 산출물의 열린 질문 표에서 이 단계가 담당으로 지정된 항목을 먼저 찾아 질문에 넣는다. 그러지 않으면 배정받은 질문을 닫지 않고 다음 단계로 재위임하게 되고, 그 사실은 검토에 가서야 드러난다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:nfr-requirements:1571a5eebbc49e5c7a935296984681b5d1e6e8cb20d8b98eaa8a8353645f1137 -->

- 상위 항목의 글자 그대로의 범위보다 넓은 하위 요구사항을 그 밑에 번호로 붙일 때는, 넓혔다는 사실과 각 항목의 실제 출처를 같은 문서에 구분선으로 적고 추적 파일에도 같은 사실을 적는다. 구분선이 없으면 다음 단계가 커버리지를 잘못 판단한다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:nfr-requirements:cdb0cf609efc80fa0f0c0c7b0e6db2a8f77e515dce32c1bd55afa4bfb6c5f45c -->

- 요구사항이 무엇을 지킬지 정했으면 설계 문서는 그것을 어느 구조가 지키게 하는지를 쓴다. 각 장치마다 무엇을 구조적으로 불가능하게 하는지를 표로 적고, 사람의 주의력에만 남는 규칙은 검사나 구조로 바꿀 방법을 함께 적는다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:nfr-design:535d597a85f3533e361bbe06424ce9ede6ad0a1c0bcf126a7d24f1010d48e885 -->

- 어떤 장치를 이번 범위에 두지 않기로 하면 근거만 적지 말고 나중에 필요해졌을 때 어디에 붙이는지를 함께 적는다. 그 자리가 한 곳으로 모여 있지 않으면 그것 자체가 지금 구조를 다시 볼 신호다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:nfr-design:90d02d54e62b5d8fe5d6856dce7c1b320814e5799dd0eee9a310bcff9b648d2a -->

- 함께 보는 전문 지식이 이 프로젝트의 전제와 맞지 않으면 억지로 대응시키지 않는다. 적용되는 부분만 옮기고, 적용되지 않는다는 사실과 그 이유를 산출물 머리에 밝혀 다음 단계가 누락으로 읽지 않게 한다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:nfr-design:71252def5e3164ac96a42b9a7c3ff5345182c81ac07b474e920e0f2d6021d164 -->

- 추적 파일의 상위 항목 목록에는 이 단계가 답한 항목뿐 아니라 산출물 본문이 근거로 인용한 항목도 모두 넣는다. 본문이 인용했는데 추적에 없으면 다음 단계가 커버리지를 잘못 판단하고, 이 누락은 검토에 가서야 드러난다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:infrastructure-design:96af1efce048082a2cb339a55645cf55f0b94f57fb52f4e3da9ada46fe2af621 -->

- 검토자에게 검증 도구를 돌리게 할 때는 실행 흔적이 작업 공간에 남지 않는 형태로 명령을 준다. 파이썬이면 바이트코드 생성을 끄고 캐시 제공자를 비활성화하며 커버리지 파일을 남기지 않는다. 그런 파일은 무시 규칙에 들어 있어도 소스 지문 계산에는 포함되므로, 검토자가 성실히 검증할수록 판정이 기록되지 못하는 상태가 된다. 검토를 요청하기 전에 기존 캐시도 함께 지운다. (learned 2026-09-18) <!-- cid:260916-scd-coaching-mvp:code-generation:75b431cc5d5398ac63bb203e0b8a176bd9f28528a263b90299b5d76e000b9388 -->

## Forbidden
- NEVER add any H2 heading other than `Q<n>`, `Requested Changes Feedback`, or a
  single `Assumption Confirmation` after the consolidated summary in a
  `<stage>-questions.md` file. Revision history, round logs, or tracking notes
  belong in the stage's `memory.md`, never in the questions file.
  (This blocked practices-discovery four times; ERROR_LOGGED shows the same
  failure earlier in intent-capture and feasibility.)
