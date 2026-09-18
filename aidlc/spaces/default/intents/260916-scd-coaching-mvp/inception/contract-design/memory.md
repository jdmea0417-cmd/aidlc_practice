<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-17T07:30:00Z — 마이그레이션 담당(Q2)과 시드 담당(Q3)을 따로 물었더니, 두 답이 만나 확정된 병렬 시작 결정(D-92)을 깨는 조합이 나왔다. 테이블을 만드는 사람, 그 테이블에 시드를 넣는 사람, 외래 키가 만드는 순서는 서로 묶여 있으므로 같은 질문 안에서 조합의 결과를 보여 주고 물었어야 했다.
- 2026-09-17T07:30:00Z — 접수 후 상태 조회(Q1)를 받자 확정된 NFR3("응답 시간 3초")의 뜻이 비었다. 응답 방식을 바꾸는 답은 시간 기준 요구사항의 측정 대상을 함께 바꾸므로, 요구사항 문서를 고치지 않고 계약 요약에 보완 기준을 적고 "두 문서가 어긋나 보이면 이 문단이 기준"이라고 명시했다.
- 2026-09-17T07:30:00Z — 연습 시도 판정과 삭제는 D-96(202 + 상태 조회)에서 빼고 동기로 두었다. D-96 질문이 업로드·전사·분석을 물었고, 삭제는 ADR-006 의 한 요청 안 트랜잭션 순서를 지켜야 하기 때문이다. 승인 게이트에서 짚는다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-17T07:30:00Z — U1 이 20개 테이블 전체와 모든 시드를 맡으면서 병렬 시작은 지켰지만, U1 이 L 복잡도에서 더 무거워지고 모든 단위의 데이터 모양을 알아야 한다. 대신 테이블마다 column_owner 를 적고, 컬럼을 바꾸는 단위가 U1 담당자를 리뷰어로 넣는 규칙으로 부담을 나눴다. delivery-planning 에서 U1 의 크기를 다시 볼 것.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-17T07:30:00Z — 계약 요약이 구현 중에도 고쳐지는 기준 문서(D-99)인데 AI-DLC 기록 폴더 안에 있다. 이후 단계가 이 파일을 입력으로 쓰므로 고칠 때마다 변경 안내가 나올 것이다. delivery-planning 에서 계약 수정 PR 의 흐름을 확인한다.
