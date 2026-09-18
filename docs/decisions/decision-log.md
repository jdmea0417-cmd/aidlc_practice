# 결정 기록 (Decision Log)

> 이 프로젝트에서 나온 **모든 질문과 사용자의 선택**을 한곳에 기록한다.
> 원본: `docs/input/07_decision-log.md`. 이 파일은 AI-DLC 실행 중 계속 갱신되는 통합본이다.
> 기존 항목은 지우지 않는다. 결정이 바뀌면 이전 항목 상태를 "변경됨 → D-xx"로 바꾸고 새 항목을 추가한다.

## 상태 표기

| 상태 | 뜻 |
|---|---|
| 확정 | 사용자가 직접 선택·지시함 |
| 기본값 적용(확인 필요) | 문서의 테스트용 기본값을 사용함. 사용자가 아직 확인하지 않음 |
| AI 가정(확인 필요) | AI가 진행을 위해 임시로 정함 |
| 미결정 | 논의했으나 결정하지 않음 |
| 변경됨 → D-xx | 이후 결정으로 대체됨 |

---

## 1. 입력 문서 준비 단계 (AI-DLC 실행 전, 2026-09-16)

### D-01 기술 스택
- **단계**: 입력 문서 준비
- **질문**: AI-DLC 기술 환경 문서에 넣을 스택은 무엇으로 할까요?
- **선택지**: ① React+FastAPI ② Next.js 단일 ③ React Native+FastAPI ④ 팀 스택 미정
- **사용자 답(원문)**: "현재 배운 것은 React+Java, 해당 기술 기반 작성+필요 시 python 연동 방안, 불가 시 1안"
- **결정**: React + Java(Spring Boot) 기반, 분석 기능은 Python 서비스로 연동. 연동 불가 시 ① React + FastAPI로 전환
- **영향 문서**: 02_tech-environment.md
- **상태**: 변경됨 → D-30 (Feasibility 단계에서 사용자가 대체안 ①을 선택함)

### D-02 테스트 범위
- **단계**: 입력 문서 준비
- **질문**: 이번 테스트 범위는 어디까지로 할까요?
- **선택지**: ① A·B·C 전체, 합성데이터 ② A→B 핵심 흐름만 ③ 실제 STT·LLM 연동
- **사용자 답(원문)**: "A·B·C 전체, 합성데이터 (권장)"
- **결정**: UI의 A·B·C 흐름 전체를 합성 데이터와 Mock STT·LLM으로 구현·테스트
- **영향 문서**: 01_vision.md, 03_ui-spec.md, 05_synthetic-test-data.md
- **상태**: 확정

### D-03 기획 방향 유지
- **단계**: 입력 문서 준비
- **질문**: (지시) 만들어진 UI 양식과 함께 AI-DLC에 입력할 수 있도록 수정
- **사용자 답(원문)**: "현재 기획을 유지하며 수정"
- **결정**: 기획서(SCD 사용자 대상 앱)와 UI 시안의 흐름을 유지. 검토 중 논의한 변경안은 반영하지 않음(D-06 참고)
- **영향 문서**: 전체
- **상태**: 확정

### D-04 보유 자료
- **단계**: 입력 문서 준비
- **질문**: 현재 기획서 외 아무런 자료도 없는 상태인데, 진행에 지장이 없겠는가?
- **사용자 답(원문)**: (자료 없음을 전제로 진행)
- **결정**: 외부 자료(온톨로지 파일, POC 코드, 인수인계 문서, 실제 데이터) 없이 자체 완결형으로 진행. 시나리오 원형 문서(06) 추가. UI 이미지는 선택
- **영향 문서**: 00_README.md, 01_vision.md, 04_domain-model.md, 06_seed-scenarios.md
- **상태**: 확정

### D-05 결정 기록
- **단계**: 입력 문서 준비
- **사용자 답(원문)**: "모든 질문과 내 선택이 내가 확인 가능한 문서로 기록되길 원함"
- **결정**: 이 문서를 만들고, AI-DLC 시작 프롬프트에 기록 의무를 넣음
- **영향 문서**: 00_README.md, 07_decision-log.md
- **상태**: 확정

### D-06 대상 정의 변경안 (검토만)
- **단계**: 기획 검토
- **논의 내용**:
  - 대상을 "구어 대화가 가능하나 화용언어에 어려움이 있는 사람(핵심: 발달장애인·특수교육대상자)"으로 확대
  - 이용 주체를 특수교사 중심, 입력을 교실 반구조화 대화로 변경
  - 언어 배경에 따른 항목별 판정 보류 규칙 추가
  - 외국인 한국어 학습자로 확장하는 안(비추천, 확장 가능성 언급만)
- **사용자 선택**: 없음. D-03에 따라 이번 테스트에는 미반영
- **반영된 흔적**: User.languageBackground 선택 필드만 추가
- **상태**: 미결정

---

## 2. 사용자 확인이 필요한 기본값 (문서 작성 시 AI가 정한 값)

| ID | 항목 | 적용한 값 | 근거 | 상태 |
|---|---|---|---|---|
| A-01 | 대상 연령 | 8–12세 | 기획서는 "약 6–12세 작업 가정"이며 AI가 좁힘 | 변경됨 → D-12 |
| A-02 | 보호자 역할 | 열람만 | 기획서 미정 | AI 가정(확인 필요) |
| A-03 | 플랫폼 | 모바일 웹 375px | UI 시안이 모바일 화면 | 변경됨 → D-62 |
| A-04 | 모의 대화 매체 | 텍스트 채팅 | 기획서 미정 | 확정 → D-63 |
| A-05 | 녹음 최대 길이 | 5분 | 기획서 미정 | AI 가정(확인 필요) |
| A-06 | 분석 응답 시간 | Mock 기준 3초 | 기획서 미정 | AI 가정(확인 필요) |
| A-07 | 비교 불충분 기준 | 유효 기회 3회 미만 | 기획서 "수치 미정" | AI 가정(확인 필요) |
| A-08 | 원음 보관 | 기본 30일 | 기획서 미정 | AI 가정(확인 필요) |
| A-09 | 버전 | Java 21, Spring Boot 3.3, React 18, PostgreSQL 16 | 일반적 최신 안정 조합 | AI 가정(확인 필요) |
| A-10 | 행동 묶음 조작적 정의 | 04_domain-model.md 4장 | 기획서 초안을 표로 정리 | 확정 → D-64 |
| A-11 | UI 세부 문구 | 03_ui-spec.md | 시안 해상도 한계로 재구성 | AI 가정(확인 필요) |
| A-12 | Mock 판정 규칙·시나리오 6개 | 06_seed-scenarios.md | 테스트 전용 창작 | AI 가정(확인 필요) |

확인 방법: 항목별로 "확정" 또는 수정값을 적고, 수정한 경우 영향 문서도 함께 고친 뒤 AI-DLC에 알린다.

---

## 3. AI-DLC 실행 중 기록 (자동 추가 영역)

### 기록 양식

```
### D-xx 제목
- 일시:
- 단계: (Workspace Detection / Requirements Analysis / User Stories / Application Design / Units / Functional Design / NFR / Code Generation / Build and Test)
- 질문 파일: (aidlc-docs/... 경로)
- 질문:
- 선택지: A) ... B) ... C) ... X) 기타
- 사용자 답(원문):
- 이유·메모:
- 결정 요약:
- 영향 문서:
- 상태:
```

승인·반려·수정 요청도 같은 양식으로 기록한다(질문 = "OO 단계 산출물 승인 여부").

### D-07 워크플로 진행 방식(플랜) 선택
- **일시**: 2026-09-16
- **단계**: AI-DLC 시작 (스코프 결정)
- **질문 파일**: (대화 내 구조화 질문)
- **질문**: 기성 플랜 중 딱 맞는 것이 없습니다. 이 프로젝트를 어떤 방식으로 진행할까요?
- **선택지**: A) compose (권장) — 작업에 맞는 단계 구성을 제안받음  B) mvp — 33단계 중 23단계  C) feature — 33단계 전부  D) classic — 33단계 중 26단계  X) 기타
- **사용자 답(원문)**: "compose (권장)"
- **이유·메모**: 입력 문서(비전·스택·UI·도메인·테스트 데이터)가 이미 확정된 부분이 많아, 확정 영역은 가볍게 두고 설계·구현을 충실히 하는 맞춤 구성이 적합
- **결정 요약**: 적응형 구성기(composer)로 맞춤 단계 구성을 제안받아 승인 후 진행
- **영향 문서**: 워크플로 전체 구성
- **상태**: 확정

### D-08 워크플로 단계 구성(scd-coach-mvp) 승인
- **일시**: 2026-09-16
- **단계**: AI-DLC 시작 (계획 구성 게이트)
- **질문 파일**: (대화 내 구조화 질문)
- **질문**: 이 계획(scd-coach-mvp, 19단계 실행 / 14단계 생략, 승인 게이트 16개)으로 진행할까요?
- **선택지**: A) 승인  B) 수정 후 승인  C) 거절  X) 기타
- **사용자 답(원문)**: "승인"
- **이유·메모**: 입력 명세가 제품 방향·화면·도메인 모델·기대 판정을 이미 확정했고 클라우드 배포가 범위 밖이므로, 탐색성 기획 단계와 운영 배포 단계를 접고 3개 서비스(React/Spring Boot/FastAPI)의 설계·계약·검증에 집중
- **결정 요약**: 커스텀 스코프 `scd-coach-mvp` 채택. depth=Standard, skeleton=on, Change Control=relaxed.
  - EXECUTE(19): workspace-scaffold, workspace-detection, state-init, intent-capture, feasibility, scope-definition, approval-handoff, practices-discovery, requirements-analysis, domain-design, units-generation, contract-design, delivery-planning, functional-design, nfr-requirements, nfr-design, infrastructure-design, code-generation, build-and-test
  - SKIP(14): market-research, team-formation, rough-mockups, reverse-engineering, user-stories, refined-mockups, ci-pipeline, deployment-pipeline, environment-provisioning, deployment-execution, observability-setup, incident-response, performance-validation, feedback-optimization
  - 되살림 조건: git 저장소를 만들어 원격에 올리면 `ci-pipeline`, 별도 고충실도 화면 설계가 필요하면 `refined-mockups`
- **영향 문서**: .claude/scopes/aidlc-scd-coach-mvp.md, .claude/tools/data/scope-grid.json, 워크플로 전체
- **상태**: 확정

### D-09 문제 정의 (Intent Capture Q1)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/intent-capture/intent-capture-questions.md` (Q1)
- **질문**: 이 서비스가 해결하려는 문제는 무엇입니까?
- **선택지**: A) 돌아보기→연습 단절 (실제 대화에서 무엇이 어려웠는지 근거와 함께 돌아볼 방법이 없고, 그 결과가 연습으로 이어지지 않음) B) 전문가 관찰 부담 경감에 초점 C) 보호자 파악 어려움에 초점 D) A+C 둘 다 E) 아직 정해지지 않음 X) 기타
- **사용자 답(원문)**: "A. 돌아보기→연습 단절"
- **결정 요약**: 문제 정의 = 실제 대화를 근거와 함께 돌아볼 방법이 없고 그 결과가 연습으로 이어지지 않는 것. 대상은 SCD로 의사소통에 어려움을 겪는 사용자.
- **영향 문서**: intent-statement.md
- **상태**: 확정

### D-10 성공 기준 (Intent Capture Q3)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q3)
- **질문**: 이번 작업의 성공을 무엇으로 판단합니까? (해당하는 것 모두 선택)
- **선택지**: A) 전 흐름 연결(합성 대화 3건이 업로드→전사→리포트→목표→모의 대화→기록까지 이어짐) B) 근거·보류 정확성 C) 시도 분리 집계 D+E) 정정·삭제 전파 및 금지 표현 없음 X) 기타
- **사용자 답(원문)**: "A. 전 흐름 연결"
- **이유·메모**: B~E를 고르지 않아 Q1(근거 기반 문제 정의)과 긴장이 있어 Q11로 재확인 중
- **결정 요약**: 성공 기준에 A를 포함. 나머지 항목 포함 여부는 Q11에서 확정
- **영향 문서**: intent-statement.md
- **상태**: 확정 (범위는 Q11에서 보완)

### D-11 추진 계기 (Intent Capture Q4)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q4)
- **질문**: 지금 이 서비스를 만드는 계기는 무엇입니까?
- **선택지**: A) 워크플로 검증 중심(실제 사용자 데이터 없이 합성 데이터로 흐름 전체가 성립하는지 확인) B) 제품 첫 구현 중심 C) A+B 둘 다 D) 외부 일정 요인 E) 아직 정해지지 않음 X) 기타
- **사용자 답(원문)**: "A. 워크플로 검증 중심"
- **결정 요약**: 계기 = AI-DLC 워크플로 검증을 겸한 테스트 MVP. 합성 데이터로 흐름 전체 성립 확인이 주목적
- **영향 문서**: intent-statement.md
- **상태**: 확정

### D-12 대상 연령 변경 — 6~12세 아동에서 13~25세로 (Intent Capture Q2)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q2)
- **질문**: 주 사용자는 누구이며, 보호자·전문가의 역할은 어떻게 합니까?
- **선택지**: A) 8–12세, 보호자 열람만 B) 6–12세, 보호자 열람만 C) 연령 미특정 아동·청소년 D) 보호자에게 추가 역할 X) 기타
- **사용자 답(원문)**: "13-25세로 계획 변경, 보호자 열람만"
- **이유·메모**: 근거 문서 `01_vision.md`의 "약 6–12세 아동" 작업 가정과 기본값 A-01(8–12세)을 사용자가 직접 뒤집음. 성인 구간(19–25세)이 포함되어 보호자 열람의 동의 주체 문제, 그리고 `06_seed-scenarios.md`의 초등학교 상황 6개와 `03_ui-spec.md`의 아동 대상 문구가 대상과 어긋나는 문제가 파생됨 → Q9·Q10으로 확인 중
- **결정 요약**: 주 사용자 연령대를 **13–25세**로 변경. 보호자는 열람만. (파생 항목 확정 전 잠정)
- **영향 문서**: 01_vision.md(2장 대상 사용자, 8장 기본값), 03_ui-spec.md, 06_seed-scenarios.md, 04_domain-model.md(User.ageBand), intent-statement.md, stakeholder-map.md
- **상태**: 확정 — 단, 파급 항목(Q9 보호자 권한, Q10 시나리오·문구)은 미확정

### A-01 변경 처리
- 기존 A-01 "대상 연령 8–12세 (AI 가정)" → **변경됨 → D-12**

### D-13 대상 연령 확정 — 13~18세 청소년 (Intent Capture Q2 재확인)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q2)
- **질문**: Q2 확인. 주 사용자를 13–25세로 확정합니까?
- **선택지**: A) 13–25세, 보호자 열람만 B) 13–18세로 좁힘 C) 13–25세 + 보호자 역할 확대 D) 근거 문서대로 6–12세 유지 X) 기타
- **사용자 답(원문)**: "13–18세로 좁힘"
- **이유·메모**: 13–25세에는 성인(19–25세)이 포함되어 보호자 열람의 동의 주체 문제가 생김. 13–18세로 좁히면 전원 미성년자라 이 문제가 사라짐
- **결정 요약**: 주 사용자 = **13–18세 청소년**. 보호자 = 열람만. 전문가 = MVP 제외. D-12를 대체함
- **영향 문서**: 01_vision.md(2장·8장), 03_ui-spec.md, 06_seed-scenarios.md, 04_domain-model.md(User.ageBand), intent-statement.md, stakeholder-map.md
- **상태**: 확정

### D-14 보호자 열람 권한 범위 (Intent Capture Q9)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q9)
- **질문**: 보호자 열람 권한을 어떻게 처리합니까?
- **선택지**: A) 본인 선택 기능, 기본 꺼짐 B) 미성년자만 제공 C) 항상 제공, 권한 수준만 선택 D) MVP에서 제외 X) 기타
- **사용자 답(원문)**: "B. 미성년자만 제공"
- **이유·메모**: D-13으로 대상이 13–18세 전원 미성년자가 되었으므로, 이번 MVP에서 B는 실질적으로 "모든 사용자에게 제공"과 같음. 성인 사용자로 확장할 때 이 규칙이 분기점이 됨
- **결정 요약**: 보호자 열람은 **미성년 사용자에게만** 제공. 권한 수준 NONE/SUMMARY/FULL은 유지
- **영향 문서**: 04_domain-model.md(SharingSetting), 03_ui-spec.md(C5), intent-statement.md
- **상태**: 확정

### D-15 아동 전용 시나리오·UI 문구 처리 (Intent Capture Q10)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q10)
- **질문**: 아동 전용으로 작성된 기존 시나리오 6개와 UI 문구는 어떻게 합니까?
- **선택지**: A) 기존 그대로, 연령만 반영 B) 새 연령대 상황으로 새로 작성 C) 인물·소재만 교체 D) Scope Definition에서 결정 X) 기타
- **사용자 답(원문)**: "B. 13–25세로 새로 작성"
- **이유·메모**: 선택지 B의 예시(대학 수업·면접)는 13–25세 기준이었으나 D-13에서 13–18세로 좁혀져 배경이 어긋남 → Q12로 배경을 다시 확인 중
- **결정 요약**: `06_seed-scenarios.md`의 시나리오 원형 6개와 `03_ui-spec.md`의 UI 문구를 새 대상 연령에 맞게 **새로 작성**한다. 구체적 배경은 Q12에서 확정
- **영향 문서**: 06_seed-scenarios.md, 03_ui-spec.md
- **상태**: 확정 (배경은 D-17에서 확정)

### D-16 성공 기준 범위 (Intent Capture Q11)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q11)
- **질문**: 성공 기준을 A(전 흐름 연결) 하나로 볼까요?
- **선택지**: A) A만으로 충분 B) A+B(근거·보류 정확성 포함) C) A+B+C D) 6개 항목 전부 X) 기타
- **사용자 답(원문)**: "A. A만으로 충분"
- **이유·메모**: Q1의 문제 정의가 "근거와 함께 돌아보기"인데 근거 발화 ID 유효성이 성공 기준에서 빠지는 긴장을 제시했고, 사용자가 A를 재확인함. 근거 유효성·보류 처리·시도 분리 집계·정정 전파·금지 표현은 성공 기준이 아니라 **기능 요구사항**으로 다룬다
- **결정 요약**: 이번 작업의 성공 기준은 **"합성 대화 3건이 업로드→전사 확인→리포트→목표 선택→모의 대화→기록까지 끊김 없이 이어진다" 하나**. 나머지는 구현 세부사항으로 분류
- **영향 문서**: intent-statement.md, 01_vision.md(6장)
- **상태**: 확정

### D-17 시나리오 배경 — 중·고등학교 생활 중심 (Intent Capture Q12)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q12)
- **질문**: 13–18세로 좁혔으니, 새로 만들 모의 대화 시나리오의 배경은 어디로 잡습니까?
- **선택지**: A) 중·고등학교 생활 중심(조별 과제, 동아리, 급식실·쉬는 시간, 교사와의 대화, 진로 상담) B) 학교 + 학교 밖 혼합 C) 또래 관계 중심 D) 나중에 결정 X) 기타
- **사용자 답(원문)**: "A. 중·고등학교 생활 중심"
- **결정 요약**: 시나리오 원형 6개(행동 묶음 3종 × 2개)를 **중·고등학교 생활 배경**으로 새로 작성한다. `04_domain-model.md`의 판정 규칙과 원형 구조는 유지. D-15의 배경을 확정함
- **영향 문서**: 06_seed-scenarios.md, 03_ui-spec.md
- **상태**: 확정

### D-18 이해관계자 (Intent Capture Q5)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q5)
- **질문**: 이 작업의 이해관계자는 누구입니까? (해당하는 것 모두 선택)
- **선택지**: A) 주 사용자(13–18세) B) 보호자·지원자 C) 프로젝트 실행자 D) 전문가(확장 기록만) X) 기타
- **사용자 답(원문)**: "A. 주 사용자(13–18세), B. 보호자·지원자"
- **이유·메모**: C(프로젝트 실행자)와 D(전문가)는 선택되지 않음 → 이해관계자 지도에 등장하지 않는다
- **결정 요약**: 이해관계자는 **주 사용자(13–18세)와 보호자·지원자 둘**. 전문가는 이해관계자로 기록하지 않음
- **영향 문서**: stakeholder-map.md
- **상태**: 확정

### D-19 결정 구조 (Intent Capture Q6)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q6)
- **질문**: 범위와 우선순위는 누가 결정합니까?
- **선택지**: A) 내가 단독 결정 B) 내가 결정하되 입력 문서(D-01~D-05) 우선 C) 다른 결정권자 있음 D) 미정 X) 기타
- **사용자 답(원문)**: "B. 내가 결정, 입력 문서 우선"
- **결정 요약**: 사용자가 단독 결정권자이되, `docs/input/`의 기존 결정(D-01~D-05)이 우선하며 이를 뒤집을 때만 별도 확인을 거친다
- **영향 문서**: stakeholder-map.md, intent-statement.md
- **상태**: 확정

### D-20 기록·공유 방식 (Intent Capture Q7)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q7)
- **질문**: 진행 상황을 어떤 방식으로 기록·공유해야 합니까?
- **선택지**: A) decision-log 한 곳 B) + 단계별 요약 보고 C) + 정기 주기 정리 D) 특별한 요구사항 없음 X) 기타
- **사용자 답(원문)**: "A. decision-log 한 곳"
- **결정 요약**: 모든 질문·답변·승인/반려를 `docs/decisions/decision-log.md` 한 곳에만 기록한다. 별도 요약 보고나 정기 주기 정리는 만들지 않는다
- **영향 문서**: stakeholder-map.md
- **상태**: 확정

### D-21 제품 경계 (Intent Capture Q8)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q8)
- **질문**: 제품의 경계 — 무엇을 만들고 무엇을 만들지 않을지가 근거 문서와 맞습니까?
- **선택지**: A) 맞다 — F01~F07 그대로 B) 일부 기능 제외 C) 다른 경계를 정의 D) Scope Definition에서 결정 X) 기타
- **사용자 답(원문)**: "A. 맞다 — F01~F07 그대로"
- **결정 요약**: 제품 경계 = `01_vision.md` 4장의 MVP 범위 F01~F07(녹음·전사, 맥락 구조화, 수행 평가, 목표·프로필, 모의 대화, 기록·다음 추천, 정정·삭제)과 5장의 범위 제외(자동진단, 임상 중증도·개선율, 공식 척도 자동 점수, 비디오 기반 평가, 청자 지식·함축 응답 평가, FAR 자동 생성, Vector RAG·GraphRAG·Neo4j, 전문가 대시보드, TTS, 결제·과금, 실제 사용자 데이터 수집, 네이티브 앱)를 그대로 채택
- **영향 문서**: intent-statement.md, 이후 Scope Definition
- **상태**: 확정

### D-22 합성 테스트 대화 3건 처리 (Intent Capture Q13)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q13)
- **질문**: 대상 연령이 13–18세로 바뀌었는데, 기존 합성 테스트 대화 3건은 어떻게 합니까?
- **선택지**: A) 그대로 둔다 B) 소재만 손봄(구조·기대 판정 유지) C) 중·고등학교 배경으로 3건 새로 작성 D) Build and Test에서 결정 X) 기타
- **사용자 답(원문)**: "A. 그대로 둔다"
- **결정 요약**: `05_synthetic-test-data.md`의 S1·S2·S3과 기대 판정을 그대로 사용한다. 시나리오 원형(D-15·D-17)만 새로 쓰고 테스트 데이터는 손대지 않는다. 성공 기준 SM1이 가리키는 "합성 대화 3건"은 이 3건이다
- **영향 문서**: 05_synthetic-test-data.md(변경 없음), intent-statement.md
- **상태**: 확정

### D-23 이해관계자 목록에 프로젝트 실행자 포함 여부 (Intent Capture Q14)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q14)
- **질문**: 프로젝트를 진행하는 본인을 이해관계자 목록에 넣습니까?
- **선택지**: A) 넣지 않는다(결정권자는 별도 항목) B) 넣는다 C) 넣되 관심사를 다르게 X) 기타
- **사용자 답(원문)**: "A. 넣지 않는다"
- **결정 요약**: 이해관계자는 제품을 쓰는 사람(주 사용자, 보호자·지원자)만 가리킨다. 결정권자는 이해관계자 지도의 별도 항목으로 둔다
- **영향 문서**: stakeholder-map.md, intent-statement.md
- **상태**: 확정

### D-24 보호자 열람 권한 초기 설정 (Intent Capture Q15)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q15)
- **질문**: 보호자 열람 권한은 누가 언제 켭니까?
- **선택지**: A) 본인이 켜고 기본 NONE B) 가입 시 기본 SUMMARY 켜짐 C) 보호자가 계정 생성·초기 권한 설정 D) Requirements Analysis에서 결정 X) 기타
- **사용자 답(원문)**: "C. 보호자가 초기 설정"
- **이유·메모**: 이 답이 Q2의 "보호자는 열람만"과 어긋나 Q16으로 충돌 해소를 요청함
- **결정 요약**: (초기 답변) 보호자가 계정을 만들고 사용자를 연결하며 초기 권한도 정한다
- **영향 문서**: stakeholder-map.md, 04_domain-model.md(SharingSetting)
- **상태**: 변경됨 → D-25

### D-25 보호자 역할 확정 — 열람만, 계정은 사용자가 생성 (Intent Capture Q16)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q16)
- **질문**: 보호자의 역할을 어떻게 정리합니까? (Q2의 "열람만"과 Q15의 "계정 생성·초기 권한 설정"이 어긋납니다)
- **선택지**: A) 보호자 역할을 넓힘(계정 생성·초기 권한 설정 후 열람만) B) Q2를 지킴(보호자는 열람만, 계정은 사용자가 생성, 기본 NONE) C) 절충(보호자 연결 필수, 기본 SUMMARY) D) Requirements Analysis에서 결정 X) 기타
- **사용자 답(원문)**: "B. Q2를 지킨다"
- **이유·메모**: 근거 문서 3장 원칙 7 "사용자가 통제한다"와 가장 가까움. D-24(Q15=C)를 대체하며 Q15의 답을 A로 되돌림
- **결정 요약**: 보호자는 **열람만** 한다. 계정은 **사용자가 만든다**. 보호자 열람 권한 초기 기본값은 **NONE**이며 사용자 본인이 켠다. 권한 수준 NONE/SUMMARY/FULL은 유지
- **영향 문서**: intent-statement.md, stakeholder-map.md, 04_domain-model.md(SharingSetting), 03_ui-spec.md(C5)
- **상태**: 확정

### D-26 Intent Capture 가정 처리 방식
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Assumption Confirmation)
- **질문**: 남은 가정 3건을 그대로 두고 다음 단계로 넘길까요, 지금 후속 질문으로 바꿔 확정할까요?
- **선택지**: A. Accept assumptions / B. Convert to follow-up questions
- **사용자 답(원문)**: "B. Convert to follow-up questions"
- **결정 요약**: 가정 3건을 Q13·Q14·Q15 후속 질문으로 전환해 확정함(그 결과 D-22·D-23·D-24→D-25). 두 산출물의 `## Assumptions & Open Questions`는 이제 `None.`
- **영향 문서**: intent-statement.md, stakeholder-map.md
- **상태**: 확정

### D-27 Intent Capture 산출물 수정 요청 (승인 게이트 반려)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing (승인 게이트)
- **질문**: Intent Capture & Framing 단계가 끝났습니다. 어떻게 할까요?
- **선택지**: Approve / Request Changes
- **사용자 답(원문)**: "Request Changes"
- **이어진 질문**: 검토 지적 5건 중 어디까지 반영할까요? — 선택지 A) 5건 전부 B) R-01~R-04 C) R-01·R-02만 D) 직접 지정
- **사용자 답(원문)**: "5건 전부"
- **이유·메모**: 제품 리드 자문 검토(verdict NOT-READY)에서 Critical 1건·Major 3건·Minor 1건이 나옴. 요지는 "확정 답변이 뒷받침하는 것보다 문서가 더 많이 말하고 있다"
- **결정 요약**: 검토 지적 R-01~R-05를 모두 반영해 두 산출물을 수정한다
  - R-01: 범위 제외 목록을 Q8 답변이 열거한 9개 항목으로 한정. 근거 문서 5장에서 추가로 옮겼던 항목(FAR 상황 자동 생성, 청자 지식·함축 응답 평가, GraphRAG, 모델 재학습 등) 제거
  - R-02: 전문가 행을 "모든 세션에 있다고 전제하지 않는다"에서 "MVP 제외"로 정정
  - R-03: 기록 갱신 시점·변경 표기 규칙을 Q17로 확정해 근거 확보
  - R-04: 권한 3단계 유지를 Q18로 확정해 근거 확보
  - R-05: 문제 정의 문단에 `[Q3]` 소스 태그 추가
- **영향 문서**: intent-statement.md, stakeholder-map.md
- **상태**: 확정

### D-28 결정 기록 갱신 시점·변경 표기 규칙 (Intent Capture Q17)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q17)
- **질문**: 결정 기록의 갱신 시점과 변경 표기 규칙을 확정합니까?
- **선택지**: A) 둘 다 확정 B) 갱신 시점만 C) 변경 표기만 D) 둘 다 규칙으로 두지 않음 X) 기타
- **사용자 답(원문)**: "A. 둘 다 확정"
- **이유·메모**: 검토 지적 R-03 해소. 지금까지 실제로 운영해 온 방식을 규칙으로 확정함
- **결정 요약**: 답변을 받은 같은 단계에서 결정 기록을 갱신한다. 바뀐 결정은 이전 항목을 지우지 않고 `변경됨 → D-xx`로 표기한 뒤 새 항목을 추가한다
- **영향 문서**: stakeholder-map.md, docs/decisions/decision-log.md
- **상태**: 확정

### D-29 보호자 열람 권한 단계 수 (Intent Capture Q18)
- **일시**: 2026-09-16
- **단계**: Intent Capture & Framing
- **질문 파일**: `.../intent-capture-questions.md` (Q18)
- **질문**: 보호자 열람 권한을 몇 단계로 둡니까?
- **선택지**: A) 세 단계 유지(NONE/SUMMARY/FULL) B) 두 단계 꺼짐·전체 C) 두 단계 꺼짐·요약만 D) Requirements Analysis에서 결정 X) 기타
- **사용자 답(원문)**: "A. 세 단계 유지"
- **이유·메모**: 검토 지적 R-04 해소. 세 단계는 그동안 선택되지 않은 옵션과 질문 서두에만 등장해 확정 근거가 없던 상태였음
- **결정 요약**: 보호자 열람 권한 수준은 NONE / SUMMARY / FULL 세 단계를 유지하고 사용자가 고른다
- **영향 문서**: intent-statement.md, stakeholder-map.md, 04_domain-model.md(SharingSetting.level)
- **상태**: 확정


### D-30 기술 스택 전환 — 단일 백엔드 (Feasibility Q1, F1)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/feasibility/feasibility-questions.md` (Q1, F1)
- **질문**: Java core + Python analysis 2-서비스 구성을 그대로 갑니까?
- **선택지**: A) 2-서비스 유지 B) 대체안 전환(React + Python FastAPI + PostgreSQL) C) Java 단일로 시작 D) 비교 먼저 X) 기타
- **사용자 답(원문)**: "B. 대체안으로 전환한다 (React + Python FastAPI + PostgreSQL 단일 백엔드)" → 확인 질문 F1 에서 "A. 전환 확정"
- **이유·메모**: D-01 이 남겨 둔 분기를 닫음. 전환이 무효화하는 확정 항목 9건(Spring Boot, Gradle, JPA·Flyway, JUnit·Mockito·Testcontainers, springdoc-openapi, core 패키지 구조, 코드 예시 3건, analysis DB 접근 금지 규칙, 컨테이너 4개)을 열거해 확인받은 뒤 반영함
- **결정 요약**: 백엔드는 Python 3.11 + FastAPI 단일 서비스. Java·Spring Boot 를 쓰지 않는다. 컨테이너는 frontend/backend/postgres 3개
- **영향 문서**: 02_tech-environment.md(전면), feasibility-assessment.md, constraint-register.md(TC-01, TC-04, TC-14), raid-log.md(R1, R2, R3, I1, I3)
- **상태**: 확정 (D-01 을 대체함)

### D-31 기술 버전 조합 확정 (Feasibility Q2)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (Q2)
- **질문**: 기존 명세가 적어 둔 버전 조합을 그대로 확정합니까?
- **선택지**: A) 그대로 확정 B) Java 버전만 변경 C) Node/React 계열만 변경 D) 설치본 확인 후 X) 기타
- **사용자 답(원문)**: "A. 그대로 확정한다"
- **이유·메모**: D-30 과 충돌하여 F1 에서 범위를 좁힘. Java 부분은 무효
- **결정 요약**: React 18 / TypeScript 5 / Vite 5 / PostgreSQL 16 / Python 3.11 + FastAPI 로 확정. 가정 A-09 중 Java 21·Spring Boot 3.3 은 무효
- **영향 문서**: 02_tech-environment.md, constraint-register.md(TC-02, TC-03)
- **상태**: 확정

### D-32 로컬 실행 환경 (Feasibility Q3)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (Q3)
- **질문**: 로컬 실행 환경에 제약이 있습니까?
- **선택지**: A) 제약 없음 B) 자원 빠듯 C) Docker 불가 D) WSL2 제약 고려 X) 기타
- **사용자 답(원문)**: "A. 제약 없다 — Docker Desktop(또는 동등한 런타임)이 있고 컨테이너 4개를 돌릴 수 있다"
- **결정 요약**: 로컬 실행에 자원 제약 없음. 클라우드 배포 없음 유지. 컨테이너는 D-30 에 따라 3개로 줄어듦
- **영향 문서**: constraint-register.md(TC-04, SC-01), raid-log.md(D5)
- **상태**: 확정

### D-33 일정과 인원 (Feasibility Q4, F4)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (Q4, F4)
- **질문**: 일정과 투입 인원은 어떻게 됩니까? / 외부 마감은 언제입니까?
- **선택지**: A) 1인 기한 없음 B) 1인 기한 있음 C) 여러 명 D) 외부 마감 X) 기타
- **사용자 답(원문)**: "D. 시연·제출 등 외부 마감이 있다" → F4 에서 "11월 5일까지, 개발 인원 5인"
- **이유·메모**: Q4 선택지에 인원 정보가 없어 F4 에서 확인. team-formation(1.5)이 범위 밖이라 이 단계에서 확정
- **결정 요약**: 마감 2026-11-05(약 7주), 개발 인원 5인
- **영향 문서**: constraint-register.md(OC-01, OC-02), raid-log.md(R5)
- **상태**: 확정

### D-34 개인정보·규제 제약 처리 수준 (Feasibility Q5)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (Q5)
- **질문**: 개인정보·규제 제약을 이번 MVP에서 어느 수준까지 다룹니까?
- **선택지**: A) 기록만 B) 기록+핵심 구현 C) 기록 안 함 D) 기록+암호화·감사로그 X) 기타
- **사용자 답(원문)**: "C. 기록하지 않는다 — 합성 데이터 전용 테스트이므로 규제 항목은 이번 범위에서 제외한다"
- **이유·메모**: 규제가 없다는 판정이 아니라 이번 범위의 제약으로 기록하지 않는다는 결정. 정정·삭제(F07)와 보호자 열람 권한은 intent-capture 에서 확정된 제품 기능이므로 그대로 유지됨을 통합 요약에서 확인받음
- **결정 요약**: 규제 제약 칸을 비운다. 제품 기능 F07 과 권한 NONE/SUMMARY/FULL 은 유지
- **영향 문서**: constraint-register.md(§4, SC-08), raid-log.md(A2)
- **상태**: 확정

### D-35 운영 파라미터 — 설정값 유지 (Feasibility Q6)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (Q6)
- **질문**: 운영 파라미터의 기본값을 확정합니까?
- **선택지**: A) 모두 확정 B) 보관기간 변경 C) 녹음길이 변경 D) 설정값으로만 X) 기타
- **사용자 답(원문)**: "D. 설정값으로만 두고 지금은 확정하지 않는다 — 기본값은 유지하되 언제든 바꿀 수 있게 한다"
- **결정 요약**: 녹음 5분 / Mock 분석 3초 / 비교 불충분 3회 / 원음 보관 30일은 확정하지 않고 설정값으로 노출한다. 코드에 하드코딩하지 않는다
- **영향 문서**: constraint-register.md(§5 PM-01~PM-04)
- **상태**: 확정 (가정 A-05~A-08 은 "설정값"으로 재분류, 확정값 아님)

### D-36 STT·LLM live 어댑터 범위 (Feasibility Q7, F2)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (Q7, F2)
- **질문**: STT·LLM의 실제 연동 어댑터를 이번 범위에서 어디까지 만듭니까?
- **선택지**: A) 인터페이스+Mock만 B) live 스텁까지 C) live 실제 구현 D) Mock만 X) 기타
- **사용자 답(원문)**: "C. live 구현체를 실제로 동작하게 만든다" → 확인 질문 F2 에서 "A. live 를 만들되 기본 실행과 SM1 검증은 Mock 으로 유지"
- **이유·메모**: C 가 승인된 의도 서술("실제 STT·LLM 연동은 이 목적에 필요하지 않다")과 충돌하여, 영향받는 확정 항목 6건을 열거해 확인받음. 기본 경로를 Mock 으로 유지해 의도 서술의 취지를 보존
- **결정 요약**: live 구현체를 만들되 기본 실행과 성공 기준 SM1 검증은 Mock. live 는 `ANALYSIS_MODE=live` 로만 켜지는 선택 경로
- **영향 문서**: intent-statement.md(Initiative Trigger 문장 갱신 필요 — raid-log.md I2), 01_vision.md, constraint-register.md(SC-04, SC-05, TC-06)
- **상태**: 확정

### D-37 live 제공자 선택 (Feasibility F3)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (F3)
- **질문**: live 어댑터를 만든다면 어느 제공자를 씁니까?
- **선택지**: A) OpenAI 전부 B) Whisper+Claude C) 로컬 오픈소스 D) 미정 X) 기타
- **사용자 답(원문)**: "D. 아직 정하지 않았다 — 인터페이스만 맞춰 두고 제공자는 나중에 고른다"
- **결정 요약**: 제공자 미정. 인터페이스만 고정하고 live 구현체 작성은 제공자 결정 후로 미룬다
- **영향 문서**: raid-log.md(R4, D2), constraint-register.md(PM-02 단서)
- **상태**: 미결정 (의도적 보류)

### D-38 팀의 Python 역량 (Feasibility F5)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (F5)
- **질문**: 5인의 Python·FastAPI 경험은 어느 정도입니까?
- **선택지**: A) 대부분 경험 B) 일부만 C) 거의 없음 D) 모름 X) 기타
- **사용자 답(원문)**: "전원 AI의 도움을 받으며 진행, 일부 Python 경험"
- **이유·메모**: D-01 의 원래 근거가 "현재 배운 것은 React+Java" 였으므로, D-30 전환 후 가장 큰 기술 위험으로 식별됨
- **결정 요약**: 전원 AI 지원을 받으며 진행하고 Python 경험은 일부. 위험 R1 로 관리한다
- **영향 문서**: constraint-register.md(OC-04), raid-log.md(R1, A5)
- **상태**: 확정

### D-39 5인 역할 분담 (Feasibility F6)
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints
- **질문 파일**: `.../feasibility-questions.md` (F6)
- **질문**: 5인의 역할을 어떻게 나눕니까?
- **선택지**: A) 프론트2/백3 B) 프론트1/백3/QA1 C) 전원 풀스택 D) 미정 X) 기타
- **사용자 답(원문)**: "C. 전원 풀스택"
- **이유·메모**: team-formation(1.5)이 범위 밖이라 이 단계에서 확정
- **결정 요약**: 5인 전원 풀스택, 작업 단위별로 그때그때 분담. 고정 역할 없음
- **영향 문서**: constraint-register.md(OC-03), raid-log.md(A5), delivery-planning(2.9) 입력
- **상태**: 확정


### D-40 Feasibility & Constraints 산출물 승인
- **일시**: 2026-09-16
- **단계**: Feasibility & Constraints (승인 게이트)
- **질문**: Feasibility & Constraints 단계 산출물 승인 여부
- **선택지**: A) Approve B) Request Changes
- **사용자 답(원문)**: "Approve"
- **결정 요약**: feasibility-assessment.md, constraint-register.md, raid-log.md, feasibility-questions.md 승인. 다음 단계는 Scope Definition(1.4)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/feasibility/` 전체
- **상태**: 확정


### D-41 F07 정정·삭제의 우선순위 (Scope Definition Q1)
- **일시**: 2026-09-16
- **단계**: Scope Definition
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/scope-definition/scope-definition-questions.md` (Q1)
- **질문**: F01~F07 중 SM1 경로 밖에 있는 F07 을 어떻게 다룹니까?
- **선택지**: A) 전부 Must B) F07 은 Should C) F07 분할 D) F07 제외 X) 기타
- **사용자 답(원문)**: "B. F01~F06 은 Must, F07 은 Should"
- **이유·메모**: 성공 기준 SM1 이 열거한 여섯 단계(업로드→전사 확인→리포트→목표 선택→모의 대화→기록) 어디에도 정정·삭제가 들어가지 않음
- **결정 요약**: F01~F06 은 Must, F07 정정·삭제는 Should. 종단 흐름을 먼저 완성한다
- **영향 문서**: scope-document.md(§3.1, §3.2), intent-backlog.md(PU-08)
- **상태**: 확정

### D-42 화면 범위 (Scope Definition Q2)
- **일시**: 2026-09-16
- **단계**: Scope Definition
- **질문 파일**: `.../scope-definition-questions.md` (Q2)
- **질문**: 화면 15개 전부를 이번 범위에 넣습니까?
- **선택지**: A) 15개 전부 Must B) C2~C5 는 Should C) C4 만 추가 Must D) 기능 우선순위만 X) 기타
- **사용자 답(원문)**: "B. A1~A5 · B1~B5 · C1 은 Must, C2~C5 는 Should"
- **결정 요약**: 화면 A1~A5, B1~B5, C1 은 Must. C2~C5 는 Should
- **영향 문서**: scope-document.md(§3.1 M7~M9, §3.2 S2~S3), intent-backlog.md(PU-07, PU-09)
- **상태**: 확정

### D-43 대화 가져오기 경로 (Scope Definition Q3)
- **일시**: 2026-09-16
- **단계**: Scope Definition
- **질문 파일**: `.../scope-definition-questions.md` (Q3)
- **질문**: 브라우저에서 직접 녹음하는 경로를 이번 범위에 넣습니까?
- **선택지**: A) 둘 다 Must B) 업로드만 Must C) 업로드만 D) 녹음만 Must X) 기타
- **사용자 답(원문)**: "A. 두 경로 모두 Must"
- **이유·메모**: SM1 은 업로드만 요구하지만 실제 사용에서는 녹음이 주 진입점
- **결정 요약**: 파일 업로드와 브라우저 직접 녹음을 모두 Must 로 만든다. 다만 축소 압박이 오면 SM1 여섯 단계가 직접 녹음보다 우선한다
- **영향 문서**: scope-document.md(§3.1 M1, §4), intent-backlog.md(PU-01)
- **상태**: 확정

### D-44 인증과 보호자 권한의 우선순위 (Scope Definition Q4, F1, F2)
- **일시**: 2026-09-16
- **단계**: Scope Definition
- **질문 파일**: `.../scope-definition-questions.md` (Q4, F1, F2)
- **질문**: 로그인·회원가입을 이번 범위에 넣습니까? / C5 한 화면 안에 Must 와 Should 가 섞인 것을 어떻게 나눕니까? / SM1 경로 밖 Must 두 건을 그대로 갑니까?
- **선택지(Q4)**: A) 정식 인증 B) 로그인만 C) 인증 없음 D) 사용자 전환만 X) 기타
- **사용자 답(원문)**: Q4 "A. 회원가입·로그인을 정식으로 만든다" → F1 "C. 보호자 권한을 Should 로 내린다" → F2 "D. 정식 인증을 Should 로 내린다 — 직접 녹음은 Must 로 유지"
- **이유·메모**: Q4=A 가 두 가지와 충돌함 — 보호자 권한을 켜는 유일한 화면 C5 가 Q2=B 로 Should 였고(F1), Q5=A 가 시연 필수선을 SM1 으로 정했는데 인증은 SM1 경로 밖이었음(F2). 두 후속 질문에서 영향 항목을 표로 열거해 확인받은 뒤 조정
- **결정 요약**: 회원가입·로그인 정식 구현과 보호자 열람 권한 동작을 모두 Should 로 내린다. Must 경로는 고정 사용자 하나로 돈다. **보호자 권한 3단계와 기본값 NONE 결정은 취소되지 않았고 만드는 시점만 뒤로 갔다.** 데이터 모델은 사용자 개념을 처음부터 갖춰 나중에 스키마를 바꾸지 않게 한다
- **영향 문서**: scope-document.md(§3.2 S4~S5), intent-backlog.md(PU-10, PU-11)
- **상태**: 확정 (Q4 의 A 는 F1·F2 로 조정됨)

### D-45 시연 필수선 (Scope Definition Q5)
- **일시**: 2026-09-16
- **단계**: Scope Definition
- **질문 파일**: `.../scope-definition-questions.md` (Q5)
- **질문**: 2026-11-05 에 반드시 보여야 하는 것은 무엇입니까?
- **선택지**: A) SM1 그대로 B) SM1+F07 C) A 흐름까지 D) 화면 전체 둘러보기 X) 기타
- **사용자 답(원문)**: "A. SM1 그대로"
- **결정 요약**: 시연 필수선은 SM1 — 합성 대화 3건이 업로드부터 기록까지 끊김 없이 이어지는 것. 범위 축소 시 이 선까지는 지킨다
- **영향 문서**: scope-document.md(§4)
- **상태**: 확정

### D-46 제작 순서 기준 (Scope Definition Q6)
- **일시**: 2026-09-16
- **단계**: Scope Definition
- **질문 파일**: `.../scope-definition-questions.md` (Q6)
- **질문**: 만드는 순서를 무엇을 기준으로 정합니까?
- **선택지**: A) 종단 슬라이스 먼저 B) 위험 큰 것 먼저 C) 가치 순서 D) 의존 순서 X) 기타
- **사용자 답(원문)**: "A. 종단 슬라이스 먼저"
- **이유·메모**: Python 역량 위험(R1)과 7주 일정 위험(R5)에 동시에 대응하는 순서
- **결정 요약**: 업로드부터 기록까지를 최소 형태로 한 번 관통시킨 뒤 각 기능의 깊이를 채운다
- **영향 문서**: scope-document.md(§5), intent-backlog.md(§4), delivery-planning(2.9) 입력
- **상태**: 확정

### D-47 병렬 작업 갈래 수 (Scope Definition Q7)
- **일시**: 2026-09-16
- **단계**: Scope Definition
- **질문 파일**: `.../scope-definition-questions.md` (Q7)
- **질문**: 5인이 동시에 붙을 수 있게 몇 갈래로 나눕니까?
- **선택지**: A) 3갈래 B) 4갈래 C) 5갈래 D) 나중에 결정 X) 기타
- **사용자 답(원문)**: "D. 지금 정하지 않는다 — 작업 단위 분해 단계에서 정한다"
- **결정 요약**: 병렬 갈래 수는 units-generation(2.7)에서 정한다. intent-backlog.md 는 proto-Unit 만 나열하고 갈래 수를 고정하지 않는다
- **영향 문서**: scope-document.md(§6), intent-backlog.md(§5)
- **상태**: 미결정 (의도적 보류, 2.7 로 이월)

### D-48 Scope Definition 산출물 승인
- **일시**: 2026-09-16
- **단계**: Scope Definition (승인 게이트)
- **질문**: Scope Definition 단계 산출물 승인 여부
- **선택지**: A) Approve B) Request Changes
- **사용자 답(원문)**: "Approve"
- **결정 요약**: scope-document.md, intent-backlog.md, scope-definition-questions.md 승인. 다음 단계는 Approval & Handoff(1.7)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/scope-definition/` 전체
- **상태**: 확정


### D-49 의도 서술의 STT·LLM 문장 갱신 (Approval & Handoff Q1)
- **일시**: 2026-09-16
- **단계**: Approval & Handoff
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/ideation/approval-handoff/approval-handoff-questions.md` (Q1)
- **질문**: 의도 서술의 STT·LLM 문장을 어떻게 갱신합니까?
- **선택지**: A) 지금 고침 B) 2.3 에서 고침 C) 고치지 않음 D) 요약서에 대체 명시 X) 기타
- **사용자 답(원문)**: "A. 지금 고친다"
- **이유·메모**: 승인된 의도 서술의 "실제 STT·LLM 연동은 이 목적에 필요하지 않다"가 D-36 과 어긋나 RAID 현안 I2 로 남아 있었음. Change Control 이 relaxed 이고 사용자가 명시적으로 지시함
- **결정 요약**: `intent-statement.md` 의 Initiative Trigger 절을 갱신했다. "실제 연동은 필요하지 않다"가 아니라 "기본 실행과 SM1 검증은 Mock, live 는 선택 경로"가 현재 기준임을 명시
- **영향 문서**: intent-statement.md, initiative-brief.md, raid-log.md(I2 해소)
- **상태**: 확정

### D-50 기존 명세 `02_tech-environment.md` 재작성 (Approval & Handoff Q2)
- **일시**: 2026-09-16
- **단계**: Approval & Handoff
- **질문 파일**: `.../approval-handoff-questions.md` (Q2)
- **질문**: 기존 명세 `02_tech-environment.md` 재작성을 언제 합니까?
- **선택지**: A) 지금 B) 2.2 에서 C) 2.3 진입 전 D) 2.6 에서 X) 기타
- **사용자 답(원문)**: "A. Inception 진입 전에 지금"
- **이유·메모**: 이 문서가 Inception 의 입력이라 Java 전제로 남아 있으면 요구사항·도메인 설계가 무효 정보를 물려받음. RAID 현안 I3, 위험 R2
- **결정 요약**: `docs/input/02_tech-environment.md` 를 v2 로 전면 개정했다. Python 3.11 + FastAPI 단일 백엔드, 컨테이너 3개, pytest 계열 테스트, Python 패키지 구조와 코드 예시, 계층 경계 금지 규칙. 미정 항목(ORM·마이그레이션·패키지 관리자, 계층 경계 정의, live 제공자)은 §8 에 별도 표로 남김
- **영향 문서**: 02_tech-environment.md(전면), raid-log.md(I3 해소, R2 부분 해소), initiative-brief.md
- **상태**: 확정

### D-51 user-stories(2.4) 단계 추가 (Approval & Handoff Q3)
- **일시**: 2026-09-16
- **단계**: Approval & Handoff
- **질문 파일**: `.../approval-handoff-questions.md` (Q3)
- **질문**: 수용 기준(Given/When/Then)을 어디서 만듭니까?
- **선택지**: A) 2.3 이 맡음 B) user-stories 추가 C) 3.1 이 맡음 D) 3.6 이 맡음 X) 기타
- **사용자 답(원문)**: "B. user-stories(2.4)를 다시 넣는다" → 계획 변경 게이트에서 "Approve"
- **이유·메모**: Inception 지침이 수용 기준을 Given/When/Then 형식으로 요구하는데 그 일을 맡을 단계가 계획에 없었음. 이대로 가면 요구사항이 검증 기준 없이 Construction 까지 감
- **결정 요약**: user-stories(2.4)를 SKIP 에서 EXECUTE 로 바꿨다. EXECUTE 단계 수 19 → 20. 수용 기준은 이 단계가 맡는다. 마감과 일정 위험 R5 는 그대로인 채 부담이 늘어난 점은 위험 R7 로 기록
- **영향 문서**: 워크플로 단계 구성(D-08 을 일부 변경), raid-log.md(R7 추가), initiative-brief.md §9
- **상태**: 확정

### D-52 이데이션 종합 판정 (Approval & Handoff Q4)
- **일시**: 2026-09-16
- **단계**: Approval & Handoff
- **질문 파일**: `.../approval-handoff-questions.md` (Q4)
- **질문**: 이데이션 종합 판정을 무엇으로 합니까?
- **선택지**: A) 진행 B) 조건부 진행 C) 보류 D) 중단 X) 기타
- **사용자 답(원문)**: "A. 진행(Go) — 조건 없이 Inception 으로 넘어간다"
- **이유·메모**: 타당성 판정의 조건부 2건(R1 팀 역량, R5 일정)은 진행을 막는 사유가 아니라 관리 대상
- **결정 요약**: 조건 없이 Inception 으로 진행한다. 위험은 RAID 로 계속 관리한다
- **영향 문서**: initiative-brief.md §10
- **상태**: 확정


### D-53 Approval & Handoff 산출물 승인 및 Ideation 종료
- **일시**: 2026-09-16
- **단계**: Approval & Handoff (승인 게이트)
- **질문**: Approval & Handoff 단계 산출물 승인 여부 및 Ideation 종료
- **선택지**: A) Approve B) Request Changes C) Reject Initiative
- **사용자 답(원문)**: "Approve"
- **결정 요약**: initiative-brief.md, decision-log.md, approval-handoff-questions.md 승인. Ideation → Inception 단계 경계 검증 통과(차단 없음, 경고 3건 이월). IDEATION 4단계 전부 완료. 다음 단계는 Practices Discovery(2.2)
- **영향 문서**: `aidlc/.../ideation/approval-handoff/` 전체, `aidlc/.../verification/phase-check-ideation.md`
- **상태**: 확정


### D-54 Python 도구 확정 (Practices Discovery Q6)
- **일시**: 2026-09-17
- **단계**: Practices Discovery
- **질문 파일**: `.../inception/practices-discovery/practices-discovery-questions.md` (Q6)
- **질문**: ORM·마이그레이션 도구·패키지 관리자를 여기서 닫습니까?
- **선택지**: A) 여기서 닫는다 B) 패키지 관리자만 변경 C) ORM만 변경 D) domain-design 으로 이월 X) 기타
- **사용자 답(원문)**: "A. 여기서 닫는다 — SQLAlchemy 2.0(동기) / Alembic / uv 로 확정"
- **결정 요약**: ORM 은 SQLAlchemy 2.0(동기), 마이그레이션은 Alembic, 패키지 관리자는 uv. 제약 TC-15 와 의존 D3 가 닫혔다
- **영향 문서**: constraint-register.md TC-15, raid-log.md D3, feasibility-assessment.md §5, initiative-brief.md §6
- **상태**: 확정

### D-55 저장소 운영과 병합 전 검사 (Practices Discovery Q1)
- **일시**: 2026-09-17
- **단계**: Practices Discovery
- **질문 파일**: `.../inception/practices-discovery/practices-discovery-questions.md` (Q1)
- **질문**: 저장소를 만들고 어떻게 운영합니까?
- **선택지**: A) 로컬만 + pre-push B) 원격 + PR + Actions C) 원격 + 직접 push D) 나중에 정한다 X) 기타
- **사용자 답(원문)**: "B. 원격(GitHub 등)을 쓰고 PR 로 병합한다 — 검사는 GitHub Actions 로 강제한다"
- **이유·메모**: 저장소 생성 전에 `.gitignore` 를 먼저 고친다. 현재 `node_modules` 만 있고 `.env`, `__pycache__/`, `.venv/`, 음성 업로드 디렉터리가 빠져 있다
- **결정 요약**: 원격 저장소 + PR 병합. 병합 전 검사는 GitHub Actions 가 강제한다 (제약 TC-16)
- **영향 문서**: constraint-register.md TC-16, raid-log.md A6, team-practices.md
- **상태**: 확정

### D-56 ci-pipeline(3.7) 재삽입 (Practices Discovery FU3)
- **일시**: 2026-09-17
- **단계**: Practices Discovery (후속 질문)
- **질문 파일**: `.../inception/practices-discovery/practices-discovery-questions.md` (FU3)
- **질문**: GitHub Actions 검사는 누가 만듭니까?
- **선택지**: A) CI 단계를 다시 넣는다 B) 첫 Bolt 에 포함 C) Actions 없이 pre-push D) 나중에 정한다 X) 기타
- **사용자 답(원문)**: "A. CI 파이프라인 단계(3.7)를 계획에 다시 넣는다 — 그 단계가 Actions 워크플로를 만든다"
- **이유·메모**: Actions 워크플로 파일을 작성할 단계가 계획에 없었다. 건너뛴 단계의 일이 주인 없이 남아 있던 경우다
- **결정 요약**: ci-pipeline(3.7)을 EXECUTE 로. EXECUTE 단계 20 → 21
- **영향 문서**: aidlc-state.md, raid-log.md R7, initiative-brief.md §9
- **상태**: 확정 (D-08·D-51 의 단계 구성을 다시 변경)

### D-57 테스트 방침 (Practices Discovery Q3·Q4·FU2)
- **일시**: 2026-09-17
- **단계**: Practices Discovery
- **질문 파일**: `.../inception/practices-discovery/practices-discovery-questions.md` (Q3, Q4, FU2)
- **사용자 답(원문)**: Q3 "C. 전부 구현 후 테스트로 단순화한다 — 방법론을 하나로 두어 헷갈리지 않게 한다" / Q4 "B. `service/` 전체에 라인 80% 하나만 건다 — 초안 그대로, 단순하다" / FU2 "B. 기대 판정표를 픽스처로 고정하는 것만 의무로 넣는다"
- **이유·메모**: 세 답을 겹치면 판정 정확성 보장이 구현 후 단위 테스트 하나로 모인다. 사용자가 이를 알고 고른 절충이며, 픽스처 고정으로 기대값의 출처만 문서에 고정했다
- **결정 요약**: 방법론은 test-after 하나. 커버리지 바닥은 `service/` 라인 80% 하나. 기대 판정은 픽스처 파일로 고정하고 단위 테스트가 그것을 읽는다
- **영향 문서**: team-practices.md `## Testing Posture`, discovered-rules.md, raid-log.md R6
- **상태**: 확정

### D-58 "배포 성공"의 판정 기준 (Practices Discovery Q5)
- **일시**: 2026-09-17
- **단계**: Practices Discovery
- **질문 파일**: `.../inception/practices-discovery/practices-discovery-questions.md` (Q5)
- **선택지**: A) 기대 판정 대조까지 B) 종단 통과만 C) 시연 직전 한 번만 D) 헬스체크만 X) 기타
- **사용자 답(원문)**: "B. 초안대로 둔다 — 끊김 없이 지나가면 성공. 판정 정확성은 별도 단위 테스트가 본다"
- **결정 요약**: `docker compose up --build` 후 헬스체크 통과 + 합성 대화 3건의 종단 통과. 기대 판정 대조는 종단 실행의 성공 조건이 아니다
- **영향 문서**: team-practices.md `## Deployment`, intent-statement.md §Success Metrics
- **상태**: 확정

### D-59 F07 을 Should 에서 Must 로 (Practices Discovery Q7 / FU1)
- **일시**: 2026-09-17
- **단계**: Practices Discovery (Q7), 후속 확인 (FU1)
- **질문 파일**: `.../inception/practices-discovery/practices-discovery-questions.md` (Q7, FU1)
- **질문**: 합성 대화 3건 중 일부 검증 항목이 Must 범위 밖입니다. 어떻게 합니까?
- **선택지**: A) 그대로 둔다 B) F07 을 Must 로 C) 그대로 두되 명시 D) S3 를 검증 대상에서 제외 X) 기타
- **사용자 답(원문)**: Q7 "B. F07 의 두 기능만 Must 로 끌어올린다 — S3 를 원래 의도대로 전부 확인한다" / FU1 "A. 전부 그대로 반영한다"
- **이유·메모**: 합성 대화 S3 의 검증 항목 2(전사 정정 후 재검토 표시)와 4(삭제 시 연결 항목 처리)가 F07 에 걸려 있어, F07 없이는 S3 가 원래 확인하려던 것의 절반이 확인되지 않는다
- **결정 요약**: F07(정정·삭제)을 Must 로 승격. 취소가 아니라 승격이며 만드는 시점만 앞으로 당겨졌다
- **영향 문서**: scope-document.md §3.1·§3.2·§4·§5·§7·§8, intent-backlog.md PU-08·§2·§3·§4, initiative-brief.md §5
- **상태**: 확정 (D-13 의 F07 등급을 변경)

### D-60 화면 C5 분할과 F07 의 제작 순서 (Scope Definition F3·F4·F5)
- **일시**: 2026-09-17
- **단계**: Scope Definition (되돌리기 회차)
- **질문 파일**: `.../ideation/scope-definition/scope-definition-questions.md` (F3, F4, F5)
- **사용자 답(원문)**: F3 "B. C5 화면 전체를 Must 로 올린다" → F5 에서 "C. F3 을 A 로 바꾼다 — C5 를 쪼개 삭제 관련 요소만 Must 로 올린다" / F4 "A. 3단계로 — Must 잔여에 직접 녹음과 함께 넣는다"
- **이유·메모**: C5 전체를 Must 로 올리면 보호자 권한(Must)이 정식 인증(Should)에 의존하게 된다. 무효화되는 확정 항목 8건을 표로 확인한 뒤 사용자가 쪼개는 안으로 바꿨다
- **결정 요약**: C5 를 쪼갠다 — 삭제 관련 요소(기록 삭제 요청, 연결 항목 미리보기, 원음만 삭제)만 Must, 보호자 권한 전환·원음 보관 기간·서비스 안내는 Should 유지. F07 은 만드는 순서 3단계(Must 잔여)에 놓는다
- **영향 문서**: scope-document.md §3.1·§3.2·§5, intent-backlog.md PU-08·PU-11
- **상태**: 확정

### D-61 이데이션 종합 판정 재확인 (Approval & Handoff Q5)
- **일시**: 2026-09-17
- **단계**: Approval & Handoff (되돌리기 회차)
- **질문 파일**: `.../ideation/approval-handoff/approval-handoff-questions.md` (Q5)
- **질문**: 이번 회차에 부담이 더 늘었습니다. 종합 판정을 유지합니까?
- **선택지**: A) 진행(Go) 유지 B) 조건부 진행 C) 진행하되 범위 축소 D) 보류 X) 기타
- **사용자 답(원문)**: "A. 진행(Go) 을 유지한다 — 늘어난 부담은 관리 대상이며 판정을 바꾸지 않는다"
- **이유·메모**: 부담을 늘린 것 셋(F07 승격, Must 비율 64%→73%, 단계 20→21)과 줄인 것 둘(도구 3종 확정, 테스트 방침 단순화)을 대조한 결과
- **결정 요약**: 조건 없이 Inception 으로 진행. 늘어난 부담은 delivery-planning(2.9)의 일정 재검증에 넣는다
- **영향 문서**: initiative-brief.md §10
- **상태**: 확정 (D-52 재확인)

### D-62 화면 크기와 지원 범위 (Requirements Analysis Q1, FU1)
- **일시**: 2026-09-17
- **단계**: Requirements Analysis
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/requirements-analysis-questions.md` (Q1, FU1)
- **질문**: 어떤 화면 크기와 브라우저에서 동작해야 합니까? / 노트북 반응형을 반영하면 바뀌는 확정 항목이 있습니다. 그대로 반영합니까?
- **선택지(Q1)**: A) 375px 만 보장 B) 모바일 기준 + 노트북에서 가운데 정렬 C) 모바일·노트북 완전 반응형 D) 375px + Chrome 한정 X) 기타
- **선택지(FU1)**: A) 반응형 + E2E 는 모바일 폭만 B) 반응형 + E2E 두 폭 C) Q1 을 B 로 변경 D) 노트북 레이아웃은 Should X) 기타
- **사용자 답(원문)**: Q1 "C. 모바일과 노트북 화면을 모두 반응형으로 제대로 지원한다" → FU1 "D. 모바일 폭은 Must, 노트북 반응형 레이아웃은 Should 로 둔다 — 종단 흐름이 선 뒤에 만든다"
- **이유·메모**: Q1=C 가 제약 TC-02(모바일 웹 375px 기준), UI 명세 §1 레이아웃, 팀 관행 "E2E 는 3건에서 늘리지 않는다", 위험 R5 를 건드려 영향 항목 5건을 표로 확인받음. 팀 관행과의 충돌을 먼저 짚음
- **결정 요약**: 모바일 폭(375px 기준) 화면은 Must. 노트북 폭 반응형 레이아웃은 Should — 취소가 아니라 만드는 시점만 뒤로 갔다. TC-02 와 팀 관행(E2E 3건)은 바뀌지 않는다. 가정 A-03 이 닫힘
- **영향 문서**: requirements.md, 03_ui-spec.md §1(Should 시점에 노트북 레이아웃 추가), 가정 A-03
- **상태**: 확정

### D-63 모의 대화 매체 (Requirements Analysis Q2)
- **일시**: 2026-09-17
- **단계**: Requirements Analysis
- **질문 파일**: `.../inception/requirements-analysis/requirements-analysis-questions.md` (Q2)
- **질문**: 모의 대화(화면 B3)는 텍스트로만 주고받습니까?
- **선택지**: A) 텍스트만 B) 음성 입력도 허용 C) 텍스트만 + 음성 입력은 확장 후보로 범위 밖에 기록 D) 텍스트만, 키보드 받아쓰기는 막지 않음 X) 기타
- **사용자 답(원문)**: "C. 텍스트로만 하되, 음성 입력은 이후 확장 후보로 요구사항의 범위 밖 항목에 적어 둔다"
- **결정 요약**: 모의 대화는 입력·출력 모두 텍스트. 음성 입력은 범위 밖(확장 후보). 가정 A-04 가 닫힘
- **영향 문서**: requirements.md, 가정 A-04
- **상태**: 확정

### D-64 행동 묶음 판정 기준 (Requirements Analysis Q3)
- **일시**: 2026-09-17
- **단계**: Requirements Analysis
- **질문 파일**: `.../inception/requirements-analysis/requirements-analysis-questions.md` (Q3)
- **질문**: 행동 묶음 3종의 판정 기준을 무엇으로 확정합니까?
- **선택지**: A) 초안 표 그대로 확정 B) 확정 + 청소년 예시 보강을 3.1 에 C) 개발용 기준(변경 가능)으로 버전 관리 D) 2.6 에서 다시 정함 X) 기타
- **사용자 답(원문)**: "A. 초안 표를 그대로 이번 MVP 의 판정 기준으로 확정한다 — 화면과 문서에 "공식 척도가 아님"을 함께 밝힌다"
- **결정 요약**: `04_domain-model.md` §4 의 행동 묶음 조작적 정의를 이번 MVP 판정 기준으로 확정. 화면과 문서에 공식 척도가 아님을 밝힌다. 가정 A-10 이 닫힘
- **영향 문서**: requirements.md, 04_domain-model.md §4(변경 없음), 가정 A-10
- **상태**: 확정

### D-65 "분석이 이상해요" 버튼의 동작 (Requirements Analysis Q4)
- **일시**: 2026-09-17
- **단계**: Requirements Analysis
- **질문 파일**: `.../inception/requirements-analysis/requirements-analysis-questions.md` (Q4)
- **질문**: 리포트의 "분석이 이상해요" 버튼을 누르면 무슨 일이 일어납니까?
- **선택지**: A) 저장만 B) A3·맥락 입력으로 돌려보내 고치고 재분석 C) 저장 + 고칠 곳 안내 D) 보류 섹션으로 옮기고 저장 X) 기타
- **사용자 답(원문)**: "C. A와 B 둘 다 — 요청을 저장하고, 고칠 곳이 전사·맥락이면 그 화면으로 안내한다"
- **이유·메모**: 요청을 받아 볼 전문가가 MVP 제외라 처리 방식이 어디에도 없었음
- **결정 요약**: 수정 요청을 저장한다(판정은 바뀌지 않음). 고칠 곳이 전사면 A3, 맥락이면 맥락 입력으로 안내한다
- **영향 문서**: requirements.md
- **상태**: 확정

### D-66 재분석 위치와 "재검토 필요" 표시 (Requirements Analysis Q5, FU3)
- **일시**: 2026-09-17
- **단계**: Requirements Analysis
- **질문 파일**: `.../inception/requirements-analysis/requirements-analysis-questions.md` (Q5, FU3)
- **질문**: 전사를 고친 뒤 "다시 분석하기"는 어느 화면에서 합니까? / "재검토 필요" 표시는 Must 화면 어디에 보입니까?
- **선택지(Q5)**: A) A3 에서 다시 분석 B) A4 에 표시와 버튼 C) C4 재분석 부분만 Must D) A와 B 둘 다 X) 기타
- **선택지(FU3)**: A) A3 상단 안내 B) A4 장면별 배지 C) A와 B 둘 다 D) 데이터에만, 배지는 C4 때 X) 기타
- **사용자 답(원문)**: Q5 "A. 대화 내용 확인 화면(A3)에서 고친 뒤 "이대로 분석하기"를 다시 누르면 재분석된다 — 새 판정이 추가되고 이전 판정은 지워지지 않는다" → FU3 "A. A3 상단에 안내한다 — 고친 발화가 있으면 "이 대화의 기존 분석은 다시 확인이 필요해요"와 영향받은 판정 수를 보여 준다"
- **이유·메모**: 명세상 재분석 버튼과 재검토 배지는 Should 화면 C4 에만 있어, F07 을 Must 로 올린 이유인 합성 대화 S3 검증 항목 2 를 Must 범위로 끝까지 확인할 수 없었음
- **결정 요약**: 재분석은 A3 에서 고친 뒤 "이대로 분석하기"로 한다. 새 판정이 추가되고 이전 판정은 남는다. 재검토 필요 표시는 A3 상단 안내(영향받은 판정 수 포함)로 Must 에 들어간다. C4 의 재분석 버튼·배지는 Should 그대로
- **영향 문서**: requirements.md, 03_ui-spec.md A3
- **상태**: 확정

### D-67 Mock 모드의 합성 대화 연결 (Requirements Analysis Q6)
- **일시**: 2026-09-17
- **단계**: Requirements Analysis
- **질문 파일**: `.../inception/requirements-analysis/requirements-analysis-questions.md` (Q6)
- **질문**: Mock 모드에서 올린 파일이나 녹음은 합성 대화 3건 중 무엇으로 처리됩니까?
- **선택지**: A) 파일 이름으로, 없으면 전사 실패 B) A2 에 합성 대화 선택 칸 C) 파일 이름으로, 없으면 S1 D) 선택 칸, 녹음은 S1 X) 기타
- **사용자 답(원문)**: "C. A와 같되, 키가 없는 파일과 브라우저 녹음은 S1(`conv_repair_01`)로 처리한다"
- **결정 요약**: Mock 모드에서 파일 이름에 conversationKey 가 있으면 그 합성 대화로 처리한다. 키가 없는 파일과 브라우저 녹음은 S1(`conv_repair_01`)로 처리한다
- **영향 문서**: requirements.md
- **상태**: 확정

### D-68 접근성 수준 (Requirements Analysis Q7)
- **일시**: 2026-09-17
- **단계**: Requirements Analysis
- **질문 파일**: `.../inception/requirements-analysis/requirements-analysis-questions.md` (Q7)
- **질문**: 접근성은 어느 수준까지 요구합니까?
- **선택지**: A) 기본만 B) WCAG 2.1 AA 핵심 항목만 C) WCAG 2.1 AA 전체 D) 요구사항 없음 X) 기타
- **사용자 답(원문)**: "B. WCAG 2.1 AA 중 핵심 항목만 — A에 더해 글자 대비 4.5:1 이상, 터치 영역 44px 이상, 키보드로 주요 흐름을 끝까지 조작 가능"
- **결정 요약**: 모든 버튼·입력에 이름표, 색만으로 의미 전달 금지, 글자 대비 4.5:1 이상, 터치 영역 44px 이상, 키보드로 주요 흐름을 끝까지 조작 가능
- **영향 문서**: requirements.md
- **상태**: 확정

### D-69 보호자 열람 범위와 연결 방식 (Requirements Analysis Q8, FU2)
- **일시**: 2026-09-17
- **단계**: Requirements Analysis
- **질문 파일**: `.../inception/requirements-analysis/requirements-analysis-questions.md` (Q8, FU2)
- **질문**: SUMMARY 와 FULL 은 각각 무엇을 보여 줍니까? / 보호자는 어떻게 들어와서 어느 화면에서 봅니까?
- **선택지(Q8)**: A) 요약=목표·추이 / 전체=+리포트, 전사·원음 제외 B) 전체=+전사 원문 C) 전체=원음까지 D) 지금 정하지 않음 X) 기타
- **선택지(FU2)**: A) 보호자 계정 + 사용자 초대 + 보호자 전용 읽기 화면 B) 열람 링크 C) 계정 + 기존 화면 재사용 D) 지금 정하지 않음 X) 기타
- **사용자 답(원문)**: Q8 "A. SUMMARY = 목표와 목표별 추이(나의 기록 C1 수준) / FULL = 거기에 더해 리포트(A4 수준)까지. 전사 원문과 원음은 두 단계 모두 보이지 않는다" → FU2 "A. 보호자도 자기 계정으로 로그인하고, 사용자가 보호자를 초대(초대 코드 등)해 연결한다. 보호자 전용 읽기 화면을 새로 둔다"
- **이유·메모**: 권한 3단계(D-29)와 기본값 NONE(D-25)은 확정이었으나 단계별 내용과 보호자 접근 경로가 어디에도 없었음. 보호자 전용 읽기 화면은 UI 명세 15개 화면에 없는 **새 화면**이며 근거는 이 답이다. 만드는 시점은 Should(S4·S5) 그대로
- **결정 요약**: SUMMARY = 목표와 목표별 추이, FULL = + 리포트. 전사 원문과 원음은 보호자에게 보이지 않는다. 보호자는 자기 계정으로 로그인하고 사용자의 초대로 연결되며, 보호자 전용 읽기 화면에서 본다. 권한은 사용자가 켜고 기본값은 NONE 그대로
- **영향 문서**: requirements.md, 04_domain-model.md(SharingSetting, 초대), 03_ui-spec.md(보호자 읽기 화면 추가 — Should 시점)
- **상태**: 확정

### D-70 Requirements Analysis 산출물 승인
- **일시**: 2026-09-17
- **단계**: Requirements Analysis (승인 게이트)
- **질문**: Requirements Analysis 단계 산출물 승인 여부
- **선택지**: A) Approve B) Request Changes
- **사용자 답(원문)**: "Approve"
- **이유·메모**: 제품 리드 자문 검토 결과 준비됨(치명 0 / 중요 1 / 경미 3). R-01(재분석 후 옛 판정과 새 판정의 집계 분모 처리 미정), R-02(시나리오 변형의 "가까운 맥락" 기준 없음), R-03(삭제 "일부 완료" 조건 없음), R-04(보탠 해석 2건이 요약 확인으로만 승인됨)를 승인과 함께 감수한 위험으로 기록. 열린 질문 OQ1(Must 화면에서 Should 화면으로 가는 이동)은 user-stories(2.4)가 담당
- **결정 요약**: requirements.md(기능 15묶음·세부 64개, 비기능 14개), requirements-analysis-questions.md 승인. 다음 단계는 User Stories(2.4)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/requirements-analysis/` 전체
- **상태**: 확정

### D-71 화면이 없는 요구사항의 스토리 처리 (User Stories Q1, FU1)
- **일시**: 2026-09-17
- **단계**: User Stories
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/user-stories/user-stories-questions.md` (Q1, FU1)
- **질문**: 화면이 없는 요구사항은 스토리로 어떻게 다룹니까? / "시연 운영자" 페르소나는 어디까지 맡습니까?
- **선택지(Q1)**: A) 스토리 없이 하위 단계로 넘김 B) 시연 운영자 페르소나 C) 체감 NFR 만 수용 기준에 녹임 D) 기술 스토리 별도 X) 기타
- **선택지(FU1)**: A) 시연자 체감 4항목만 B) 화면 없는 것 전부 C) 4항목만, 품질은 하위로 D) A + 보안·데이터 X) 기타
- **사용자 답(원문)**: Q1 "B. "시연 운영자" 페르소나를 따로 세워 FR1.5·NFR10 같은 항목을 스토리로 쓴다 — 이해관계자 목록(D-23)은 바꾸지 않고 스토리 작성용으로만 둔다" → FU1 "A. 시연자가 직접 겪는 네 항목(FR1.5, FR11.1, NFR5, NFR10)만 운영자 스토리로 쓴다. 사용자가 체감하는 품질(접근성 NFR2, 화면 상태 NFR9, 문구 NFR7·NFR8, 화면 폭 NFR1)은 사용자 스토리의 수용 기준에 녹이고, 나머지(NFR3·NFR4·NFR6·NFR11~NFR14, FR11.2)는 추적표에서 담당 하위 단계로 넘긴다"
- **이유·메모**: 화면 없는 품질 속성까지 운영자 스토리로 쓰면 가치 문장이 억지가 되어 범위를 FU1 로 좁힘. 이해관계자는 제품 사용자만이라는 D-23 은 바뀌지 않음
- **결정 요약**: "시연 운영자" 페르소나는 스토리 작성용이며 FR1.5·FR11.1·NFR5·NFR10 네 항목만 맡는다. NFR1·NFR2·NFR7·NFR8·NFR9 는 사용자 스토리 수용 기준에, NFR3·NFR4·NFR6·NFR11~NFR14·FR11.2 는 추적표에서 하위 단계로 넘긴다
- **영향 문서**: personas.md, stories.md, traceability.json
- **상태**: 확정

### D-72 스토리 묶음 축과 크기 (User Stories Q2, Q3)
- **일시**: 2026-09-17
- **단계**: User Stories
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/user-stories/user-stories-questions.md` (Q2, Q3)
- **질문**: 스토리를 어떤 축으로 묶습니까? / 스토리 하나의 크기를 어느 정도로 잡습니까?
- **선택지(Q2)**: A) 사용자 여정 순서 B) 기능 ID 순서 C) 화면 흐름 순서 D) 여정 + 슬라이스 구분 X) 기타
- **선택지(Q3)**: A) 세부 요구당 1개(~60) B) 사용자 행동당 1개(25~35) C) 화면당 1개(~17) D) Must 는 B, Should 는 C X) 기타
- **사용자 답(원문)**: Q2 "A. 사용자 여정 순서로 — 가져오기 → 전사 확인·정정 → 리포트 → 목표 선택 → 모의 대화 → 기록 → 삭제, 그 뒤에 Should 묶음. 성공 기준 SM1 의 여섯 단계와 맞물린다" / Q3 "B. 사용자 행동 하나당 스토리 하나 — 여러 세부 요구사항을 묶어 약 25~35개, 스토리마다 수용 기준 3~6개"
- **결정 요약**: 스토리는 사용자 여정 순서로 묶고, 사용자 행동 하나당 스토리 하나(약 25~35개, 수용 기준 3~6개)
- **영향 문서**: stories.md, units-generation(2.7)·delivery-planning(2.9) 입력
- **상태**: 확정

### D-73 Must 화면에서 Should 화면으로 가는 버튼 (User Stories Q4)
- **일시**: 2026-09-17
- **단계**: User Stories
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/user-stories/user-stories-questions.md` (Q4)
- **질문**: Must 화면에서 아직 없는 Should 화면으로 가는 버튼은 어떻게 합니까?
- **선택지**: A) 목적지를 Must 화면으로 B) 버튼 숨김 C) "곧 볼 수 있어요" 안내 D) C3·C4 최소형 Must X) 기타
- **사용자 답(원문)**: "C. 버튼은 두되 누르면 "곧 볼 수 있어요" 안내를 띄운다"
- **이유·메모**: 요구사항의 열린 질문 OQ1 을 닫음. B5 "기록 보기"(→C3), C1 목록 항목·추천 근거 링크(→C2~C4)가 대상
- **결정 요약**: Should 화면이 생기기 전까지 버튼은 두고, 누르면 "곧 볼 수 있어요" 안내를 띄운다. 화면 등급은 바뀌지 않는다
- **영향 문서**: stories.md, requirements.md OQ1(닫힘)
- **상태**: 확정

### D-74 재분석 후 이전 판정의 집계 (User Stories Q5)
- **일시**: 2026-09-17
- **단계**: User Stories
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/user-stories/user-stories-questions.md` (Q5)
- **질문**: 전사를 고쳐 다시 분석한 뒤, 이전 판정은 기록 추이에 셉니까?
- **선택지**: A) 재분석 후 새 판정만 B) 표시 즉시 제외 C) 최신 분석 회차만 D) 둘 다 세고 표시 X) 기타
- **사용자 답(원문)**: "A. 재분석 전까지는 이전 판정을 그대로 세고, 재분석으로 새 판정이 생기면 이전 판정은 빼고 새 판정만 센다"
- **이유·메모**: 요구사항 승인 때 감수한 위험으로 기록된 검토 지적 R-01(D-70)을 닫음. 요구사항 FR8.3 의 분모 규칙을 보완하는 결정이며, 근거는 이 답이다
- **결정 요약**: 재분석 전에는 재검토 필요로 표시된 이전 판정도 분모에 센다. 재분석으로 새 판정이 생기면 대체된 이전 판정은 분모에서 빼고 새 판정만 센다. 이전 판정은 지우지 않는다
- **영향 문서**: stories.md(기록 추이 수용 기준), requirements.md FR8.3(보완 — 이 결정이 기준)
- **상태**: 확정

### D-75 지난 대화 재열람과 C5 진입 경로 (User Stories Q6)
- **일시**: 2026-09-17
- **단계**: User Stories (몹 검토 후 질문)
- **질문 파일**: `.../inception/user-stories/user-stories-questions.md` (Q6)
- **질문**: 지난 대화를 다시 열고 삭제 화면(C5)에 들어가는 길을 Must 에 어떻게 둡니까?
- **선택지**: A) 대화 돌아보기 탭=실제 대화 목록, C5 는 C1 상단 버튼 B) C1 실제 대화 항목→A4(D-73 일부 변경) C) A + C5 는 홈 설정 D) 3.1 로 넘김 X) 기타
- **사용자 답(원문)**: "A. 하단 탭 "대화 돌아보기"를 **실제 대화 목록**으로 정의한다 — 항목을 누르면 그 대화의 리포트(A4)를 열고 거기서 전사(A3)로 갈 수 있다. C5 는 나의 기록(C1) 상단 "자료·공유 설정" 버튼으로 들어간다. D-73(C1 항목은 안내)은 그대로"
- **이유·메모**: 디자이너 검토 — Must 수용 기준(재분석 US3.3, 원음 삭제 후 확인 AC8.3.2, 삭제 US8)이 지난 대화 재열람과 C5 진입을 전제하는데 Must 화면에 그 길이 없었음. 실제 대화 목록은 UI 명세에 없던 요소이며 근거는 이 답이다
- **결정 요약**: 하단 탭 "대화 돌아보기" = 실제 대화 목록(항목 → A4 → A3). C5 는 C1 상단 "자료·공유 설정" 버튼으로 진입. D-73 은 그대로
- **영향 문서**: stories.md, 03_ui-spec.md(탭 목적지·목록·C5 진입 — 3.1 반영)
- **상태**: 확정

### D-76 PARTIAL 판정의 리포트 표시 (User Stories Q7)
- **일시**: 2026-09-17
- **단계**: User Stories (몹 검토 후 질문)
- **질문 파일**: `.../inception/user-stories/user-stories-questions.md` (Q7)
- **질문**: 합성 대화 S1 의 "일부 보였어요"(PARTIAL) 판정은 리포트 어디에 보입니까?
- **선택지**: A) 어려움 장면에 B) 잘한 장면에 C) 네 번째 섹션 신설 D) 3.1 에서 정함 X) 기타
- **사용자 답(원문)**: "자세한 설명 요청" → 설명 후 "A와 B의 경우 모두 출력하는 방안"
- **이유·메모**: 디자이너·품질 검토 — PARTIAL 이 리포트 세 섹션 어디에도 배정되지 않았음
- **결정 요약**: PARTIAL 판정은 잘한 장면과 어려움이 보인 장면 두 섹션에 모두 보인다. 잘한 장면에는 해낸 부분을, 어려움 장면에는 부족했던 부분과 "이렇게 말해볼 수도 있어요" 대응을 보여 준다. 세 섹션 구성은 유지
- **영향 문서**: stories.md(AC4.1.x), 03_ui-spec.md A4(3.1 반영)
- **상태**: 확정

### D-77 SM1 에서 S2·S3 의 연습 경로 (User Stories Q8)
- **일시**: 2026-09-17
- **단계**: User Stories (몹 검토 후 질문)
- **질문 파일**: `.../inception/user-stories/user-stories-questions.md` (Q8)
- **질문**: 성공 기준 SM1 에서 S2·S3 는 "목표 선택 → 모의 대화"를 어떻게 지납니까?
- **선택지**: A) A5 에서 일반 연습 선택 B) S2 는 잘한 장면 목표, S3 는 일반 연습 C) 연습 안 함 후 B1 D) 3.1 로 넘김 X) 기타
- **사용자 답(원문)**: "A. 추천이 없거나 부족하면 A5 에서 **검토된 일반 연습**을 고르는 것으로 목표 선택 단계를 지난다 — S2·S3 모두 일반 연습(원형 시나리오)으로 모의 대화를 한 번 하고 기록까지 간다"
- **이유·메모**: 품질 검토 — S2 는 추천 목표가 없고 S3 는 분석 부족이라 SM1 종단 테스트를 쓸 수 없었음
- **결정 요약**: A5 는 추천이 없거나 부족할 때 검토된 일반 연습을 고를 수 있다. S2·S3 는 이 경로로 원형 시나리오 모의 대화를 거쳐 기록까지 간다
- **영향 문서**: stories.md(US5.1, US9.3), 03_ui-spec.md A5(3.1 반영)
- **상태**: 확정

### D-78 다음 코칭 추천 규칙 (User Stories Q9, Q10)
- **일시**: 2026-09-17
- **단계**: User Stories (몹 검토 후 질문)
- **질문 파일**: `.../inception/user-stories/user-stories-questions.md` (Q9, Q10)
- **질문**: "다음 코칭 추천"은 무엇을 반복 어려움으로 봅니까? / 추천 단순화가 승인된 요구사항을 바꿉니다. 그대로 반영합니까?
- **선택지(Q9)**: A) 2회 이상 + 기대값 확정 B) A + 횟수 설정값 C) 최근 어려움 하나만 D) 3.1 로 넘김 X) 기타
- **선택지(Q10)**: A) C 그대로, 나머지 Should B) C + 거절 목표 제외 C) Q9 를 A 로 D) Q9 를 D 로 X) 기타
- **사용자 답(원문)**: Q9 "C. 이번 MVP 는 가장 최근 어려움 장면의 목표 하나를 추천하는 것으로 단순화한다 — 반복 판정은 하지 않는다" → Q10 "A. C 그대로 반영한다 — FR8.5 를 이번 Must 에서는 "가장 최근 어려움 장면의 목표 하나"로 좁히고, 반복 어려움·도움 후 성공·선택 이력 반영은 Should 로 둔다(취소가 아니라 만드는 시점만 뒤로 간다)"
- **이유·메모**: 개발자 검토 — 반복 기준과 기대 추천이 없어 AC7.3.1 을 판정할 수 없었음. Q9=C 가 승인된 FR8.5·도메인 규칙 8 을 좁혀 영향 4건을 표로 확인받음. 거절한 목표가 최근 어려움이면 다시 추천되는 흐름(영향 4번)을 먼저 짚었고 사용자가 알고 수용함
- **결정 요약**: Must 의 다음 코칭 추천 = 가장 최근 어려움 장면의 목표 하나. 반복 어려움·도움 후 성공·사용자 선택 이력 반영은 Should(취소 아님). 충분성 표시는 유지. 요구사항 FR8.5 를 이번 Must 에서 좁히며 근거는 이 결정이다
- **영향 문서**: stories.md(US7.3, Should 스토리 추가), requirements.md FR8.5(이 결정이 기준)
- **상태**: 확정 (D-70 에서 승인된 FR8.5 를 Must 범위에서 조정)

### D-79 User Stories 산출물 승인
- **일시**: 2026-09-17
- **단계**: User Stories (승인 게이트)
- **질문**: User Stories 단계 산출물 승인 여부
- **선택지**: A) Approve B) Request Changes
- **사용자 답(원문)**: "Approve"
- **이유·메모**: 제품 리드 자문 검토 결과 준비됨(치명 0 / 중요 1 / 경미 1). R-01(삭제 화면 C5 가 375px·대비 자동 검증에서 빠짐), R-02(금지 표현 허용 문장 목록의 담당 단계 없음)를 승인과 함께 감수한 위험으로 기록
- **결정 요약**: stories.md(스토리 37개, Must 28 / Should 9), personas.md, user-stories-assessment.md, traceability.json, 기여 파일 3건 승인. 다음 단계는 Domain Design(2.6)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/user-stories/` 전체
- **상태**: 확정

### D-80 추천의 주인 (Domain Design Q1)
- **일시**: 2026-09-17
- **단계**: Domain Design
- **질문 파일**: `.../inception/domain-design/domain-design-questions.md` (Q1)
- **질문**: 목표 추천(A5)과 다음 코칭 추천(C1)은 어느 컴포넌트가 가집니까?
- **선택지**: A) 하나, Record B) 둘로 나눔 C) 둘 다 Training D) 하나, Assessment X) 기타
- **사용자 답(원문)**: "C. 둘 다 연습(Training)이 가진다 — 추천의 결과가 곧 연습 목표이기 때문이다"
- **이유·메모**: 기술 명세 §6 은 추천을 record/ 에 두었음 — Q8 에서 영향 확인
- **결정 요약**: 목표 추천과 다음 코칭 추천 모두 Training 이 가진다. Record 는 C1 표시를 위해 Training 에서 추천을 받는다
- **영향 문서**: components.md, 02_tech-environment.md §6(3.1 반영)
- **상태**: 확정

### D-81 판정 버전 정보 (Domain Design Q2)
- **일시**: 2026-09-17
- **단계**: Domain Design
- **질문 파일**: `.../inception/domain-design/domain-design-questions.md` (Q2)
- **질문**: 판정의 버전 정보(기준·프롬프트·모델·전사 버전)는 어떻게 둡니까?
- **선택지**: A) 값 객체 B) Record 엔티티+순환 허용 C) Assessment 엔티티 D) A+버전 목록표 X) 기타
- **사용자 답(원문)**: "A. 별도 엔티티를 두지 않고, 버전 값을 판정·시도에 함께 저장하는 **값 객체**로 둔다 — 순환이 없어지고 팀 관행과 맞는다. 버전 "이력" 조회는 판정을 읽는 쪽이 모아 보여 준다"
- **이유·메모**: 명세대로면 Assessment↔Record 순환
- **결정 요약**: VersionInfo 엔티티를 두지 않고 판정·시도의 값 객체로 저장한다
- **영향 문서**: components.md, 04_domain-model.md(VersionInfo — 3.1 반영)
- **상태**: 확정

### D-82 모의 대화 시도 판정 (Domain Design Q3)
- **일시**: 2026-09-17
- **단계**: Domain Design
- **질문 파일**: `.../inception/domain-design/domain-design-questions.md` (Q3)
- **질문**: 모의 대화 시도의 판정은 누가 만듭니까?
- **선택지**: A) Training 이 만들고 Assessment 에 저장 B) 전부 Assessment C) Training 별도 엔티티 D) A+공유 규칙 모듈 X) 기타
- **사용자 답(원문)**: "A. 연습(Training)이 시도 판정을 만들되, 저장은 평가(Assessment)가 가진 같은 판정 엔티티에 Assessment 의 인터페이스로 한다"
- **결정 요약**: 시도 판정은 Training 이 만들고, Assessment 가 가진 판정 엔티티에 Assessment 인터페이스로 저장한다(근거 검증 등 저장 규칙은 Assessment 가 적용)
- **영향 문서**: components.md
- **상태**: 확정

### D-83 계정 컴포넌트 신설 (Domain Design Q4, Q8)
- **일시**: 2026-09-17
- **단계**: Domain Design
- **질문 파일**: `.../inception/domain-design/domain-design-questions.md` (Q4, Q8)
- **질문**: 사용자·동의·보호자 초대·권한의 주인 / 계정 신설과 추천 이동이 팀 관행 5개 이름과 어긋남
- **선택지**: Q4: A) 모두 Privacy B) Account 신설(초대 포함) C) Account 최소 D) B 를 Should 때 / Q8: A) 그대로(6개) B) privacy/ 하위 모듈 C) Q4 를 D 로 D) Q4 를 A 로 X) 기타
- **사용자 답(원문)**: "B. 새 계정(Account) 컴포넌트를 만든다 — 사용자·동의·로그인·보호자 계정과 초대는 Account, 열람 권한과 삭제 요청은 Privacy" → Q8 "A. 그대로 반영한다 — 컴포넌트는 6개(Account 추가), 추천은 Training. 팀 관행의 "5개 이름"과의 차이는 이 단계의 배움 기록으로 프로젝트 규칙에 남겨, 다음 단계들이 설계 문서를 기준으로 읽게 한다"
- **이유·메모**: 영향 4건(팀 관행 파일 구조 5개 이름, 기술 명세 §6, 삭제 진입점, US7.3)을 표로 확인. 팀 관행 문서와의 차이를 먼저 짚음
- **결정 요약**: 컴포넌트 6개: Conversation, Assessment, Training, Record, Account(신설), Privacy. Account 는 사용자·동의·로그인·보호자 계정과 초대, Privacy 는 열람 권한과 삭제 요청
- **영향 문서**: components.md, team.md Code Style(차이는 배움 기록으로), 02_tech-environment.md §6
- **상태**: 확정 (팀 관행 파일 구조 5개 이름을 설계에서 6개로 조정)

### D-84 삭제 전파 방식 (Domain Design Q5, Q9)
- **일시**: 2026-09-17
- **단계**: Domain Design
- **질문 파일**: `.../inception/domain-design/domain-design-questions.md` (Q5, Q9)
- **질문**: 대화 삭제 시 연결 데이터 지우기 전파 / 커밋 후 파일 삭제가 AC8.1.4 와 부딪힘
- **선택지**: Q5: A) 확정, 커밋 후 파일 B) 확정, 파일 먼저 C) 사건 알림 D) FK 연쇄 주 수단 / Q9: A) 그대로+남은 파일 추적 B) Q5 를 B 로 C) 삭제 대기 폴더 D) 기동 시 정리 X) 기타
- **사용자 답(원문)**: "A. 잠정 규칙을 확정한다 — Privacy 의 삭제 유스케이스가 각 컴포넌트의 정리 인터페이스를 순서대로 부르고, 한 트랜잭션 안에서 DB 행을 지운 뒤 커밋 후 파일을 지운다" → Q9 "A. Q5=A 그대로 두고 **남은 파일 추적**을 더한다 — 삭제 요청이 지울 파일 경로를 영향 항목에 먼저 기록하고, 커밋 후 파일 삭제에 실패한 경로는 요청 상태를 "일부 완료"로 두어 다시 삭제 요청 시 그 경로만 지운다"
- **이유·메모**: Q5=A 가 팀 관행 잠정 규칙(파일 → DB 행, 남는 쪽은 DB 행)과 승인된 AC8.1.4(다시 삭제 요청)와 부딪혀 영향 3건을 표로 확인. AC8.1.4 의존을 먼저 짚음
- **결정 요약**: Privacy 삭제 유스케이스가 각 컴포넌트 정리 인터페이스를 순서대로 호출, 한 트랜잭션에서 DB 행 삭제 후 커밋, 이어서 파일 삭제. 지울 파일 경로는 영향 항목에 먼저 기록하고 실패한 경로는 일부 완료로 남겨 재요청 시 지운다
- **영향 문서**: components.md, decisions.md, team.md Code Style 삭제 잠정 규칙(이 결정이 대체)
- **상태**: 확정

### D-85 재분석 모델 (Domain Design Q6)
- **일시**: 2026-09-17
- **단계**: Domain Design
- **질문 파일**: `.../inception/domain-design/domain-design-questions.md` (Q6)
- **질문**: 재분석으로 생기는 분석 회차를 어떻게 모델링합니까?
- **선택지**: A) 분석 회차 엔티티 B) 판정끼리 대체 연결 C) 판정 상태 값 D) A+사회적 사건도 회차 X) 기타
- **사용자 답(원문)**: "B. 판정마다 "대체한 판정" 연결을 둔다 — 회차 개념은 없고 판정끼리 이어진다"
- **결정 요약**: 판정마다 대체한 판정 연결을 둔다. 회차 엔티티는 두지 않는다
- **영향 문서**: components.md, decisions.md
- **상태**: 확정

### D-86 근거 필수 규칙의 예외 (Domain Design Q7)
- **일시**: 2026-09-17
- **단계**: Domain Design
- **질문 파일**: `.../inception/domain-design/domain-design-questions.md` (Q7)
- **질문**: 근거 발화가 없어도 되는 판정은 어디까지입니까?
- **선택지**: A) 결과 있는 판정만 필수 B) PRESENT 면 필수 C) 기회 없음만 예외 D) A+있으면 검증 X) 기타
- **사용자 답(원문)**: "D. A 와 같되, 보류라도 근거를 줄 수 있으면 함께 저장한다(없어도 되지만 있으면 검증한다)"
- **이유·메모**: 도메인 규칙 3 을 그대로 두면 S3 의 UNCERTAIN·맥락 부족 두 판정이 기대 판정과 어긋났음
- **결정 요약**: 근거는 결과가 있는 판정(PRESENT, 보류 없음)에만 필수. 보류는 근거 없이 가능하나 주어지면 저장·검증. 없는 발화 ID 를 가리키면 어떤 판정이든 INVALID_EVIDENCE
- **영향 문서**: components.md, 04_domain-model.md 규칙 3(보완 — 이 결정이 기준)
- **상태**: 확정

### D-87 Domain Design 산출물 승인
- **일시**: 2026-09-17
- **단계**: Domain Design (승인 게이트)
- **질문**: Domain Design 단계 산출물 승인 여부
- **선택지**: A) Approve B) Request Changes
- **사용자 답(원문)**: "Approve"
- **이유·메모**: 아키텍처 검토 결과 준비됨(치명 0 / 중요 0 / 경미 2). R-01(Assessment→Conversation 의존 항목에 동기 조회와 사건 구독이 한 style 로 묶임)을 감수한 위험으로 기록. R-02(5→6 이름 차이 기록)는 배움 기록으로 project.md 에 저장해 해소. 요약 확인 뒤 리드가 정한 ADR-009(프로세스 안 사건), ADR-010(Record 읽기 전용)을 게이트에서 짚었고 함께 승인됨
- **결정 요약**: components.md(업무 컴포넌트 6개 + 지원 컴포넌트 2개, 엔티티 20개), decisions.md(ADR 10건), traceability.json 승인. 다음 단계는 Units Generation(2.7)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/domain-design/` 전체
- **상태**: 확정

### D-88 작업 단위를 자르는 기준
- **일시**: 2026-09-17
- **단계**: Units Generation (Q1)
- **질문**: 작업 단위를 무엇을 기준으로 자릅니까?
- **선택지**: A) 컴포넌트별 세로 단위 B) 백엔드와 화면을 따로 C) 기능(F01~F07) 단위 D) 큰 단위 3개 X) Other
- **사용자 답(원문)**: "C. 기능(F01~F07) 단위 — 컴포넌트를 가로질러 기능 하나씩 단위로 삼는다"
- **이유·메모**: 범위 문서의 F01~F07 이 이미 등급·성공 기준과 연결되어 있어 단위와 1:1 로 추적된다. 한 기능 단위가 여러 컴포넌트(D-83 의 6개 업무 컴포넌트)를 가로지른다
- **결정 요약**: 작업 단위는 기능 F01~F07 각각 하나씩(U3~U9). 컴포넌트 경계(ADR)는 코드 구조로 유지하고 작업 분담은 기능 기준으로 한다
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/units-generation-questions.md`, 이후 `unit-of-work.md` · `unit-of-work-dependency.md` · `unit-of-work-story-map.md`
- **상태**: 확정

### D-89 공통 기반 코드의 자리
- **일시**: 2026-09-17
- **단계**: Units Generation (Q2)
- **질문**: 여러 단위가 함께 쓰는 기반 코드는 어디에 둡니까?
- **선택지**: A) 기반 단위 하나 B) 기반 단위 둘 C) 처음 필요한 단위가 만든다 D) B + ProviderAdapters 별도 단위 X) Other
- **사용자 답(원문)**: "B. 기반 단위 둘 — 백엔드 기반(설정·DB·오류·픽스처·Mock 어댑터·시드 사용자)과 화면 기반(앱 틀·공통 컴포넌트)을 나눈다"
- **이유·메모**: 백엔드 기반과 화면 기반을 나눠 두 사람이 동시에 시작할 수 있게 한다
- **결정 요약**: U1 backend-foundation(service): 설정·DB·Alembic·오류 봉투·request_id·픽스처·Mock 어댑터·시드 사용자·동의·시연 기동(US9.1·US9.2). U2 web-foundation(ui): 앱 틀·탭·화면 상태 4종·안내 문구·첫 방문 동의·홈(US1)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/units-generation-questions.md`, 이후 `unit-of-work.md` · `unit-of-work-dependency.md` · `unit-of-work-story-map.md`
- **상태**: 확정

### D-90 Should 기능의 단위 배치
- **일시**: 2026-09-17
- **단계**: Units Generation (Q3)
- **질문**: Should 기능은 작업 단위에 어떻게 넣습니까?
- **선택지**: A) Should 를 별도 단위로 B) 해당 컴포넌트 단위에 함께 C) Should 전체를 단위 하나로 D) Must 뒤 다시 분해 X) Other
- **사용자 답(원문)**: "A. Should 를 별도 단위로 — Must 단위는 Must 스토리만 가져 먼저 닫을 수 있게 하고, Should 스토리는 따로 묶은 단위(들)로 둔다"
- **이유·메모**: Must 단위가 Must 스토리만 가져 먼저 닫을 수 있게 한다. Should 를 후순위로 둔 것은 만드는 시점의 문제이며 확정된 Should 스토리를 취소한 것이 아니다
- **결정 요약**: Should 스토리(US10~US14)는 Must 단위와 섞지 않고 별도 단위로 둔다. 개수는 D-93
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/units-generation-questions.md`, 이후 `unit-of-work.md` · `unit-of-work-dependency.md` · `unit-of-work-story-map.md`
- **상태**: 확정

### D-91 병렬 작업 갈래 수 (D-47 닫음)
- **일시**: 2026-09-17
- **단계**: Units Generation (Q4)
- **질문**: 5인이 동시에 붙을 병렬 갈래는 몇 개로 잡습니까?
- **선택지**: A) 3갈래 B) 4갈래 C) 5갈래 D) 고정하지 않음 X) Other
- **사용자 답(원문)**: "B. 4갈래 — 한 갈래에 1명 이상, 1명이 기반·통합을 맡는다"
- **이유·메모**: 한 갈래에 1명 이상, 1명이 기반·통합을 맡는다. Scope Definition 에서 units-generation 으로 이월된 D-47 을 이 결정으로 닫는다. 갈래별 담당과 순서는 Delivery Planning(2.9)이 정한다
- **결정 요약**: 동시에 진행하는 작업 갈래는 최대 4개
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/units-generation-questions.md`, 이후 `unit-of-work.md` · `unit-of-work-dependency.md` · `unit-of-work-story-map.md`
- **상태**: 확정

### D-92 기능 단위 사이 의존의 기준
- **일시**: 2026-09-17
- **단계**: Units Generation (Q5 (후속))
- **질문**: 기능 단위의 의존을 "구현 완료"로 봅니까, "계약 합의"로 봅니까?
- **선택지**: A) 계약 기준 B) 구현 완료 기준 C) 섞어서 D) 계약 기준 + F07 만 구현 완료 X) Other
- **사용자 답(원문)**: "A. 계약 기준 — 기능 단위는 기반 단위 둘에만 구현 완료 의존을 두고, 다른 기능 단위와는 계약(2.8)과 시드·픽스처로 연결한다"
- **이유·메모**: 기반이 끝나면 여러 기능 단위가 함께 시작할 수 있다. 리드 해석: 보호자·공유(U12)는 로그인한 보호자가 있어야 열람이 성립해 계정·로그인(U11)에 구현 완료 의존을 둔다(요약 확인에서 승인)
- **결정 요약**: 기능·Should 단위는 U1·U2 에만 구현 완료 의존을 두고, 서로는 계약(2.8)과 시드·픽스처로 연결한다. 예외: U12 → U11
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/units-generation-questions.md`, 이후 `unit-of-work.md` · `unit-of-work-dependency.md` · `unit-of-work-story-map.md`
- **상태**: 확정

### D-93 Should 단위 개수
- **일시**: 2026-09-17
- **단계**: Units Generation (Q6 (후속))
- **질문**: 별도로 둘 Should 단위는 몇 개로 묶습니까?
- **선택지**: A) 하나로 B) 둘로 C) 셋으로 D) 스토리 묶음마다 하나씩 — 5개 X) Other
- **사용자 답(원문)**: "D. 스토리 묶음마다 하나씩 — 5개"
- **이유·메모**: Should 스토리 묶음 US10~US14 가 각각 독립적으로 뺄 수 있는 크기다
- **결정 요약**: U10 s-detail-views(US10), U11 s-account-auth(US11), U12 s-guardian-sharing(US12), U13 s-laptop-layout(US13, ui), U14 s-recommendation-plus(US14)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/units-generation-questions.md`, 이후 `unit-of-work.md` · `unit-of-work-dependency.md` · `unit-of-work-story-map.md`
- **상태**: 확정

### D-94 작업 단위 분해 계획 요약 확인
- **일시**: 2026-09-17
- **단계**: Units Generation (요약 확인)
- **질문**: 작업 단위 분해 계획으로 산출물을 만들까요?
- **선택지**: Looks correct / Request changes
- **사용자 답(원문)**: "Looks correct"
- **이유·메모**: 리드가 정한 스토리 배치(US1→U2, US9.1·9.2→U1, US9.3→U8, US3.2→U3, US3.3→U9)와 화면 공유(A2: U3·U4, A3: U3·U9, A4: U5·U9)를 요약에서 짚었고 함께 승인됨
- **결정 요약**: 단위 14개(Must 9 / Should 5) 계획 확정. 기능 단위 종류는 지정하지 않아 이후 설계 산출물 전체를 받는다
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/units-generation-questions.md`, 이후 `unit-of-work.md` · `unit-of-work-dependency.md` · `unit-of-work-story-map.md`
- **상태**: 확정

### D-95 Units Generation 산출물 승인
- **일시**: 2026-09-17
- **단계**: Units Generation (승인 게이트)
- **질문**: Units Generation 단계 산출물 승인 여부
- **선택지**: A) Approve B) Request Changes
- **사용자 답(원문)**: "Approve"
- **이유·메모**: 첫 검토(치명 0 / 중요 2 / 경미 1)의 지적 R-01·R-02·R-03 을 반영한 뒤, 복구 절차에서 사용자가 변경 요청 "검토 지적 3건 반영"을 기록하고 재검토를 받았다. 재검토 결과 준비됨, 이전 3건 해소 확인. 새 지적 R-04(경미 — U9·U11 의 "넘기는 것", U12 의 "넘기는 것"·"경계" 소절 누락)는 반영하지 않은 채 승인되어 감수한 위험으로 기록한다
- **결정 요약**: unit-of-work.md(단위 14개, Must 9 / Should 5), unit-of-work-dependency.md(기반 단위 둘에만 의존, 예외 U12 → U11), unit-of-work-story-map.md(스토리 37개 배정), traceability.json 승인. 열린 질문 OQ-U1·OQ-U2 는 Contract Design(2.8), OQ-U3 는 Delivery Planning(2.9) 으로 넘긴다. 다음 단계는 Contract Design(2.8)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/units-generation/` 전체
- **상태**: 확정

### D-96 전사·분석 요청의 응답 방식
- **일시**: 2026-09-17
- **단계**: Contract Design (Q1)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: 전사와 분석 요청은 응답을 어떻게 돌려줍니까?
- **선택지**: A) 동기 B) 접수 후 상태 조회 C) 전사만 B·분석은 동기 D) API 는 B·구현은 동기 X) Other
- **사용자 답(원문)**: "B. 접수 후 상태 조회 — 요청은 바로 "접수됨"(202)과 대화 ID 를 돌려주고, 작업은 서버 안 백그라운드로 돈다. 화면은 상태 조회 API 를 주기적으로 불러 완료·실패를 확인한다"
- **이유·메모**: practices-discovery 가 이 단계로 넘긴 "전사 응답이 동기인지 202 + 폴링인지"를 닫는다. live 제공자 응답 시간이 미정(D-37)인 점이 근거. 리드 해석(요약 확인에서 승인): 화면은 1초 간격 조회, FastAPI 요청 후 작업(같은 프로세스)으로 실행하고 별도 작업 큐는 두지 않음, 서버 재시작으로 진행 중 상태가 남은 대화는 기동 때 실패로 바꾼다
- **결정 요약**: 업로드·전사·분석·재분석 요청은 202 + 상태 조회 계약. NFR3 의 기준은 D-103
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-97 테이블 마이그레이션 담당 (OQ-U1) — 첫 답
- **일시**: 2026-09-17
- **단계**: Contract Design (Q2)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: 테이블 마이그레이션은 누가 만듭니까?
- **선택지**: A) U1 이 전체 초기 스키마 B) 단위별 C) U1 Must + Should 단위 X) Other
- **사용자 답(원문)**: "B. 각 기능 단위가 자기 엔티티 테이블을 만든다 — 리비전이 갈라지면 병합하는 사람이 alembic merge 로 합친다"
- **이유·메모**: Q3 답(U1 전체 시드)과 함께 두면 D-92(기반 단위에만 구현 완료 의존)가 깨져 후속 질문 Q7 로 확인했다
- **결정 요약**: D-102 로 변경됨
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 변경됨 (D-102)

### D-98 시드 상태 담당 (OQ-U2)
- **일시**: 2026-09-17
- **단계**: Contract Design (Q3)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: 병렬로 시작하기 위한 시드 상태는 누가 만들고 유지합니까?
- **선택지**: A) U1 이 전부 B) 기본은 U1·이후는 만드는 단위 C) 목록·모양 계약 고정 + B X) Other
- **사용자 답(원문)**: "A. U1 이 시드 틀과 모든 상태 시드를 한 번에 만들고 유지한다 — 한 곳에서 관리하지만, U1 담당자가 모든 단위의 데이터 모양을 알아야 한다"
- **이유·메모**: Units Generation 의 OQ-U2 를 닫는다. D-102(U1 전체 스키마)와 함께 성립한다
- **결정 요약**: U1 이 scripts/seed.py 의 틀과 모든 상태 시드를 소유한다. 시드 상태 목록은 계약 요약에 적는다
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-99 API 계약의 기준 문서
- **일시**: 2026-09-17
- **단계**: Contract Design (Q4)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: API 경로와 응답 모양의 기준 문서는 무엇입니까?
- **선택지**: A) 계약 요약 B) 구현 전 계약·구현 후 생성 스키마 C) 생성 스키마 + CI 대조 X) Other
- **사용자 답(원문)**: "A. 계약 요약이 기준 — 구현은 계약 요약에 맞춰 만들고, 어긋나면 구현을 고친다. 계약을 바꾸려면 계약 요약을 먼저 고친다"
- **이유·메모**: 리드 해석(요약 확인에서 승인): 계약 요약은 AI-DLC 기록 폴더에 두고 구현 중에도 PR 로 이 파일을 고친다. 모든 경로는 /api/v1 아래
- **결정 요약**: contract-summary.md 가 API·내부 인터페이스·사건·스키마·시드 계약의 기준
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-100 깨는 계약 변경의 처리
- **일시**: 2026-09-17
- **단계**: Contract Design (Q5)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: 이미 합의한 계약을 깨는 변경은 어떻게 처리합니까?
- **선택지**: A) 소비 단위 담당자 PR 승인 B) decision-log + 팀 합의 C) 통합 전 금지 X) Other
- **사용자 답(원문)**: "A. 추가는 자유, 깨는 변경은 그 계약을 쓰는 단위 담당자의 PR 리뷰 승인이 필요하다 — 계약 요약을 같은 PR 에서 고친다"
- **이유·메모**: 팀 관행의 병합 전 리뷰(만들지 않은 사람 1인)에 소비 단위 담당자 승인 조건을 더한다
- **결정 요약**: 필드 추가는 자유(받는 쪽은 모르는 필드 무시), 이름 변경·삭제는 소비 단위 담당자 승인 + 같은 PR 에서 계약 요약 수정
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-101 같은 화면을 만지는 단위의 화면 경계
- **일시**: 2026-09-17
- **단계**: Contract Design (Q6)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: 여러 단위가 같은 화면을 만질 때 화면 경계를 어떻게 나눕니까?
- **선택지**: A) 페이지 소유 + 끼워 넣기 B) 구역별 하위 라우트 C) 먼저 만든 단위 파일에 이어 쓰기 X) Other
- **사용자 답(원문)**: "B. 화면을 구역별 하위 라우트로 나눠 단위마다 따로 소유한다"
- **이유·메모**: 리드 해석(요약 확인에서 승인): A2 는 업로드(U3) 라우트와 맥락 입력 하위 라우트(U4), A4 는 U5 소유이고 U9 는 조회 조건만 더한다. A3 는 D-104
- **결정 요약**: 화면은 구역별 하위 라우트 단위로 소유한다
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-102 테이블 마이그레이션 담당 — 충돌 해소 (OQ-U1 닫음)
- **일시**: 2026-09-17
- **단계**: Contract Design (Q7 (후속))
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: 단위별 마이그레이션(Q2)과 U1 의 전체 시드(Q3)를 함께 두면 병렬 시작 결정이 깨집니다. 어떻게 맞춥니까?
- **선택지**: A) Q2 를 U1 전체 스키마로 B) Q3 변경 + 의존 간선 추가(2.7 재개) C) 둘 다 유지(D-92 무효) X) Other
- **사용자 답(원문)**: "A. Q2 를 바꾼다 — U1 이 20개 테이블 전체를 초기 스키마 하나로 만든다 — Q3(U1 이 모든 시드)와 D-92 가 그대로 유지된다. 이후 컬럼 변경은 해당 단위가 새 리비전으로 추가한다"
- **이유·메모**: 단위별 테이블 생성은 외래 키(판정 근거→발화, 목표→판정, 시도→판정 등)로 숨은 구현 의존을 만들고, U1 전체 시드는 U1 이 기능 단위에 의존하는 순환을 만들었다. 영향 항목(D-92, D-94)을 표로 보여 확인받았다
- **결정 요약**: U1 이 엔티티 20개 테이블 전체를 초기 스키마 하나로 만든다. 이후 컬럼 변경은 해당 단위의 새 리비전, 갈라지면 alembic merge. D-97 을 대체
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-103 Mock 분석 시간(NFR3)의 측정 기준
- **일시**: 2026-09-17
- **단계**: Contract Design (Q8 (후속))
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: 분석을 접수 후 상태 조회로 바꾸면 "Mock 분석 3초 이내"(NFR3)는 무엇을 재는 기준이 됩니까?
- **선택지**: A) 접수~완료 3초 B) 접수 응답 3초 C) 접수 1초 + 완료 3초 X) Other
- **사용자 답(원문)**: "C. 접수 응답은 1초 이내, 완료까지는 3초 이내 둘 다 — 두 단언을 모두 둔다"
- **이유·메모**: D-96 으로 요청이 바로 돌아오게 되어 NFR3 문장의 "응답 시간" 해석이 필요했다. 품질 목표를 약하게 하지 않는 방향으로 정했다. 접수 응답 1초는 이 단계에서 새로 생긴 목표다
- **결정 요약**: Mock 모드에서 분석 접수 응답(202) 1초 이내, 접수부터 상태 완료까지 PM-02(기본 3초) 이내. 통합 테스트가 두 경과 시간을 단언한다. 이 해석은 requirements.md 의 NFR3 을 보완하며 계약 요약이 기준
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-104 A3 재검토 안내의 라우트 구조
- **일시**: 2026-09-17
- **단계**: Contract Design (Q9 (후속))
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: 구역별 하위 라우트(Q6)에서, 전사 확인 화면(A3) 위에 함께 보여야 하는 재검토 안내는 어떻게 둡니까?
- **선택지**: A) 부모 레이아웃 라우트 B) 이 자리만 끼워 넣기 C) 별도 하위 라우트 X) Other
- **사용자 답(원문)**: "A. 부모 레이아웃 라우트로 둔다 — A3 의 부모 레이아웃(U9 소유)이 재검토 안내를 그리고, 그 안의 하위 라우트(U3 소유)가 전사를 그린다. URL 은 하나다"
- **이유·메모**: 하위 라우트는 한 번에 하나만 그려져 FR3.4(A3 상단 안내, D-66)와 맞추려면 방식을 정해야 했다
- **결정 요약**: A3 = U9 부모 레이아웃(재검토 안내) + U3 하위 라우트(전사)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-105 계약 설계 계획 요약 확인
- **일시**: 2026-09-17
- **단계**: Contract Design (요약 확인)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-design-questions.md`
- **질문**: Does this all look correct before I generate the artifact?
- **선택지**: Looks correct / Request changes
- **사용자 답(원문)**: "Looks correct"
- **이유·메모**: 리드가 정한 항목(계약 목록, /api/v1, 1초 간격 상태 조회와 요청 후 작업, 재시작 시 실패 처리, LLM 포트 모양, A2·A4 라우트, 계약 요약 위치)을 요약에서 짚었고 함께 승인됨
- **결정 요약**: 계약 설계 계획 확정
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-106 Contract Design 변경 요청 — 검토 지적 3건 수용
- **일시**: 2026-09-17
- **단계**: Contract Design (승인 게이트)
- **질문**: Contract Design 단계 산출물 승인 여부
- **선택지**: A) Approve B) Request Changes
- **사용자 답(원문)**: "Request Changes" / 바꿀 내용: "R-01, R02, R-03 모두 검토자 제안을 수용"
- **이유·메모**: 아키텍처 검토 결과 준비됨(치명 0 / 중요 2 / 경미 1). R-01 LLM 포트에 전사 버전이 없어 Mock 이 정정 전·후 S3 를 구분 못함, R-02 백그라운드 작업과 요청당 세션 관행의 충돌, R-03 status/analysisStatus 분리가 도메인 설계와 다르다는 기록 없음
- **결정 요약**: C14 `assess_conversation` 에 `transcript_version` 추가와 C9→C14→C10 전달 경로 명시, 공통 규칙에 "백그라운드 작업은 새 세션을 열어 커밋, 실패 시 별도 세션으로 FAILED 기록" 행 추가(세부는 3.1), C2·C15 에 "API 는 두 필드, 내부 컬럼 구성은 3.1" 명시. 고친 산출물로 재검토
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/contract-summary.md`
- **상태**: 확정

### D-107 Contract Design 산출물 승인
- **일시**: 2026-09-17
- **단계**: Contract Design (승인 게이트)
- **질문**: Contract Design 단계 산출물 승인 여부
- **선택지**: A) Approve B) Request Changes
- **사용자 답(원문)**: "Approve"
- **이유·메모**: D-106 변경 요청으로 검토 지적 R-01·R-02·R-03 을 반영한 뒤 재검토 결과 준비됨, 3건 모두 해소, 새 지적 없음. 리드가 정한 기술 세부(연습 시도 판정·삭제는 동기, 사건 구독 실패 시 정정까지 롤백, 시드 상태 9개 이름, 새 열거값 이름)를 게이트에서 짚었고 함께 승인됨
- **결정 요약**: contract-summary.md(계약 18개 — REST 9, 프로세스 안 인터페이스 5, 사건 1종, 공유 스키마 2, 라우트 트리 1) 승인. 열린 질문 6건은 Functional Design(3.1)으로 넘긴다. 다음 단계는 Delivery Planning(2.9)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/contract-design/` 전체
- **상태**: 확정

### D-108 D-46 실현 방식 — 첫 답
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q1)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: "얇은 종단 슬라이스 먼저, 그다음 깊이"(D-46)를 기능 단위 위에서 어떻게 실현합니까?
- **선택지**: A) 뼈대+SM1 흐름 단위 먼저 완성 B) 뼈대를 넓혀 여섯 단계 최소 관통 C) 단위 다시 자르기 X) Other
- **사용자 답(원문)**: "B. 뼈대 Bolt 를 넓혀 여섯 단계를 최소 형태로 모두 잇는다"
- **이유·메모**: 팀 관행의 뼈대 정의·R5·단위의 Construction 1회 통과와 부딪혀 후속 Q7 로 확인했다
- **결정 요약**: D-114 로 변경됨
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 변경됨 (D-114)

### D-109 뼈대 Bolt 에서 U1 의 범위
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q2)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: 뼈대 Bolt 에서 백엔드 기반(U1)을 어디까지 끝냅니까?
- **선택지**: A) U1 전체 B) 테이블 + 앞쪽 시드만 C) U1·U2 먼저 병렬 + 나머지는 설계 X) Other
- **사용자 답(원문)**: "B. 뼈대 Bolt 에서 U1 의 테이블 20개와 앞쪽 시드(base·consented·s1-transcribed)까지만 끝내고, 뒤쪽 시드(s1-analyzed 이후 6개)는 U1 담당이 병렬 기간 첫 주 안에 추가한다"
- **이유·메모**: D-92 와의 관계를 후속 Q8 로 확인했고 그대로 유지(D-115)
- **결정 요약**: 뼈대에서 U1 = 테이블 20 + 앞쪽 시드 3. 뒤쪽 시드 6 은 병렬 첫 주(갈래 4 의 첫 작업)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정

### D-110 Bolt 크기
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q3)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: 한 Bolt 에 작업 단위를 몇 개 담습니까?
- **선택지**: A) 단위 하나=Bolt 하나 B) 붙은 단위 묶기 C) 갈래 하나=Bolt 하나 X) Other
- **사용자 답(원문)**: "B. 화면이나 흐름이 붙어 있는 단위를 묶는다 — 예: U3+U4(대화 가져오기·맥락), U6+U7(목표·연습)"
- **이유·메모**: 리드 해석(요약 확인에서 승인): U9 는 A3·A4 두 화면에 걸쳐 따로 두고, Should 는 의존이 있는 U11+U12 만 묶는다
- **결정 요약**: Bolt 9개: B1(U1·U2·U3·U4), B2(U5), B3(U6+U7), B4(U8), B5(U1 뒤쪽 시드→U9), B6(U10), B7(U11+U12), B8(U13), B9(U14)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정

### D-111 기능 Bolt 의 갈래 배정 순서
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q4)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: 뼈대 뒤 기능 Bolt 들은 어떤 순서로 갈래에 배정합니까?
- **선택지**: A) SM1 흐름 순서 B) 위험 큰 것 먼저 C) 점수(WSJF) X) Other
- **사용자 답(원문)**: "A. SM1 흐름 순서 — 수행 평가(U5)·목표(U6)·연습(U7)·기록(U8)을 먼저 네 갈래에 두고, 맥락(U4)·정정·삭제(U9)는 그다음, Should 는 마지막"
- **이유·메모**: U4 는 D-116 으로 뼈대에 들어갔다. 형식 점수 모델(WSJF)은 쓰지 않는다
- **결정 요약**: 뼈대 뒤 갈래 1~3 = B2·B3·B4, 갈래 4 = 뒤쪽 시드 후 U9. B4(SM1 리허설)는 B2·B3 병합 뒤 닫는다(OQ-U3 닫음)
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정

### D-112 Bolt 담당 표기
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q5)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: Bolt 를 누가 맡습니까?
- **선택지**: A) 갈래에만 배정 B) 사람을 갈래에 배정 C) 갈래 + 역할 자리만 X) Other
- **사용자 답(원문)**: "A. 갈래에만 배정한다 — Bolt 를 갈래 1~4 에 배정하고 사람 이름은 적지 않는다. 누가 어느 갈래를 맡을지는 Bolt 시작 때 정한다"
- **이유·메모**: OC-03(고정 역할 없음)과 맞춘다
- **결정 요약**: team-allocation.md 는 Bolt → 갈래 배정만 적는다
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정

### D-113 일정 보호선
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q6)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: 일정이 밀릴 때를 대비해 어떤 선을 긋습니까?
- **선택지**: A) Must·SM1 전 Should 금지 B) 날짜 선 C) 둘 다 X) Other
- **사용자 답(원문)**: "A. Must 완료와 SM1 리허설 통과 전에는 Should Bolt 를 시작하지 않는다 — 갈래가 비어도 Must 통합·테스트를 돕는다"
- **이유·메모**: R5·R7 재검증의 결론. 날짜 선은 두지 않았다
- **결정 요약**: Should Bolt(B6~B9)의 시작 조건 = B1~B5 완료 + SM1 리허설 통과
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정

### D-114 뼈대 구성 — 충돌 해소 (D-46 표현 변경)
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q7 (후속))
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: 넓힌 뼈대(Q1)는 확정된 팀 관행의 뼈대 정의와 부딪힙니다. 뼈대를 어떻게 짭니까?
- **선택지**: A) Q1 B 그대로 B) 뼈대 두 겹 C) Q1 을 A 로 X) Other
- **사용자 답(원문)**: "C. Q1 을 A 로 바꾼다 — 뼈대는 팀 관행 그대로, SM1 흐름 단위를 먼저 병렬로 완성한다. D-46 의 "여섯 단계 최소 관통" 표현이 바뀐다"
- **이유·메모**: 영향 항목(팀 관행 뼈대 정의, 뼈대 대기와 R5, 단위의 Construction 1회 통과·D-92)을 표로 보여 확인받았다
- **결정 요약**: D-46 의 "여섯 단계를 최소 형태로 한 번 이은 뒤 깊이"를 "뼈대 Bolt 로 스택 관통(R1) + SM1 흐름 단위를 먼저 완성(R5)"으로 바꾼다. D-108 을 대체
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정 (D-46 의 표현을 변경)

### D-115 U1 부분 완료와 의존 규칙 — D-92 좁힘
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q8 (후속))
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: U1 을 부분 완료로 두고 기능 Bolt 를 시작하면(Q2) 확정된 의존 규칙의 뜻이 바뀝니다. 어떻게 맞춥니까?
- **선택지**: A) Q2 B 그대로 B) Q2 를 A 로 C) 뒤쪽 시드를 줄임 X) Other
- **사용자 답(원문)**: "A. Q2 의 B 그대로 — D-92 의 "U1 구현 완료"를 "테이블 20개 + 앞쪽 시드 3개"로 좁혀 기록한다. 뒤쪽 시드 6개는 U1 담당이 병렬 첫 주 안에 추가하고, 늦으면 임시 데이터로 일한다"
- **이유·메모**: 의존이 깨지는 자리(필수 기반의 완료가 기능 단위 시작보다 늦어짐)를 짚어 확인받았다
- **결정 요약**: D-92 의 "U1 구현 완료" = 테이블 20개 + 시드 base·consented·s1-transcribed. 뒤쪽 시드 6개는 기능 단위 시작 뒤 병렬 첫 주 안에
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정 (D-92 를 좁힘)

### D-116 뼈대 Bolt 의 단위 구성
- **일시**: 2026-09-17
- **단계**: Delivery Planning (Q9 (후속))
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: 뼈대 Bolt 에는 어느 단위를 담습니까?
- **선택지**: A) U1+U2+U3 B) U1+U2+U3+U4 X) Other
- **사용자 답(원문)**: "B. U1 + U2 + U3 + U4 — A2 화면(업로드·맥락 입력)을 뼈대에서 한 번에 끝낸다. Q3 의 묶음이 그대로 유지되지만 뼈대가 더 커져 네 갈래 대기가 길어진다"
- **이유·메모**: 팀 관행의 뼈대는 업로드(U3 소속)로 관통하고, 단위는 두 Bolt 에 나눌 수 없다
- **결정 요약**: B1 뼈대 = U1(테이블 20 + 앞쪽 시드 3) + U2 + U3 + U4. 혼자 진행, 승인 뒤 네 갈래 시작
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정

### D-117 Bolt 계획 요약 확인
- **일시**: 2026-09-17
- **단계**: Delivery Planning (요약 확인)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: Does this all look correct before I generate the artifact?
- **선택지**: Looks correct / Request changes
- **사용자 답(원문)**: "Looks correct"
- **이유·메모**: 리드가 정한 Bolt 표(B1~B9), 묶음 해석(U9 단독, U11+U12), 갈래 4 의 첫 작업을 U1 뒤쪽 시드로 둔 것, 단위 하나씩 끝내는 Construction 진행 방식을 요약에서 짚었고 함께 승인됨
- **결정 요약**: Bolt 계획 확정
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, risk-and-sequencing-rationale.md)
- **상태**: 확정

<!-- 이 아래에 AI-DLC가 항목을 추가한다 -->

### D-118 Construction 진행 담당
- **일시**: 2026-09-18
- **단계**: Delivery Planning (Construction 진행 방식)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: Construction 을 어떻게 진행할까요? (이 대화에서 단위를 하나씩 / 갈래마다 단위를 맡아 따로 승인)
- **선택지**: One session here / Several teams
- **사용자 답(원문)**: "Several teams"
- **이유·메모**: 5인 전원 풀스택이고 B2~B5 를 네 갈래로 동시에 돌리는 계획(D-111, D-91)과 모양이 맞는다. D-117 이 확정한 단위 하나씩 끝내는 진행 방식이 이 선택의 전제이며 이미 기록되어 있다
- **결정 요약**: 갈래가 각자 작업 단위를 맡아 자기 몫을 따로 승인받는다
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, team-allocation.md)
- **상태**: 확정

### D-119 갈래별 승인 주기
- **일시**: 2026-09-18
- **단계**: Delivery Planning (Construction 진행 방식)
- **질문 파일**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/delivery-planning-questions.md`
- **질문**: 갈래가 자기 단위를 만드는 동안 승인을 얼마나 자주 받을까요? (단계마다 / 단위가 끝날 때 한 번)
- **선택지**: After each stage / Once at the end
- **사용자 답(원문)**: "After each stage"
- **이유·메모**: Python 경험이 일부뿐인 조합(OC-04, R1)에서 잘못 든 방향을 다음 단계가 그 위에 쌓기 전에 잡는 쪽을 택했다. 되돌리는 범위가 단계 하나로 제한된다
- **결정 요약**: 갈래마다 기능 설계·품질 요구·품질 설계·인프라 설계·코드 각 단계가 끝날 때 승인받는다
- **영향 문서**: `aidlc/spaces/default/intents/260916-scd-coaching-mvp/inception/delivery-planning/` (bolt-plan.md, team-allocation.md)
- **상태**: 확정


---

## 4. 미확인 항목 요약

> 상태가 "기본값 적용(확인 필요)", "AI 가정(확인 필요)", "미결정"인 항목의 ID를 여기에 유지한다.

- OQ-U1 은 D-102, OQ-U2 는 D-98, OQ-U3 는 D-111 로 닫힘
- D-46 은 D-114 로 표현 변경, D-92 는 D-115 로 좁힘
- A-11, A-12 (A-01은 D-12로 확정·변경됨, A-02는 D-25로 확정됨, A-03은 D-62·A-04는 D-63·A-10은 D-64로 닫힘)
- A-05 ~ A-08 — D-35 로 "설정값"으로 재분류. 확정값이 아니며 언제든 변경 가능
- A-09 — D-31 로 부분 확정. React 18 / TS 5 / Vite 5 / PostgreSQL 16 / Python 3.11 부분은 확정, Java 21 · Spring Boot 3.3 부분은 D-30 으로 무효
- D-06
- D-37 (live 제공자 미정 — 의도적 보류)
- A6 (원격 저장소와 GitHub Actions 사용 가능 여부 — 저장소 생성 시점에 확인)
- TC-15 는 D-54 로 확정되었고, D3 도 함께 닫혔다
- D-47 은 D-91 로 닫힘(4갈래)

