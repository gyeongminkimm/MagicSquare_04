# Magic Square 4×4 — FR-01~FR-05 Dual-Track RED 설계 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `09_MagicSquare_Full_DualTrack_RED_Design_Report` |
| **전제 보고서** | [`02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md), [`07_MagicSquare_PRD_And_Review_Report.md`](07_MagicSquare_PRD_And_Review_Report.md), [`08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md`](08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md) |
| **기준 SSOT** | [`docs/PRD_MagicSquare.md`](../docs/PRD_MagicSquare.md) v0.2, [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md), `.cursor/rules/*.mdc` |
| **작성일** | 2026-05-29 |
| **상태** | **RED 설계표만 확정** — 테스트 코드·프로덕션 코드·pytest 실행 없음 |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [산출물 목록](#2-산출물-목록)
3. [프로젝트 계약 (고정)](#3-프로젝트-계약-고정)
4. [격자 별칭 G0~G3](#4-격자-별칭-g0g3)
5. [Track A — Boundary / UI Contract RED](#5-track-a--boundary--ui-contract-red)
6. [Track B — Domain / Logic RED](#6-track-b--domain--logic-red)
7. [RED 설계 자체 검수](#7-red-설계-자체-검수)
8. [SSOT 정합·Open Questions](#8-ssot-정합open-questions)
9. [다음 단계](#9-다음-단계)

---

## 1. 세션 요약

| Phase | 사용자 요청 | 결과 |
|-------|-------------|------|
| 1 | FR-01~FR-05 **Dual-Track RED 설계표** 작성 (코드·파일·pytest 금지) | Track A 10건 + Track B 11건 설계표 (채팅 산출) |
| 2 | Report·Prompt Transcript Export | 본 문서, [`Prompt/09_...`](../Prompt/09_MagicSquare_Full_DualTrack_RED_Design_Transcript_Prompt.md) |

**TDD phase:** RED — 구현·테스트·스켈레톤·GREEN/REFACTOR 진입 없음.

**Dual-Track 정합**

| Track | RED ID 접두 | Domain Mock | 비고 |
|-------|-------------|-------------|------|
| A (Boundary) | `U-IN-*`, `U-OUT-*`, `U-FLOW-*` | `execute` / resolver **mock·spy만** | Failure envelope (E00x), 예외 아님 |
| B (Logic) | `D-LOC-*`, `D-MIS-*`, `D-VAL-*`, `D-SOL-*` | **금지** | G0~G3·F1/F2 격자 직접 호출 |

---

## 2. 산출물 목록

| 유형 | 경로 | 비고 |
|------|------|------|
| RED 설계표 (본문) | 본 문서 §5~§6 | U-* 10건, D-* 11건 |
| 세션 보고서 | `Report/09_MagicSquare_Full_DualTrack_RED_Design_Report.md` | 본 문서 |
| Transcript | [`Prompt/09_MagicSquare_Full_DualTrack_RED_Design_Transcript_Prompt.md`](../Prompt/09_MagicSquare_Full_DualTrack_RED_Design_Transcript_Prompt.md) | 대화형 Export |
| 기존 Track A 부분 RED | `tests/boundary/test_ac_fr_01_01_*` | AC-FR-01-01만 구현·별도 08 보고서 |
| PRD / 02 설계 | `docs/PRD_MagicSquare.md`, Report/02 | SSOT |

---

## 3. 프로젝트 계약 (고정)

| 항목 | 규칙 |
|------|------|
| **입력** | 4×4 `int[][]`, `0`=빈칸(정확히 2), 값 `0` 또는 `1..16`, 비0 중복 금지 |
| **출력** | `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index** |
| **마법합** | M = 34 (`MagicConstant` SSOT) |
| **검증 순서 (short-circuit)** | null → size → empty count → value range → duplicate |
| **Boundary invalid** | Failure envelope; `E003` null, `E001` size, `E002` blank, `E004` range, `E005` duplicate |
| **U-FLOW-02** | invalid 시 `SolvePartialMagicSquare.execute` **0회** |
| **Domain** | Entity/Control; **Domain Mock 금지** |

---

## 4. 격자 별칭 G0~G3

Report/02 부록에 G0~G3 라벨이 없어, F1/F2/TD-*와 정합되는 **논리 별칭**으로 고정한다. 부록 확정 시 1:1 치환.

| 별칭 | 격자 (0=blank) | 1-index blank | 용도 |
|------|----------------|---------------|------|
| **G0** | F1 완성본 `[[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]` | — | 완전·유효 마방진 |
| **G1** | F2 / TD-02 `[[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]` | (2,2), (3,3) | 누락 {7,10}; solve `[2,2,7,3,3,10]` |
| **G2** | F1 / TD-01 `[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]` | (1,2), (2,3) | Step A 실패·B 성공 `[1,2,3,2,3,11]` |
| **G3** | **PLACEHOLDER** (F3 / TD-07 미확정) | — | `UnsolvableDomainError` |

---

## 5. Track A — Boundary / UI Contract RED

### 5.1 UI RED Tests

| Test ID | Layer | 테스트 이름 | Given | When | Then | Expected RED Failure | 실패 이유 | Boundary 계약 | Invariant/AC |
|---------|-------|-------------|-------|------|------|----------------------|-----------|---------------|--------------|
| U-IN-01 | Boundary | `test_validate_null_grid_returns_e003` | `matrix = null` | `InputValidator.validate(matrix)` | `code == "E003"`; message null 전용 SSOT; `execute` 0회 | `ModuleNotFoundError` / `AttributeError` / assertion | E003·null 1순위 | FR-01; AC-05; UI-IN-01 |
| U-IN-02 | Boundary | `test_validate_non_4x4_grid_returns_e001` | 3×4 등 (parametrize: `[]`, `[[]]*4`, 4×3, 5×5, 2×2) | `InputValidator.validate(matrix)` | `E001`; `Grid must be 4x4.`; `execute` 0회 | assertion / size 분기 없음 | AC-01; AC-FR-01-01; BR-01 | UI-IN-02~03 |
| U-IN-03a | Boundary | `test_validate_zero_blanks_returns_e002` | TD-04 (0개) | `InputValidator.validate(matrix)` | `E002`; blank message; `execute` 0회 | assertion | AC-03; BR-02; UI-IN-05 | ES-02 |
| U-IN-03b | Boundary | `test_validate_three_blanks_returns_e002` | 0 세 개 (F1+추가 blank) | `InputValidator.validate(matrix)` | 동일 E002 | assertion | 동일 | ES-02 |
| U-IN-04 | Boundary | `test_validate_out_of_range_cell_returns_e004` | TD-06 (`17`); parametrize `-1` | `InputValidator.validate(matrix)` | `E004`; value message; `execute` 0회 | assertion | AC-02; BR-03; UI-IN-04 | ES-03 |
| U-IN-05 | Boundary | `test_validate_duplicate_nonzero_returns_e005` | TD-05 | `InputValidator.validate(matrix)` | `E005`; duplicate message; `execute` 0회 | assertion | AC-04; BR-04; UI-IN-06 | ES-04 |
| U-OUT-01 | Boundary | `test_solve_success_returns_length_six` | G2; mock `execute` → `[1,2,3,2,3,11]` | `MagicSquareBoundary.solve(matrix)` | 성공 envelope; `len == 6` | `AttributeError` / len assertion | AC-18; UI-OUT-01; BR-13 | FR-05 |
| U-OUT-02 | Boundary | `test_solve_success_coordinates_are_one_indexed` | G1; mock → `[2,2,7,3,3,10]` | `MagicSquareBoundary.solve(matrix)` | r,c ∈ [1,4] | 좌표 assertion | AC-19; UI-OUT-02; BR-12 | FR-05 |
| U-FLOW-02 | Boundary | `test_invalid_input_never_calls_execute` | U-IN 대표 입력 parametrize | `MagicSquareBoundary.solve(matrix)` | spy `call_count == 0` | `call_count >= 1` | AC-05; U-FLOW-02 | PRD §13 |

**메시지 (Report/02 / PRD §13 바이트 일치)**

| code | message |
|------|---------|
| E003 (null) | `Grid must not be null.` (또는 GREEN 시 SSOT 재정합) |
| E001 | `Grid must be 4x4.` |
| E002 | `Grid must contain exactly 2 blank cells (0).` |
| E004 | `Cell value must be 0 or between 1 and 16.` |
| E005 | `Duplicate non-zero value is not allowed.` |

---

## 6. Track B — Domain / Logic RED

설계용 별칭: `find_blank_coords`, `find_not_exist_nums`, `is_magic_square`, `solution` (구현명·파일 구조 미확정).

### 6.1 Logic RED Tests

| Test ID | Layer | 테스트 이름 | Given | When | Then | Expected RED Failure | Logic Invariant | 필요성 |
|---------|-------|-------------|-------|------|------|----------------------|-----------------|--------|
| D-LOC-01 | Entity | `test_find_blank_coords_g1_row_major_order` | G1 | `find_blank_coords(matrix)` | `(2,2)`, `(3,3)` 1-index | `NotImplementedError` / assertion | I6; BR-05 | FR-02 |
| D-MIS-01 | Entity | `test_find_not_exist_nums_g1_sorted_missing` | G1 | `find_not_exist_nums(matrix)` | `{7, 10}` 오름차순 | assertion | I7, I11; BR-06~07 | FR-03 |
| D-VAL-01 | Entity | `test_is_magic_square_g0_complete_returns_true` | G0 | `is_magic_square(matrix)` | `True` | `False` / 미구현 | I1~I5; BR-08~09 | FR-04 AC-12 |
| D-VAL-02 | Entity | `test_is_magic_square_row_sum_mismatch_returns_false` | G0, 행1 합 깨짐 | `is_magic_square(matrix)` | `False` | `True` | I1 | 행 검증 분리 |
| D-VAL-03 | Entity | `test_is_magic_square_col_sum_mismatch_returns_false` | G0, 열 합 깨짐 | `is_magic_square(matrix)` | `False` | `True` | I2 | 열 검증 분리 |
| D-VAL-04 | Entity | `test_is_magic_square_diagonal_mismatch_returns_false` | G0, D2 깨짐 | `is_magic_square(matrix)` | `False` | `True` | I3 | 대각 검증 |
| D-VAL-05 | Entity | `test_is_magic_square_invalid_set_or_duplicate_returns_false` | 17 또는 중복 | `is_magic_square(matrix)` | `False` | `True` | I4 | 집합 규칙 |
| D-VAL-06 | Entity | `test_is_magic_square_with_zero_in_complete_grid_returns_false` | G0+`0` 1칸 | `is_magic_square(matrix)` | `False` | `True` | I4 | incomplete 오판 방지 |
| D-SOL-01 | Control | `test_solution_g1_step_a_success_vector` | G1 | `solution(matrix)` | `[2,2,7,3,3,10]` | assertion / 조기 unsolvable | I8; I-O2 | FR-05 AC-15 |
| D-SOL-02 | Control | `test_solution_g2_step_a_fail_step_b_success` | G2 | `solution(matrix)` | `[1,2,3,2,3,11]` | 오답 벡터 | I9; I-O2 | FR-05 AC-16 |
| D-SOL-03 | Control | `test_solution_g3_both_steps_fail_raises_unsolvable` | G3 PLACEHOLDER | `solution(matrix)` | `UnsolvableDomainError` | 정상 반환 | I10 | FR-05 AC-17 |
| D-SOL-04 | Control | `test_solution_return_length_six` | G1 또는 G2 | `solution(matrix)` | `len == 6` | `len != 6` | I8/I9; BR-13 | 출력 포맷 |
| D-SOL-05 | Control | `test_solution_coordinates_one_indexed` | G2 | `solution(matrix)` | r,c ∈ [1,4] | 0 또는 >4 | I8/I9; BR-12 | 좌표 계약 |

**Domain Mock 금지:** Track B 전건 실제 Domain API 호출만 허용.

---

## 7. RED 설계 자체 검수

| 항목 | 결과 |
|------|------|
| Boundary E00x Failure schema (generic Exception 아님) | ✅ |
| invalid → `execute` 0회 (U-FLOW-02) | ✅ |
| U-IN vs U-OUT 분리 | ✅ |
| Logic Track Domain Mock 없음 | ✅ |
| I1~I11·AC-FR* 추적 가능 | ✅ (표 AC/Invariant 열) |
| 코드/스켈레톤/구현 없음 | ✅ |

---

## 8. SSOT 정합·Open Questions

| # | 항목 | 상태 | 권장 조치 |
|---|------|------|-----------|
| OQ-09-01 | `E003` vs `test_plan` `INVALID_SIZE` (null) | Open | GREEN 전 code 매핑표 1편 (`E00x` ↔ `ERR_*` ↔ QA code) |
| OQ-09-02 | G3 / F3 / TD-07 격자 | Decision Needed | 확정 후 D-SOL-03 Given 갱신 |
| OQ-09-03 | Report/02 `UI-P0-*` vs 본 설계 `U-IN-*` | 정합 | Traceability에 U-* ↔ UI-P0 매핑 행 추가 |
| OQ-09-04 | AC-FR-01-01 이미 GREEN (08) vs 본 RED 전체 | 병행 | U-IN-02는 08과 중복 가능 — parametrized 통합 시 08 보고서 갱신 |

---

## 9. 다음 단계

| 순서 | 작업 | Track |
|------|------|-------|
| 1 | OQ-09-01 code SSOT 확정 | 문서 |
| 2 | `tests/boundary/` — U-IN-03a~05, U-OUT-*, U-FLOW-02 RED | A |
| 3 | `tests/domain/` — D-LOC~D-SOL RED (G3 placeholder 또는 xfail 금지) | B |
| 4 | 최소 GREEN (트랙별 독립) | A ∥ B |
| 5 | INT-N-01 (F1 E2E) — 양 트랙 P0 GREEN 이후 | Integration |

---

## 식별자 부록

| 구분 | ID |
|------|-----|
| Track A RED | U-IN-01~05, U-IN-03a/b, U-OUT-01~02, U-FLOW-02 |
| Track B RED | D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~05 |
| 픽스처 | F1, F2, G0~G3, TD-01~07 |
| FR | FR-01~FR-05 |
| 선행 세션 | Report 08 (AC-FR-01-01) |

---

*본 보고서는 구현·테스트 코드를 포함하지 않는 RED 설계 명세이다. 테스트 코드 작성 시 본 §5~§6 표를 SSOT로 사용한다.*
