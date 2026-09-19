<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-18T01:27:30Z — u1-backend-foundation 은 테이블 20개를 다 만들지만 소유 엔티티는 User 하나뿐이다. 나머지 19개는 entities.md 에 "이번에 적는 것 / 소유 단위에 남기는 것" 경계표로 등록해, 상위 문서가 이 단계에 남긴 자리만 채우고 다른 단위의 설계를 앞지르지 않게 했다.
- 2026-09-18T01:27:30Z — 스키마 적용을 기동 흐름 밖의 별도 단계로 두었다. 기동할 때마다 마이그레이션이 도는 모양은 컨테이너가 동시에 뜰 때 경쟁이 생기고, 팀 관행이 전진 방향만 쓰기로 한 것과도 결이 맞지 않는다. 상위 문서가 정하지 않은 자리라 리드 판단으로 적고 가정에 남겼다.
- 2026-09-18T00:54:16Z — 설치된 실행 파일의 "알 수 없는 명령" 실패는 기능 부재의 근거가 아니라고 해석한다. 저장소가 함께 들여온 도구에 그 명령이 있는지, 버전 기록이 무엇인지, 대체 호출 경로가 되는지를 먼저 확인한 뒤에야 기능 부재로 판단한다.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-18T00:54:16Z — 이 단계 진입 시 `next` 가 `unknown verb 'refresh-unit-progress'` 로 실패했다. 설치된 `aidlc` 실행 파일만 근거로 "갈래별 소유가 지원되지 않는다"고 잘못 판단해 사용자의 확정 결정(D-118)을 되돌리자고 두 차례 제안했다. 사용자의 되물음으로 확인한 결과 프로젝트 셸과 실행 파일이 같은 2.8.2 이고 그 명령은 `.claude/tools/aidlc-state.ts` 에 이미 있었으며, 프로젝트 도구를 직접 호출하니 정상 동작했다. D-118·D-119 를 유지하고, 이 단계부터는 `bun .claude/tools/aidlc-*.ts` 로 호출한다. 자세한 경위는 `docs/decisions/decision-log.md` D-120.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-18T01:27:30Z — 대화 상태를 두 컬럼으로 나눴다(Q2). 조합 규칙 BR7.1~BR7.3 을 새로 써야 하는 비용을 받고, 재분석 중에도 전사가 화면에 남는 성질을 얻었다. 컬럼 하나였다면 F07 재검토 흐름이 전사 표시를 따로 우회해야 했다.
- 2026-09-18T01:27:30Z — 헬스체크가 저장소까지 확인하게 했다(Q4). 저장소가 잠깐 느릴 때 실패로 보이는 비용을 받고, "컨테이너는 떴는데 못 붙은" 상태가 시연 당일 첫 요청에서 처음 드러나는 일을 막았다.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-18T01:27:30Z — 검토가 낸 R-01: 이 단위가 정한 내부 상태값 이름(TRANSCRIBED, NOT_ANALYZED 등)이 확정된 API 계약 C2 의 값(READY, NOT_STARTED)과 다르다. 대응표나 번역 소유자를 아무 문서도 적지 않았다. 사람의 판단이 필요해 승인 게이트로 올린다.
- 2026-09-18T01:27:30Z — 검토가 낸 R-02: 상태 기계 SM-A 가 파일 저장 실패와 전사 실패를 한 상태로 합쳤는데, 계약 C2 의 다시 시도는 전사만 가리킨다. 저장 실패의 회복 경로가 적히지 않았다. 사람의 판단이 필요해 승인 게이트로 올린다.
- 2026-09-18T00:54:16Z — `~/.local/bin/aidlc` 가 프로젝트 셸 2.8.2 보다 뒤처진 빌드다. 팀원 5인의 실행 파일도 같은 상태일 가능성이 높으므로 재설치가 필요하다. 저장소 밖의 일이라 이 워크플로가 고칠 수 없다.
