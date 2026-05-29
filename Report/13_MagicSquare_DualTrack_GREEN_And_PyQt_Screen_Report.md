# Magic Square 4×4 — Dual-Track GREEN·PyQt Screen 세션 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Report` |
| **전제 보고서** | [`09_MagicSquare_Full_DualTrack_RED_Design_Report.md`](09_MagicSquare_Full_DualTrack_RED_Design_Report.md), [`11_MagicSquare_AC_FR_01_01_GREEN_Verification_Report.md`](11_MagicSquare_AC_FR_01_01_GREEN_Verification_Report.md), [`12_MagicSquare_AC_FR_01_01_TDD_Checklist_Report.md`](12_MagicSquare_AC_FR_01_01_TDD_Checklist_Report.md) |
| **기준 SSOT** | [`docs/PRD_MagicSquare.md`](../docs/PRD_MagicSquare.md), [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md), [`README.md`](../README.md) |
| **작성일** | 2026-05-29 |
| **상태** | **Track A/B P0 GREEN + PyQt Screen 완료** — U-IN-04~08·D-VAL-02~ 등 잔여 RED |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [산출물 목록](#2-산출물-목록)
3. [Track A — Boundary GREEN](#3-track-a--boundary-green)
4. [Track B — Entity·Control GREEN](#4-track-b--entitycontrol-green)
5. [PyQt Screen UI](#5-pyqt-screen-ui)
6. [F2 출력 벡터 SSOT](#6-f2-출력-벡터-ssot)
7. [pytest·회귀](#7-pytest회귀)
8. [미완·후속](#8-미완후속)
9. [Transcript](#9-transcript)

---

## 1. 세션 요약

| Phase | 사용자 요청 | 결과 |
|-------|-------------|------|
| 1 | AC-FR-01-01 `grid=None` GREEN (지정 node) | 이미 GREEN — `src/` 수정 없음 |
| 2 | U-IN G1 `InputValidator` GREEN bundle 1 | `ValidationSuccess` + G1 pass |
| 3 | UIBoundary `resolve()` 격리 GREEN | `ui_boundary.py`, `SolvePartialMagicSquare` stub |
| 4 | Track B Turn 5~8 (D-LOC/MIS/VAL/SOL) | Entity 4건 GREEN, Mock 금지 |
| 5 | Control `SolvePartialMagicSquare.resolve` | locate→find→solve 오케스트레이션 |
| 6 | U-OUT-01 성공 envelope | `SuccessResponse(data=int[6])` |
| 7 | PyQt Screen UI + 수동 검증 | `boundary/screen/app.py`, `pip install -e ".[gui]"` |
| 8 | `python run_gui.py` 실행 | 루트 `run_gui.py` 런처 |
| 9 | Report·Prompt Export | 본 문서, [`Prompt/13_*`](../Prompt/13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Transcript_Prompt.md) |

**아키텍처:** ECB 유지 — Screen → UIBoundary → Control → Entity; Entity/Control에 PyQt 없음.

---

## 2. 산출물 목록

### 2.1 Boundary (`src/magicsquare/boundary/`)

| 파일 | 역할 |
|------|------|
| `ui_boundary.py` | `UIBoundary.solve()` — `FailureResponse` / `SuccessResponse` |
| `schemas.py` | `FailureResponse`, `SuccessResponse`, `ValidationSuccess` |
| `validation/input_validator.py` | FR-01 `validate()` (차원 G1 bundle) |
| `screen/app.py` | `MagicSquareMainWindow`, `--verify` |
| `screen/grid_defaults.py` | G1 기본 격자 |

### 2.2 Control (`src/magicsquare/control/`)

| 파일 | 역할 |
|------|------|
| `solve_partial_magic_square.py` | `resolve()` — `find_blank_coords` → `find_not_exist_nums` → `solve_two_blank_puzzle` |

### 2.3 Entity (`src/magicsquare/entity/`)

| 파일 | 역할 |
|------|------|
| `locator/empty_cell_locator.py` | D-LOC-01 `find_blank_coords` |
| `resolver/missing_number_finder.py` | D-MIS-01 `find_not_exist_nums` |
| `validator/magic_square_validator.py` | D-VAL-01 `is_magic_square` |
| `solver/two_blank_puzzle_solver.py` | D-SOL-01 UC-D4 |
| `value_objects/` | `GRID_SIZE`, `MAGIC_SUM`, `CellPosition`, `SolutionVector`, `MissingPair` |

### 2.4 실행·alias

| 경로 | 역할 |
|------|------|
| `run_gui.py` | **`python run_gui.py`** 루트 런처 |
| `src/boundary/screen/` | `python -m boundary.screen.app` alias |
| `pyproject.toml` | `[gui]` → PyQt6; `magicsquare-gui` script |

### 2.5 테스트 (신규·확장)

| 파일 | GREEN 건수 (대표) |
|------|------------------|
| `tests/boundary/test_u_in_04_08_input_validation.py` | G1 `ValidationSuccess` (U-IN-04~08 RED 잔여) |
| `tests/boundary/test_ac_fr_01_01_ui_boundary_flow.py` | `resolve()` 0회 (`grid=None`) |
| `tests/boundary/test_u_out_01_03_output_contract.py` | U-OUT-01 `SuccessResponse` |
| `tests/control/test_solve_partial_magic_square.py` | G1 `int[6]` |
| `tests/entity/test_d_loc_01_empty_cell_locator.py` | D-LOC-01 |
| `tests/entity/test_d_mis_01_missing_number_finder.py` | D-MIS-01 |
| `tests/entity/test_d_val_01_06_magic_square_validator.py` | D-VAL-01 only |
| `tests/entity/test_d_sol_01_04_two_cell_solver.py` | D-SOL-01 only |

---

## 3. Track A — Boundary GREEN

### 3.1 AC-FR-01-01 (기존)

- [`test_ac_fr_01_01_dimension_validation.py`](../tests/boundary/test_ac_fr_01_01_dimension_validation.py) — **29/29 PASS** (Report/11)
- `MagicSquareBoundary` + `BoundaryValidator` (기존)

### 3.2 UIBoundary·U-FLOW

- `grid=None` → `FailureResponse(INVALID_SIZE, "Grid must be 4x4.")`, `resolve()` **0회**
- 노드: `test_ac_fr_01_01_ui_boundary_flow.py::TestResolveIsolation::test_none_grid_resolve_never_called_spy`

### 3.3 InputValidator (G1 bundle)

- `InputValidator.validate(G1)` → `ValidationSuccess(type="OK")`
- U-IN-04~08 (blank/range/duplicate) — **RED 잔여** (5 fail)

### 3.4 U-OUT-01 성공 envelope

```text
UIBoundary.solve(G1) → SuccessResponse(type="OK", data=[2, 2, 10, 3, 3, 7])
```

- 실패: `FailureResponse` — `code` / `message` (pytest·GUI 동일 문구)
- U-OUT-02~03 — **RED 잔여**

---

## 4. Track B — Entity·Control GREEN

| ID | API | G1/G0 기대 | Mock |
|----|-----|------------|------|
| D-LOC-01 | `find_blank_coords` | `(2,2)`, `(3,3)` 1-index | 금지 |
| D-MIS-01 | `find_not_exist_nums` | `{7,10}`, smaller=7, larger=10 | 금지 |
| D-VAL-01 | `is_magic_square` | G0 → `True` | 금지 |
| D-SOL-01 | `solve_two_blank_puzzle` | F2 `int[6]` | 금지 |
| Control | `SolvePartialMagicSquare.resolve` | 동일 F2 벡터 | 금지 |

D-VAL-02~06, D-SOL-02~04 — 구 스켈레ton `pytest.fail` **RED 잔여**.

---

## 5. PyQt Screen UI

### 5.1 실행

```powershell
pip install -e ".[gui]"
python run_gui.py
```

| 대안 | 명령 |
|------|------|
| 모듈 | `python -m boundary.screen.app` |
| 스크립트 | `magicsquare-gui` |
| 진단 | `python run_gui.py --verify` → `오류: Grid must be 4x4.` |

### 5.2 UI 계약

| 항목 | 구현 |
|------|------|
| 창 제목 | `Magic Square 4x4` |
| 격자 | 4×4 `QSpinBox` 0~16, 기본 G1 |
| 버튼 | `풀기` → `UIBoundary.solve(grid)` only |
| 성공 라벨 | `결과 (r1, c1, n1, r2, c2, n2): …` |
| 실패 라벨 | `오류: {message}` |
| Composition root | `UIBoundary(resolver=SolvePartialMagicSquare())` |

`DomainError`(예: 전부 0 격자) — Screen에서 메시지 표시만; Domain 로직 복제 없음.

---

## 6. F2 출력 벡터 SSOT

| 출처 | G1 / F2 `int[6]` |
|------|------------------|
| **Report/02·README·Entity/Control/GUI** | `[2, 2, 10, 3, 3, 7]` |
| 일부 프롬프트 Step A 표기 | `[2, 2, 7, 3, 3, 10]` (유효 마방진 **아님**) |

**판정:** min→첫 빈칸 배치는 G1에서 실패; max→첫·min→둘째(I-O2)가 유효. 테스트·GUI·Control은 **F2 SSOT** 따름.

---

## 7. pytest·회귀

### 7.1 세션 GREEN 묶음 (대표)

```powershell
pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py -q          # 29 passed
pytest tests/boundary/test_ac_fr_01_01_ui_boundary_flow.py -q            # 1 passed
pytest tests/boundary/test_u_out_01_03_output_contract.py::TestSuccessOutputContract -q
pytest tests/control/test_solve_partial_magic_square.py -q
pytest tests/entity/test_d_loc_01_empty_cell_locator.py tests/entity/test_d_mis_01_missing_number_finder.py -q
pytest tests/entity/test_d_val_01_06_magic_square_validator.py::TestDVal01CompleteGrid -q
pytest tests/entity/test_d_sol_01_04_two_cell_solver.py::TestDSol01StepASuccess -q
```

### 7.2 의도적 RED (미착수)

- `tests/boundary/test_u_in_04_08` — U-IN-04~08 (5건)
- `tests/boundary/test_u_out_01_03` — U-OUT-02~03
- `tests/entity/test_d_*.py` 구 스켈레ton — `pytest.fail`
- Report/09 U-FLOW 확장, U-IN-01~03 code SSOT (OQ-09-01)

---

## 8. 미완·후속

| 우선순위 | 항목 |
|----------|------|
| P1 | U-IN-04~08 GREEN (blank·range·duplicate) — `InputValidator` short-circuit |
| P2 | D-VAL-02~06, D-SOL-02~04 Entity RED→GREEN |
| P3 | U-OUT-02~03, U-FLOW-02 확장 |
| P4 | INT F1/F2 E2E |
| P5 | OQ-09-01 `E00x` ↔ `INVALID_SIZE` code SSOT |

**다음 Report/Prompt 번호:** `14`

---

## 9. Transcript

대화형 Export: [`Prompt/13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Transcript_Prompt.md`](../Prompt/13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Transcript_Prompt.md)
