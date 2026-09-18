<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
- 2026-09-17T00:55:07Z — 단계를 다시 열었을 때 Q19 가 이미 "고칠 것이 없다"로 닫혀 있었다. 그대로 승인으로 넘기지 않고, 이 단계가 끝난 뒤 하위 단계에서 실제로 달라진 사실 두 가지(백엔드 단일화 D-30, F07 의 Must 승격과 배포 성공 판정 확정)를 대조해 Q20 으로 다시 물었다. 되돌아온 이유가 무엇이든, 다시 물을 근거는 하위 단계가 만든 새 사실에서 찾는 것이 맞다고 보았다.
- 2026-09-17T00:55:07Z — F07 의 Must 승격은 이 산출물에 반영하지 않기로 했다. intent-statement 의 제품 경계는 F01~F07 을 등급 없이 나열하므로 등급 변경과 충돌하지 않고, 등급은 scope-document 가 담당한다. 상위 문서가 등급을 말하기 시작하면 두 문서가 어긋날 자리가 생긴다.
- 2026-09-16T05:14:01Z — 검토 지적 R-06 을 사람이 받아들여, 성공 기준에서 빠진 다섯 항목의 분류를 '기능 요구사항'에서 Q11 답변 원문인 '구현 세부사항'으로 되돌렸다. 두 표현은 이후 requirements-analysis 에서 이 항목들이 정식 FR 로 올라오는지를 가르는 차이였고, 사용자가 확정한 것보다 강한 주장을 문서에 남기지 않는 쪽을 골랐다.
- 2026-09-16T05:04:07Z — 검토는 끝났으나 그 결과가 기록되기 전에 세션이 끊겨, 다음 세션에서 기록만 이어서 마무리했다. 두 산출물의 바이트가 검토 요청 이후 바뀌지 않았기에 재검토 없이 그대로 기록됐다. 검토 결과는 진행 가능(READY)이며 지적 R-06 한 건이 열려 있어 승인 단계에서 사용자가 판단한다.
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-16T04:23:18Z — 프로젝트 설명이 docs/input/ 아래 6개 경로를 지목해 단일 문서 입력 규칙에 걸림; 사용자에게 물어 01_vision.md 하나를 근거 문서로 등록했다. 나머지 5개는 이후 단계에서 기존 명세로 다룬다.
- 2026-09-16T04:23:18Z — 성공 기준을 SM1 하나로 확정하면서, 근거 발화 ID 유효성·보류 처리·시도 분리 집계·정정 전파·금지 표현을 기능 요구사항으로 재분류했다. 문제 정의가 '근거와 함께'인데 성공 기준에서 빠지는 긴장을 사용자에게 제시했고 사용자가 재확인했다.
- 2026-09-16T04:47:34Z — 검토 지적 R-03·R-04 는 확정 답변 없이 내가 쓴 내용이었다. 문서에서 지우는 대신 Q17·Q18 로 사람에게 물어 근거를 만들었고, 둘 다 기존 서술대로 확정되었다. 지적의 핵심은 내용이 틀렸다는 것이 아니라 근거가 없다는 것이었다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-16T04:23:18Z — 확인 체크포인트의 요약 브리핑 생성 명령(review-brief summary)이 실패해 그 출력 없이 확인 질문을 제시했다. 요약 자체는 대화로 제시했고 확인 영수증은 정상 기록되었다.
- 2026-09-16T04:47:34Z — 자문 검토가 NOT-READY 를 냈고 사람이 지적 5건 전부 반영을 요청했으나, 이 단계의 검토 예산이 1회라 재검토가 거부되었다. 수정 후 revised 보고도 검토 증거 부재로 거부되어, 도구가 제시한 redo 점프로 단계를 다시 열었다.
- 2026-09-16T04:47:34Z — 검토 브리핑 생성 명령(review-brief review/summary)이 두 번 모두 실패해, 검토 기록 JSON 의 body 를 직접 읽어 지적 사항을 사람에게 그대로 전달했다.

## Tradeoffs
- 2026-09-17T00:54:42Z — 질문 파일의 이전 회차 확인 기록을 보존하려고 별도 H2 절로 옮겼으나, 확인 절 뒤에는 Q<n> 과 지정된 두 절만 올 수 있다는 검사에 걸렸다. 기록은 결정 로그와 감사 기록에 이미 남아 있으므로 파일에서는 이번 회차 내용으로 대체하는 쪽을 택했다. 보존 위치를 한 곳으로 두는 편이 파일 구조를 흔드는 것보다 낫다.
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-16T04:23:18Z — 사용자가 대상 연령을 13~25세로 바꾸겠다고 했을 때 그대로 받지 않고 파급 항목(보호자 열람 동의 주체, 아동 전용 시나리오·문구)을 먼저 물었다. 그 결과 13~18세로 좁혀졌고 시나리오를 새로 쓰기로 정해졌다. 질문 한 라운드를 더 쓴 대신 성인 사용자 동의 문제를 피했다.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-16T04:23:18Z — 05_synthetic-test-data.md의 합성 대화 3건은 대상 연령 변경 시 처리 방침이 정해지지 않았다. 시나리오 원형과 UI 문구만 새로 쓰기로 했고 이 3건은 그 결정에 포함되지 않았다.
- 2026-09-16T04:23:18Z — 보호자 열람 권한을 누가 언제 켜는지(사용자 본인인지 가입 시 기본 설정인지)가 확인되지 않았다.

