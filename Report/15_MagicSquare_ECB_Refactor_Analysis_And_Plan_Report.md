# Magic Square 4×4 — ECB·리팩터 분석 및 계획 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Report` |
| **전제 보고서** | [`13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Report.md`](13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Report.md), [`14_MagicSquare_Golden_Master_Regression_Report.md`](14_MagicSquare_Golden_Master_Regression_Report.md), [`09_MagicSquare_Full_DualTrack_RED_Design_Report.md`](09_MagicSquare_Full_DualTrack_RED_Design_Report.md) |
| **기준 SSOT** | [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md), [`.cursor/rules/magicsquare-ecb-architecture.mdc`](../.cursor/rules/magicsquare-ecb-architecture.mdc), [`.cursor/rules/magicsquare-tdd-testing.mdc`](../.cursor/rules/magicsquare-tdd-testing.mdc) |
| **작성일** | 2026-05-29 |
| **상태** | **분석·계획 완료** — `src/` REFACTOR **미착수** |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [ECB 매핑 (프롬프트 → 실제 파일)](#2-ecb-매핑-프롬프트--실제-파일)
3. [코드 리뷰 요약](#3-코드-리뷰-요약)
4. [코드 스멜 (우선순위)](#4-코드-스멜-우선순위)
5. [SRP 위반 점검](#5-srp-위반-점검)
6. [테스트 갭·RED 스켈레톤](#6-테스트-갭red-스켈레톤)
7. [리팩터링 대상 목록](#7-리팩터링-대상-목록)
8. [테스트 선행 필요 항목](#8-테스트-선행-필요-항목)
9. [REFACTOR phase 게이트](#9-refactor-phase-게이트)
10. [리팩터 후 검증](#10-리팩터-후-검증)
11. [미완·후속](#11-미완후속)
12. [Transcript](#12-transcript)

---

## 1. 세션 요약

| Phase | 작업 | 결과 |
|-------|------|------|
| 1 | `code-reviewer` 서브에이전트 전체 리뷰 | **조건부 승인** — ECB core·F2 경로 양호, Boundary 계약·이중 API 드리프트 |
| 2 | `control/*`·`boundary/*` 테스트 대응·RED→GREEN 게이트 | P0 테스트 다수 RED/가짜 GREEN (`test_u_in_04_08` assert만 존재) |
| 3 | ECB 역할·이동 대상·Control/Entity 경계 | P0: InputValidator content, ui_boundary E006/E007, solve_partial 중복 제거 |
| 4 | SRP (함수 다중 역할·클래스 책임) | `ui_boundary`·`screen/app.py` 위반; UI 비즈니스 판단(34/Step A/E00x) **해당 없음** |
| 5 | 리팩터링 계획서·README 반영 | 본 문서 — **코드 변경 없음** |

**판정:** REFACTOR 시작 전 **Step A (Boundary P0 테스트 GREEN)** 필수.

---

## 2. ECB 매핑 (프롬프트 → 실제 파일)

| 프롬프트 | 실제 경로 | ECB 레이어 | 적합성 |
|----------|-----------|------------|--------|
| `domain.py` | `src/magicsquare/control/solve_partial_magic_square.py` | **Control** | 적합 — 알고리즘은 Entity |
| `boundary.py` | `src/magicsquare/boundary/ui_boundary.py` | **Boundary** | **부분** — E002~E007·예외 매핑 미완 |
| `gui/main_window` | `src/magicsquare/boundary/screen/app.py` (`MagicSquareMainWindow`) | **Screen** | **부분** — Control 직접 조립·`DomainError` UI 처리 |

**의존:** `boundary → control → entity` 준수.  
**금지 위반:** `screen/app.py` — `SolvePartialMagicSquare` 직접 import·`create_boundary()` 조립.

**Entity 대응:** `entity/solver/two_blank_puzzle_solver.py` (프롬프트 `two_cell_solver` 대응).

---

## 3. 코드 리뷰 요약

### 잘 된 점

- Entity 매직 넘버 SSOT (`magic_constant.py`)
- AC-FR-01-01 **29/29 GREEN** (`MagicSquareBoundary` + mock)
- F2 `int[6]` — Control + U-OUT-01 + Entity solver 일치
- Boundary 일부 테스트 mock 격리 (`test_ac_fr_01_01_ui_boundary_flow`)

### Critical (리팩터 전 계약 위험)

| # | 항목 |
|---|------|
| C1 | `InputValidator` — 차원만 통과, E002/E004/E005 미구현 |
| C2 | `MagicSquareBoundary` 기본 `SolveTwoBlankPuzzle` → `NotImplementedError` |
| C3 | 이중 Boundary API (`MagicSquareBoundary` vs `UIBoundary`, `FailureResult` vs `FailureResponse`) |
| C4 | `UnsolvableDomainError` → boundary envelope 미매핑 |
| C5 | `SolvePartialMagicSquare` — locate/find **이중 호출**(solver 내부와 중복) |
| C6 | `UIBoundary._validator` dead code; `solve()`에서 `InputValidator`만 사용 |

---

## 4. 코드 스멜 (우선순위)

| 파일 | 줄 | 스멜 | 우선순위 |
|------|-----|------|----------|
| `validation/input_validator.py` | 16–23 | FR-01 content 미구현 | **High** |
| `ui_boundary.py` | 33, 37–40 | dead `_validator`; E006/E007 없음 | **High** |
| `control/solve_partial_magic_square.py` | 22–23 | 무시 반환값·solver 중복 orchestration | **High** |
| `ui/magic_square_boundary.py` | 30, 40 | stub resolver → `NotImplementedError` | **High** |
| `screen/app.py` | 121–125 | `DomainError` → envelope 우회 | **High** |
| `schemas.py` | 8–33 | `FailureResult` / `FailureResponse` 이중 envelope | **High** |
| `constants.py` ↔ `entity/.../magic_constant.py` | — | 이중 SSOT | Medium |
| `ui_boundary.py` + `magic_square_boundary.py` | — | 이중 Boundary 패턴 | Medium |
| `screen/app.py` | 57–105 | UI 구성 + G1 데이터 주입 | Medium |
| `control/solve_two_blank_puzzle.py` | 11 | permanent `NotImplementedError` | Medium |

---

## 5. SRP 위반 점검

### ① 함수 다중 역할

| 파일:줄번호 | 역할 1 | 역할 2 |
|-------------|--------|--------|
| `control/solve_partial_magic_square.py:13-25` | 오케스트레이션 | `to_array()` 결과 조립 |
| `boundary/ui_boundary.py:35-41` | 검증 게이트 | 위임 + `SuccessResponse` 직렬화 |
| `boundary/screen/app.py:57-105` | UI 구성 | `DEFAULT_G1_GRID` 주입 |
| `boundary/screen/app.py:118-129` | `solve` 호출 | 예외/결과 라우팅 + 표시 |

### ② 클래스 — 데이터+검증 혼재

**해당 없음** (격자 데이터 보관 + 도메인 판정 동시 담당 클래스 없음).

**클래스 복수 책임:** `UIBoundary` (DI + validate/delegate/envelope), `MagicSquareMainWindow` (UI + solve 워크플로).

### ③ UI 비즈니스 판단

**해당 없음** — 마법합 34, Step A/B, E00x 코드 결정 없음.

---

## 6. 테스트 갭·RED 스켈레톤

| 구분 | 파일 | 상태 |
|------|------|------|
| GREEN | `test_ac_fr_01_01_dimension_validation.py` | 29건 — 회귀 앵커 |
| GREEN | `test_solve_partial_magic_square.py`, U-OUT-01 | Control·envelope 앵커 |
| assert만·구현 RED | `test_u_in_04_08_input_validation.py` | **P0 GREEN 선행** |
| `pytest.fail` | `test_u_flow_execute_isolation.py` (4) | UIBoundary SUT로 재작성 |
| `pytest.fail` | `test_u_out_01_03` U-OUT-02/03 | GREEN 선행 |
| 중복 RED | `test_u_in_validation.py`, `test_u_out_contract.py` | GREEN 후 정리 |

**Control:** `solve_two_blank_puzzle.py` 전용 `tests/control/test_*` **없음**.

---

## 7. 리팩터링 대상 목록

| 순번 | 대상 파일 | 문제 | 적용 기법 | 우선순위 |
|------|-----------|------|-----------|----------|
| 1 | `validation/input_validator.py` | E002/E004/E005 미구현 | short-circuit GREEN 구현 | **P0** |
| 2 | `ui_boundary.py` | E006/E007 미매핑; dead `_validator` | Replace Error with Envelope; dead field 제거 | **P0** |
| 3 | `control/solve_partial_magic_square.py` | locate/find 이중 호출 | Remove Duplication — solver 단일 진입 | **P0** |
| 4 | `tests/boundary/test_u_flow_execute_isolation.py` | SUT/API 불일치 | 테스트 정렬 (UIBoundary + mock) | **P0** |
| 5 | `tests/boundary/test_u_out_01_03_output_contract.py` | U-OUT-02/03 RED | RED→GREEN | **P0** |
| 6 | `screen/app.py` | Control 직접 조립; `DomainError` UI | Extract Factory; 예외→boundary | **P1** |
| 7 | `ui/magic_square_boundary.py` + `ui_boundary.py` | 이중 API·stub | Collapse / Adapter | **P1** |
| 8 | `boundary/constants.py` + entity VO | 이중 SSOT | Single Source of Truth | **P1** |
| 9 | `ui_boundary.py` `solve()` | 함수 다중 역할 | Extract Method (공개 API 불변) | **P1** |
| 10 | `screen/app.py` `__init__` | UI+데이터 주입 | Extract Method | **P2** |
| 11 | 중복 RED 테스트 파일 | CI 노이즈 | GREEN 후 삭제/격리 | **P2** |
| 12 | `control/solve_two_blank_puzzle.py` | stub | Remove Dead Code 또는 통합 | **P2** |
| 13 | `tests/golden_master/capture.py` | content 검증 중복 | InputValidator 위임 (연관) | **P2** |

**실행 순서:** Step A 테스트 GREEN → Step B P0 리팩터 → Step C 회귀 → Step D P1/P2.

---

## 8. 테스트 선행 필요 항목

### Boundary P0 (REFACTOR 전 필수)

| 함수 / API | 테스트 파일 | ID |
|------------|-------------|-----|
| `InputValidator.validate` | `test_u_in_04_08_input_validation.py` | U-IN-04~08 |
| `UIBoundary.solve` | `test_u_flow_execute_isolation.py` (재작성) | U-FLOW-02 |
| `UIBoundary.solve` | `test_u_out_01_03_output_contract.py` | U-OUT-01~03 |
| `UIBoundary.solve` | `test_ac_fr_01_01_ui_boundary_flow.py` | AC-FR-01-01 격리 |

### Control P0

| 함수 / API | 테스트 파일 |
|------------|-------------|
| `SolvePartialMagicSquare.resolve` | `test_solve_partial_magic_square.py` |

### 권장 신규

| 함수 / API | 제안 테스트 |
|------------|-------------|
| `UIBoundary.solve` | `test_ui_boundary_error_mapping.py` — unsolvable → FailureResponse |

### 리팩터 범위 한정 시 게이트 아님

- `tests/entity/test_d_val_*`, `test_d_sol_*` (Domain 트랙)
- `test_ac_fr_01_01_dimension_validation` — 이중 API 정리 시 함께 검토

---

## 9. REFACTOR phase 게이트

`.cursor/rules/magicsquare-tdd-testing.mdc` 기준:

- **GREEN 확인 후에만 refactor**
- 공개 API·**E001~E007**·**`int[6]`**·F1/F2 기대값 불변
- 동일 스위트 GREEN, 커버리지 ≥ 리팩터 전
- 금지: 테스트 삭제·완화·skip/xfail, F1/F2 임의 변경

**한 줄:** GREEN으로 고정된 계약 없이 구조 변경 시 E00x·`int[6]` 회귀를 증명할 수 없음.

---

## 10. 리팩터 후 검증

### 회귀 명령 (PowerShell)

```powershell
cd c:\DVV\MagicSquare_XX

python -m pytest tests/boundary/test_u_in_04_08_input_validation.py -v
python -m pytest tests/boundary/test_u_flow_execute_isolation.py -v
python -m pytest tests/boundary/test_u_out_01_03_output_contract.py -v
python -m pytest tests/boundary/test_ac_fr_01_01_ui_boundary_flow.py -v
python -m pytest tests/control/test_solve_partial_magic_square.py -v
python -m pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py -v
python -m pytest tests/golden_master/test_golden_master_magic_square.py -v
python -m pytest tests/ -q --cov=src/magicsquare --cov-report=term-missing
```

### 외부 동작 불변 확인

| 항목 | 방법 |
|------|------|
| FR-01 실패 | U-IN 코드·메시지 바이트 일치 |
| 성공 `int[6]` | G1→`[2,2,10,3,3,7]`; F1→`[1,2,3,2,3,11]` (Domain GREEN 후) |
| resolver 격리 | invalid → mock `resolve` 0회 |
| Golden Master | `golden_master_expected.txt` diff 없음 |
| GUI | `python run_gui.py` — G1 풀기 동일 결과 |

---

## 11. 미완·후속

| 우선순위 | 항목 | 상태 |
|----------|------|------|
| P0 | Step A: U-IN-04~08·U-FLOW·U-OUT-02/03 GREEN | [ ] |
| P0 | Step B: P0 리팩터 (본 보고서 §7 순번 1–5) | [ ] |
| P1 | Screen composition·이중 Boundary 통합 | [ ] |
| P1 | E006/E007 매핑 테스트 | [ ] |
| P2 | 중복 RED 스켈레톤 정리 | [ ] |
| — | F1/F3 Domain 트랙 (별도) | [ ] |

**다음 Report/Prompt 번호:** `16` (REFACTOR 실행 세션 시)

---

## 12. Transcript

[`Prompt/15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Transcript_Prompt.md`](../Prompt/15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Transcript_Prompt.md)
