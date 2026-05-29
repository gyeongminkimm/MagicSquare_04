# MagicSquare_XX

4×4 마방진(Magic Square) **2칸 퍼즐 완성**을 Dual-Track TDD로 구현하는 프로젝트입니다.  
문제 정의·설계(STEP 1–5, Report/02)는 완료되었고, **AC-FR-01-01 Boundary 구조 검증**은 GREEN 완료 상태입니다.

---

## 프로젝트 목적

**4×4 격자**에 **1부터 16**까지를 각 칸에 한 번씩 배치했을 때, 합의한 **관심 선**(행·열·대각선)마다 합이 같아지는 배치를 **일관된 기준으로 판별**하고, 필요하면 그 조건을 만족하는 배치를 **반복·검증·공유 가능한 형태**로 다루는 것이 목표입니다.

단순히 “마방진 프로그램을 만든다”가 아니라, **규칙·불변 조건·판별과 생성의 분리·명확한 입출력 계약**을 훈련하는 것이 핵심입니다.

### 한 줄 정의

> 4×4에 1~16을 한 번씩 배치할 때, **합의된 선들의 합 일치와 숫자 집합 조건**을 명확히 정의하고 일관되게 판별하며, 필요 시 그 조건을 만족하는 배치를 얻는 과정을 **반복·검증·공유 가능하게** 다룬다.

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| 문제 인식·정의 (STEP 1–5) | 완료 |
| 문제 정의 보고서 | [`Report/01_MagicSquare_ProblemDefinition_Report.md`](Report/01_MagicSquare_ProblemDefinition_Report.md) |
| Dual-Track TDD / Clean Architecture 설계 | 완료 — [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
| Cursor Rules (모듈형 `.mdc`) | 완료 — [`Report/04_MagicSquare_Modular_CursorRules_Report.md`](Report/04_MagicSquare_Modular_CursorRules_Report.md) |
| AC-FR-01-01 Boundary RED/GREEN | 완료 — [`Report/08`](Report/08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md), [`Report/11`](Report/11_MagicSquare_AC_FR_01_01_GREEN_Verification_Report.md) (29/29 PASS) |
| PyQt6 Screen UI (`boundary.screen`) | **실행 가능** — G1 기본 격자 · UIBoundary 연동 |
| Dual-Track RED 스켈레톤 (Report/09) | RED 작성 — U-IN-04~08 등 일부 GREEN 미착수 |
| ECB·리팩터 분석·계획 (Report/15) | **계획 완료** — `src/` REFACTOR **미착수** |
| REFACTOR 프로그램 Phase 0 게이트 (Report/16) | **G-02만 PASS** — Wave 1 **착수 불가** |

---

## 도메인 요약

| 항목 | 내용 |
|------|------|
| 격자 | 4×4 (16칸) |
| 숫자 | 1 ~ 16, 각 값 1회 |
| 마법합 | 34 (행·열·대각선 기준) |
| 유효성 정책 (현재 가정) | 4행 + 4열 + 2대각선, 합 모두 34 |
| 성공 기준 | 교과서 예시와 **동일한 격자**가 아니라 **규칙 충족** (해는 여러 개 존재) |

---

## 핵심 Invariant (요약)

완성된 유효 배치에서 성립해야 하는 조건입니다. 상세는 보고서 STEP 5를 참고하세요.

- **구조·집합:** 16칸, 값 집합 = {1,…,16}, 중복·누락·범위 밖 없음  
- **합:** 관심하는 모든 선의 합 = 34  
- **판별:** 동일 격자·동일 규칙 → 항상 같은 유효/무효 판단  
- **생성 계약:** 조건을 만족하는 배치를 얻는 결과는 합의된 검사를 통과해야 함  

---

## 문제 정의 워크숍 (STEP 1–5)

| STEP | 주제 | 요지 |
|------|------|------|
| **1** | Observation | 4×4·합 제약과 소프트웨어 목표 사이의 간극 관찰 |
| **2** | Why #1 | “완성”의 의미, 다해, 생성/검증/퍼즐 역할 혼동 주의 |
| **3** | Why #2 | 반복 가능성, 검증 자동화, 오류 방지, 규칙 기반 사고 |
| **4** | Why #3 | TDD로 규칙·역할·불변식·입출력을 설계 전에 고정 |
| **5** | 진짜 문제 정의 | 표면 정의 vs 개선 정의, Invariant, 훈련 사고 능력 |

### 표면 정의 vs 개선 정의

| | 표면 (피할 표현) | 개선 (정확한 초점) |
|---|------------------|---------------------|
| 초점 | 프로그램·출력물 | 규칙·판별·재현 가능한 판단 |
| 성공 | 격자를 만듦 | 합의된 불변 조건 충족 |
| 범위 | 생성만 | 판별 우선, 생성·부분 상태는 선택 |

---

## 설계 원칙 (문제 정의 단계에서 확정한 방향)

1. **판별과 생성 분리** — “맞는지 확인”과 “맞는 배치를 얻기”는 다른 책임  
2. **규칙을 먼저 고정** — 어떤 선까지 검사할지 정책으로 합의  
3. **TDD 친화** — 불변 조건을 관찰 가능한 명세·테스트로 옮길 수 있어야 함  
4. **다해 수용** — 하나의 예시 격자에 과적합하지 않음  

---

## 설계 단계에서 확정한 것 (02 보고서)

- **1순위 시나리오:** 2칸 퍼즐 완성 → `int[6]` 반환  
- **검증 범위:** 행·열·대각선 포함, 마법합 34  
- **입력 표현:** `int[4][4]`, `0`=빈칸(정확히 2개)  
- **아키텍처:** Dual-Track (Domain ∥ UI Boundary) + Clean Architecture + Repository(메모리 1차)

## 아직 구현 전·미완인 것

- U-IN-04~08 blank/range/duplicate Boundary 검증 GREEN  
- F3(UNSOLVABLE) 픽스처 숫자 고정  
- File 기반 Repository (2차)  
- INT F1/F2 E2E

---

## ECB 리팩터 분석·계획 (Report/15)

> **상태:** 분석·계획만 반영 — **코드 리팩터링은 아직 하지 않음.**  
> SSOT: [`Report/15`](Report/15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Report.md), [`Report/16`](Report/16_MagicSquare_REFACTOR_Program_Phase0_Gate_And_Roadmap_Report.md) (Phase 0 실측·Wave 로드맵), [`Prompt/15`](Prompt/15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Transcript_Prompt.md), [`Prompt/16`](Prompt/16_MagicSquare_REFACTOR_Program_Phase0_Gate_And_Roadmap_Transcript_Prompt.md)

### 프롬프트 → 실제 파일 (ECB)

| 프롬프트 | 실제 경로 | 레이어 |
|----------|-----------|--------|
| `domain.py` | `src/magicsquare/control/solve_partial_magic_square.py` | Control |
| `boundary.py` | `src/magicsquare/boundary/ui_boundary.py` | Boundary |
| `gui/main_window` | `src/magicsquare/boundary/screen/app.py` | Screen |

### REFACTOR 전 게이트 (Step A — 테스트 GREEN)

| 우선 | 테스트 | 내용 |
|------|--------|------|
| P0 | `test_u_in_04_08_input_validation.py` | U-IN-04~08 (E002/E004/E005) |
| P0 | `test_u_flow_execute_isolation.py` | U-FLOW-02 — `UIBoundary` + mock `resolve` 0회 |
| P0 | `test_u_out_01_03_output_contract.py` | U-OUT-02/03 (`pytest.fail` → GREEN) |
| 앵커 | `test_solve_partial_magic_square.py`, `test_ac_fr_01_01_dimension_validation.py` (29), Golden Master | 회귀 유지 |

### P0 리팩터 대상 (계획만 — 미착수)

1. `validation/input_validator.py` — FR-01 content 구현  
2. `ui_boundary.py` — E006/E007 envelope 매핑, dead `_validator` 정리  
3. `solve_partial_magic_square.py` — locate/find **중복 제거** (solver 단일 진입)  
4. 이중 Boundary (`MagicSquareBoundary` vs `UIBoundary`) — P1에서 통합 검토  

### REFACTOR 3유형 요약 (Report/15)

| 유형 | 건수 | 핵심 |
|------|------|------|
| 1. 계약·검증 | 4 | E002–E007, resolver, GM 검증 위임 |
| 2. 구조·ECB | 8 | 중복·dead·이중 API/SSOT·Screen·SRP |
| 3. 테스트 | 3 | P0 GREEN → REFACTOR 후 정리 |

**실행 순서:** 유형 3 → 1 → 2 (Step A → 계약 → 구조). 상세 항목(대상·문제·기법): Report/15 §7.

#### REFACTOR 3유형 To-Do

- [ ] **유형 3 — 테스트** (3건) — P0 GREEN → REFACTOR 후 정리  
- [ ] **유형 1 — 계약·검증** (4건) — E002–E007, resolver, GM 검증 위임  
- [ ] **유형 2 — 구조·ECB** (8건) — 중복·dead·이중 API/SSOT·Screen·SRP  

### 회귀 명령 (리팩터 후)

```powershell
cd c:\DVV\MagicSquare_XX
python -m pytest tests/boundary/test_u_in_04_08_input_validation.py tests/boundary/test_u_flow_execute_isolation.py tests/boundary/test_u_out_01_03_output_contract.py tests/control/test_solve_partial_magic_square.py tests/boundary/test_ac_fr_01_01_dimension_validation.py tests/golden_master/test_golden_master_magic_square.py -v
```

상세 표·스멜·SRP: Report/15 §7–10.

---

## GUI 실행 (PyQt6)

### 1. 설치

```powershell
cd c:\DVV\MagicSquare_XX
pip install -e ".[gui]"
```

### 2. 실행 (아래 중 하나)

```powershell
python run_gui.py
python -m boundary.screen.app
python -m boundary.screen
python -m magicsquare.boundary.screen
magicsquare-gui
```

진단 모드 (`grid=None` → `오류: Grid must be 4x4.`):

```powershell
python run_gui.py --verify
python -m boundary.screen.app --verify
```

### 3. 사용법

| UI | 동작 |
|----|------|
| 4×4 숫자 격자 | `QSpinBox` 0~16 (0=빈칸), **기본값 = G1** |
| **풀기** | `UIBoundary.solve(grid)` 호출 |
| 결과 라벨 | 성공: `결과 (r1, c1, n1, r2, c2, n2): …` / 실패: `오류: …` |

G1 기본 격자에서 **풀기** → `2, 2, 10, 3, 3, 7` (F2 계약, Report/02).

구현 위치: `src/magicsquare/boundary/screen/app.py` (Screen → UIBoundary만 호출).

---

## 디렉터리 구조

```
MagicSquare_XX/
├── README.md
├── src/magicsquare/          # entity, control, boundary (+ boundary/screen PyQt)
├── src/boundary/             # python -m boundary.screen 실행 alias
├── tests/                    # domain, boundary, entity (RED/GREEN)
├── Report/                   # 01~15 세션 보고서
├── docs/                     # PRD, test_plan, defect_list, golden_master
├── Prompt/                   # Transcript Export
└── .cursor/rules/            # magicsquare-*.mdc
```

---

## 문서

- **문제 정의:** [Report/01_...](Report/01_MagicSquare_ProblemDefinition_Report.md) — STEP 1–5, Invariant  
- **TDD 설계:** [Report/02_...](Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) — Domain/UI/Data/통합, RED 목록, Traceability  
- **Cursor Rules (초기·User):** [Report/03_...](Report/03_MagicSquare_CursorRules_And_InitialImplementation_Report.md)  
- **Cursor Rules (모듈형 `.mdc`):** [Report/04_...](Report/04_MagicSquare_Modular_CursorRules_Report.md)  
- **프롬프트 Export:** [Prompt/02_...](Prompt/02_MagicSquare_DualTrack_TDD_Design_Prompt.md), [Prompt/03_...](Prompt/03_MagicSquare_CursorRules_UserEntity_Prompt.md), [Prompt/04_...](Prompt/04_MagicSquare_Modular_CursorRules_Prompt.md)
- **Dual-Track GREEN·PyQt Screen:** [Report/13](Report/13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Report.md), [Prompt/13](Prompt/13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Transcript_Prompt.md)
- **Golden Master 회귀:** [Report/14](Report/14_MagicSquare_Golden_Master_Regression_Report.md), [Prompt/14](Prompt/14_MagicSquare_Golden_Master_Regression_Transcript_Prompt.md), [docs/golden_master_approval_design.md](docs/golden_master_approval_design.md)
- **ECB·리팩터 분석·계획:** [Report/15](Report/15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Report.md), [Prompt/15](Prompt/15_MagicSquare_ECB_Refactor_Analysis_And_Plan_Transcript_Prompt.md) — REFACTOR **미착수**
- **REFACTOR 프로그램·Phase 0 게이트:** [Report/16](Report/16_MagicSquare_REFACTOR_Program_Phase0_Gate_And_Roadmap_Report.md), [Prompt/16](Prompt/16_MagicSquare_REFACTOR_Program_Phase0_Gate_And_Roadmap_Transcript_Prompt.md) — Wave 1 **착수 불가** (G-01·G-03·G-04 미충족)
- **테스트·QA (AC-FR-01-01):** [Report/08](Report/08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md), [Report/11](Report/11_MagicSquare_AC_FR_01_01_GREEN_Verification_Report.md), [Report/12](Report/12_MagicSquare_AC_FR_01_01_TDD_Checklist_Report.md) (TDD 체크리스트·RED/GREEN 커밋 묶음), [docs/test_plan.md](docs/test_plan.md), [docs/defect_list.md](docs/defect_list.md), [docs/golden_master_approval_design.md](docs/golden_master_approval_design.md), [docs/README.md](docs/README.md) (RED To-Do·Golden Master 체크리스트)

---

## TDD 체크리스트 — AC-FR-01-01 (구조·차원 검증)

> SSOT: [`tests/boundary/test_ac_fr_01_01_dimension_validation.py`](tests/boundary/test_ac_fr_01_01_dimension_validation.py), [`tests/boundary/conftest.py`](tests/boundary/conftest.py), [`docs/test_plan.md`](docs/test_plan.md)  
> 계약: `grid=None` 등 구조 실패 → `code=INVALID_SIZE`, `message=Grid must be 4x4.`, `resolve()` **0회**  
> **현재:** Report/11 기준 **29/29 GREEN** — 아래 GREEN 항목은 회귀·재현용; RED 커밋 묶음은 히스토리 분리 시 참고. 상세: [Report/12](Report/12_MagicSquare_AC_FR_01_01_TDD_Checklist_Report.md), [Prompt/12](Prompt/12_MagicSquare_AC_FR_01_01_TDD_Checklist_Transcript_Prompt.md).

### RED 커밋 묶음 (5 commits — 테스트만, `src/` 금지)

각 커밋 후 `pytest`로 **의도적 FAIL** 또는 ImportError 확인.

- [x] **RED-1** — `conftest.py` + `TestFailureReturnOnNoneGrid` (5건, #001~005)
- [x] **RED-2** — `TestBoundaryDimensionValues` (5건, #006~010)
- [x] **RED-3** — `TestDomainResolverIsolation` (5건, #011~015)
- [x] **RED-4** — `TestMessageExactMatch` (9 nodes, #016~024)
- [x] **RED-5** — `TestScopeRestriction` (5건, #025~029) — `src/` 변경 없이 PASS 가능

### 테스트 케이스 — 오름차순 (#001~029)

| # | 체크 | 클래스 / 테스트 | BV·입력 |
|---|------|-----------------|--------|
| 001 | [x] | `TestFailureReturnOnNoneGrid::test_none_grid_returns_failure_not_success_list` | BV-01 `None` |
| 002 | [x] | `…::test_none_grid_returns_invalid_size_code` | BV-01 |
| 003 | [x] | `…::test_none_grid_returns_grid_must_be_4x4_message` | BV-01 |
| 004 | [x] | `…::test_none_grid_returns_pydantic_failure_result_type` | BV-01 |
| 005 | [x] | `…::test_none_grid_returns_identical_failure_on_repeat` | BV-01 / SP-08 |
| 006 | [x] | `TestBoundaryDimensionValues::test_empty_list_returns_invalid_size_code` | BV-02 `[]` |
| 007 | [x] | `…::test_four_empty_rows_returns_invalid_size_code` | BV-03 `[[]]*4` |
| 008 | [x] | `…::test_three_by_four_returns_invalid_size_code` | BV-04 `GRID_3X4` |
| 009 | [x] | `…::test_empty_list_returns_grid_must_be_4x4_message` | BV-02 |
| 010 | [x] | `…::test_four_empty_rows_returns_grid_must_be_4x4_message` | BV-03 |
| 011 | [x] | `TestDomainResolverIsolation::test_none_grid_resolve_not_called` | BV-01 |
| 012 | [x] | `…::test_empty_list_resolve_not_called` | BV-02 |
| 013 | [x] | `…::test_four_empty_rows_resolve_not_called` | BV-03 |
| 014 | [x] | `…::test_three_by_four_resolve_not_called` | BV-04 |
| 015 | [x] | `…::test_none_grid_resolve_call_count_zero` | BV-01 |
| 016 | [x] | `TestMessageExactMatch::test_dimension_failure_message_exact_match_prd[none]` | BV-01 |
| 017 | [x] | `…[empty_list]` | BV-02 |
| 018 | [x] | `…[four_empty_rows]` | BV-03 |
| 019 | [x] | `…[three_by_four]` | BV-04 |
| 020 | [x] | `…[two_by_two]` | BV-07 2×2 |
| 021 | [x] | `…::test_none_grid_message_no_extra_whitespace` | BV-01 |
| 022 | [x] | `…::test_none_grid_message_terminal_period_exact` | BV-01 |
| 023 | [x] | `…::test_none_grid_code_message_pair_consistency` | BV-01 |
| 024 | [x] | `…::test_empty_list_message_matches_prd_not_null_wording` | BV-02 / SP-03 |
| 025 | [x] | `TestScopeRestriction::test_scope_excludes_f1_valid_grid_literal` | 메타 |
| 026 | [x] | `…::test_scope_excludes_f2_valid_grid_literal` | 메타 |
| 027 | [x] | `…::test_scope_excludes_ac_fr_01_03_error_codes` | 메타 |
| 028 | [x] | `…::test_scope_excludes_ac_fr_01_04_error_codes` | 메타 |
| 029 | [x] | `…::test_scope_excludes_fr02_to_fr05_error_codes` | 메타 |

> BV-05(4×3), BV-06(5×5)는 본 파일 RED에 없음 — 후속 AC 또는 Report/09 U-IN-02와 통합 시 추가.

### GREEN 구현 묶음 (`src/magicsquare/boundary/`만)

| 단계 | 체크 | 통과 # | 최소 구현 |
|------|------|--------|-----------|
| **G1** | [x] | 001~005, 011, 015, 016, 021~023 | `None` → `FailureResult`; validator 실패 시 resolver 미호출 |
| **G2** | [x] | 006~010, 012~014, 017~019, 024 | `[]`, `[[]]*4`, 3×4 행·열 길이 검증 |
| **G3** | [x] | 020 | 2×2 등 행·열 ≠ 4 분기 |
| **G4** | [x] | (016~024 message) | 상수 1곳 — G1~G3와 동시 통과 가능 |
| **G5** | [x] | 025~029 | 구현 없음 (Scope 메타) |

**RED↔GREEN 1:1 커밋 예:** GREEN-1 ← RED-1, GREEN-2 ← RED-2, GREEN-3 ← RED-3 (message는 GREEN-4 생략 가능).

### 회귀 명령 (PowerShell)

```powershell
cd c:\DVV\MagicSquare_XX
python -m pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py -v
python -m pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py::TestFailureReturnOnNoneGrid -v
python -m pytest "tests/boundary/test_ac_fr_01_01_dimension_validation.py::TestMessageExactMatch::test_dimension_failure_message_exact_match_prd[two_by_two]" -v
```

### AC-FR-01-01 이후 — Dual-Track GREEN (Report/09)

- [ ] **A-1** `test_u_in_validation.py` — U-IN-04~08 (빈칸·값·중복)
- [ ] **A-2** `test_u_flow_execute_isolation.py` — U-FLOW-02
- [ ] **A-3** `test_u_out_contract.py` — U-OUT-01~03 (F1/F2 mock)
- [ ] **B-1** `test_d_loc.py` → **B-2** `test_d_mis.py` → **B-3** `test_d_val.py` → **B-4** `test_d_sol.py`
- [ ] OQ-09-01: `E003` vs `INVALID_SIZE` code SSOT 확정 후 U-IN-01~02 정합

### 커버리지·결함

- [x] [`docs/defect_list.md`](docs/defect_list.md) 생성 (DEF-001, DEF-002 Closed)
- [ ] Boundary validation **≥85%** (DEF-004 Open — 비리스트·jagged 미테스트)
- [ ] Domain Logic **≥95%** (Track B GREEN 후)
- [ ] 전체 TOTAL **≥90%**
- [ ] Open 결함 해소 후 회귀 (DEF-003, DEF-004, DEF-005, DEF-006)

---

## 다음 단계 (권장 순서)

1. **Report/16 Phase 0** — `pytest tests/` GREEN + G-03·G-04 ([Report/16](Report/16_MagicSquare_REFACTOR_Program_Phase0_Gate_And_Roadmap_Report.md))  
2. **Report/15 REFACTOR 3유형 To-Do** — 유형 3 → 1 → 2 ([§ REFACTOR 3유형](#refactor-3유형-요약-report15))  
3. **Report/15 Step A** — U-IN-04~08·U-FLOW·U-OUT-02/03 테스트 GREEN (REFACTOR 게이트)  
4. **Report/15 Step B** — P0 리팩터 (`InputValidator`, `ui_boundary`, `solve_partial` 중복 제거)  
5. OQ-09-01 code SSOT 확정 → 이중 Boundary API 정리 (P1)  
6. Track B **D-LOC~D-SOL** GREEN (F3 확정 후 D-SOL-03)  
7. INT F1/F2 E2E → File Repository 확장  

---

## 라이선스 / 기여

(미정 — 필요 시 추가)
