# Magic Square 4×4 — AC-FR-01-01 TDD 체크리스트·README 통합 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `12_MagicSquare_AC_FR_01_01_TDD_Checklist_Report` |
| **전제 보고서** | [`08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md`](08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md), [`11_MagicSquare_AC_FR_01_01_GREEN_Verification_Report.md`](11_MagicSquare_AC_FR_01_01_GREEN_Verification_Report.md), [`09_MagicSquare_Full_DualTrack_RED_Design_Report.md`](09_MagicSquare_Full_DualTrack_RED_Design_Report.md) |
| **기준 SSOT** | [`docs/test_plan.md`](../docs/test_plan.md), [`tests/boundary/test_ac_fr_01_01_dimension_validation.py`](../tests/boundary/test_ac_fr_01_01_dimension_validation.py), [`README.md`](../README.md) |
| **작성일** | 2026-05-29 |
| **상태** | **체크리스트·README 반영 완료** — 테스트/프로덕션 로직 변경 없음 |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [산출물 목록](#2-산출물-목록)
3. [RED 커밋 묶음 (5 commits)](#3-red-커밋-묶음-5-commits)
4. [테스트 케이스 오름차순 (#001~029)](#4-테스트-케이스-오름차순-001029)
5. [GREEN 구현 묶음 (G1~G5)](#5-green-구현-묶음-g1g5)
6. [Dual-Track 후속 체크리스트](#6-dual-track-후속-체크리스트)
7. [Report/08·11과의 관계](#7-report0811과의-관계)

---

## 1. 세션 요약

| Phase | 사용자 요청 | 결과 |
|-------|-------------|------|
| 1 | TDD GREEN용 테스트 케이스 **오름차순** 정리 + RED 몇 개씩 묶어 커밋 가이드 | pytest 수집 순 #001~029, RED-1~5 / GREEN G1~G5 매핑표 작성 |
| 2 | 위 내용을 **체크리스트** 형식으로 README 반영 | [`README.md`](../README.md) §「TDD 체크리스트 — AC-FR-01-01」신설·프로젝트 상태 갱신 |
| 3 | Report·Prompt Transcript Export | 본 문서, [`Prompt/12_*`](../Prompt/12_MagicSquare_AC_FR_01_01_TDD_Checklist_Transcript_Prompt.md) |

**TDD phase:** 문서·운영 가이드만 — **RED/GREEN/REFACTOR 코드 변경 없음**.

**전제:** Report/11 기준 AC-FR-01-01 **29/29 이미 GREEN**. 체크리스트는 회귀·히스토리 분리·후속 Dual-Track용.

---

## 2. 산출물 목록

| 유형 | 경로 | 비고 |
|------|------|------|
| 운영 체크리스트 (SSOT for humans) | [`README.md`](../README.md) § TDD 체크리스트 | RED-1~5, #001~029, G1~G5, Report/09 후속 |
| 테스트 (변경 없음) | `tests/boundary/test_ac_fr_01_01_dimension_validation.py` | 29 collected |
| 세션 보고서 | `Report/12_MagicSquare_AC_FR_01_01_TDD_Checklist_Report.md` | 본 문서 |
| Transcript | [`Prompt/12_MagicSquare_AC_FR_01_01_TDD_Checklist_Transcript_Prompt.md`](../Prompt/12_MagicSquare_AC_FR_01_01_TDD_Checklist_Transcript_Prompt.md) | 대화형 Export |

**본 세션에서 변경한 파일:** `README.md`, `Report/12_*`, `Prompt/12_*` only.

---

## 3. RED 커밋 묶음 (5 commits)

`src/` 수정 **금지**. 각 커밋 후 해당 클래스만 `pytest` → FAIL 또는 ImportError 확인.

| ID | 포함 | 노드 # | 커밋 메시지 예 |
|----|------|--------|----------------|
| **RED-1** | `conftest.py` + `TestFailureReturnOnNoneGrid` | 001~005 | `test(boundary): RED AC-FR-01-01 None grid failure contract` |
| **RED-2** | `TestBoundaryDimensionValues` | 006~010 | `test(boundary): RED AC-FR-01-01 dimension BV-02~04` |
| **RED-3** | `TestDomainResolverIsolation` | 011~015 | `test(boundary): RED AC-FR-01-01 resolve isolation` |
| **RED-4** | `TestMessageExactMatch` (9 nodes) | 016~024 | `test(boundary): RED AC-FR-01-01 message UX-01` |
| **RED-5** | `TestScopeRestriction` | 025~029 | `test(boundary): RED AC-FR-01-01 scope gate` |

`test_plan` P0 매핑: RED-1 ≈ `RED-BND-VAL-001` / `UI-P0-01`; RED-2 ≈ `RED-BND-VAL-004` / `UI-P0-02`; RED-4 ≈ `UI-X-01`.

---

## 4. 테스트 케이스 오름차순 (#001~029)

정렬 기준: **pytest `--collect-only` 파일 정의 순** (= `test_ac_fr_01_01_dimension_validation.py` 선언 순).

| # | 클래스 / 테스트 (요약) | BV·입력 |
|---|------------------------|---------|
| 001~005 | `TestFailureReturnOnNoneGrid` (5) | BV-01 `None` |
| 006~010 | `TestBoundaryDimensionValues` (5) | BV-02 `[]`, BV-03 `[[]]*4`, BV-04 `GRID_3X4` |
| 011~015 | `TestDomainResolverIsolation` (5) | BV-01~04 + `call_count==0` |
| 016~020 | `TestMessageExactMatch` parametrize + 2×2 | BV-01~04, BV-07 |
| 021~024 | `TestMessageExactMatch` (4) | whitespace, period, pair, null wording |
| 025~029 | `TestScopeRestriction` (5) | 메타 (F1/F2·AC-02~05 소스 게이트) |

**미포함 (test_plan BV-05·06):** 4×3, 5×5 — 본 RED 파일에 없음. Report/09 `U-IN-02` 또는 후속 AC에서 추가.

전체 pytest 노드 ID 목록: README 체크리스트 표 또는 Prompt/12 §부록.

---

## 5. GREEN 구현 묶음 (G1~G5)

수정 허용: `src/magicsquare/boundary/` (`BoundaryValidator`, `MagicSquareBoundary`, `FailureResult`).

| 단계 | 통과 # | 최소 구현 |
|------|--------|-----------|
| **G1** | 001~005, 011, 015, 016, 021~023 | `grid is None` → `FailureResult(INVALID_SIZE, …)`; 실패 시 `resolve()` 미호출 |
| **G2** | 006~010, 012~014, 017~019, 024 | `[]`, `[[]]*4`, 3×4 행·열 길이 |
| **G3** | 020 | 2×2 등 행·열 ≠ 4 |
| **G4** | (016~024 message) | 상수 단일 SSOT — G1~G3와 동시 통과 가능 (별도 커밋 생략 가능) |
| **G5** | 025~029 | **`src/` 변경 없음** |

**RED↔GREEN 1:1:** GREEN-1←RED-1, GREEN-2←RED-2, GREEN-3←RED-3.

### 회귀 명령 (PowerShell)

```powershell
cd c:\DVV\MagicSquare_XX
python -m pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py -v
python -m pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py::TestFailureReturnOnNoneGrid -v
python -m pytest "tests/boundary/test_ac_fr_01_01_dimension_validation.py::TestMessageExactMatch::test_dimension_failure_message_exact_match_prd[two_by_two]" -v
```

**현재 회귀:** 29 passed (Report/11과 동일).

---

## 6. Dual-Track 후속 체크리스트

README에 미완 `[ ]`로 기록. 권장 GREEN 순서:

| 순서 | ID | 파일 / 범위 |
|------|-----|-------------|
| 1 | A-1 | `test_u_in_validation.py` — U-IN-04~08 |
| 2 | A-2 | `test_u_flow_execute_isolation.py` — U-FLOW-02 |
| 3 | A-3 | `test_u_out_contract.py` — U-OUT-01~03 |
| 4 | B-1~4 | `test_d_loc` → `test_d_mis` → `test_d_val` → `test_d_sol` |
| 선행 | OQ-09-01 | `E003` vs `INVALID_SIZE` SSOT (Report/09) |

---

## 7. Report/08·11과의 관계

| 구분 | Report/08 | Report/11 | Report/12 (본 세션) |
|------|-----------|-----------|---------------------|
| 목적 | RED 작성·최초 GREEN | GREEN 회귀 검증 | **커밋·케이스 순서 운영 가이드** |
| 테스트 변경 | 29건 작성 | 없음 | 없음 |
| `src/` 변경 | 최초 Boundary | 없음 | 없음 |
| README | defect_list 링크 등 | — | **TDD 체크리스트 SSOT** |
| Prompt | 08 | 11 | **12** |

---

## 변경 이력

| 날짜 | 변경 |
|------|------|
| 2026-05-29 | 초안 — AC-FR-01-01 TDD 체크리스트 정리·README 통합·Transcript Export |
