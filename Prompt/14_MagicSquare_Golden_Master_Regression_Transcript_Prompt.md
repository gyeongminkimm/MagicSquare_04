# 14 Magic Square Golden Master Regression Transcript Export

## 메타

| 항목 | 내용 |
|------|------|
| **목적** | Golden Master(Approval) 회귀 테스트 구축 세션의 프롬프트/응답 흐름 보관 |
| **범위** | baseline 생성 → approve 패턴 → GM-TC-01~05 → contracts → docs/README GM 체크리스트 → Report Export |
| **형식** | User / Assistant 순차 기록 (핵심 산출·판단 포함) |
| **대응 보고서** | [`Report/14_MagicSquare_Golden_Master_Regression_Report.md`](../Report/14_MagicSquare_Golden_Master_Regression_Report.md) |
| **SSOT** | [`docs/golden_master_approval_design.md`](../docs/golden_master_approval_design.md), [`Report/02`](../Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) F1/F2 |

---

## 대화형 Transcript

### Turn 1 — User

**[P]** 회귀 테스트(Approval/Golden Master) 설계 전문가.  
**[T]** Magic Square Solver 출력 기반 Golden Master 기준 파일 생성.

구현 요구사항:

1. 기준 출력 파일 생성 — 정상/reverse/invalid blank/duplicate/no valid solution
2. approve 패턴 — 없으면 생성, 있으면 diff 후 FAIL
3. 기준 파일 구조 `[normal_success]` Input/Output 또는 Error
4. **산출:** `tests/golden_master_expected.txt` + 생성 스크립트 + 설계 문서

### Turn 2 — Assistant

- `tests/golden_master/` harness 신규: `scenarios.py`, `capture.py`, `approval.py`
- `SuccessResponse` DTO 직렬화; 시맨틱 Error (`INVALID_BLANK_COUNT` 등)
- `scripts/generate_golden_master.py`, `docs/golden_master_approval_design.md`
- `tests/golden_master_expected.txt` 생성, `git add` 안내
- **판정:** normal_success 사용자 예시 grid → 실제 솔버 `[3,3,6,4,4,1]` (I-O2 reverse 경로) — baseline은 **실제 출력** SSOT

---

### Turn 3 — User

**[T]** Golden Master **테스트 코드** 작성.

- stdout 또는 API serialization
- `open(expected).read()` vs actual, approve 패턴
- `@pytest.mark.golden_master`, `pytest -m golden_master -v`
- 실패 시 `--- expected` / `+++ actual` unified diff
- GM-TC-01~05: 정상/reverse/INVALID_BLANK_COUNT/DUPLICATE_NUMBER/**NO_VALID_MAGIC_SQUARE**
- 계약: int[6], row-major, 1-index, small-first, reverse fallback, Error Contract

### Turn 4 — Assistant

| 산출 | 경로 |
|------|------|
| 테스트 | `tests/golden_master/test_golden_master_magic_square.py` |
| 계약 assert | `tests/golden_master/contracts.py` |
| 마커 | `pyproject.toml` `markers.golden_master` |
| baseline | F1→`[1,2,3,2,3,11]`, F2→`[2,2,10,3,3,7]` (Report/02 SSOT) |

- GM-TC-01: GRID_G2 (F1) small-first
- GM-TC-05: `NO_VALID_MAGIC_SQUARE` (이전 `NO_VALID_SOLUTION`에서 rename)
- `approve_scenario_block` + `normalize_block` (trailing newline 정합)
- **6 passed** (`pytest -m golden_master -v`)
- 구 `tests/test_golden_master.py` 삭제 → 패키지 내 테스트로 이동

---

### Turn 5 — User

**@docs/README.md** — `## RED 단계 To-Do 리스트` 아래 Golden Master 회귀 안전장치 섹션 추가.

- GM-01~10 체크리스트 (기준 파일 / 테스트 / 회귀 보호)

### Turn 6 — Assistant

- `docs/README.md` **신규** (기존 부재) — 문서 인덱스 + RED To-Do + GM-01~10 `[x]`
- 루트 `README.md` — `docs/README.md`, `golden_master_approval_design.md` 링크

---

### Turn 7 — User

**Report 폴더에 보고서 생성, Prompting 폴더에 Transcript Export.**

### Turn 8 — Assistant (현재 작업)

- Report `01`~`13` 존재 → **`14`** 할당
- [`Report/14_MagicSquare_Golden_Master_Regression_Report.md`](../Report/14_MagicSquare_Golden_Master_Regression_Report.md)
- [`Prompt/14_MagicSquare_Golden_Master_Regression_Transcript_Prompt.md`](14_MagicSquare_Golden_Master_Regression_Transcript_Prompt.md) (본 파일)

> **경로:** 레포 convention은 `Prompt/` (Prompting 아님).

---

## 실행 명령·점검 요약

| 점검 | 결과 |
|------|------|
| Report 번호 | `01`~`13` → **`14`** |
| Transcript SSOT | **`Prompt/14_*`** |
| Golden Master | `pytest -m golden_master -v` → **6 passed** |
| Baseline | `tests/golden_master_expected.txt` (5 sections) |
| Approve | `GOLDEN_MASTER_APPROVE=1` 또는 `generate_golden_master.py --approve` |

### 재현 명령 (PowerShell)

```powershell
cd c:\DVV\MagicSquare_XX
python -m pytest -m golden_master -v
python scripts/generate_golden_master.py
python -m pytest tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_01_normal_combination_success -v
```

### 실행 결과 예시

```text
collected 92 items / 86 deselected / 6 selected

tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_01_normal_combination_success PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_02_reverse_combination_success PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_03_invalid_blank_count PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_04_duplicate_number PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_05_no_valid_magic_square PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_full_baseline_file_matches PASSED

6 passed, 86 deselected
```

### diff 실패 예시 (approve 없이 drift 시)

```text
AssertionError: [GoldenMaster] normal_success mismatch - re-run with GOLDEN_MASTER_APPROVE=1 to update baseline.
--- expected
+++ actual
@@ -6,4 +6,3 @@
 4 15 14 1
 Output:
 [1, 2, 3, 2, 3, 11]
-
```

---

## 세션 산출물 인덱스

| Phase | 산출물 | 저장 위치 |
|-------|--------|-----------|
| Baseline | `golden_master_expected.txt` | `tests/` |
| Harness | capture, approval, contracts, scenarios | `tests/golden_master/` |
| Tests | GM-TC-01~05 + aggregate | `test_golden_master_magic_square.py` |
| CLI | `generate_golden_master.py` | `scripts/` |
| Design | Approve 패턴 SSOT | `docs/golden_master_approval_design.md` |
| Checklist | GM-01~10 | `docs/README.md` |
| Report 14 + Prompt 14 | 본 Export | Turn 8 |

---

## 식별자 부록

| 구분 | 값 |
|------|-----|
| GM-TC-01 grid (F1) | `[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]` |
| GM-TC-01 Output | `[1, 2, 3, 2, 3, 11]` |
| GM-TC-02 grid (F2) | `[[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]` |
| GM-TC-02 Output | `[2, 2, 10, 3, 3, 7]` |
| Error tokens | `INVALID_BLANK_COUNT`, `DUPLICATE_NUMBER`, `NO_VALID_MAGIC_SQUARE` |
| pytest marker | `golden_master` |
| env approve | `GOLDEN_MASTER_APPROVE=1` |

---

## 비고

- Golden harness `_validate_content()`는 U-IN-04~08 GREEN 전 interim; GREEN 후 `InputValidator` 위임 권장 (Report/14 §9 P1).
- F3(G3) 확정 시 GM-TC-05 격자만 갱신 + `--approve`.
- 다음 백업 시 Report/Prompt 번호 **`15`** 사용.
