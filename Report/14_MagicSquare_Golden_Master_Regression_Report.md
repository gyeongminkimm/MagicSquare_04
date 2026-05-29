# Magic Square 4×4 — Golden Master 회귀 테스트 세션 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `14_MagicSquare_Golden_Master_Regression_Report` |
| **전제 보고서** | [`13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Report.md`](13_MagicSquare_DualTrack_GREEN_And_PyQt_Screen_Report.md), [`02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
| **기준 SSOT** | [`docs/golden_master_approval_design.md`](../docs/golden_master_approval_design.md), [`Report/02`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) F1/F2·I-O2, [`docs/README.md`](../docs/README.md) GM-01~10 |
| **작성일** | 2026-05-29 |
| **상태** | **Golden Master 회귀 안전장치 구축 완료** — GM-TC-01~05 **6/6 PASS** |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [산출물 목록](#2-산출물-목록)
3. [Golden Master 설계](#3-golden-master-설계)
4. [테스트 케이스 (GM-TC-01~05)](#4-테스트-케이스-gm-tc-0105)
5. [Approve 패턴](#5-approve-패턴)
6. [계약 검증 (contracts)](#6-계약-검증-contracts)
7. [pytest·회귀](#7-pytest회귀)
8. [문서·체크리스트](#8-문서체크리스트)
9. [미완·후속](#9-미완후속)
10. [Transcript](#10-transcript)

---

## 1. 세션 요약

| Phase | 사용자 요청 | 결과 |
|-------|-------------|------|
| 1 | Golden Master 기준 파일·생성 스크립트·approve 설계 | `golden_master_expected.txt`, `scripts/generate_golden_master.py`, `docs/golden_master_approval_design.md` |
| 2 | GM-TC-01~05 테스트 코드·`@pytest.mark.golden_master` | `tests/golden_master/test_golden_master_magic_square.py` — **6 passed** |
| 3 | `docs/README.md` GM-01~10 체크리스트 | RED To-Do 하위 Golden Master 섹션 추가 |
| 4 | Report·Prompt Export | 본 문서, [`Prompt/14_*`](../Prompt/14_MagicSquare_Golden_Master_Regression_Transcript_Prompt.md) |

**목적:** Refactoring 시작 전·GREEN 완료 직후 **출력 회귀**를 Approval/Golden Master 패턴으로 고정. `src/` 변경 없이 `tests/` 전용 harness.

---

## 2. 산출물 목록

### 2.1 기준 파일 (버전 관리 필수)

| 파일 | 역할 |
|------|------|
| [`tests/golden_master_expected.txt`](../tests/golden_master_expected.txt) | 5 시나리오 baseline — `git add` 대상 |

### 2.2 Golden Master harness (`tests/golden_master/`)

| 파일 | 역할 |
|------|------|
| `scenarios.py` | GM-TC-01~05 격자·키 정의 (F1/F2 + FR-01 오류) |
| `capture.py` | `SuccessResponse` API 직렬화 → 섹션 텍스트 |
| `approval.py` | approve 패턴 — 없으면 생성, 있으면 `--- expected` / `+++ actual` diff |
| `contracts.py` | int[6]·row-major·1-index·small-first·reverse·Error Contract assert |
| `conftest.py` | `golden_master` 마커·fixture |
| `test_golden_master_magic_square.py` | GM-TC-01~05 + full-file aggregate |

### 2.3 스크립트·설정

| 파일 | 역할 |
|------|------|
| [`scripts/generate_golden_master.py`](../scripts/generate_golden_master.py) | CLI baseline 생성·`--approve` |
| [`pyproject.toml`](../pyproject.toml) | `markers = ["golden_master: …"]` |

### 2.4 문서

| 파일 | 역할 |
|------|------|
| [`docs/golden_master_approval_design.md`](../docs/golden_master_approval_design.md) | Approve 패턴 설계 SSOT |
| [`docs/README.md`](../docs/README.md) | GM-01~10 체크리스트 |

---

## 3. Golden Master 설계

### 3.1 캡처 전략

- **Primary:** `SuccessResponse` / 시맨틱 `Error:` 토큰 직렬화 (stdout 아님)
- **경로:** `SolvePartialMagicSquare.resolve()` (성공) + harness `_validate_content()` (FR-01 오류, U-IN GREEN 전 interim)

### 3.2 기준 파일 형식

```text
[normal_success]
Input:
16 0 2 13
...
Output:
[1, 2, 3, 2, 3, 11]

________________________________________

[reverse_success]
...
```

섹션 구분: `________________________________________` (LF, UTF-8).

### 3.3 시맨틱 Error 토큰

| Boundary / Domain | Golden `Error:` |
|-------------------|-----------------|
| `E002` (blank count) | `INVALID_BLANK_COUNT` |
| `E005` (duplicate) | `DUPLICATE_NUMBER` |
| `UnsolvableDomainError` | `NO_VALID_MAGIC_SQUARE` |

---

## 4. 테스트 케이스 (GM-TC-01~05)

| ID | 섹션 키 | 시나리오 | 기대 |
|----|---------|----------|------|
| **GM-TC-01** | `normal_success` | F1 / TD-01 (GRID_G2) small-first | `[1, 2, 3, 2, 3, 11]` |
| **GM-TC-02** | `reverse_success` | F2 / TD-02 (GRID_G1) reverse fallback | `[2, 2, 10, 3, 3, 7]` |
| **GM-TC-03** | `invalid_blank_count` | 빈칸 3개 (U-IN-05) | `INVALID_BLANK_COUNT` |
| **GM-TC-04** | `duplicate_number` | 비0 중복 (U-IN-08) | `DUPLICATE_NUMBER` |
| **GM-TC-05** | `no_valid_magic_square` | 양쪽 조합 실패 (F3 stand-in) | `NO_VALID_MAGIC_SQUARE` |
| — | *(aggregate)* | `open(expected).read()` vs `render_golden_master()` | 전체 파일 일치 |

**마킹:** `@pytest.mark.golden_master` — `pytest -m golden_master -v`

---

## 5. Approve 패턴

| 조건 | 동작 |
|------|------|
| `golden_master_expected.txt` **없음** | 현재 캡처로 **자동 생성**, PASS |
| 기준 **있음**, 출력 **일치** | PASS |
| 기준 **있음**, 출력 **불일치** | unified diff (`--- expected` / `+++ actual`) 후 **FAIL** |
| `GOLDEN_MASTER_APPROVE=1` 또는 `--approve` | baseline **덮어쓰기** |

```powershell
# 회귀
python -m pytest -m golden_master -v

# 기준 갱신 (의도적 계약 변경 후)
$env:GOLDEN_MASTER_APPROVE = "1"
python -m pytest -m golden_master -v
python scripts/generate_golden_master.py --approve
git add tests/golden_master_expected.txt
```

---

## 6. 계약 검증 (contracts)

| GM ID | 검증 함수 | 규칙 |
|-------|-----------|------|
| GM-07 | `assert_row_major_blank_order` | FR-02 row-major 빈칸 스캔 순서 |
| GM-08 | `assert_int_six_format` | int[6], 좌표 1-index ∈ [1,4] |
| GM-09 | `assert_small_first_combination` / `assert_reverse_fallback_combination` | I-O2 min→첫 / reverse fallback |
| GM-10 | `assert_error_contract` | 시맨틱 Error 토큰 일치 |

**ECB:** harness는 `tests/` 전용 — Entity 실제 호출(Mock 금지), Boundary `src/` 미수정.

---

## 7. pytest·회귀

### 7.1 Golden Master (본 세션)

```powershell
cd c:\DVV\MagicSquare_XX
python -m pytest -m golden_master -v
```

**결과 (2026-05-29):** `6 passed, 86 deselected`

| 테스트 | 결과 |
|--------|------|
| `test_gm_tc_01_normal_combination_success` | PASS |
| `test_gm_tc_02_reverse_combination_success` | PASS |
| `test_gm_tc_03_invalid_blank_count` | PASS |
| `test_gm_tc_04_duplicate_number` | PASS |
| `test_gm_tc_05_no_valid_magic_square` | PASS |
| `test_gm_full_baseline_file_matches` | PASS |

### 7.2 기존 Dual-Track 회귀 (권장 병행)

```powershell
python -m pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py -q
python -m pytest tests/control/test_solve_partial_magic_square.py -q
```

---

## 8. 문서·체크리스트

[`docs/README.md`](../docs/README.md) §RED 단계 To-Do — Golden Master 회귀 안전장치:

| ID | 항목 | 상태 |
|----|------|------|
| GM-01 | `golden_master_expected.txt` 생성 | [x] |
| GM-02 | 정상/역순/오류 시나리오 | [x] |
| GM-03 | `git add tests/golden_master_expected.txt` | [x] |
| GM-04 | `test_golden_master_magic_square` | [x] |
| GM-05 | approve 패턴 | [x] |
| GM-06 | Golden Master PASS | [x] |
| GM-07 | row-major 보호 | [x] |
| GM-08 | 1-index 보호 | [x] |
| GM-09 | reverse fallback 보호 | [x] |
| GM-10 | Error Contract 보호 | [x] |

루트 [`README.md`](../README.md) 문서 섹션에 `docs/README.md`·`golden_master_approval_design.md` 링크 추가.

---

## 9. 미완·후속

| 우선순위 | 항목 |
|----------|------|
| P1 | U-IN-04~08 GREEN 후 `capture._validate_content` → `InputValidator.validate()` 위임 |
| P2 | F3(G3) SSOT 확정 → `GRID_NO_VALID_MAGIC_SQUARE` 갱신 + `--approve` |
| P3 | UIBoundary E2E Golden Master 확장 (optional — 현재 Control+DTO 경로) |
| P4 | CI에 `pytest -m golden_master` 추가 |

**다음 Report/Prompt 번호:** `15`

---

## 10. Transcript

대화형 Export: [`Prompt/14_MagicSquare_Golden_Master_Regression_Transcript_Prompt.md`](../Prompt/14_MagicSquare_Golden_Master_Regression_Transcript_Prompt.md)
