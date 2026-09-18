<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-18T02:53:08Z — 로컬 전용이라 확장성·가용성 범주가 비었다. 명목 수치로 형식을 채우는 대신 "목표를 두지 않는다"를 이유와 함께 명시하고, 그 자리에 이번 범위에서 실제로 지킬 것(한 명령 기동, 실패를 사람이 알아채는 방법, 되돌리기)을 적었다. 검증할 수 없는 수치를 남기지 않는 쪽을 골랐다.
- 2026-09-18T02:53:08Z — 상위 NFR 의 글자 그대로의 범위보다 넓은 요구사항을 그 밑에 붙일 때는, 넓혔다는 사실과 실제 출처를 같은 문서에 구분선으로 적었다. 검토가 지적하기 전에는 이 구분이 없어 다음 단계가 커버리지를 잘못 판단할 수 있었다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-18T02:53:08Z — 상위 산출물이 이 단계에 배정한 열린 질문(OQ-F4 헬스체크 확인 질의 시간 제한)을 처음에는 질문 목록에서 빠뜨려 다음 단계로 재위임했다. 검토(R-02)가 짚어 1초로 닫았다. 질문을 만들 때 상위 산출물의 "담당 단계" 표를 먼저 훑지 않은 것이 원인이다.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-18T02:53:08Z — 제공자가 미정인 채로 타임아웃 값을 먼저 박았다(연결 5초 / 읽기 60초). 값이 제공자에 안 맞을 위험을 받고, 어댑터 코드가 지금 완결되는 것과 값만 바꾸면 되는 것을 얻었다. 설정값이라 되돌리는 비용이 낮다는 점이 결정 근거다.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-18T02:53:08Z — 검토가 낸 R-06(Minor): tech-stack-decisions.md §3 의 "이 단계에서 새로 정한 설정값" 표에 헬스체크 질의 시간 제한 1초가 빠졌다. 값 자체는 다른 세 문서에 있으나 한 표에서 누락됐다. 승인 게이트로 올린다.
