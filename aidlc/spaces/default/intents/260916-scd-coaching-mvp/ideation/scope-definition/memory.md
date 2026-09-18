<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
- 2026-09-17T01:37:46Z — F07 승격을 반영할 때 실제로 열려 있던 것은 두 가지뿐이었다: 화면 C5 중 어디까지가 Must 인가, 그리고 F07 이 만드는 순서의 어느 단계로 가는가. 등급 변경 자체는 practices-discovery 에서 이미 닫혔으므로 다시 묻지 않고, 그 변경이 남긴 빈칸만 물었다.
- 2026-09-17T01:37:46Z — 사용자가 처음 고른 C5 전체 승격(F3 = B)이 보호자 권한을 Should 로 둔 확정 결정(F1 = C)과 부딪혔다. 바로 반영하지 않고 무효화되는 확정 항목 8건을 표로 열거해 확인받았더니, 그중 6번(Must 항목이 Should 항목에 의존하게 됨)을 보고 사용자가 C5 를 쪼개는 안으로 바꿨다. 표가 없었다면 의존 문제가 units-generation 까지 내려갔을 것이다.
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
- 2026-09-17T01:37:46Z — Must 비율이 64%에서 73%로 올라 프레임워크 권고 60%를 더 크게 넘게 되었다. 수치를 맞추려 내용을 줄이지 않고, 초과 사실과 그 이유(PU-01~07 은 성공 기준의 종단 경로 자체이고 PU-08 은 그 성공 기준을 판정할 자료의 절반을 확인 가능하게 만든다)를 산출물에 의도된 것으로 적었다.
- 2026-09-17T01:37:46Z — 질문 파일에 F3 = B 답변을 지우지 않고 "변경됨 → F5" 표기와 함께 남겼다. 무엇이 왜 바뀌었는지가 파일 안에서 읽히는 편이, 최종 답만 남기는 것보다 하위 단계에 쓸모 있다고 보았다.
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->

## Interpretations

- 2026-09-16T06:20:00Z — 질문을 "F01~F07 안에서 무엇을 먼저 만드는가"로 좁혔다; 기능 목록과 제외 항목, 성공 기준, 대상, 스택, 일정은 앞 단계가 모두 닫아 두었기 때문이다. 질문 파일 서두에 다시 묻지 않는 항목을 명시해 사용자가 중복 질문으로 오해하지 않게 했다.
- 2026-09-16T06:20:00Z — F07(정정·삭제)이 성공 기준 SM1의 종단 경로 밖에 있다는 점을 우선순위 질문의 축으로 삼았다; SM1이 열거한 여섯 단계 어디에도 정정·삭제가 없어서, 7주 일정에서 가장 먼저 논의해야 할 경계선이 그 지점이라고 판단했다.
- 2026-09-16T06:40:00Z — C5 화면이 Must 기능과 Should 기능을 동시에 담고 있다는 점을 모순으로 잡아냈다; 보호자 권한은 Must(Q4=A)인데 그 권한을 켜는 유일한 화면인 C5는 Should(Q2=B)로 내려가 있었다. 화면 단위 우선순위와 기능 단위 우선순위가 한 화면에서 충돌할 수 있다는 것이 이 단계에서 배운 점이다.
- 2026-09-16T06:40:00Z — 답변들이 범위를 줄이는 방향과 늘리는 방향으로 동시에 움직인 것을 범위-일정 검증 질문(F2)으로 되돌렸다; Q1·Q2가 F07과 C2~C5를 Should로 내린 만큼을 Q3·Q4의 직접 녹음과 정식 인증이 다시 채워, 순 감소가 사실상 없었다.

## Deviations

- 2026-09-16T06:40:00Z — Must가 proto-Unit 11개 중 7개로 프레임워크 지침의 60% 상한을 넘었지만 줄이지 않았다; Must 7개가 곧 성공 기준 SM1의 종단 경로 자체라 더 줄이면 최소 가치 범위가 무너지기 때문이다. 초과를 숨기지 않고 작업 목록 §2에 의도된 것으로 명시했다.

## Tradeoffs

- 2026-09-16T06:40:00Z — 인증을 Should로 내리면서 Must 경로를 "고정 사용자 하나"로 돌리기로 했고, 대신 데이터 모델은 사용자 개념을 처음부터 갖추도록 작업 목록에 못 박았다; 인증 구현은 미루되 스키마 변경 비용은 미루지 않는 쪽을 택한 것이다.
- 2026-09-16T06:40:00Z — 보호자 권한 3단계 결정이 "취소된 것이 아니라 시점만 뒤로 갔다"는 문장을 범위 문서와 작업 목록 양쪽에 넣었다; Should로 내려간 항목이 하위 단계에서 "확정 취소"로 읽히면 이미 승인된 의도 서술과 어긋나기 때문이다.

## Open questions

- 2026-09-16T06:40:00Z — Should 항목의 착수 시점은 종단 흐름이 언제 서는지에 달려 있어 이 단계에서 정할 수 없었다; 작업 계획 단계에서 잔여 일정을 보고 다시 판단해야 한다.
