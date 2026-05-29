# 09 Magic Square FR-01~FR-05 Dual-Track RED 설계 Transcript Export

## 메타

| 항목 | 내용 |
|------|------|
| **목적** | FR-01~FR-05 전체 Dual-Track **RED 설계표** 세션의 프롬프트/응답 흐름 보관 |
| **범위** | RED 설계표 작성(코드 금지) → Report·Prompt Export |
| **형식** | User / Assistant 순차 기록 (핵심 산출·판단 포함) |
| **구현** | 테스트 코드·프로덕션 코드·pytest·파일 저장(1차 턴) 없음 — **설계표 텍스트만** |
| **대응 보고서** | [`Report/09_MagicSquare_Full_DualTrack_RED_Design_Report.md`](../Report/09_MagicSquare_Full_DualTrack_RED_Design_Report.md) |
| **SSOT** | [`docs/PRD_MagicSquare.md`](../docs/PRD_MagicSquare.md) v0.2, [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](../Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md), `.cursor/rules/*.mdc` |

---

## 대화형 Transcript

### Turn 1 — User

**Dual-Track UI + Logic TDD — RED phase 설계표만** 작성 요청.

**금지 (엄격)**

- 구현·테스트·스켈레톤 코드
- 클래스/파일 구조 확정
- GREEN / REFACTOR
- pytest 실행·코드 생성·파일 저장 (설계표 텍스트 출력만)

**SSOT:** PRD v0.2, Report/02, `.cursorrules` (ECB, Dual-Track, Test ID)

**프로젝트 계약**

- 입출력 4×4 / `int[6]` 1-index / M=34
- short-circuit: null → size → empty → range → duplicate
- Boundary: E003, E001, E002, E004, E005; invalid 시 `execute` 0회 (U-FLOW-02)
- Domain: Domain Mock 금지

**범위:** FR-01~FR-05 Dual-Track RED (전체)

**Track A — Boundary**

1. `matrix=null` → E003  
2. size ≠ 4×4 → E001  
3. blank ≠ 2 → E002 (0개·3개)  
4. range → E004  
5. duplicate → E005  
6. U-OUT-01: 길이 6  
7. U-OUT-02: 좌표 1-index  
8. U-FLOW-02: invalid → execute 0회  

**Track B — Logic**

- `find_blank_coords` (G1 → (2,2),(3,3)) D-LOC-01  
- `find_not_exist_nums` (G1 → {7,10}) D-MIS-01  
- `is_magic_square` 분리 D-VAL-01~06 (G0~변형)  
- `solution` 분리 D-SOL-01~05 (G1/G2/G3, 길이·좌표)  

**출력 형식:** `# UI RED Tests` / `# Logic RED Tests` 표 + RED 자체 검수 체크리스트

### Turn 2 — Assistant

**TDD phase: RED** — 설계표 출력 (코드·파일 없음).

**Track A (10행)**

| ID | 요지 |
|----|------|
| U-IN-01 | null → E003 |
| U-IN-02 | 3×4 등 → E001 |
| U-IN-03a/b | 0개·3개 blank → E002 |
| U-IN-04 | TD-06 (-1/17) → E004 |
| U-IN-05 | TD-05 duplicate → E005 |
| U-OUT-01 | mock 성공 → len 6 |
| U-OUT-02 | mock → coords [1,4] |
| U-FLOW-02 | invalid parametrize → execute call_count 0 |

**격자 별칭 (Report/02 부록 없음 → F1/F2 정합)**

| 별칭 | 매핑 |
|------|------|
| G0 | F1 완성본 |
| G1 | F2 / TD-02 — blank (2,2)(3,3), solve `[2,2,7,3,3,10]` |
| G2 | F1 / TD-01 — solve `[1,2,3,2,3,11]` |
| G3 | PLACEHOLDER (F3/TD-07) |

**Track B (11행)**

- D-LOC-01, D-MIS-01  
- D-VAL-01~06 (행/열/대각/집합/0포함)  
- D-SOL-01~05 (G1/G2/G3, len, 1-index)  
- **Domain Mock 금지** 명시

**검수 체크리스트 6항목** — 전부 ✅

**GREEN 전 참고:** `test_plan` AC-FR-01-01은 null에 `INVALID_SIZE`; 본 RED는 **E003/E001 분리**. G3는 F3 확정 전 PLACEHOLDER.

---

### Turn 3 — User

**Report** 폴더에 보고서 생성, **Prompt** 폴더에 Transcript Export.

### Turn 4 — Assistant (현재 작업)

Report 최대 번호 `08` → **`09`** 할당:

- `Report/09_MagicSquare_Full_DualTrack_RED_Design_Report.md`
- `Prompt/09_MagicSquare_Full_DualTrack_RED_Design_Transcript_Prompt.md` (본 파일)

---

## 실행·점검 요약

| 점검 | 결과 |
|------|------|
| Report 번호 | `01`~`08` 존재 → **`09`** 할당 |
| Prompt | `08` 패턴 → **`09`** 신규 |
| TDD phase | RED 설계만; 테스트·src 미생성 |
| 선행 구현 | Report 08 — AC-FR-01-01 Boundary 일부 GREEN (별도 추적) |

---

## 세션 산출물 인덱스

| Phase | 산출물 | 저장 위치 |
|-------|--------|-----------|
| 1 | Dual-Track RED 설계표 (U-* 10, D-* 11) | 채팅 → Report 09 §5~§6 |
| 2 | Report 09 + Prompt 09 | Turn 4 |

---

## 식별자 부록

| 구분 | ID |
|------|-----|
| Track A | U-IN-01~05, U-IN-03a/b, U-OUT-01~02, U-FLOW-02 |
| Track B | D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~05 |
| FR | FR-01~FR-05 |
| 오류 (Boundary RED) | E001, E002, E003, E004, E005 |
| 격자 | G0, G1, G2, G3 (G3 PLACEHOLDER) |
| Open | OQ-09-01~04 (Report 09 §8) |

---

## 비고

- 본 transcript는 **RED 설계 명세** 세션만 기록한다. pytest·`tests/domain/` 작성은 다음 RED 구현 턴에서 수행.
- Track A 출력 계약(U-OUT)은 Boundary 테스트에서 **execute mock** 필수 (ECB).
- Track B는 **Domain mock 금지** — Report 02·`.cursor/rules/magicsquare-forbidden.mdc`와 동일.
- 다음 백업 시 Report/Prompt 번호 **`10`** 사용.
