<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-17T06:20:00Z — 기능 단위 기준(Q1)과 4갈래(Q4)를 함께 받고 나서야 기능끼리 구현 완료 의존을 두면 흐름이 거의 한 줄이 되어 기반 직후 병렬로 시작할 수 있는 단위가 하나뿐이라는 충돌이 드러났다. 그래서 의존의 뜻을 Q5 로 따로 물었다. 단위 기준과 병렬 수를 묻는 단계에서는 의존을 무엇으로 볼지를 같은 회차에 함께 묻는 편이 낫다.
- 2026-09-17T06:20:00Z — yaml 간선 블록의 단위 이름을 요약의 짧은 이름(backend-foundation)이 아니라 디렉터리 이름(u1-backend-foundation)으로 썼다. Construction 단계들이 단위를 `u1-auth` 모양으로 가리키므로 이름과 디렉터리가 같아야 조인이 깨지지 않는다.
- 2026-09-17T06:20:00Z — 기능 단위가 백엔드와 화면을 함께 담아 kind 를 지정하지 않았다. 억지로 service 를 붙이면 화면 설계 산출물이 빠지므로 전체 설계 산출물을 받는 쪽을 택했다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-17T06:20:00Z — 계약 기준 의존(Q5)은 병렬도를 얻는 대신 통합 시점의 위험을 DAG 밖으로 옮긴다. US9.3(SM1 종단 리허설)처럼 여러 기능 단위가 통합되어야 통과하는 수용 기준은 간선으로 표현되지 않으므로, 간선을 추가해 확정 결정을 넘어서지 않고 열린 질문 OQ-U3 로 delivery-planning 에 넘겼다.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-17T06:20:00Z — OQ-U1: 기능 단위가 병렬로 Alembic 리비전을 만들면 헤드가 갈라진다. 초기 스키마를 기반 단위가 한 번에 만들지, 단위별로 만들고 병합 규칙을 둘지 contract-design(2.8)에서 정한다.
- 2026-09-17T06:20:00Z — OQ-U2: 계약 기준 병렬 시작에 필요한 시드 상태 목록과 시드 유지 담당은 contract-design(2.8)에서 정한다.
- 2026-09-17T06:20:00Z — OQ-U3: US9.3 의 수용 기준(AC9.3.1)은 동의부터 기록까지 흐름이 지나는 U2~U7 이 통합되어야 통과한다. U8 의 마감 시점은 delivery-planning(2.9)에서 정한다.
