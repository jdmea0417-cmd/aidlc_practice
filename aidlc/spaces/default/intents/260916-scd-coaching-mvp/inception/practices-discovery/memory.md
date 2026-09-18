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

- 2026-09-16T08:10:00Z — 승격 도구가 `## Mandated` / `## Forbidden` 절 안의 비어 있지 않은 모든 줄을 각각 하나의 규칙으로 취급한다는 것을 도구 구현에서 확인했다. 리드 초안은 규칙 하나를 세 줄에 걸쳐 줄바꿈해 두어, 그대로 승격하면 규칙 하나가 세 조각으로 쪼개져 `project.md` 에 들어간다. 통합 단계에서 각 규칙을 한 줄로 합치도록 지시해야 한다.
- 2026-09-16T08:10:00Z — 같은 확인에서 `## Sources` 나 `## 여기 올리지 않은 것` 같은 추가 H2 는 무해하다는 것도 알았다. 절 추출이 이름으로 지정된 절만 가져가기 때문이다. 리드가 걱정한 두 가지 중 하나만 실제 문제였다.
- 2026-09-16T08:20:00Z — 품질 검토가 성공 기준 SM1 의 실제 범위를 좁혔다. 합성 대화 3건 중 S3 의 검증 항목 2(전사 정정 후 재분석)와 4(삭제 시 연결 항목 처리)가 F07 과 화면 C5 에 걸려 있는데 둘 다 Should 로 내려가 있어, Must 범위만으로는 그 두 항목을 확인할 수 없다. 이는 관행 문제가 아니라 범위 문제이므로 인터뷰에서 사용자에게 직접 확인해야 한다.
- 2026-09-16T08:20:00Z — 품질 검토가 리드 초안의 근거 하나가 실제 원문과 다르다는 것을 짚었다. 가정 A4 의 원문은 "이식한 코드에 원래 테스트 케이스를 그대로 옮겨 통과시킨다"로 오히려 test-after 서술인데, 초안은 이를 test-first 의 근거로 인용했다. 결론(규칙 엔진만 테스트 선행)은 기대 판정표가 이미 문서로 존재한다는 별개 근거로 여전히 서지만, 인용은 통합 단계에서 고쳐야 한다.
- 2026-09-16T08:35:00Z — 걷는 뼈대 영역에서 스테이지 파일이 지정한 문장("얇은 종단 슬라이스를 먼저 만들까요?")을 그대로 묻지 않고 뼈대의 내용을 묻는 질문으로 바꿨다. 뼈대를 먼저 만든다는 것 자체는 D-46 과 활성 스코프의 `skeleton: on` 으로 이미 닫혀 있어, 그대로 물으면 project.md 의 "앞 단계가 닫은 영역은 다시 묻지 않는다" 규칙과 정면으로 부딪힌다. 영역은 덮되 열려 있는 부분만 물었다.
- 2026-09-16T08:35:00Z — 검토자 세 명의 반대 의견 중 대부분을 인터뷰로 올리지 않고 통합 단계의 정정 사항으로 분류했다. 사실관계 오류(A4 인용, SQLModel 기각 근거, .gitignore 실존), 누락 보완(오류 처리 규약, 역방향 계층 규칙, 잠금 파일), 강제 수단 제안은 리드와 다투는 문제가 아니라 리드가 반영할 내용이기 때문이다. 사람의 판단이 필요한 것 — 저장소 운영, 뼈대 내용, 테스트 시점, 커버리지 바닥, 배포 성공 정의, 도구 확정 시점, 범위 밖 검증 항목 — 일곱 가지만 올렸다.
