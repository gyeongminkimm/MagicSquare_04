# Magic Square 4×4 — REFACTOR 프로그램 Phase 0 게이트 및 로드맵 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `16_MagicSquare_REFACTOR_Program_Phase0_Gate_And_Roadmap_Report` |
| **전제 보고서** | [`15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Report.md`](15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Report.md), [`14_MagicSquare_Golden_Master_Regression_Report.md`](14_MagicSquare_Golden_Master_Regression_Report.md), [`09_MagicSquare_Full_DualTrack_RED_Design_Report.md`](09_MagicSquare_Full_DualTrack_RED_Design_Report.md) |
| **기준 SSOT** | [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md), [`.cursor/rules/magicsquare-tdd-testing.mdc`](../.cursor/rules/magicsquare-tdd-testing.mdc), [`docs/golden_master_approval_design.md`](../docs/golden_master_approval_design.md) |
| **작성일** | 2026-05-29 |
| **상태** | **Phase 0 미통과** — Wave 1(C1~C4) **착수 불가** |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [프로그램 범위·금지](#2-프로그램-범위금지)
3. [프로젝트·경로 매핑](#3-프로젝트경로-매핑)
4. [Phase 0 게이트 실측](#4-phase-0-게이트-실측)
5. [Wave 1 착수 판정](#5-wave-1-착수-판정)
6. [REFACTOR 3유형 요약](#6-refactor-3유형-요약)
7. [전체 로드맵 (Wave 1~4)](#7-전체-로드맵-wave-14)
8. [C1 RF-01 실행 계획](#8-c1-rf-01-실행-계획)
9. [ISS-012-01 GM 영향 (C3)](#9-iss-012-01-gm-영향-c3)
10. [커밋·위험 구간](#10-커밋위험-구간)
11. [Report/15와의 관계](#11-report15와의-관계)
12. [미완·후속](#12-미완후속)
13. [Transcript](#13-transcript)

---

## 1. 세션 요약

| Phase | 작업 | 결과 |
|-------|------|------|
| 1 | 리팩터 대상 **3유형** 분류·README To-Do 반영 | 유형 1~3 표·체크리스트 — [`README.md`](../README.md) § REFACTOR 3유형 |
| 2 | REFACTOR **다중 커밋 프로그램** 프롬프트 수신 (Report/14 + RF/R-L/R-U) | Phase 0~4 로드맵·GM 규칙·금지 사항 정리 |
| 3 | Phase 0 게이트 **실측** (`pytest`) | G-02만 충족; G-01·G-03·G-04·G-05 미충족 |
| 4 | Wave 1·C1·C3 GM·위험 분석 | 본 문서 — **코드 변경 없음** |

**판정:** REFACTOR Wave 1 전에 Report/15 **Step A (유형 3 → 유형 1 GREEN)** 필수.

---

## 2. 프로그램 범위·금지

### 목적 (이번 프로그램)

- 코드 품질·중복 제거·ECB/SRP·invariant 가독성·회귀 안전성
- 기능 추가·계약 변경·출력 변경·architecture redesign **금지**
- 커밋당 프롬프트 A(단일 커밋, semantic-preserving)

### 고정 계약 (전 Phase 불변)

| 항목 | 내용 |
|------|------|
| 입력 | 4×4 `int[][]`, `0`=빈칸(정확히 2), 값 `0\|1~16`, 비0 중복 금지, row-major 첫 빈칸 |
| 출력 | `int[6]` `[r1,c1,n1,r2,c2,n2]`, 1-index, 작은 수→첫 빈칸, 실패 시 reverse fallback |
| 오류 | E001~E007 envelope 불변 |
| Golden Master | normal/reverse success, E002, E005, E006 시나리오 |

### 금지 (프로그램 전체)

- Wave 1 미완료 시 Entity R-L* 선행
- 한 세션에 Wave 전체 구현
- RED 테스트를 refactor로 우회
- generic framework·plugin·repository 신규 도입
- GM `expected.txt` 무단 수정 (`--approve-golden` 없이)

---

## 3. 프로젝트·경로 매핑

프롬프트 템플릿은 **MagicSquare_1004** 명칭을 사용하나, 실측·산출물은 **MagicSquare_XX** 기준이다.

| 프롬프트 (1004) | MagicSquare_XX |
|-----------------|----------------|
| `tests/test_gm_01_magic_square_golden_master.py` | `tests/golden_master/test_golden_master_magic_square.py` |
| `SC-CTL-002~004` | ID 없음 → `tests/control/test_solve_partial_magic_square.py` (1건 GREEN) |
| `ValidationResult` | `ValidationSuccess` \| `FailureResponse` (`boundary/schemas.py`) |
| `tests/boundary/test_main_window.py` | **미존재** (Wave 2 RF-06 전제) |

---

## 4. Phase 0 게이트 실측

**측정일:** 2026-05-29  
**환경:** `python -m pytest` (프로젝트 루트)

### 검증 명령

```powershell
cd c:\DVV\MagicSquare_XX
python -m pytest tests/ -v
python -m pytest tests/golden_master/test_golden_master_magic_square.py -v
```

### 결과 요약

| 게이트 | 기준 | 실측 | 판정 |
|--------|------|------|------|
| **G-01** | `pytest tests/` 전체 GREEN | **52 passed, 40 failed** | **FAIL** |
| **G-02** | GM-1 matched | GM-TC-01~05 + full-file **6/6 PASS** | **PASS** |
| **G-03** | U-FLOW-02, U-OUT-02~03, U-IN-06~08 GREEN | 아래 §4.1 | **FAIL** |
| **G-04** | D-SOL-03, SC-CTL-002~004 GREEN | 아래 §4.2 | **FAIL** |
| **G-05** | `test_main_window.py` 존재 (P1) | 파일 없음 | **FAIL** |

### §4.1 G-03 상세

| 테스트 | 결과 | 비고 |
|--------|------|------|
| `test_u_in_04_08` G1 | PASS | 차원·G1 통과만 구현 |
| `test_u_in_04_08` U-IN-04~08 | **5 FAIL** | `InputValidator` E002/E004/E005 미구현 |
| `test_u_flow_execute_isolation` ×4 | **4 FAIL** | `pytest.fail` RED; SUT=`MagicSquareBoundary` |
| `test_u_out_01_03` U-OUT-01 | PASS | UIBoundary + 실제 resolve |
| `test_u_out_01_03` U-OUT-02~03 | **2 FAIL** | `pytest.fail` RED |

### §4.2 G-04 상세

| 테스트 | 결과 | 비고 |
|--------|------|------|
| `test_solve_partial_magic_square` | PASS | G1 → `[2,2,10,3,3,7]` |
| `test_d_sol_01_04` D-SOL-01 | PASS | F2 경로 |
| `test_d_sol_01_04` D-SOL-02~04, D-SOL-03 | **FAIL** | `pytest.fail` RED (F2·F3·G3) |
| SC-CTL-002~004 | N/A | 테스트 ID 미정의 |

### §4.3 G-01 실패 구성 (40건)

| 영역 | 건수(대략) | 원인 |
|------|------------|------|
| Boundary U-IN/U-FLOW/U-OUT | 14+ | content 미구현·RED 스켈레톤·중복 파일 |
| Entity D-VAL/D-SOL/D-LOC/D-MIS | 26 | RED 스켈레톤·이중 테스트 모듈 |

> 프롬프트 “RED 19건”과 차이: 중복 RED 파일(`test_u_in_validation.py`, `test_u_out_contract.py`, `test_d_*.py` 쌍) 및 Entity 스켈레톤 전체 포함.

---

## 5. Wave 1 착수 판정

| 항목 | 판정 |
|------|------|
| Wave 1 (C1~C4) 착수 | **불가** — Phase 0 미통과 |
| 선행 필수 | Report/15 Step A — **유형 3(테스트)** → **유형 1(계약)** GREEN |
| GM만 통과한 채 REFACTOR | **금지** — TDD REFACTOR phase 규칙 위반 |

---

## 6. REFACTOR 3유형 요약

README To-Do와 동일. 실행 순서: **유형 3 → 1 → 2**.

| 유형 | 건수 | 핵심 | 대표 산출 |
|------|------|------|-----------|
| **1. 계약·검증** | 4 | E002–E007, resolver, GM 검증 위임 | `input_validator.py`, `ui_boundary.py`, GM `capture.py` |
| **2. 구조·ECB** | 8 | 중복·dead·이중 API/SSOT·Screen·SRP | `solve_partial`, `screen/app.py`, 이중 Boundary |
| **3. 테스트** | 3 | P0 GREEN → REFACTOR 후 정리 | `test_u_flow`, `test_u_out`, 중복 RED 파일 |

상세(대상·문제·기법): Report/15 §7.

---

## 7. 전체 로드맵 (Wave 1~4)

Report/14 GM + REFACTOR 프로그램 템플릿 통합. **Wave 1은 Phase 0 PASS 후에만 착수.**

### Wave 1 — P0 계약·SSOT (커밋 1~4)

| 커밋 | ID | Track | 작업 | 검증 test ID |
|------|-----|-------|------|--------------|
| C1 | RF-01 | Boundary | ValidationResult, NotImplementedError 제거 | U-IN-*, U-FLOW-02 |
| C2 | RF-02 | Boundary | E006 ErrorMapper | U-OUT-03, GM G3 |
| C3 | RF-03 | Control | SolutionResult.values SSOT | SC-CTL-002~003*, GM G1/G2 |
| C4 | RF-04 | Control+Entity | locate/find 중복 정리 | SC-CTL-004*, D-SOL-* |

\* XX: `tests/control/test_solve_partial_magic_square.py` 등으로 대체.

### Wave 2 — P1 DRY·Screen (커밋 5~8)

| C5 | RF-05 | Boundary | `_failure()` extract | U-IN-* |
| C6 | RF-06 | Screen | ResultPresenter | `test_main_window` (G-05 선행) |
| C7 | RF-07 | Screen | G1 fixture·상수 SSOT | GM, Screen |
| C8 | RF-08 | Screen | `_init_ui()` extract | Screen |

### Wave 3 — P2 Entity (커밋 9~12)

R-L3 → R-L2 → R-L1 → R-L4 (MATRIX_SIZE, sumRow/Col/Diag, Coordinate VO, tryPlacement)

### Wave 4 — P2 Boundary polish (커밋 13~14)

R-U2 Error 상수화, R-U3 ResultFormatter (1-index SSOT)

---

## 8. C1 RF-01 실행 계획

**전제:** Phase 0 G-03 일부 충족 후(특히 U-IN-04~08 GREEN). C1에 content 구현을 넣으면 **GREEN 커밋**과 분리할 것.

### 수정 파일 (XX)

| 파일 | 변경 |
|------|------|
| `boundary/validation/input_validator.py` | E002/E004/E005 (GREEN — RF-01과 분리 권장) |
| `boundary/schemas.py` | 검증 결과 타입 SSOT (`ValidationSuccess` / alias) |
| `boundary/ui_boundary.py` | dead `_validator` 제거 |
| `boundary/ui/magic_square_boundary.py` | `SolveTwoBlankPuzzle` stub → `SolvePartialMagicSquare` 또는 Adapter |
| `control/solve_two_blank_puzzle.py` | `NotImplementedError` 제거·위임 |

### 검증

```powershell
python -m pytest tests/boundary/test_u_in_04_08_input_validation.py -v
python -m pytest tests/boundary/test_u_flow_execute_isolation.py -v
python -m pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py -v
python -m pytest -m golden_master -v
```

### 롤백

- 단일 커밋 `git revert`
- GM diff → (a) 회귀 롤백 (b) 문서화된 SSOT만 `--approve-golden`

---

## 9. ISS-012-01 GM 영향 (C3)

저장소에 `ISS-012-01` ID는 **미등록**. 프로그램 C3(RF-03 `SolutionResult.values` SSOT)을 XX에 대응할 때의 GM 리스크이다.

| 요소 | GM 연관 |
|------|---------|
| 캡처 | `SolvePartialMagicSquare.resolve()` → `SuccessResponse.data` |
| baseline | `normal_success` `[1,2,3,2,3,11]`, `reverse_success` `[2,2,10,3,3,7]` |
| VO | `SolutionVector.to_array()` |

| diff 유형 | 조치 |
|-----------|------|
| `int[6]` 숫자 변경 | 버그 → **롤백** |
| 내부 타입만, 출력 동일 | GM matched 유지 |
| 의도적 계약 정정(Report 근거) | `--approve-golden` |

C1에서 `InputValidator` SSOT화 시 `capture._validate_content`와 메시지 정합 — 시맨틱 토큰 불변이면 approve 불필요.

---

## 10. 커밋·위험 구간

| 구간 | 커밋 수 | 위험 | 완화 |
|------|---------|------|------|
| Phase 0 GREEN | 3~8 (추정) | 최고 | 유형 3→1 순; mock 격리 |
| Wave 1 | 4 | 높음 | GM 매 커밋; UIBoundary 단일 SUT |
| Wave 2 | 4 | 중간 | G-05 `test_main_window` 선행 |
| Wave 3~4 | 6 | 중~낮 | Wave 1 완료 후만 Entity R-L* |

**커버리지 80%:** Phase 0 미통과 — DEF-004/005 Open ([`docs/defect_list.md`](../docs/defect_list.md)).

---

## 11. Report/15와의 관계

| Report/15 | 본 문서 (16) |
|-------------|--------------|
| ECB 스멜·SRP·§7 리팩터 목록 | Phase 0 **실측**·Wave 로드맵 **착수 판정** |
| Step A~D | Phase 0 게이트 = Step A의 **정량 게이트** |
| 3유형 (README) | §6 동일 SSOT |

다음 실행 세션: Phase 0 GREEN 커밋 묶음 → Wave 1 C1.

---

## 12. 미완·후속

| 우선 | 항목 | 상태 |
|------|------|------|
| P0 | G-01: `pytest tests/` 전체 GREEN | [ ] |
| P0 | G-03: U-IN-04~08, U-FLOW, U-OUT-02~03 | [ ] |
| P0 | G-04: D-SOL-02~03 GREEN | [ ] |
| P1 | G-05: `test_main_window.py` | [ ] |
| — | Wave 1 C1~C4 REFACTOR | [ ] |
| — | Report/17 (Wave 1 완료 보고) | 예정 |

**다음 Report/Prompt 번호:** `17` (Wave 1 실행 세션 시)

---

## 13. Transcript

[`Prompt/16_MagicSquare_REFACTOR_Program_Phase0_Gate_And_Roadmap_Transcript_Prompt.md`](../Prompt/16_MagicSquare_REFACTOR_Program_Phase0_Gate_And_Roadmap_Transcript_Prompt.md)
