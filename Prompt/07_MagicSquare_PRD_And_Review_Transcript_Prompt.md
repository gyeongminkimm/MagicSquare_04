# 07 Magic Square PRD 작성·검토 Transcript Export

## 메타

| 항목 | 내용 |
|------|------|
| **목적** | PRD 참고 문서 분석 → PRD 본문 작성 → 파일 저장 → 7항목 검토 세션의 프롬프트/응답 흐름 보관 |
| **범위** | Phase 1 분석부터 Report·Prompting Export 요청까지 |
| **형식** | User / Assistant 순차 기록 (핵심 산출·판단 포함) |
| **구현** | 구현·테스트 코드 작성 없음 (PRD·문서만) |
| **대응 보고서** | [`Report/07_MagicSquare_PRD_And_Review_Report.md`](../Report/07_MagicSquare_PRD_And_Review_Report.md) |
| **PRD SSOT** | [`docs/PRD_MagicSquare.md`](../docs/PRD_MagicSquare.md) |

---

## 대화형 Transcript

### Turn 1 — User

**PRD 작성 전 참고 문서 분석·매핑** 요청.

- 역할: PRD 작성 전문가 + Dual-Track UI + Logic TDD 기획자
- 목표: 구현 전 PRD 작성 **이전** 단계 — 본문 작성 금지
- 참고 문서 6종: Report/1, 2, 3, 4, `.cursorrules`, `.cursor/rules/*.mdc`
- 산출 형식: Overall Judgment, Document Summary, PRD Section Mapping, Source Priority, Body vs Appendix, Conflicts, Recommended Outline (8섹션)
- **제약:** 구현/테스트/파일 수정/PRD 본문 작성 금지

### Turn 2 — Assistant

**PRD Reference Document Analysis** 출력.

- **판정:** PRD 작성 가능 (조건부); 1차 = Report/06 + Report/02
- **경로 정합:** 요청 `Report/4.UserJourney` → 실제 `Report/06_*`; Report/04 = Cursor Rules 모듈 전환
- **매핑:** 01→Background/Why, 06→Vision/Journey/AC, 02→Contract/Invariant/FR, 03+mdc→Quality/Engineering
- **충돌:** F3 미확정, SC-DOM-SOL-001 vs F1/F2 벡터, Coverage 80% vs 95/85%, Control 계층
- **권장 목차:** 23섹션 초안 (본문 미작성)

---

### Turn 3 — User

**PRD 본문 전체 작성** 요청.

- Senior Product/Software Architect 역할
- 23섹션 구조 필수, Dual-Track, Traceability Matrix 필수
- 고정 I/O·Solving Order·Magic Constant 34
- FR-01~05, BR, AC, NFR, Test Plan, Component, Risks, Open Questions
- **제약:** 구현/테스트/범위 확장/모호 표현 금지; 파일 생성 금지 (Markdown 본문만)

### Turn 4 — Assistant

**PRD — Magic Square 4x4 TDD Practice** 전문 출력 (§1~§23).

- FR-01~05, AC-01~20, BR-01~15
- §13: UNSOLVABLE = Domain `UNSOLVABLE_PUZZLE` → Boundary `ERR_UNSOLVABLE`
- §16.4: TD-01(F1), TD-02(F2), TD-07 Decision Needed
- §22 Open Questions 4건 (F3, 문서명, Coverage, Control)
- §21 Traceability Matrix (Concept 15행)

---

### Turn 5 — User

`docs/PRD_MagicSquare.md` **파일로 저장** 요청.

### Turn 6 — Assistant

`docs/PRD_MagicSquare.md` 생성·저장 완료 안내.

---

### Turn 7 — User

**PRD 검토** 요청 (수정 금지, 문제·개선안만).

7기준:
1. FR별 테스트 가능 AC
2. AC ↔ Traceability Matrix
3. Boundary/Domain 혼합
4. 오류 정책 미정
5. small-first vs reverse 데이터 구분
6. 1-index·row-major
7. 구현/테스트 코드 포함 여부

### Turn 8 — Assistant

**PRD 검토 보고** 출력.

| 기준 | 판정 |
|------|------|
| 1 | 부분 충족 (출력 FR·null·FR-04 AC 부족) |
| 2 | 미충족 (AC-06, 15~17, 20 등 Matrix 누락) |
| 3 | 부분 문제 (FR-05, ResultFormatter) |
| 4 | 부분 미정 (F3, ERR_INTERNAL, null) |
| 5 | 부분 충족 (기대 `int[6]` 없음) |
| 6 | 부분 충족 (pos2·내부 좌표계) |
| 7 | 충족 |

- 우선 보완 5건: F1/F2 벡터, F3, FR-06, AC Index, null/message

---

### Turn 9 — User

`Report` 폴더에 보고서 생성, `Prompting` 폴더에 Transcript Export 요청.

### Turn 10 — Assistant (현재 작업)

기존 Report 최대 번호 `06` 확인 후 `07` 할당:

- `Report/07_MagicSquare_PRD_And_Review_Report.md`
- `Prompt/07_MagicSquare_PRD_And_Review_Transcript_Prompt.md` (본 파일)

---

## 실행 명령·점검 요약

| 점검 | 결과 |
|------|------|
| Report 번호 | `01`~`06` 존재 → `07` 할당 |
| Prompting | `06_*` 존재 → `07_*` 할당 |
| PRD 파일 | `docs/PRD_MagicSquare.md` (Turn 6) |
| 구현 변경 | 없음 |

---

## 세션 산출물 인덱스

| Phase | 산출물 | 저장 위치 |
|-------|--------|-----------|
| 1 | 참고 문서 분석 8섹션 | 채팅 (Report 07 §3 요약) |
| 2 | PRD 23섹션 전문 | `docs/PRD_MagicSquare.md` |
| 3 | 파일 저장 | `docs/PRD_MagicSquare.md` |
| 4 | 7항목 검토 보고 | 채팅 (Report 07 §6~§8 요약) |
| 5 | Report 07 + Prompting 07 | Turn 10 |

---

## PRD 핵심 식별자 (Transcript 부록)

| 구분 | ID 범위 |
|------|---------|
| Functional Requirements | FR-01 ~ FR-05 |
| Acceptance Criteria | AC-01 ~ AC-20 |
| Business Rules | BR-01 ~ BR-15 |
| Non-Functional | NFR-01 ~ NFR-09 |
| Test Data | TD-01 ~ TD-07 |
| Normal/Exception Scenarios | NS-01~02, ES-01~05, BS-01~05 |

---

## 비고

- 본 transcript는 세션 핵심 요청·응답·판단을 대화형으로 정리한 export 기록이다.
- PRD 전문은 `docs/PRD_MagicSquare.md`가 SSOT이며, Report 07이 분석·검토·보완 권고를 통합한다.
- 다음 백업 시 번호 `08` 사용.
