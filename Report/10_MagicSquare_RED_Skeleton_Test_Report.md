# Magic Square 4×4 — RED Skeleton 테스트 세션 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `10_MagicSquare_RED_Skeleton_Test_Report` |
| **전제 보고서** | [`09_MagicSquare_Full_DualTrack_RED_Design_Report.md`](09_MagicSquare_Full_DualTrack_RED_Design_Report.md), [`08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md`](08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md), [`02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
| **기준 SSOT** | Report/09 §5~§6, [`docs/PRD_MagicSquare.md`](../docs/PRD_MagicSquare.md), `.cursor/rules/magicsquare-tdd-testing.mdc` |
| **작성일** | 2026-05-29 |
| **상태** | **RED Skeleton 완료** — `pytest.fail`·collection ERROR; GREEN/REFACTOR·`src/` 확장 미착수 |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [산출물 목록](#2-산출물-목록)
3. [스켈레톤 규칙](#3-스켈레톤-규칙)
4. [생성 테스트 파일·Test ID](#4-생성-테스트-파일test-id)
5. [pytest RED 결과](#5-pytest-red-결과)
6. [Report/09 ↔ 스켈레톤 ID 매핑](#6-report09--스켈레톤-id-매핑)
7. [Report/08과의 관계](#7-report08과의-관계)
8. [Open Questions / 다음 단계](#8-open-questions--다음-단계)

---

## 1. 세션 요약

| Phase | 사용자 요청 | 결과 |
|-------|-------------|------|
| 1 | Report/09 기반 **RED Skeleton**만 작성 (`pytest.fail`, assert 금지) | `tests/boundary/test_u_*.py`, `tests/entity/test_d_*.py` 등 10파일 |
| 2 | Report·Prompt Transcript Export | 본 문서, [`Prompt/10_...`](../Prompt/10_MagicSquare_RED_Skeleton_Test_Transcript_Prompt.md) |

**TDD phase:** RED (Skeleton) — 의도적 실패만; 실제 계약 assert는 GREEN에서 교체.

| Track | 경로 | Mock 정책 |
|-------|------|-----------|
| A | `tests/boundary/test_u_*.py` | U-OUT/U-FLOW: resolve spy **주석만** (GREEN 시 `conftest` mock) |
| B | `tests/entity/test_d_*.py` | **Domain Mock 금지** |

---

## 2. 산출물 목록

| 유형 | 경로 | 비고 |
|------|------|------|
| 공통 placeholder | [`tests/conftest.py`](../tests/conftest.py) | G0~G3 주석 |
| Entity fixture | [`tests/entity/conftest.py`](../tests/entity/conftest.py) | TD-04/05/06 주석 |
| Boundary U-IN | [`tests/boundary/test_u_in_validation.py`](../tests/boundary/test_u_in_validation.py) | U-IN-04~08 |
| Boundary U-OUT | [`tests/boundary/test_u_out_contract.py`](../tests/boundary/test_u_out_contract.py) | U-OUT-01~03 |
| Boundary U-FLOW | [`tests/boundary/test_u_flow_execute_isolation.py`](../tests/boundary/test_u_flow_execute_isolation.py) | U-FLOW-02 ×4 |
| Entity D-LOC | [`tests/entity/test_d_loc.py`](../tests/entity/test_d_loc.py) | collection ERROR |
| Entity D-MIS | [`tests/entity/test_d_mis.py`](../tests/entity/test_d_mis.py) | collection ERROR |
| Entity D-VAL | [`tests/entity/test_d_val.py`](../tests/entity/test_d_val.py) | collection ERROR |
| Entity D-SOL | [`tests/entity/test_d_sol.py`](../tests/entity/test_d_sol.py) | 4× pytest.fail |
| Report/08 (유지) | [`tests/boundary/test_ac_fr_01_01_dimension_validation.py`](../tests/boundary/test_ac_fr_01_01_dimension_validation.py) | **미수정** |
| 세션 보고서 | `Report/10_MagicSquare_RED_Skeleton_Test_Report.md` | 본 문서 |
| Transcript | `Prompt/10_MagicSquare_RED_Skeleton_Test_Transcript_Prompt.md` | 대화형 Export |

**`src/` 변경:** 없음.

---

## 3. 스켈레톤 규칙

| # | 규칙 |
|---|------|
| 1 | AAA — Given/When/Then **주석만** |
| 2 | 본문 한 줄: `pytest.fail("RED: <Test ID> — <요약>")` |
| 3 | 기대값 `assert` **금지** (GREEN에서 추가) |
| 4 | `skip` / `xfail` **금지** |
| 5 | production import **허용** (`magicsquare.*`; 미존재 모듈 → collection ERROR = RED) |
| 6 | naming: `test_<test_id>_<scenario>` |

---

## 4. 생성 테스트 파일·Test ID

### 4.1 Track A — Boundary (12건 + import 성공)

| Test ID | 테스트 함수 | RED 유형 |
|---------|-------------|----------|
| U-IN-04 | `test_u_in_04_zero_empty_cells_returns_e002` | pytest.fail |
| U-IN-05 | `test_u_in_05_three_blanks_returns_e002` | pytest.fail |
| U-IN-06 | `test_u_in_06_cell_value_17_returns_e004` | pytest.fail |
| U-IN-07 | `test_u_in_07_cell_value_negative_one_returns_e004` | pytest.fail |
| U-IN-08 | `test_u_in_08_duplicate_nonzero_returns_e005` | pytest.fail |
| U-OUT-01 | `test_u_out_01_solve_success_returns_length_six` | pytest.fail |
| U-OUT-02 | `test_u_out_02_solve_success_coordinates_one_indexed` | pytest.fail |
| U-OUT-03 | `test_u_out_03_solve_success_n1_n2_distinct_in_range` | pytest.fail |
| U-FLOW-02 | `test_u_flow_02_*_resolve_call_count_zero` (×4) | pytest.fail |

### 4.2 Track B — Entity (11건)

| Test ID | 파일 | RED 유형 |
|---------|------|----------|
| D-LOC-01 | `test_d_loc.py` | ModuleNotFoundError (`entity.locator`) |
| D-MIS-01 | `test_d_mis.py` | ModuleNotFoundError (`entity.resolver`) |
| D-VAL-01~06 | `test_d_val.py` (7 함수) | ModuleNotFoundError (`entity.validator`) |
| D-SOL-01 | `test_d_sol_01_g1_step_a_returns_vector` | pytest.fail |
| D-SOL-02 | `test_d_sol_02_g2_step_b_success_vector` | pytest.fail (`G2 TBD`) |
| D-SOL-03 | `test_d_sol_03_g3_raises_unsolvable_domain_error` | pytest.fail |
| D-SOL-04 | `test_d_sol_04_solution_length_six` | pytest.fail |

**미작성 (의도):** U-IN-01~03 (Report/08), D-SOL-05 (Report/09 범위 외).

---

## 5. pytest RED 결과

```bash
python -m pytest tests/boundary/test_u_*.py tests/entity/ -v
```

| 구분 | 건수 | 결과 |
|------|------|------|
| 수집·실행 | 16 | **FAILED** (`pytest.fail`) |
| 수집 실패 | 3 모듈 (7 테스트) | **ERROR** (`ModuleNotFoundError`) |
| Report/08 | 29 (별도 파일) | 변경 없음 — GREEN assert 유지 |

**신규 스켈레톤만:** `16 failed, 0 passed`  
**entity 3파일 포함:** `3 errors during collection` + 16 failed

---

## 6. Report/09 ↔ 스켈레톤 ID 매핑

| Report/09 | Skeleton ID | 비고 |
|-----------|-------------|------|
| U-IN-03a | U-IN-04 | 0 blanks → E002 |
| U-IN-03b | U-IN-05 | 3 blanks → E002 |
| U-IN-04 | U-IN-06, U-IN-07 | 17 / -1 → E004 |
| U-IN-05 | U-IN-08 | duplicate → E005 |
| U-OUT-01~02 | U-OUT-01~02 | 동일 |
| — | U-OUT-03 | UI-OUT-03 (n1,n2 distinct) |
| U-FLOW-02 | U-FLOW-02 ×4 | blank/range/dup 확장 |
| D-LOC-01 ~ D-SOL-04 | 동일 | D-SOL-02 메시지 `G2 TBD` |

---

## 7. Report/08과의 관계

| 항목 | Report/08 | 본 세션 (10) |
|------|-----------|--------------|
| AC | AC-FR-01-01 (null·차원) | U-IN-04~08, U-OUT, U-FLOW |
| 코드 | `INVALID_SIZE` assert Full RED/GREEN | E002/E004/E005 skeleton |
| 파일 | `test_ac_fr_01_01_*` | `test_u_*`, `test_d_*` |
| 수정 | — | **08 파일 touch 금지** 준수 |

---

## 8. Open Questions / 다음 단계

| # | 항목 | 권장 조치 |
|---|------|-----------|
| OQ-10-01 | E00x vs `INVALID_SIZE` (08) | GREEN 전 code SSOT 표 (Report/09 OQ-09-01) |
| OQ-10-02 | `entity.locator|resolver|validator` 패키지명 | Domain GREEN 시 Report/02 컴포넌트명과 정합 |
| OQ-10-03 | G3 / D-SOL-03 | F3 확정 후 Given·import 경로 갱신 |
| OQ-10-04 | D-SOL-02 `G2 TBD` | G2 fixture 활성화 후 assert 교체 |

**GREEN 순서 (권장)**

1. Boundary: `BoundaryValidator` — blank/range/duplicate → U-IN-04~08 assert  
2. Boundary: U-FLOW-02 spy + U-OUT mock  
3. Entity: 모듈 스캐폴드 → D-LOC/D-MIS/D-VAL collection 해소  
4. Control: `SolveTwoBlankPuzzle` — D-SOL-01~04  

---

## 식별자 부록

| 구분 | 값 |
|------|-----|
| TDD phase | RED (Skeleton) |
| 신규 테스트 | 23 (16 fail + 7 error) |
| 선행 설계 | Report/09 |
| 선행 구현·QA | Report/08 |

---

*본 보고서는 스켈레톤 테스트 추가 세션 기록이다. GREEN 단계에서 `pytest.fail`을 계약 assert로 교체할 때 본 §4·§6을 SSOT로 사용한다.*
