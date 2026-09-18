<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-18T00:13:15Z — team-formation(1.5)이 범위 밖이라 팀 구성표가 없어, AI-DLC 의 mob 자리에 이 팀의 "갈래"를 대응시켰다. Bolt 를 갈래 1~4 에만 배정하고 사람 이름은 적지 않았다(D-112). 5인 전원 풀스택·고정 역할 없음이라는 제약(OC-03)이 그 근거다.
- 2026-09-18T00:13:15Z — Bolt 사이 순서를 위상 정렬이 아니라 시연 필수선(SM1)의 흐름 순서로 잡았다. 의존 DAG 가 허용하는 경로 중 사람이 고른 경제적 경로이며, 벗어난 자리는 risk-and-sequencing-rationale.md §3 에 남겼다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-18T00:13:15Z — 산출물 네 개를 쓴 뒤에 Construction 진행 담당·승인 주기 답(D-118, D-119)이 나왔다. 확정된 산출물을 다시 쓰지 않고 bolt-plan.md 의 "Construction 진행 방식" 절과 team-allocation.md 의 "배정 원칙" 절에 덧붙여 갱신했다. 앞 절의 내용은 그대로 두었다.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-18T00:13:15Z — 갈래별 승인 주기를 "단계마다"로 두었다(D-119). 단위가 끝날 때 한 번만 보는 쪽이 갈래의 속도는 빠르지만, Python 경험이 일부뿐인 조합(OC-04, R1)에서는 되돌리는 범위가 단위 통째가 된다. 중단이 늘어나는 비용을 받고 되돌리는 범위를 단계 하나로 묶는 쪽을 골랐다.
- 2026-09-18T00:13:15Z — 뼈대 Bolt 에 U4(맥락)까지 담아 A2 화면을 한 번에 끝냈다(D-116). 뼈대가 커져 네 갈래의 대기가 길어지는 대신, 화면 하나가 두 Bolt 로 갈라지지 않는다.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-18T00:13:15Z — 누가 어느 갈래를 맡는지는 이름 없이 남겨 두었다. B1 승인 직후 팀이 정해 docs/decisions/decision-log.md 에 남긴다(OC-05).
- 2026-09-18T00:13:15Z — 계약 요약의 열린 질문 6건과 품질 요구 항목(NFR4·NFR6·NFR11 등)은 functional-design(3.1)·nfr-requirements(3.2)가 닫는다. phase-check-inception.md §3·§4 에 담당 단계와 함께 적어 두었다.
