<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-18 — u1: 상위 산출물이 이 단계를 담당으로 지정한 열린 질문이 정확히 세 건(OQ-F5, OQ-F2, OQ-N1)이었다. 그 셋만 묻고 이미 닫힌 영역은 다시 묻지 않았다. OQ-N1 은 "제공자가 정해지면"이 조건이라 이 단계에서 닫히지 않고 그대로 남는다 — 닫힌 척하지 않았다.
- 2026-09-18 — u1: `plan_profile.steps` 의 `Frontend behavior` 두 줄을 생략했다. U1 은 `kind: service` 인 백엔드 단위이고 화면은 u2 가 소유한다. 계약이 허용한 "genuinely inapplicable layer" 에 해당하며 방법론과 나머지 순서는 바꾸지 않았다. 생략 사실과 근거를 계획 §3 과 Step 10 뒤에 명시했다.
- 2026-09-18 — u1: 계획의 `## Plan Approval` 절을 처음에 계획 파일에 썼다가 질문 파일로 옮겼다. 단계 지침이 그 절을 `code-generation-questions.md` 에 두라고 정하고 `--questions-file` 도 그 파일을 가리킨다. 옮긴 뒤 지문을 다시 계산했다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-18 — u1: `docker-compose.yml` 에 frontend 서비스를 두지 않았다. 인프라 명세 §2 가 "frontend 는 u2 가 소유한다, 이 문서는 자리만 표시한다"고 적었고, 빈 껍데기 이미지는 u2 가 지울 코드가 된다. 그 결과 **AC9.1.1(세 컨테이너)은 이 단위에서 닫히지 않는다** — B1 완료 기준이지 U1 완료 기준이 아니라는 점을 계획 §2 에 적었다.
- 2026-09-18 — u1: Docker 가 이 환경에 없어 기준 명령(`docker compose run --rm backend ...`)을 그대로 돌리지 못했다. 시험 지침 §2 가 함께 적어 둔 호스트 실행 형태로 돌렸고, 통합 시험은 실제 PostgreSQL 16 을 `TEST_DATABASE_URL` 로 가리켜 돌렸다. 가짜로 대체하지 않았다. **Docker 위에서 다시 확인해야 하는 것 셋**(컨테이너 기동 + 헬스체크, 이미지 빌드, Testcontainers 경로)을 `code-summary.md` §4 에 남겼다.
- 2026-09-18 — u1: 어댑터가 HTTP 도구를 직접 import 하지 못하게 하는 수단을 린터 규칙에서 구조로 바꿨다. `TID251` 은 "전역 금지 + per-file 해제" 모양이라 "providers 에서만 금지"를 표현할 수 없다. 감싸기 장치가 클라이언트를 만들어 어댑터에 넘기고, 검사는 `test_layer_boundaries.py` 가 한다. `security-design.md` §2 의 가정이 이 대체 수단 자리를 열어 두었다.
- 2026-09-18 — u1: Ruff `per-file-ignores` 에 `app/api/**` → `B008` 을 더했다. FastAPI 의 `Depends` 기본값을 도구가 모르는 자리다. 품질 목표를 낮춘 것이 아니라 도구가 이 틀을 모르는 지점만 좁혀 해제했다.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-18 — u1: Q1 에서 배경 작업 예약 수단으로 프레임워크 기본값(A)을 골랐다. 새 의존성 0 이라는 이득의 대가는 **동시 작업 수를 제한할 수단이 없다**는 것이고, 인프라 §2.1 이 연결 풀 5 를 "동시 작업 2개" 전제로 계산했으므로 그 전제가 강제되지 않는다. 계획 §1 에 대가와 대응 두 가지(작업 식별자 로그, 연결 수 증가 시험)를 명시했다. 3개를 넘는 상황이 생기면 실행자를 두는 B 로 바꾼다.
- 2026-09-18 — u1: 프롬프트 격리를 구분자 제거가 아니라 `<`·`>` 이스케이프로 구현했다. 구분자 일부만 지우면 조각을 이어 붙여 되살릴 수 있다. 두 문자를 막으면 자료가 어떤 문자열이든 구분자를 흉내 낼 수 없다.
- 2026-09-18 — u1: 말이 되지 않는 상태 조합을 DB 검사 제약으로 내렸다(BR7.1, 실패 사유는 실패 상태에서만). 규칙이 사람의 주의력이 아니라 스키마가 된다.
- 2026-09-18 — u1: 업로드 최대 크기 기본값 25MiB 를 이 단계에서 정했다. 상위 문서는 "설정값"이라고만 정했고 값이 없었다. 설정으로만 살며 시험이 값을 바꿔 확인한다.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-18 — u1: `base` 시드가 시나리오 원형을 1개만 넣는다(계약 C16 은 6개). 기존 명세가 이름을 적은 원형은 `tpl_repair_person_01` 하나뿐이고 나머지 다섯의 식별자·내용은 어디에도 글로 없다. 지어내면 u7-f05-practice 가 확정할 값과 어긋난다(BR8.1). **담당: u7-f05-practice 의 기능 설계.**
- 2026-09-18 — u1: `entities.md` §3 이 `behavior_judgments` 의 부모 참조를 적지 않아 `docs/input/04_domain-model.md` §1 의 `SocialEvent ─< BehaviorJudgment` 를 따라 `social_event_id` 를 넣었다. `context_infos` 도 같은 문서의 `{value, status}` 짝을 따라 만들었다. 추측이 아니라 명세 인용이지만 **u5·u4 가 자기 기능 설계에서 확인**해 주는 편이 좋다.
- 2026-09-18 — u1: 승인된 `unit-test-instructions.md` 의 "단위 78개" 합계가 산술 오류였다. 구성 요소별 표를 더하면 83 이고, 파일별 개수는 계획 그대로 만들어 결과가 83 이다. 개수를 줄인 것이 아니라 합계 줄이 틀렸다.
- 2026-09-18 — u1: OQ-N1 이 열린 채로 남는다. live 제공자가 정해지면 타임아웃 두 값(5초 / 60초)을 실측으로 조정한다. 설정값이므로 코드 변경이 아니다.

### 검토 1회차 뒤 (2026-09-18)

- 2026-09-18 — u1 (Deviations): 검토 1회차 판정 **READY**(Critical 0 · Major 0 · Minor 2)를 기록하려 하자 "검토 요청 이후 작업 공간 소스가 바뀌었다"며 거부되었다. 원인은 검토자가 지시대로 검증 도구를 돌리며 **`__pycache__/*.pyc` 와 `.coverage` 가 새로 쓰인 것**이다. 두 파일 모두 `.gitignore` 에 있으나 소스 지문 계산에는 들어간다. 같은 회차 `--retry-pending` 은 "대기 중에 바뀐 소스를 다시 기준으로 삼을 수 없다"며, 새 회차 열기는 "1회차가 판정을 기다린다"며 거부되었다. 엔진이 준 유일한 경로는 변경 요청이었다. **다음 회차부터 검증은 `PYTHONDONTWRITEBYTECODE=1` 로 돌리고 커버리지 파일을 남기지 않는다.**
- 2026-09-18 — u1 (Interpretations): 두 Minor 는 문서 정합성 지적이라 **응용 코드는 한 줄도 바뀌지 않았다**. R-01 은 승인된 시험 지침의 합계 줄이 78 로 적힌 산술 오류(구성 요소별 표를 더하면 83)였고, 구성 요소별 개수를 건드리지 않은 채 합계만 바로잡았다 — 시험 범위를 늘리거나 줄인 것이 아니다. R-02 는 `traceability.json` 의 PARTIAL 다섯 건에 근거가 없던 것이라, 각 항목에 U1 이 무엇까지 만들었고 남은 몫의 담당이 누구인지를 `note` 로 적었다.
