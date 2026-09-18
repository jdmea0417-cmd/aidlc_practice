---
name: scd-coach-mvp
depth: Standard
keywords: []
description: SCD 소통 코칭 모바일 웹 MVP — 명세 확정·로컬 전용 그린필드
skeleton: on
change_control: relaxed
---

# scd-coach-mvp scope

SCD(사회적 의사소통장애) 소통 코칭 모바일 웹 서비스 MVP를 위한 합성
스코프. 그린필드이지만 제품 방향·화면·도메인 모델·기대 판정 픽스처가
`docs/input/` 아래 6개 명세로 이미 확정돼 있고, 클라우드 배포는 명시적
범위 제외(로컬 Docker Compose 전용)라는 두 가지 사실이 이 그리드를
결정한다. 예산은 3개 서비스(React / Spring Boot core / FastAPI analysis)
사이의 설계·계약·검증에 집중한다.

Change Control은 relaxed다: 승인 이후 입력이 바뀌면 한 줄로 기록·통지하고
진행한다. 미결정 11건이 실행 중 순차 확정될 예정이라, 매번 승인을 다시
여는 대신 `docs/decisions/decision-log.md`에 기록하고 이어간다. 게이트
자체는 16개 그대로 유지된다.

Walking skeleton은 on이다. 성공 기준 1번이 "합성 대화 3건이 업로드 →
전사 확인 → 리포트 → 목표 선택 → 모의 대화 → 기록까지 끊김 없이
이어진다"로, 교차 언어 A→B→C 전체 연결 자체가 첫 번째 증명 대상이다.

## Why these stages, why skip those

**Ideation은 탐색이 아니라 확정·기록으로 축소된다.** `market-research`,
`team-formation`, `rough-mockups`는 SKIP — 대상 사용자·포지셔닝·범위
제외가 `01_vision.md`에 이미 있고, 15개 화면의 구성·상태·내비게이션이
`03_ui-spec.md`와 시안 이미지로 고정돼 있으며, 1인 로컬 실행이라 조율할
다중 팀이 없다. 남는 것은 `intent-capture`(미결정 11건과 D-01 스택 분기를
질문으로 올림), `scope-definition`(F01~F07을 intent backlog로, "클라우드
없음·진단 없음·종합점수 없음" 경계를 산출물로 고정), `feasibility`(D-01의
Java–Python 연동 가부는 컴포넌트 모델 확정 **전에** 결론이 나야 함),
그리고 위상 경계인 `approval-handoff`.

**구조 단계 3개는 기계적 기본값을 뒤집어 EXECUTE한다.**
`units-generation`은 프론트 15화면 / core 6패키지 / analysis 3라우터로
논리 단위가 2개를 크게 넘기 때문이고, `contract-design`은 프론트엔드
타입이 springdoc OpenAPI에서 **생성**되고 core→analysis가
`AnalysisClient`·`SttProvider`·`LlmProvider` 인터페이스로 Mock/HTTP 교체를
전제하기 때문이며(계약이 틀리면 세 단위가 동시에 깨진다),
`delivery-planning`은 Flyway 스키마 → core 판정·집계 → analysis 계약 →
프론트 A·B·C로 이어지는 교차 언어 의존 순서가 단순하지 않기 때문이다.

**NFR 두 단계를 모두 유지한다.** 서비스 원칙 10개(진단 금지, 종합점수
금지, 모든 판정에 근거 발화 ID), 금지 표현, 전사문 프롬프트 인젝션 방어,
삭제·공유 권한 전파는 단일 목표가 아니라 세 서비스를 가로지르며 서로
얽힌 제약이다. "종합점수가 구조적으로 불가능"하도록 만드는 방법은
자명하지 않으므로 `nfr-design`이 별도로 선다.

**Operation 전체와 `ci-pipeline`은 SKIP.** 클라우드 배포가 범위 밖이라
구축할 파이프라인도, 프로비저닝할 환경도, 배포 대상도 없다 —
`docker compose up`은 `infrastructure-design`과 `build-and-test`가 담당한다.
`performance-validation`도 SKIP: 성능 목표가 "Mock 기준 분석 3초 이내"
단일 수치뿐이고 실사용 부하가 없어 E2E 단언으로 닫힌다. `ci-pipeline`은
현재 git 저장소가 아니어서 트리거가 없기 때문이며, 5종 테스트 스택과
커버리지 기준은 `build-and-test`가 그대로 실행한다.

## 되살릴 조건 (un-SKIP triggers)

- `ci-pipeline`: git 저장소를 만들고 원격에 푸시할 계획이 생기는 시점.
  이 그리드에서 가장 먼저 되살릴 단계다.
- `refined-mockups`: `03_ui-spec.md`와 시안 이미지만으로 화면을 확정하기
  어렵다고 판단될 때. 현재 이 둘이 화면 설계의 유일한 근거다.
- Operation 단계 전체: 로컬 전용 제약이 풀리고 실제 배포가 범위에 들어올 때.
- `performance-validation`: 실사용 부하나 Mock 외 실제 STT·LLM 연동이
  범위에 들어올 때.

## Membership

Keyword triggers: 없음 (`keywords: []`). 합성 스코프는 추론에 참여하지
않으며 `--scope scd-coach-mvp`로만 해석된다. Initialization 3단계, 축소된
ideation 4단계, inception 전체(reverse-engineering·user-stories·
refined-mockups 제외), construction의 빌드 경로(ci-pipeline 제외)가
실행되고 operation은 전체 SKIP이다. 총 19 EXECUTE / 14 SKIP.
