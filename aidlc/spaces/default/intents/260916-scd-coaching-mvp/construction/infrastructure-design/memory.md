<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-18T05:10:11Z — 이 단계로 배정된 열린 질문이 넷이어서, 질문 파일 서두에 그 목록과 어느 질문이 어느 것을 닫는지를 표로 먼저 적고 시작했다. 앞 단계에서 배정받은 질문을 빠뜨린 적이 있어 같은 실수를 구조로 막았다.
- 2026-09-18T05:10:11Z — 이 단계의 cicd-pipeline.md 와 ci-pipeline(3.7)이 같은 것을 두 번 만들 수 있어, 이 문서를 요구 명세로 두고 역할 경계를 문서 머리에 표로 못박았다. 어긋나 보이면 무엇이 어느 문서 기준인지도 함께 적었다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-18T05:24:22Z — 검토 판정 접수가 세 번 막혔다. 검토 자체는 끝났는데 검토자가 쓴 지적 표 안에 표 기호가 그대로 들어가 칸 수가 어긋났고, 그래서 판정이 기록되지 않았다. 규정된 재시도 한 번을 쓴 뒤에도 같은 자리에서 걸려, 사용자 결정으로 지적을 먼저 고치고 변경 요청 기록으로 검토 회차를 초기화한 뒤 다시 받았다. 세 번째 요청에서 표 형식 규칙을 명시하니 접수되었다.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-18T05:24:22Z — 추적 파일에 무엇을 넣을지 정할 때 "이 단계가 인프라로 답한 항목"만 골랐는데, 검토가 두 번(R-02, R-06) 같은 종류의 누락을 짚었다. 산출물 본문이 근거로 인용한 항목은 답한 항목이 아니어도 추적에 들어가야 한다는 것이 두 지적의 공통점이다.
- 2026-09-18T05:10:11Z — 연결 풀을 작게(5) 잡아 누수가 빨리 드러나게 했다. 다만 검토(R-02)가 짚었듯 응답 이후 작업의 별도 연결과 실패 기록용 추가 연결까지 세어 보지 않았다. 누수 감지라는 이득과 동시 사용 시 고갈 위험을 저울질했어야 하는데 한쪽만 계산했다.
- 2026-09-18T05:10:11Z — 컨테이너 헬스체크 상한을 재기동 목표와 같은 60초로 맞췄다. 두 값이 같으면 목표를 넘겼을 때 즉시 드러나는 이득이 있으나, 헬스체크 통과가 곧 목표 측정이라 61초를 재는 수단은 되지 못한다.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-18T05:24:22Z — 검토가 낸 R-06(Major): 산출물이 근거로 인용한 NFR10.13·NFR5.2·NFR12.5 가 추적 파일에 없다. R-02 와 같은 종류의 누락이 반복된 것이라 승인 게이트로 올린다.
- 2026-09-18T05:24:22Z — 검토가 낸 R-05(Minor): §2.1 의 동시 연결 상한 3 계산이 인용한 근거 문서와 정확히 맞지 않는다. 한 작업만 보면 2이고, 3이 되려면 서로 다른 대화의 작업이 겹쳐야 하는데 그 전제를 적지 않았다. 풀 5는 어느 쪽 해석에서도 여유가 있다. 승인 게이트로 올린다.
- 2026-09-18T05:10:11Z — 검토가 낸 R-01·R-02(Major): traceability.json 의 upstream_ids 에서 NFR10.2(무상태)와 NFR10.14(작업 실패 기록용 별도 연결)가 빠졌다. 특히 NFR10.14 는 연결 풀 크기 판단에 반드시 들어갔어야 할 항목이다. 승인 게이트로 올린다.
- 2026-09-18T05:10:11Z — 검토가 낸 R-03·R-04(Minor): 컨테이너 헬스체크의 timeout·start_period 미지정, NFR10.1 추적 설명이 실제 보장보다 강하게 적혔다. 승인 게이트로 올린다.

### 2회차 승인 게이트 — Request Changes (R-05, R-06)

READY 판정이었으나 사용자가 두 지적을 먼저 고치기로 했다. 결론값(연결 풀 5, 헬스체크 설정)은 어느 쪽도
바뀌지 않았고 바뀐 것은 근거 서술과 추적 목록이다.

- **R-06 (Major)** — `infrastructure-specification.md` §2.1 이 인용한 NFR10.13, `monitoring-design.md` 가
  인용한 NFR5.2·NFR12.5 가 `traceability.json` 의 상위 항목 목록에 없었다. 세 항목을 상위 목록과 커버리지에
  더해 25 → 28 이 되었다. 두 산출물의 출처 표도 같은 ID 를 담도록 맞췄다. **R-02 와 같은 결함이 같은 단계
  안에서 재발한 것**이며, 이번 회차의 §13 의식에서 규칙(c1)으로 승격되었다.
- **R-05 (Minor)** — §2.1 의 "동시 점유 상한 3" 이 인용 출처인 `reliability-design.md` §2 와 어긋났다. 그
  문서는 작업 연결을 닫은 **뒤에** 실패 기록 연결을 열므로 두 줄은 겹치지 않고, 한 작업만 기준으로 하면
  상한은 2다. 3 은 서로 다른 두 대화의 작업이 겹칠 때 나오는 값인데 그 전제가 문서에 없었다. 세 문단으로
  나눠 다시 썼다 — 한 작업일 때 2, 두 작업이 겹칠 때 3, 이 절이 쓰는 값은 보수적인 3. 확장식도
  `1 + (작업 수 × 2)` 에서 `1 + 작업 수` 로 고쳤다(한 작업은 어느 순간에도 연결 하나만 점유한다).
