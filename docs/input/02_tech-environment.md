# Technical Environment — SCD 소통 코칭

> **개정 이력**
> - 2026-09-16 (v2): 백엔드를 Java·Spring Boot 2-서비스 구성에서 **Python·FastAPI 단일 백엔드**로 전면 개정. 근거는 결정 D-30(Feasibility Q1, F1)이며, 이 결정이 D-01 의 Java 경로를 대체했다. 개정 대상 항목은 `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/feasibility/feasibility-assessment.md` §2.1 표에 정리되어 있다.
> - 2026-09-16 (v1): 최초 작성(Java core + Python analysis 2-서비스 구성).

## 1. 구성 개요

```
[React 모바일 웹] --REST/JSON--> [Python FastAPI 백엔드]
                                        |
                                   [PostgreSQL 16]
                                   [로컬 파일 저장소(음성)]
                                   [STT / LLM 어댑터 (Mock 기본)]
```

<!-- Text fallback: React 모바일 웹이 REST/JSON 으로 Python FastAPI 백엔드 하나를 호출하고, 그 백엔드가 PostgreSQL 16 과 로컬 파일 저장소를 소유하며 STT·LLM 어댑터도 그 안에 둔다. -->

- **backend(Python)**: 인증, 사용자·대화·전사·맥락·목표·연습·기록·정정·삭제, 규칙 기반 집계, DB 소유권, STT·LLM 어댑터를 모두 담는다.
- 백엔드 내부는 계층으로 나눈다: `api`(HTTP 경계) → `service`(업무 규칙) → `repository`(영속성). 어댑터(`providers`)는 `service` 가 인터페이스로만 참조한다.
- **결정 D-30**: 원래 명세의 Java core + Python analysis 2-서비스 구성은 폐기되었다. 분석 기능을 별도 서비스로 분리하지 않고 같은 백엔드의 모듈로 둔다. 실제 제공자 연결이 필요해지면 그때 분리를 다시 검토한다.

## 2. 언어·프레임워크

| 영역 | 선택 |
|---|---|
| Frontend | React 18, TypeScript 5, Vite 5, React Router 6, TanStack Query 5, CSS Modules |
| Backend | Python 3.11, FastAPI, Pydantic v2, uvicorn |
| ORM·마이그레이션 | **미정** — practices-discovery(2.2) 또는 domain-design(2.6)에서 결정 (제약 TC-15) |
| 패키지 관리 | **미정** — 위와 같은 시점에 결정 |
| Build | npm (frontend) / 결정된 Python 패키지 관리 도구 (backend) |
| DB | PostgreSQL 16 (판정 근거·변형 규칙 등 가변 구조는 JSONB) |
| API 문서 | FastAPI 내장 OpenAPI 3 — frontend 타입은 이 스키마에서 생성 |
| 녹음 | 브라우저 MediaRecorder API (webm/opus), 업로드는 multipart |
| 로컬 실행 | Docker Compose (frontend, backend, postgres — **3 컨테이너**) |
| 배포 | 이번 테스트는 로컬만. 클라우드 배포 없음 |

버전 조합은 결정 D-31 로 확정되었다. 가정 A-09 중 Java 21 · Spring Boot 3.3 부분은 D-30 으로 무효가 되었다.

## 3. 테스트

| 영역 | 도구 |
|---|---|
| backend 단위 | pytest |
| backend API | pytest + httpx TestClient |
| backend DB 연동 | Testcontainers (PostgreSQL) |
| frontend | Vitest, React Testing Library, MSW(API 모킹) |
| E2E | Playwright — `05_synthetic-test-data.md`의 시나리오 3건 |

Test Strategy 는 Standard 다. 구성 요소마다 5–8개, 단위 테스트와 주요 경계의 통합 테스트를 쓴다.

## 4. 외부 연동 원칙

- STT·LLM 은 `SttProvider`, `LlmProvider` 인터페이스로 분리하고 기본 구현은 `Mock*`(고정 fixture 반환).
- 실제 제공자 연결은 환경변수 `ANALYSIS_MODE=mock|live` 로 전환한다. **기본값은 `mock` 이고, 성공 기준 SM1 의 검증도 `mock` 경로로 한다** (결정 D-36).
- live 구현체는 만들되 선택 경로다. 제공자는 아직 정하지 않았다 (결정 D-37).
- API 키는 백엔드 서비스의 환경변수에만 둔다. 저장소에 커밋하지 않는다.
- LLM 호출에는 모델명·프롬프트 버전·기준 버전을 응답에 포함해 함께 저장한다.
- 평가용 프롬프트와 코칭(모의 대화)용 프롬프트는 파일·버전을 분리한다.
- 전사 텍스트는 프롬프트에서 구분자로 감싼 데이터 블록으로만 전달한다. 시스템 명령으로 취급하지 않는다.

## 5. 금지 사항

| 금지 | 이유 | 대안 |
|---|---|---|
| 프론트엔드에서 STT/LLM API 직접 호출 | 키 노출, 기록 누락 | 백엔드 경유 |
| `api` 계층이 `repository` 를 직접 호출 | 업무 규칙을 건너뛰어 삭제 전파·권한 검사가 누락된다 | 반드시 `service` 를 경유 |
| ORM 모델을 API 응답으로 그대로 반환 | 필드 노출·순환 참조 | Pydantic 응답 모델 |
| 음성 파일을 DB BLOB 으로 저장 | 삭제·권한 분리 어려움 | 파일 저장소 + 메타데이터 테이블 |
| LangChain 등 오케스트레이션 프레임워크 | 프롬프트·버전 추적 어려움 | 제공자 SDK 또는 HTTP 직접 호출 |
| Neo4j·벡터DB 도입 | MVP 범위 외 | PostgreSQL JSONB |
| 종합점수·백분위 계산 코드 | 서비스 원칙 위반 | 행동별 상태·기회 수 집계 |
| 전역 상태 관리 라이브러리(Redux 등) | 서버 상태 위주 앱에 과함 | TanStack Query + 로컬 state |

**주의**: v1 의 금지 항목 "analysis 서비스의 DB 직접 접근"은 서비스 분리 자체가 사라져 의미를 잃었다. 그 항목이 막던 위험(데이터 소유권 분산으로 인한 삭제 누락)은 위 표의 계층 경계 규칙이 대신 막는다. 구체적인 경계 정의는 domain-design(2.6)에서 확정한다 (제약 TC-14, 위험 R3).

## 6. 패키지 구조

```
backend/app/
  api/          (HTTP 라우터 — 화면 흐름 A/B/C 에 대응)
  service/      (업무 규칙)
    conversation/  (업로드, 전사, 맥락, 정정)
    assessment/    (기회·행동 판정 저장, 집계 규칙)
    training/      (목표, 시나리오, 연습 세션, 시도, 힌트)
    record/        (기록, 추천, 버전 이력)
    privacy/       (공유 권한, 삭제 요청)
  repository/   (영속성)
  providers/    (stt_mock.py, llm_mock.py, stt_live.py, llm_live.py)
  prompts/      (assess_v1.md, coach_v1.md)
  fixtures/     (합성 데이터 기대 결과)
  common/       (예외, 응답 형식)
frontend/src/
  pages/ (A1..A5, B1..B5, C1..C5 — 03_ui-spec 화면 ID와 동일 명명)
  components/ api/ hooks/ styles/
```

## 7. 코드 예시

### 7.1 backend — 엔드포인트

```python
router = APIRouter(prefix="/api/conversations")

@router.get("/{conversation_id}/report", response_model=ReportResponse)
def get_report(
    conversation_id: UUID,
    user: AppUser = Depends(current_user),
    service: ReportService = Depends(get_report_service),
) -> ReportResponse:
    return service.get_report(conversation_id, user.id)
```

### 7.2 backend — 집계 함수 (규칙 엔진)

보류와 기회 없음을 분모에서 제외하고, 독립 수행과 도움 후 수행을 섞지 않는다.

```python
@dataclass(frozen=True)
class BehaviorSummary:
    group: BehaviorGroup
    valid_opportunities: int
    observed: int
    partial: int
    not_observed: int
    status: SummaryStatus


def summarize(
    group: BehaviorGroup,
    judgments: list[BehaviorJudgment],
    mode: PerformanceMode,
    min_opportunities: int,
) -> BehaviorSummary:
    valid = [
        j for j in judgments
        if j.group == group
        and j.mode == mode                              # 독립/도움 후 혼합 금지
        and j.opportunity is OpportunityStatus.PRESENT
        and j.hold_reason is None                       # 보류는 분모 제외
    ]
    observed = sum(1 for j in valid if j.result is JudgmentResult.OBSERVED)
    partial = sum(1 for j in valid if j.result is JudgmentResult.PARTIAL)
    not_observed = sum(
        1 for j in valid if j.result is JudgmentResult.NOT_OBSERVED_THIS_TIME
    )
    status = (
        SummaryStatus.INSUFFICIENT_FOR_COMPARISON
        if len(valid) < min_opportunities
        else SummaryStatus.AVAILABLE
    )
    return BehaviorSummary(
        group, len(valid), observed, partial, not_observed, status
    )
```

### 7.3 backend — 테스트

```python
def test_보류와_기회없음은_분모에서_제외된다():
    judgments = [
        judgment(PRESENT, OBSERVED, None),
        judgment(ABSENT, None, None),
        judgment(PRESENT, None, HoldReason.UNCLEAR_TRANSCRIPT),
    ]
    s = summarize(
        BehaviorGroup.CLARIFICATION_REPAIR,
        judgments,
        PerformanceMode.INDEPENDENT,
        min_opportunities=3,
    )
    assert s.valid_opportunities == 1
    assert s.status is SummaryStatus.INSUFFICIENT_FOR_COMPARISON
```

### 7.4 backend — 판정 엔드포인트와 근거 검증

```python
@router.post("/assess", response_model=AssessResponse)
def assess(
    req: AssessRequest,
    llm: LlmProvider = Depends(get_llm),
) -> AssessResponse:
    candidates = llm.detect_behaviors(
        utterances=req.utterances,
        context=req.context,
        criteria_version=req.criteria_version,
    )
    return AssessResponse(
        judgments=validate_evidence(candidates, req.utterances),
        model_version=llm.model_version,
        prompt_version="assess_v1",
    )


def test_evidence_ids_must_exist(client):
    fixture = load_fixture("conv_repair_01")
    res = client.post("/api/assess", json=fixture)
    ids = {u["id"] for u in fixture["utterances"]}
    for j in res.json()["judgments"]:
        assert set(j["evidence_utterance_ids"]) <= ids
```

`validate_evidence` 는 존재하지 않는 발화 ID 를 가진 판정을 `hold_reason=INVALID_EVIDENCE` 로 바꾼다.

## 8. 아직 정하지 않은 것

| 항목 | 정해질 시점 | 근거 |
|---|---|---|
| ORM·마이그레이션 도구·패키지 관리자 | practices-discovery(2.2) 또는 domain-design(2.6) | 제약 TC-15, RAID D3 |
| 계층 경계 규칙의 구체적 정의 | domain-design(2.6) | 제약 TC-14, RAID R3 |
| live STT·LLM 제공자 | nfr-requirements(3.2), 늦어도 code-generation(3.5) 착수 전 | 결정 D-37, RAID R4·D2 |
