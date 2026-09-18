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

- 2026-09-17T03:50:00Z — 질문을 두 갈래로만 만들었다. 앞 단계가 이 단계로 넘긴 가정 3건(A-03 플랫폼, A-04 모의 대화 매체, A-10 판정 기준)과, 확정된 기능·화면을 요구사항 문장으로 옮기다 드러난 미정 동작 5건이다. 기능 목록·우선순위·성공 기준·기술 스택은 모두 닫혀 있어 묻지 않고 질문 파일 서두에 열거했다.
- 2026-09-17T03:50:00Z — 화면 단위 등급과 기능 단위 등급을 교차 검토해 빈자리 하나를 찾았다. F07 을 Must 로 올린 이유가 합성 대화 S3 의 검증 항목 2(정정 후 재검토 표시와 재분석)인데, 재분석 버튼과 재검토 배지는 Should 화면 C4 에만 있었다. Q5 와 FU3 로 A3 에 두 기능을 옮겨 Must 안에서 닫았다.
- 2026-09-17T04:05:00Z — Q1 의 답(노트북까지 완전 반응형)이 확정 제약 TC-02 와 확정 팀 관행 "E2E 는 3건에서 늘리지 않는다"를 건드려 바로 반영하지 않고 영향 표를 만들어 FU1 로 확인했다. 표에서 팀 관행과의 충돌을 먼저 짚었고, 사용자는 노트북 레이아웃을 Should 로 미뤄 두 확정 항목을 모두 지켰다.
- 2026-09-17T04:05:00Z — Q8 로 보호자 열람 범위를 정하자 보호자가 들어오는 경로와 보는 화면이 어느 단계도 묻지 않는 값으로 드러나 FU2 로 그 자리에서 확정했다. 보호자 전용 읽기 화면은 UI 명세 15개 화면에 없는 새 화면이므로 요구사항에서 근거를 FU2 로 명시한다.

## Deviations

- 2026-09-17T04:20:00Z — 요구사항 문서를 쓰는 도중에 Must 화면에서 Should 화면으로 가는 이동(B5 "기록 보기"→C3, C1 목록→C2~C4)이 빈자리로 드러났다. 통합 요약 확인이 이미 끝난 뒤라 질문 파일을 다시 열지 않고, 열린 질문 OQ1 로 적어 수용 기준을 쓰는 user-stories(2.4)에 담당을 지정했다. 승인 게이트에서 사용자에게 짚는다.

## Tradeoffs

- 2026-09-17T04:05:00Z — FU2=A(보호자도 자기 계정)와 D-25("계정은 사용자가 만든다")는 해석이 갈릴 수 있다. D-25 는 사용자 본인의 계정을 보호자가 대신 만들지 않는다는 결정이었고, 보호자가 사용자의 초대를 받아 자기 계정을 만드는 것은 그와 충돌하지 않는다고 읽었다. 이 해석은 통합 요약 확인에서 다시 확인받는다.
- 2026-09-17T04:05:00Z — Q4=C 의 "고칠 곳이 전사·맥락이면 안내"를 시스템이 판단할 방법이 없어, 수정 요청에서 사용자가 이유 종류(전사가 틀림 / 맥락이 틀림 / 판단이 이상함)를 고르게 하는 것으로 해석했다. 통합 요약에 적어 확인받는다.
