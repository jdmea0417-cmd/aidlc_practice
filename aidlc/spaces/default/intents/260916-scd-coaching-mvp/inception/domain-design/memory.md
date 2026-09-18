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

## Deviations

- 2026-09-17T05:10:00Z — 백엔드 업무 컴포넌트를 팀 관행의 5개 이름(conversation, assessment, training, record, privacy)에서 account 를 더한 6개로 바꿨다(D-83). 팀 관행 문서는 이 단계에서 고칠 수 없어, 이후 단계는 파일 구조의 이름 수를 도메인 설계의 컴포넌트 카탈로그 기준으로 읽어야 한다.
- 2026-09-17T05:10:00Z — 팀 관행의 삭제 전파 잠정 규칙("파일 삭제 → DB 행 삭제, 남는 쪽은 항상 DB 행")을 "한 트랜잭션에서 DB 행 삭제 후 커밋, 이어서 파일 삭제, 실패한 파일 경로는 삭제 요청에 기록해 다시 지움"으로 대체했다(D-84). 이후 단계는 삭제 순서를 도메인 설계 ADR-006 기준으로 읽어야 한다.

## Interpretations

- 2026-09-17T05:15:00Z — 요약 확인 뒤 카탈로그를 쓰다가 정정 → 재검토 → 추천 재계산 흐름이 순환 의존을 만든다는 것을 발견했다. 사용자가 정한 경계를 지키는 기술 선택이라 묻지 않고 프로세스 안 사건(ADR-009)으로 정했고, Record 를 엔티티 없는 읽기 전용(ADR-010)으로 둔 것도 앞 결정에서 따라 나온 리드 결정으로 기록해 승인 게이트에서 짚는다.
- 2026-09-17T05:15:00Z — 업무 컴포넌트 6개라는 확정 표현을 지키려고, 기술 명세가 이미 자리를 정한 화면 코드(WebApp)와 STT·LLM 어댑터(ProviderAdapters)는 "지원 컴포넌트"로 따로 이름 붙여 카탈로그에 올렸다.
