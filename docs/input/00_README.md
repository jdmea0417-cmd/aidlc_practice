# SCD 소통 코칭 — AI-DLC 입력 패키지

AI-DLC(awslabs/aidlc-workflows) 테스트용 입력 문서입니다.
기존 기획서(`SCD_service_proposal_reviewed_v1`, 2026.09.15)의 제품 방향을 유지하고, UI 시안(A/B/C 상세 사용자 흐름 v2)을 화면 명세로 옮겼습니다.

## 파일 구성

| 파일 | 역할 | AI-DLC에서 쓰이는 단계 |
|---|---|---|
| `01_vision.md` | 무엇을·누구를 위해·왜 만드는지, MVP 범위/제외, 미결정 사항 | Requirements Analysis, User Stories |
| `02_tech-environment.md` | 스택(React + Java Spring Boot, Python 분석 서비스 연동), 금지 사항, 코드 예시 | Application Design, Construction |
| `03_ui-spec.md` | UI 시안의 화면 ID·구성요소·상태·이동 | User Stories, Functional Design |
| `04_domain-model.md` | 데이터 모델, 판정 상태, 집계 규칙 | Application Design, Functional Design |
| `05_synthetic-test-data.md` | 합성 대화 3건과 기대 판정 결과 | Build and Test |
| `07_decision-log.md` | 지금까지의 질문·선택 기록과 이후 기록 양식 | 전 단계 (계속 갱신) |
| `06_seed-scenarios.md` | 모의 대화 시나리오 원형 6개, 힌트 문구, Mock 상대 발화 | Functional Design, Build and Test |

## 준비

1. 프로젝트 저장소 루트에 AI-DLC 규칙을 설치합니다(aidlc-workflows README 참고).
2. 이 폴더를 저장소의 `docs/input/`에 넣습니다.
3. (선택) UI 시안 이미지가 있으면 `docs/input/ui/`에 넣습니다. 없어도 `03_ui-spec.md`만으로 진행할 수 있습니다.

> 이 패키지는 **자체 완결형**입니다. 기존 온톨로지 파일, POC 코드, 인수인계 문서, 실제 데이터 없이 진행하도록 작성했습니다.
> AI-DLC가 외부 파일을 찾으면 "No existing files. Use only docs/input." 로 답합니다.

## 시작 프롬프트

```
I want to start a new project. Please read docs/input/01_vision.md and
docs/input/02_tech-environment.md, then begin the AIDLC workflow.
Also treat docs/input/03_ui-spec.md, docs/input/04_domain-model.md and
docs/input/05_synthetic-test-data.md, docs/input/06_seed-scenarios.md
(and images in docs/input/ui/ if present) as
existing specifications and add them to the inception documents.
This is a greenfield project with no existing code or data files.
All documents, questions and UI text should be written in Korean.

DECISION LOGGING (mandatory):
Maintain docs/decisions/decision-log.md, starting from docs/input/07_decision-log.md.
- Every clarification question you ask, at every stage, must be appended as a new
  entry using the template in that file: stage, question, all options,
  my answer exactly as written, reason, affected documents, status.
- Every approval, rejection or change request at a gate is also an entry.
- Never answer a question on my behalf. If you must assume something to proceed,
  log it as "AI 가정 (사용자 확인 필요)" and list it in the "미확인 항목" section.
- If a later answer changes an earlier decision, do not delete the old entry:
  mark it "변경됨 → D-xx" and add a new entry.
- Update the log in the same step in which the answer is received.
```

## 진행 중 유의사항

- 질문 파일의 `[Answer]:`에 답하고 "We have answered your clarification questions. Please re-read the file and proceed." 로 진행합니다.
- 질문이 `01_vision.md`의 "미결정 사항"과 겹치면 **테스트용 기본값**으로 답해도 됩니다. 이 경우 기록 상태는 "기본값 적용(확인 필요)"입니다.
- **모든 질문과 선택은 `docs/decisions/decision-log.md` 한 곳에서 확인합니다.** 단계마다 승인 전에 이 파일에 방금 답한 내용이 들어갔는지 확인하고, 빠졌으면 "Please log my answers to docs/decisions/decision-log.md before proceeding." 라고 요청합니다.
- AI-DLC가 자체적으로 남기는 질문 파일·기록(`aidlc-docs/`)은 원본 증거로 그대로 둡니다. decision-log는 사람이 읽기 위한 통합본입니다.
- 생성된 코드를 직접 고치지 말고, 설계 문서를 고친 뒤 재생성합니다.
- 승인 단계마다 컨텍스트를 새로 시작합니다.
