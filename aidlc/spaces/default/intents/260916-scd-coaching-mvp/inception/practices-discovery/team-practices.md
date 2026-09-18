# Team Practices — SCD 소통 코칭 MVP

우리 팀이 이 프로젝트에서 따르는 관행이다. 여기 적힌 것은 인터뷰와 확인 게이트를 거쳐
확정된 사실이며, 제안이 아니다. 근거 태그의 뜻과 각 결정의 대안 검토, 남은 미결 사항은
`evidence.md` 에 있다.

## Way of Working

원격 저장소(GitHub 등)를 쓰고 **PR 로 병합한다**. 병합 전 검사는 **GitHub Actions** 가
강제한다 `[Q1]`. Actions 워크플로와 품질 게이트 자체는 ci-pipeline(3.7)이 만든다 —
이 단계를 계획에 다시 넣었다 `[FU3]`.

- **저장소 준비 순서가 곧 규칙이다: ignore 규칙 추가 → `git init` → 첫 `git add`**
  `[devsecops §1]`. "Construction 시작 전에"가 아니라 "첫 `git add` 전에"다. 한 번 커밋에
  들어간 키는 `.gitignore` 로 지워지지 않고, 5인이 clone 한 뒤에 이력을 다시 쓰는 비용은
  훨씬 크다.
- `.gitignore` 는 **이미 존재한다**(저장소 루트, 85줄). 다만 내용이 전부
  `# BEGIN AI-DLC:gitignore` / `# END AI-DLC:gitignore` 마커로 감싼 **프레임워크 소유
  블록**이고, 팀에 필요한 항목은 `node_modules` 를 빼면 하나도 들어 있지 않다. 지금 상태로
  `git init && git add -A` 를 하면 그 시점에 디스크에 있는 `.env` 가 첫 커밋에 들어간다
  `[devsecops §1]`.
- 팀 항목은 반드시 `# END AI-DLC:gitignore` **아래**에 별도 구역으로 넣는다. 마커 안에
  넣으면 프레임워크가 블록을 다시 쓸 때 조용히 사라진다. 첫 커밋 전에 들어가야 하는 최소
  항목: `.env`, `.env.*`(단 `!.env.example`), `__pycache__/`, `*.py[cod]`, `.venv/`,
  `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `.coverage`, `htmlcov/`, 업로드 음성
  저장 경로(예: `storage/audio/`), `*.webm` `[devsecops §1]`.
- 우리는 **trunk-based** 로 일한다. worktree base 는 `main`, merge target 도 `main`,
  Bolt 하나당 squash-merge 한 커밋이다. 5인 전원이 풀스택이고 작업 단위별로 그때그때
  나누며 `[constraint:OC-03]`, 남은 기간이 약 7주뿐이라 `[constraint:OC-01]` 오래 사는
  브랜치의 병합 부채를 감당할 여유가 없다.
- 브랜치 이름은 Bolt slug 를 그대로 쓴다. 커밋 메시지 한 줄 요약은 한국어로 쓴다
  `[constraint:OC-06]`.
- 병합 전 확인은 그 작업 단위를 만들지 않은 사람 1인의 리뷰로 한다. 고정 역할이 없으므로
  `[constraint:OC-03]` 리뷰어도 고정하지 않는다. **리뷰의 필수 확인 항목은 하나다 — 해당
  PR 의 GitHub Actions 검사가 통과했는가** `[quality §8][Q1]`. 주장이 아니라 확인 가능한
  사실이다.
- **의존성을 새로 추가하는 커밋은 리뷰어가 새 패키지 이름 각각을 공식 문서와 PyPI·npm
  페이지에서 확인한다** `[devsecops §6]`. 전원이 AI 보조로 작업하고 Python 경험이 일부뿐인
  조합에서 `[constraint:OC-04][raid:R1]` 가장 흔한 공급망 실패는 알려진 CVE 가 아니라
  존재하지 않는 패키지 이름을 제안받아 설치하는 것이다. 비용은 이름당 30초다.
- 의존성 잠금 파일(`uv.lock`, `package-lock.json`)을 **커밋하고**, 설치는 잠금에서만 한다
  (`uv sync --frozen`, `npm ci`). 새 의존성은 매니페스트와 잠금이 **같은 커밋에 함께**
  들어가게 추가한다 `[devsecops §6]`. 잠금이 커밋되지 않으면 5인 재현성이라는 uv 채택
  이유가 사라진다.
- 모든 질문과 승인은 `docs/decisions/decision-log.md` 에 남긴다 `[constraint:OC-05]`.


**이 절의 근거 결정: D-55, D-56** (`decision-log.md` §5-2) `[log §5-2][FU4]`. D-55 는 원격
저장소(GitHub 등)를 쓰고 PR 로 병합하며 병합 전 검사를 GitHub Actions 가 강제한다는 것
(제약 TC-16), 그리고 저장소 생성 전에 `.gitignore` 를 먼저 고친다는 것이다. 위 워크플로
자체를 만드는 단계는 D-56 — ci-pipeline(3.7)을 계획에 다시 넣어 EXECUTE 단계가 20 → 21 이
되었고, Actions 워크플로와 품질 게이트는 그 단계가 만든다.

## Walking Skeleton

활성 스코프가 `skeleton: on` 이므로 첫 Bolt 는 얇은 종단 슬라이스이고, 혼자 돌리며,
나머지 Bolt 로 넘어가기 전에 사용자 승인을 받는다 `[scope]`.

- **스켈레톤은 실제 첫 기능(PU-01 업로드)으로 종단을 관통한다. 임시 엔드포인트를 쓰지
  않는다** `[Q2]`.
- 관통 경로: React 화면 1개 → FastAPI 엔드포인트 1개 → `service` → `repository` →
  PostgreSQL 테이블 1개 → Mock provider 1회 호출 → 다시 화면 표시. 전부 Docker Compose
  3 컨테이너(frontend, backend, postgres) 안에서 돈다 `[constraint:TC-04]`. 한 조각이라도
  빼면 스켈레톤이 막으려는 위험을 못 막는다.
- 목적은 기능을 만드는 것이 아니다. 팀 배경은 React+Java 인데 백엔드가 Python 으로
  확정되었고 Python 경험은 일부뿐이다 `[constraint:OC-04][raid:R1]`. 아무도 익숙하지 않은
  조립 지점 — FastAPI 의존성 주입, ORM 세션 수명, Alembic 마이그레이션 적용 시점, 컨테이너
  간 연결 — 을 7주 중 첫 주에 한 번 관통시켜, 나머지 Bolt 들이 같은 자리에서 반복해
  넘어지지 않게 하는 것이다.
- **가정 A1 확인을 첫 Bolt 안에서 함께 한다** `[Q2]`. `localhost` 가 보안 컨텍스트로
  취급되어 HTTPS 없이 MediaRecorder 녹음이 동작하는지를 실제로 한 번 돌려 본다
  `[raid:A1]`. 이 가정이 틀리면 로컬 개발용 인증서 작업이 통째로 추가되는데, 그건 늦게
  알수록 비싸다.
- 합성 대화 S1 의 종단 Playwright 테스트를 이 Bolt 의 인수 테스트로 만들고, 그때부터 계속
  초록으로 유지한다 `[quality §7]`.
- Bolt 1 이 끝나면 나머지 Bolt 를 어떻게 돌릴지(자율 진행 / 매 Bolt 승인)를 묻는다. 그
  선택은 `aidlc-state.md` 의 `Construction Autonomy Mode` 로 남는다 `[org]`.


**이 절에는 이번 회차에 새로 붙는 결정 ID 가 없다** `[FU4]`. 걷는 뼈대의 내용은 인터뷰
답변 `[Q2]` 에서 확정되었고 `decision-log.md` §5-2 가 별도 결정 ID 를 발급하지 않았다
`[log §5-2]`. 다른 네 절과 달리 근거 결정 줄이 없는 이유가 이것이며, 근거가 빠진 것이
아니다 — 되짚을 자리는 `[Q2]` 와 `evidence.md` 의 "인터뷰가 확정한 것" 이다.

## Testing Posture

- **Methodology**: test-after
- **Ordering**: 모든 계층(`api`, `service`, `repository`, `providers`, frontend)을 구현한
  뒤 그 계층의 테스트를 쓰고 실행한다. 어느 계층도 테스트를 먼저 쓰지 않는다 `[Q3]`.

방법론을 하나로 둔 이유는 헷갈리지 않기 위해서다 `[Q3]`. 초안이 제안했던 `custom`(규칙
모듈만 테스트 선행)은 채택되지 않았다.

- **기대 판정은 픽스처 파일로 고정한다** `[FU2]`. 테스트 시점은 위 `Ordering` 그대로지만,
  `docs/input/05_synthetic-test-data.md` 의 기대 판정을 기계가 읽는 픽스처 파일 한 벌로
  두고, 판정 관련 단위 테스트가 그 파일을 읽는다. **기대값을 테스트 코드에 직접 적지
  않는다.** 이 의무는 위 `Methodology` / `Ordering` 두 줄을 대체하지 않는다.
- 픽스처는 **단일 출처**다. Mock provider, backend 단위 테스트, frontend MSW 핸들러,
  Playwright 단언이 전부 같은 한 벌을 읽는다 `[quality §9(a)]`. 사람이 같은 표를 두 번
  적는 자리를 0 으로 만든다 — 손으로 옮긴 사본은 반드시 어긋나고, 어긋나도 각자 초록이라
  아무도 모른다. 위치는 `backend/app/fixtures/` 로 두되 `[spec:02 §6]`, Mock 이 런타임에
  반환하는 고정 응답(시연 경로의 일부다 `[constraint:SC-04]`)과 테스트 기대값을 같은 벌로
  다룬다는 점을 파일 머리에 적어 둔다.
- **Test Strategy 는 Standard** 다. 구성 요소마다 5–8개, 단위 테스트와 주요 경계의 통합
  테스트를 쓴다 `[state][spec:02 §3]`.
- 도구는 `docs/input/02_tech-environment.md` §3 에서 이미 정해졌다. backend 단위는 pytest,
  backend API 는 pytest + httpx TestClient, DB 연동은 Testcontainers(PostgreSQL), frontend
  는 Vitest + React Testing Library + MSW, E2E 는 Playwright 로 합성 대화 3건을 돌린다.
- **커버리지 바닥은 `backend/app/service/` 전체의 라인 커버리지 80% 하나다** `[Q4]`.
  저장소 전체 바닥은 없고, 분기 커버리지 바닥도 두지 않는다. 활성 스코프
  `scd-coach-mvp` 는 `org.md` 가 80% 바닥을 주는 목록에 없으므로 이건 무언가를 좁힌 것이
  아니라 **없던 자리에 바닥을 새로 세운 것**이다 `[quality §3(c)]`. 이 선택이 판정
  정확성에 남기는 위험은 `evidence.md` 에 기록했다.
- **병합 전 강제 수단은 GitHub Actions** 다 `[Q1][FU3]`. 로컬 `scripts/check.sh` 는
  개발자 편의 수단으로 남길 수 있으나 게이트가 아니다. 워크플로 안에서 기계적으로 검증하는
  지점은 하나 더 있다 — `build-and-test`(3.6)는 EXECUTE 이고, 정의된 커버리지 바닥과 확정
  품질 목표를 검증한다 `[quality §8][state]`. 통과시키려고 목표를 낮추는 것은 `org.md` 가
  금지한다.
- `scripts/check.sh` 를 두는 경우 **컨테이너 안에서 돌린다**(`docker compose run --rm
  backend ...`) `[devsecops §2][quality §8]`. 5인의 로컬 Python·Node 버전이 제각각인데
  호스트에서 돌리면 "내 자리에선 통과했다"가 분쟁이 된다. 빠른 것과 느린 것을 나눈다 —
  `check.sh` = ruff + mypy + `pytest -m "not integration and not e2e"` + vitest(목표 2분
  이내), `check-full.sh` = 여기에 Testcontainers 통합 + Playwright.
- pytest 마커 `integration`, `e2e` 를 **지금** 정한다 `[quality §9(b)]`. 나중에 정하면
  전부 한 덩어리가 되어 있고 되돌리는 비용이 크다.
- 수용 기준 추적은 이름이 아니라 마커로 단다: `@pytest.mark.ac("AC1.3.2")`
  `[quality §9(f)]`. user-stories(2.4)가 만들 수용 기준 ID 를 `build-and-test`(3.6)가
  기계적으로 대조할 수 있게 된다.
- **Testcontainers 격리 규약** `[quality §9(c)]`: 컨테이너는 세션당 1개, 스키마는 세션
  시작 시 `alembic upgrade head` 로 한 번 만든다(`Base.metadata.create_all()` 을 쓰지
  않는다 — 그래야 마이그레이션이 실제로 한 번은 실행된다 `[developer §2.3]`), 테스트마다
  트랜잭션 후 롤백으로 격리한다. 테스트 독립성은 타협 대상이 아니다.
- 어떤 구현이 와도 통과하는 테스트(`assert True` 류)는 쓰지 않는다. 테스트는 행복 경로와
  최소 2개의 오류·경계 경우를 덮는다 `[phase:construction]`.
- **Mock 픽스처 대조 테스트를 둔다** `[quality §4]`. `MockLlmProvider` 가 각
  `conversationKey` 에 대해 픽스처와 정확히 같은 `group / opportunity / result /
  holdReason / evidence` 를 반환하는지 검증한다. 이게 없으면 Mock 픽스처가 기대 판정표에서
  한 칸 어긋났을 때 SM1 도 E2E 도 단위 테스트도 전부 초록인 채로 전 구간이 일관되게
  거짓말한다.
- **프롬프트 빌더 단위 테스트를 둔다** `[quality §4][devsecops §4]`. TC-08 은 Mock 경로에서
  살아남는 유일한 보안 속성인데, Mock 은 전사를 읽지 않으므로 SM1 통과가 이 속성을 전혀
  증명하지 않는다. LLM 없이 지금 쓸 수 있는 테스트 2건: (a) 전사에 주입 문구가 들어간 경우
  렌더 결과에서 그 문장이 데이터 블록 **안**에 있고 지시문 영역이 하나뿐임을 단언한다,
  (b) 전사에 구분자 문자열 자체가 들어간 경우 렌더 결과에 구분자가 여는 것/닫는 것 각 1회만
  남거나 이스케이프된 형태로만 남는다.
- frontend 에는 수치 바닥을 걸지 않는다. 빠뜨린 것이 아니라 뺀 것이고, 대신 비수치 의무를
  하나 둔다 — SM1 경로의 A/B/C 화면은 정상 표시가 아니라 **빈·부족·보류 상태**에 최소
  1개의 RTL 테스트를 둔다 `[quality §3(d)]`. `05_synthetic-test-data.md` 가 직접 요구하는
  것들이다: S2 의 "어려움 장면 0개일 때 화면이 비지 않고 잘한 장면만 표시", S3 의 보류
  표시, C1 의 "아직 비교하기엔 기록이 부족해요". Mock 행복 경로 E2E 가 절대 못 잡는다.
- **Playwright 주기와 범위** `[quality §7]`: 빠른 루프(병합 전)는 S1 만, 3건 전체는 Bolt
  완료 시점과 주 1회 고정 시각, 태그·리허설 전에는 반드시 전체. E2E 개수는 3건에서 늘리지
  않는다 — 새 동작은 통합·단위로 내린다. S2 는 보류 표시와 목적 완료 판정이 들어오는
  Bolt 에, S3 는 보류 사유가 들어오는 Bolt 에 붙인다. **S3 의 검증 항목 2·4(전사 정정 후
  재검토 표시, 삭제 시 연결 항목 처리)는 F07 이 Must 로 올라가면서 이번 범위 안에 들어왔다**
  `[Q7][FU1]`.
- `live` 경로는 인터페이스 준수 계약 테스트만 두고, **네트워크를 타는 테스트는 기본
  실행에서 제외한다** `[quality §9(g)]`. 제공자가 미정인 동안 `[raid:D2]` 누군가 API 키가
  필요한 테스트를 쓰면 기본 스위트가 실행 불가능해진다.
- 결함은 고치기 전에 **재현 테스트를 먼저 쓴다** `[quality §9(e)]`. 이슈 트래커가 없으므로
  기록 자리는 `docs/decisions/decision-log.md` 다 `[constraint:OC-05]`.

**규칙마다 강제 테스트** — `discovered-rules.md` 의 항목 중 무엇이 테스트로 지켜지는지를
여기에 고정한다 `[quality §5]`. 테스트 없는 규칙은 7주 안에 조용히 썩는다.

| 규칙 | 강제하는 테스트 |
|---|---|
| TC-08 전사는 데이터 블록으로만 | 프롬프트 빌더 단위 테스트 2건 |
| TC-10 모델명·프롬프트 버전·기준 버전 저장 | 판정 저장 후 세 필드 존재를 단언하는 통합 테스트 |
| TC-13 종합점수·백분위 금지 | 리포트 응답 스키마에 해당 필드가 없음을 단언 |
| TC-14 `api` → `service` → `repository` | `api` 모듈이 `repository` 를 import 하지 않음을 검사하는 테스트 + Ruff `TID251` |
| TC-05 음성 BLOB 금지 | 스키마 검사 |
| SC-04 `ANALYSIS_MODE` fail closed | 미설정·모르는 값에서 mock 으로 뜨고, 키 없는 `live` 에서 기동이 거부되는지 단위 테스트 |
| F07 삭제 전파 | 대화 1건을 만들고 삭제한 뒤 관련 테이블 전부와 파일 경로가 비었는지 확인하는 검사 |
| TC-07 프론트에서 STT·LLM 직접 호출 금지 | 테스트로 잡기 어려움 — 규칙만 |

**운영 파라미터 검증** — `performance-validation`(4.6)이 SKIP 이라 PM-01~PM-04 를 확인할
단계가 계획에 없다. 부하 시험을 하자는 것이 아니라 기존 테스트 안의 단언 한 줄씩이다
`[quality §9(d)]`.

| 항목 | 값 | 어디서 확인 |
|---|---|---|
| PM-01 녹음 최대 길이 | 5분 | 업로드 검증 경계 단위 테스트(4:59 / 5:01) |
| PM-02 Mock 분석 응답 시간 | 3초 이내 | 분석 API 통합 테스트에 경과 시간 단언 추가 |
| PM-03 "비교 불충분" 기준 | 유효 기회 3회 미만 | 경계 단위 테스트 2 / 3 / 4 |
| PM-04 원음 보관 기간 | 30일 | 설정값이 노출되고 기본값이 30일인지만 확인한다. 경과 시간에 따른 만료 삭제 동작은 7주 안에 실측할 수 없으므로 이번 범위에서 검증하지 않는다 |


**이 절의 근거 결정: D-57** (`decision-log.md` §5-2) `[log §5-2][FU4]`. 방법론은
**test-after** 하나, 커버리지 바닥은 `service/` **라인 80%** 하나, 기대 판정은 **픽스처
파일로 고정**하고 단위 테스트가 그것을 읽는다 — 위 세 항목이 그 결정의 세 갈래다.

## Deployment

클라우드 배포가 없고 `[constraint:SC-01]` staging / production 이라는 환경이 존재하지
않으며 Operation 단계(4.1~4.7)가 전부 SKIP 이므로, `org.md` 의 환경 승격 절차는 걸 대상
자체가 없다. 아래가 그 자리를 대신한다.

- 배포 대상은 개발자 각자의 로컬 Docker Compose 3 컨테이너뿐이다. "환경 승격"이라는 개념을
  이번 범위에 두지 않는다.
- **"배포에 성공했다"의 정의** `[Q5]`: `docker compose up --build` 후 backend 헬스체크가
  통과하고, `docs/input/05_synthetic-test-data.md` 의 합성 대화 3건이 업로드 → 전사 확인 →
  리포트 → 목표 선택 → 모의 대화 → 기록까지 **끊김 없이 지나간다**. 명령이 성공적으로 끝난
  것은 배포 성공이 아니다. **기대 판정과의 대조는 종단 실행의 성공 조건이 아니다** —
  판정 정확성은 위 `## Testing Posture` 의 픽스처 기반 단위 테스트가 본다 `[FU2]`.
- 헬스체크 응답에 현재 `ANALYSIS_MODE` 를 포함한다 `[devsecops §7]`. 시연 리허설은 그 값이
  `mock` 임을 **단언**할 수 있어야 한다. 눈으로 확인하는 것에 기대면 시연 당일에는 확인하지
  않게 된다.
- 유일한 릴리스 사건은 2026-11-05 시연이다 `[constraint:OC-01]`. 시연 전에 `main` 을 태그로
  고정하고, 그 태그에서 **새로 clone 한 상태로** 한 번 처음부터 올려 위 성공 정의를
  통과시켜 본다. 각자 노트북에만 남아 있는 설정에 의존하고 있지 않은지는 이 방법으로만
  드러난다. 이때 새 clone 트리에 `.env` 가 **없다**는 것도 함께 확인한다 — 있으면 커밋된
  것이다 `[devsecops §7]`.
- **되돌리기**: `git revert <커밋>` 후 `docker compose up --build`. 스키마가 함께 되돌아가야
  하면 `docker compose down -v` 로 볼륨을 비우고 마이그레이션을 처음부터 다시 적용한 뒤
  시드를 다시 넣는다. 모든 데이터가 합성이라 `[constraint:SC-02]` 이 초기화로 잃는 것이
  없다.
- 마이그레이션은 **Alembic 으로 전진 방향만** 쓴다. `downgrade` 스크립트는 쓰지 않는다 —
  로컬 초기화가 더 싸고, 쓰지 않을 코드에 테스트를 붙이게 되기 때문이다.
- Alembic 운영 규칙 `[developer §2.3]`: `--autogenerate` 결과는 **초안이다**(enum 변경,
  server default, 인덱스 이름 변경을 놓친다). 사람이 읽고 고친 뒤 커밋한다. Bolt 하나당
  마이그레이션 파일 하나, 병합된 마이그레이션은 수정 금지, `down_revision` 이 갈라지면 새
  파일을 만들지 말고 `alembic merge` 를 쓴다.
- **시드 데이터**: Must 경로는 미리 만들어 둔 고정 사용자 하나로 돈다 `[scope]`. 그 고정
  사용자와 합성 대화 3건을 넣는 `scripts/seed.py` 를 저장소에 둔다.
- 비밀값과 API 키는 backend 컨테이너의 환경변수로만 다룬다. `.env` 는 커밋하지 않고
  `.env.example` 만 저장소에 둔다 `[spec:02 §4]`.
- STT·LLM 의 기본 실행 경로는 `ANALYSIS_MODE=mock` 이다 `[constraint:SC-04]`. 설정이
  어긋났을 때의 동작까지 정한다 `[devsecops §5]`: 미설정·빈 값·모르는 값이면 `mock` 으로
  동작한다(절대 `live` 로 흘러가지 않는다). `ANALYSIS_MODE=live` 인데 키 환경변수가 없으면
  **기동을 거부한다** — 조용히 `mock` 으로 되돌아가지도 않고, 첫 사용자 요청에서 터지지도
  않는다. provider factory 가 기동 시점에 확인한다.
- 제공자가 미정인 동안 `[raid:D2]` 아무의 `.env` 에도 실제 키를 넣지 않는다. `live`
  구현체는 만들되 키 없이 둔다. 키가 존재하지 않는 기간에는 유출될 키도 없다
  `[devsecops §5]`.


**이 절의 근거 결정: D-58** (`decision-log.md` §5-2) `[log §5-2][FU4]`. "배포 성공"은
`docker compose up --build` 후 헬스체크 통과 + 합성 대화 3건의 종단 통과이며, 기대 판정
대조는 종단 실행의 성공 조건이 아니다.

## Code Style

**Frontend**

- ESLint + Prettier, TypeScript 5 `strict`, CSS Modules `[spec:02 §6]`. 전역 상태 관리
  라이브러리를 쓰지 않고 TanStack Query + 지역 state 로 간다 `[constraint:TC-12]`.
- **`react/no-danger` 를 `error` 로 켠다** `[devsecops §4(d)]`. 전사 텍스트와 LLM 이 만든
  코칭 문구가 둘 다 화면에 렌더링되는 앱이다. 마크다운처럼 생긴 LLM 출력을 예쁘게 보이려고
  `dangerouslySetInnerHTML` 에 손대는 순간 LLM 출력발 저장형 XSS 가 된다. 이 한 줄이 정확히
  그 벡터만 막고 비용은 0 이다.
- 화면 컴포넌트 이름은 **화면 ID + 영어 역할** 형태로 쓴다(`A1UploadPage.tsx`,
  `B3GoalSelectPage.tsx`) `[developer §5.3]`. UI 명세 화면 ID(A1~A5, B1~B5, C1~C5)와의 대조는
  접두사로 그대로 되고, 파일 이름은 ASCII 로 유지된다. `A1.tsx` 는 import 문과 스택
  트레이스에서 아무 의미가 없다.
- API 호출은 얇은 클라이언트 한 곳을 지나고, 거기서 오류 봉투를 타입 있는 오류로 바꾼다.
  컴포넌트마다 `fetch` 를 부르면 오류 처리가 화면 수만큼 갈린다. `alert()` 로 오류를 띄우지
  않고 화면에 표시 자리를 둔다. TanStack Query 의 재시도 기본값을 그대로 두지 않는다 —
  업로드·전사 같은 비멱등 호출은 재시도를 끈다 `[developer §4.2]`.
- API 타입은 OpenAPI 스키마에서 `openapi-typescript` 로 생성해 커밋하고, 손으로 고치지
  않는다(파일 머리에 생성물 표시). 재생성 후 diff 가 비어 있지 않으면 백엔드 계약과 프론트
  타입이 갈라졌다는 뜻이다 `[developer §2.7]`.

**Backend 도구 (여기서 확정)** `[Q6][constraint:TC-15][raid:D3]`

- **패키지 관리자: uv.** 의존성과 도구 설정(Ruff, mypy, pytest)을 `pyproject.toml` 하나에
  모은다. `uv run` 을 쓰면 가상환경 활성화라는 개념 자체가 사라진다 — Python 이 처음인
  사람이 첫 주에 가장 많이 넘어지는 자리다 `[developer §2.1]`. backend Dockerfile 도 uv 로
  설치하고 uv 버전을 태그로 고정한다. 컨테이너가 `pip install -r requirements.txt` 로 다르게
  설치되면 로컬과 컨테이너가 갈라지고, 그 어긋남은 시연 전날에 드러난다.
- **ORM: SQLAlchemy 2.0 declarative — 동기(sync)로 못박는다** `[developer §2.2]`.
  `Mapped[str]` / `mapped_column()` 선언 스타일은 JPA 엔티티와 읽는 느낌이 거의 같고 mypy 가
  그대로 이해한다. 라우트도 동기 `def` 로 쓴다(FastAPI 가 스레드풀에서 돌리므로 이벤트 루프를
  막지 않는다). 이 프로젝트는 로컬 데모에 사용자 5명이라 동시성 요구가 없고
  `[constraint:SC-01][constraint:OC-01]`, async 로 가면 `await` 전파와 `MissingGreenlet`,
  테스트 픽스처 복잡도가 따라온다. 명세 §7.1 의 예시 자체가 이미 동기 `def` 다.
- SQLAlchemy 관계는 **`lazy="raise"`** 를 기본값으로 둔다 `[developer §1.4]`. ORM 객체가
  API 쪽으로 새면 직렬화 시점에 조용히 N+1 이 되지 않고 즉시 예외로 터진다.
- **마이그레이션: Alembic.** SQLAlchemy 의 짝이라 모델 정의에서 마이그레이션 초안을 뽑아낼
  수 있다. 운영 규칙은 `## Deployment` 에 있다.
- **Ruff 하나로 lint 와 format 을 쓴다.** `org.md` 는 Python 포매터로 Black 을 들고 있는데
  Ruff 의 포매터는 Black 과 같은 결과를 내도록 만들어진 구현이므로, 이건 org 기본을 뒤집은
  것이 아니라 도구 하나로 좁힌 것이다. **규칙 집합을 정하지 않으면 거의 아무 일도 안 한다**
  (Ruff 기본 활성은 `E4`, `E7`, `E9`, `F` 뿐이라 사실상 문법 오류 검출기다)
  `[developer §2.4]`. 출발 집합: **`E`, `F`, `I`, `UP`, `B`, `SIM`, `TID`, `RUF`, `S`**.
  `I`(import 정렬)는 5인 병렬에서 import 순서 차이가 그 자체로 병합 충돌 원인이라 이득이
  가장 크다. `S`(flake8-bandit 이식, 보안)를 넣으면 도구를 늘리지 않고 SAST 를 얻는다 —
  하드코딩된 비밀값 후보(`S105`/`S106`), `subprocess` 호출(`S6xx`), SQL 문자열 조립
  (`S608`)이 잡힌다 `[devsecops §3]`. `tests/` 에는 `S101` per-file-ignore 를 둔다. 줄
  길이는 기본 88 을 그대로 쓴다.
- **mypy 를 켠다. `strict` 는 끄되 검사가 실제로 걸리게 설정한다** `[developer §2.5]`.
  기본 설정의 mypy 는 타입이 없는 함수의 본문을 아예 검사하지 않아서, "붙인다"가 사람의
  선의로만 남고 안 붙인 쪽이 오히려 검사에서 자유로워진다. `pyproject.toml` 에 전역
  `check_untyped_defs = true`, `warn_unused_ignores = true`, 서드파티
  `ignore_missing_imports = true`, `plugins = ["pydantic.mypy"]` 를 두고,
  **`app.service.*` 오버라이드에만 `disallow_untyped_defs = true`** 를 켠다. 이걸로
  "`service/` 공개 함수는 타입 필수"가 문장이 아니라 검사가 된다.
- 지금 목록에 올려 두지 않으면 첫 주에 막히는 의존성 `[developer §2.7]`:
  `python-multipart`(FastAPI multipart 업로드에 필수 — 없으면 업로드 라우트가 기동 시점에
  죽는다), `pydantic-settings`(Pydantic v2 에서 설정 관리가 별도 패키지로 분리되었다),
  `httpx`(이미 테스트 도구로 잡혀 있으니 제공자 HTTP 호출에 같은 것을 쓴다).
- `.env.example` 의 값 자리는 비우거나 `<발급받은-키>` 로 둔다. **실제 키를 닮은 더미
  (`sk-...` 류)를 넣지 않는다** `[devsecops §1]` — 나중에 붙일 어떤 스캐너든 매번 그 줄에서
  걸려 경보가 무시되기 시작한다.

**계층 경계** `[constraint:TC-14][spec:02 §5][raid:R3]`

- `api` → `service` → `repository` 순으로만 내려간다. `api` 가 `repository` 를 직접 부르지
  않는다. 어댑터(`providers`)는 `service` 가 인터페이스로만 참조한다. ORM 모델을 API 응답으로
  그대로 반환하지 않고 Pydantic 응답 모델로 바꾼다.
- **역방향 금지** `[developer §1.3]`: `service` 는 `fastapi` 를 import 하지 않는다(특히
  `HTTPException` 을 `service` 에서 던지지 않는다). `repository` 는 `service` 를 import 하지
  않는다. `providers` 는 `service`·`repository` 를 import 하지 않는다 — 어댑터는 도메인을
  모른다. 이 문장이 없으면 계층은 한 주 만에 섞인다.
- **`SttProvider` / `LlmProvider` 인터페이스(Protocol)는 `providers/` 가 아니라
  `service/ports.py` 에 둔다** `[developer §1.3]`. 인터페이스가 구현체와 같은 패키지에 있으면
  `service` 가 `providers` 를 import 하게 되고, `providers/__init__.py` 를 타고
  `stt_live.py` 가 함께 로드되어 `ANALYSIS_MODE=mock` 인데 live SDK 가 없다고 죽는 실패가
  난다. `[constraint:SC-04]` 가 mock 을 기본 경로로 못박았으므로 가상의 위험이 아니다.
- 계층 규칙은 사람이 아니라 검사가 지킨다 `[developer §1.4]`: 모든 라우트에 `response_model`
  을 선언하고, Ruff `TID251` 로 `app.repository` import 를 전역 금지한 뒤
  `per-file-ignores` 로 `app/service/**`·`app/repository/**`·`tests/**` 만 해제한다. 새 도구가
  0개이고 Python 초심자 부담이 없다.
- **삭제 전파(잠정 규칙 — domain-design(2.6)이 최종 정의를 닫고, 바뀌면 그쪽이 이긴다)**
  `[developer §1.1~1.2]`. 계층 규칙만으로는 R3 이 걱정하던 자리를 막지 못한다 — TC-05 때문에
  저장소가 DB 와 파일 둘이라 "대화 삭제"는 DB 트랜잭션 하나로 끝나지 않는 연산이고,
  `service` 를 경유해도 파일이 디스크에 남으면 F07 은 깨진 것이다. F07 이 Must 로 올라간
  지금 `[Q7][FU1]` 이 규칙은 더 중요해졌다.
  1. **한 애그리거트의 삭제 진입점은 하나다.** 대화/음성/전사/판정/기록에 걸친 삭제는
     `service/privacy/` 의 삭제 유스케이스 한 곳에서만 시작한다. 다른 `service` 모듈은 자기
     소유 테이블의 정리 함수를 노출하고, 삭제 유스케이스가 그것들을 호출한다.
  2. **파일과 행의 순서를 못박는다.** 쓰기는 `DB 행(status=pending)` → `파일 저장` →
     `DB 행(status=ready)`, 삭제는 `파일 삭제` → `DB 행 삭제`. 어느 쪽이 중간에 죽어도
     남는 쪽이 항상 DB 행이 되게 한다 — 삭제 경로가 찾을 수 있는 것은 DB 행뿐이므로 고아는
     반드시 DB 쪽에 생겨야 한다.
  3. **FK 에 `ON DELETE CASCADE` 를 건다** — 애플리케이션 규칙의 대체물이 아니라 그물로.
     파일 저장소에는 그물이 없으므로 1·2 가 여전히 필요하다.

**파일 구조** `[spec:02 §6][developer §5]`

- 계층 우선 구조를 유지하되 그 대가를 규칙으로 상쇄한다: **`api/` 와 `repository/` 도
  `service/` 와 똑같은 5개 이름으로 나눈다** — `conversation`, `assessment`, `training`,
  `record`, `privacy`. 이름이 세 계층에서 일치하면 한 기능을 고칠 때 세 자리를 찾는 일이
  기계적이 되고, 5인 병렬에서 파일 충돌도 줄어든다.
- 명세 §6 이 비워 둔 자리를 여기서 채운다: Pydantic 요청·응답 모델은
  `api/<기능>/schemas.py`, SQLAlchemy 모델은 `repository/models.py`(또는
  `repository/<기능>/models.py`) — 둘을 물리적으로 떨어뜨리는 것 자체가 TC-14 를 돕는다.
  `config.py`(pydantic-settings 설정 객체), `db.py`(엔진·세션·`Depends`), `main.py`(앱 조립,
  예외 핸들러 등록, `request_id` 미들웨어), `alembic/` + `alembic.ini`(`backend/` 아래,
  `app/` 밖), `backend/tests/`(`app/` 의 계층 구조를 거울처럼), 업로드 저장 경로(설정값이며
  `.gitignore` 대상이고 Docker 볼륨으로 뺀다), `scripts/`(`check.sh`, `seed.py`,
  `migrate.sh`).
- `app/prompts/assess_v1.md` 처럼 파일 이름이 버전을 들고 있으면 **프롬프트 로더가 파일
  이름에서 버전을 뽑아** `prompt_version` 으로 쓴다 `[developer §5.3]`. 코드가 버전 문자열을
  따로 들고 있으면 TC-10 이 저장하라는 그 값과 어긋난다. 로더는 모듈 기준 상대 경로로 읽는다.

**오류 처리** `[developer §4][phase:construction]`

- `common/exceptions.py` 에 기반 예외 `AppError(code, message, http_status)` 하나와 하위
  예외를 둔다: `NotFoundError`(404), `PermissionDeniedError`(403), `ValidationError`(422),
  `ConflictError`(409), `ProviderError`(502), `ProviderTimeoutError`(504).
- **`service` 는 `AppError` 하위만 던진다. `HTTPException` 은 던지지 않는다.** HTTP 로의
  번역은 `common/` 의 예외 핸들러 한 곳이 담당한다.
- 오류 봉투는 하나로 고정한다:
  `{"error": {"code": "...", "message": "...", "details": [...], "request_id": "..."}}`.
  **`code` 는 영어 고정 토큰, `message` 는 한국어다** — `[constraint:OC-06]` 은 사람이 읽는
  것을 한국어로 하라는 규칙이고, `code` 는 프론트가 분기하는 기계용 값이라 영어로 안정적이어야
  한다. `request_id` 는 미들웨어에서 요청마다 발급해 로그와 응답에 같은 값을 넣는다. 처리되지
  않은 예외는 500 + 같은 봉투로 나가되 내부 메시지를 노출하지 않고 스택은 로그에만 남긴다.
- **업로드(multipart)**: 디스크에 쓰기 **전에** 검증한다 — content-type 허용 목록
  (MediaRecorder 의 webm/opus), 최대 크기(`MAX_UPLOAD_BYTES` 설정값 — 코드에 숫자를 박지
  않는다), 빈 파일 거부. 크기 초과는 413. `await file.read()` 로 통째로 메모리에 올리지 않고
  청크로 흘려 쓴다. 임시 경로에 쓴 뒤 성공 시 최종 경로로 옮기고 실패 시 임시 파일을 지운다.
  저장 경로는 설정값이다.
- **STT·LLM 제공자 호출**: 모든 호출에 명시적 타임아웃을 준다(connect 와 read 를 따로).
  재시도는 타임아웃·연결 실패에만 최대 1회, 4xx 는 재시도하지 않는다 — 무한 재시도는 데모
  중에 화면이 멈추는 가장 흔한 원인이다. **제공자 예외는 `providers/` 를 넘지 않는다** —
  `httpx` 예외나 SDK 예외를 그대로 올려 보내지 말고 어댑터 경계에서 `ProviderError` /
  `ProviderTimeoutError` 로 바꾼다. 그래야 Mock↔live 교체가 상위 코드에 안 보인다
  `[constraint:TC-06]`. 로그에는 모델명·프롬프트 버전·소요 시간·`request_id` 를 남기고
  **전사 본문은 남기지 않는다.**
- **LLM 출력 파싱**: LLM 출력은 신뢰할 수 없는 입력이다. Pydantic 으로 파싱하고, 계약을 어긴
  결과가 리포트 전체를 500 으로 만들지 않게 한다. 명세 §7.4 의 `validate_evidence` 가 존재하지
  않는 발화 ID 를 `hold_reason=INVALID_EVIDENCE` 로 바꾸는 방식을 일반 규칙으로 올린다 —
  **LLM 계약 위반은 500 이 아니라 "보류"가 된다.** 저장 전에 응답 모델로 검증하고, 맞지 않으면
  강제 변환하지 말고 거부한다 `[devsecops §4(d)]`.
- **설정**: `ANALYSIS_MODE` 를 비롯한 환경변수는 기동 시 한 번 `pydantic-settings` 로
  파싱한다. 코드 곳곳에서 `os.environ` 을 직접 읽지 않고 설정 객체 하나를 주입한다.
- **DB**: 요청당 세션 하나를 `Depends` 로 주입한다. **커밋은 `service` 경계에서 한 번**,
  `repository` 는 커밋하지 않는다 — 각자 커밋하면 부분 저장이 생기고 그게 삭제 누수와 같은
  계열의 사고다. `IntegrityError` 는 500 이 아니라 `ConflictError`(409)로 번역한다.
  `repository` 에서 예외를 잡아 `None` 을 반환하지 않는다 — "없음"과 "실패"는 서로 다른 값이다.

**이름** `[developer §3][spec:02 §7.3]`

- Python 은 snake_case, TypeScript 는 camelCase.
- **한국어는 `def test_...` 함수 이름에만 쓴다.** 파일 이름, fixture 이름, 클래스 이름,
  마커, 파라미터화 id 를 포함한 그 밖의 모든 식별자는 영어다. fixture 이름은 다른 테스트의
  매개변수 이름이 되므로 여기에 한국어가 들어오면 규칙이 바로 깨진다.
- 테스트 이름의 언어는 **무엇을 검증하는가**로 가른다: 판정 규칙(보류, 기회 없음, 독립 수행,
  도움 후 수행, 분모 제외) 자체를 검증하는 것은 한국어(기준 문서와 한 줄씩 대조해야 한다),
  기술적·배관 동작(ID 검증, 상태 코드, 직렬화, 권한, 마이그레이션)을 검증하는 것은 영어.
  명세 §7.3 과 §7.4 가 이미 두 스타일로 갈려 있어 경계를 정하지 않으면 파일마다 달라진다.
- **도메인 용어집 `docs/glossary.md` 를 첫 주에 만든다** `[developer §3.3]`. 한국어 용어 →
  확정 영어 식별자 표를 두고, 명세 §7.2 가 이미 쓴 이름을 씨앗으로 삼는다(`BehaviorGroup`,
  `BehaviorJudgment`, `OpportunityStatus`, `JudgmentResult`, `HoldReason`, `PerformanceMode`,
  `SummaryStatus`, `valid_opportunities`, `min_opportunities`). 새 도메인 명사는 표에 먼저
  한 줄 추가한 뒤 코드에 쓴다. 5명이 AI 보조로 병렬로 쓰면 "판정"이 `judgment` /
  `assessment` / `evaluation` 으로 갈라지고, 그렇게 갈라진 이름은 나중에 한꺼번에 고치기가
  가장 비싼 부채다. 이 표는 domain-design(2.6)과 contract-design(2.8)의 입력이 된다.
- TC-10 의 세 값(`model_version`, `prompt_version`, `criteria_version`)은 **묶어서 다닌다**
  `[developer §3.4]`. 값 객체 하나(`JudgmentProvenance` 등)로 다루고, LLM 판정을 저장하는
  테이블은 세 컬럼을 `NOT NULL` 로 둔다. "함께 저장한다"가 사람의 주의력이 아니라 스키마
  제약이 된다.
- 사람이 읽는 것 — 주석, 산출물, UI 문구, 커밋 메시지 — 은 한국어로 쓴다
  `[constraint:OC-06]`.

**이 절의 근거 결정: D-54** (`decision-log.md` §5-2) `[log §5-2][FU4]`. Python 도구 확정 —
ORM **SQLAlchemy 2.0(동기)**, 마이그레이션 **Alembic**, 패키지 관리자 **uv**. 이 결정으로
제약 TC-15 와 의존 D3 가 닫혔다.
