<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->

## Interpretations

- 2026-09-17T04:30:00Z — 여정 순서 묶음(Q2)이 가져오기부터 시작하도록 확정되었지만, 홈은 여정의 입구라 US1 로 맨 앞에 두었다. 확정 순서의 나머지는 바꾸지 않았다.
- 2026-09-17T04:45:00Z — 몹 검토가 요약 확인 뒤에 사람의 판단이 필요한 빈자리 4건을 냈다. 요약 확인 후 발견한 빈자리는 열린 질문으로 넘긴다는 규칙과, 몹의 판단 문제는 그 자리에서 사람에게 올린다는 단계 지침이 부딪혔는데, 몹 지침을 따랐다. 네 건 모두 Must 흐름(삭제 진입, SM1 종단, 리포트 표시, 추천)에 걸려 넘기면 수용 기준을 쓸 수 없었기 때문이다.
- 2026-09-17T04:45:00Z — 요약 확인 뒤에 추가한 질문은 H2 제목을 FU 가 아니라 Q6~Q10 으로 붙였다. 질문 파일은 요약 뒤에 Q<n> / Requested Changes Feedback / Assumption Confirmation 만 허용하기 때문이다. 추가 질문으로 확인된 내용이 바뀌었으므로 요약을 갱신해 다시 확인받은 뒤 산출물을 다시 썼다.

## Deviations

- 2026-09-17T04:50:00Z — Q9 의 답(최근 어려움 하나만 추천)이 승인된 요구사항 FR8.5 를 좁혀 바로 반영하지 않고 영향 표와 Q10 으로 확인했다. 거절한 목표가 다시 추천되는 자리를 먼저 짚었고, 사용자는 알고 수용했다. 요구사항 문서는 승인된 상태라 고치지 않고, 결정 D-78 과 스토리 US7.3·US14.1 이 기준이 되도록 적었다.

## Tradeoffs

- 2026-09-17T04:55:00Z — 몹의 지식 문제 반대 의견을 전부 리드가 받아들여 2라운드를 돌리지 않았다. 의견끼리 부딪히는 자리가 없었고, 반영 내역과 올리지 않은 이유는 평가 문서에 표로 남겼다. 그 대가로 스토리가 37개, 일부 스토리의 수용 기준이 6~7개로 확정 크기를 조금 넘었고 그 사실을 산출물에 적었다.
