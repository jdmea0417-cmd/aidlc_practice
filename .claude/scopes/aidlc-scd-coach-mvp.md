---
name: scd-coach-mvp
depth: Standard
keywords: []
description: SCD 소통 코칭 MVP - 로컬 Docker Compose 전용 그린필드 빌드
skeleton: on
change_control: relaxed
---

# scd-coach-mvp scope

SCD(사회적 의사소통장애) 소통 코칭 모바일 웹 서비스 MVP를 위해 구성된
맞춤 scope입니다. 그린필드 신규 구축이며, 배포 대상은 로컬 Docker
Compose 환경뿐입니다. 총 19개 스테이지가 EXECUTE, 14개가 SKIP입니다.

Change Control은 relaxed입니다. 승인 이후 입력이 바뀌면 한 줄로 기록·안내하고
실행을 계속합니다.

## Why these stages, why skip those

**Ideation이 축소된 이유**: 제품 방향과 MVP 범위(F01~F07)가 이미
`docs/input/01_vision.md`에 확정되어 있습니다. 따라서 market-research와
team-formation은 새로 알아낼 것이 없어 SKIP합니다. 화면 명세가
`docs/input/03_ui-spec.md`에 A1-A5 / B1-B5 / C1-C5로 이미 작성되어 있어
rough-mockups와 refined-mockups도 SKIP합니다. 대신 feasibility는
EXECUTE로 남깁니다 - 3개 서비스(React / Spring Boot / FastAPI)를 로컬
Compose 한 벌로 묶는 구성에는 확인할 제약이 실재합니다.

**reverse-engineering을 SKIP하는 이유**: 기존 코드와 데이터가 없는
그린필드이므로 역공학할 대상 자체가 없습니다.

**user-stories를 SKIP하는 이유**: 기능 범위와 화면 흐름이 입력 명세에
이미 행위 수준으로 기술되어 있어, requirements-analysis가 그 명세를
추적 가능한 요구사항으로 옮기는 것으로 충분합니다.

**Inception과 Construction 설계 스테이지를 모두 EXECUTE하는 이유**:
판정 상태와 집계 규칙(`04_domain-model.md`)이 이 제품의 핵심 로직이므로
domain-design, units-generation, contract-design이 필요합니다. 서비스가
3개로 나뉘므로 contract-design이 경계를 고정해야 합니다.

**Operation 전체와 ci-pipeline을 SKIP하는 이유**: 클라우드 배포가 없고
로컬 Docker Compose만 사용합니다. 배포 파이프라인, 환경 프로비저닝,
관측성, 인시던트 대응은 운영되는 제품의 몫이며 이 MVP의 범위 밖입니다.
infrastructure-design은 EXECUTE로 남습니다 - Compose 구성 자체가
설계 대상이기 때문입니다.

## Membership

키워드 트리거 없음(조합된 scope는 자동 추론 대상이 아니며, `--scope
scd-coach-mvp`로 명시 선택합니다). Initialization 전체, 축소된 ideation
집합, user-stories와 refined-mockups를 제외한 inception 전체,
ci-pipeline을 제외한 construction이 실행되고 operation은 전부 SKIP됩니다.
