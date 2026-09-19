<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-18T04:23:46Z — 요구사항이 "무엇을 지킬까"를 정했으므로 설계 단계의 일은 "그것을 어느 구조가 지키게 할까"로 읽었다. 그 결과 산출물의 중심이 패턴 목록이 아니라 공통 장치 여섯 개와 각 장치가 구조적으로 막는 것의 표가 되었다.
- 2026-09-18T04:23:46Z — 함께 본 플랫폼 지식이 클라우드 서비스를 전제로 해서 이 프로젝트에 대부분 적용되지 않았다. 억지로 대응시키지 않고 적용되는 부분(컨테이너 점검, 상태 확인 지점)만 옮긴 뒤 그 사실을 문서 머리에 밝혔다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-18T04:23:46Z — 목표가 넉넉한 프로젝트라 성능 설계를 "빠르게 만드는 것"이 아니라 "조용히 느려질 자리를 없애는 것"으로 썼다. 최적화 기법을 적는 대신 N+1·연결 고갈·요청 내 외부 호출·무거운 기동 네 자리를 차단 설계로 짝지었다.
- 2026-09-18T04:23:46Z — 회로 차단기를 두지 않기로 하면서, 대신 나중에 붙일 자리(공용 감싸기 장치)를 함께 적었다. 지금 안 만드는 것의 비용을 "나중에 어디를 고치면 되는가"로 갚는 방식이다.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-18T04:23:46Z — 검토가 낸 R-01(Minor): traceability.json 의 reverse 항목이 ID 가 아니라 한국어 서술 라벨이다. 기계 대조가 어려워질 수 있다. 승인 게이트로 올린다.
- 2026-09-18T04:23:46Z — 검토가 낸 R-02(Minor): security-design.md §1.2 와 logical-components.md §1 이 "구조적으로 불가능"을 단정하는데, 같은 문서의 가정 절이 그 일부를 전제에 기대고 있다고 적어 본문과 가정이 긴장 관계에 있다. 승인 게이트로 올린다.
