# Magic Square 4×4 — 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| **문서 ID** | `defect_list.md` |
| **기준** | [`docs/test_plan.md`](docs/test_plan.md), [`docs/PRD_MagicSquare.md`](docs/PRD_MagicSquare.md), AC-FR-01-01 RED/GREEN 사이클 |
| **최종 갱신** | 2026-05-29 |
| **회귀 기준** | `python -m pytest tests/ -v` |

## 요약

| 상태 | 건수 | 비고 |
|------|------|------|
| **Closed** | 2 | GREEN 최소 구현·메타 테스트 정합 |
| **Open** | 4 | Track B·커버리지·SSOT·문서 |
| **합계** | 6 | |

> **현재 회귀:** `pytest tests/` → **38 passed** (AC-FR-01-01 Boundary 29 + Domain 9).  
> Open 결함은 AC-FR-01-01 범위 밖이거나 후속 스프린트 항목이다.

---

## 결함 상세

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 | 상태 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|------|
| DEF-001 | Critical | AC-FR-01-01 | 1) `src/magicsquare/boundary` 미존재 상태에서 2) `pytest tests/boundary/` 실행 | 테스트 수집·실행 가능, `grid=None` 시 `FailureResult(code="INVALID_SIZE", message="Grid must be 4x4.")` | `ModuleNotFoundError: No module named 'magicsquare.boundary'` (conftest import 단계) | RED 단계에서 Boundary/Control 패키지·`MagicSquareBoundary` 미구현 | `boundary`·`control` 최소 패키지 추가, `BoundaryValidator` + `solve()` 조기 실패 반환 | **Closed** |
| DEF-002 | Major | AC-FR-01-01 | 1) Boundary 구현 후 2) `pytest tests/boundary/::TestScopeRestriction -v` | 소스에 F1/F2·AC-02~04 금지 패턴 없음 → 5건 PASS | `AssertionError`: `_F1_GRID_SNIPPET`·`ERR_BLANK_COUNT` 등이 테스트 모듈 소스에 그대로 존재 | 범위 제한 메타 테스트가 검사 대상 문자열을 상수·주석에 포함 (자기 모순) | 금지 리터럴을 런타임 조합(`"".join`, `"ERR_" + "BLANK_COUNT"`)으로 분리, 주석 문구 정리 | **Closed** |
| DEF-003 | Critical | FR-05 / AC-15~20 | 1) 유효 4×4·빈칸 2개 격자(F1 등) 준비 2) `MagicSquareBoundary().solve(grid)` 호출 (mock resolver 미사용) | `list[int]` 길이 6 (예: F1 → `[1,2,3,2,3,11]`) | `NotImplementedError: Domain solve not implemented yet.` (`SolveTwoBlankPuzzle.resolve`) | Control/Domain Track B 미구현, GREEN은 FR-01 구조 검증만 완료 | `SolveTwoBlankPuzzle` + Domain solver 연동, F1/F2 통합 RED(`tests/integration/`) | **Open** |
| DEF-004 | Medium | AC-FR-01-01 / SP-01~02 | 1) `pytest tests/ --cov=magicsquare.boundary.validation --cov-report=term-missing` 2) `grid="not a grid"`, `grid=123` 등 비리스트 입력은 AC-FR-01-01 테스트에 없음 | Boundary validation branch **≥85%** (NFR-02) | `boundary_validator.py` **83%** — L19·L24·L27 미실행 (`not isinstance` 분기) | AC-FR-01-01 RED가 `None`·`[]`·행열 불일치만 포함, 비리스트·jagged 미포함 | SP-01/02·SP-04용 Boundary 테스트 추가 또는 후속 AC-FR-01-01 확장 RED | **Open** |
| DEF-005 | Medium | AC-FR-01-01 | 1) `pytest tests/ --cov=magicsquare.boundary.ui --cov-report=term-missing` | `MagicSquareBoundary.solve` 성공 경로 커버 | `magic_square_boundary.py` L40 (`return self._resolver.resolve(grid)`) **미실행** | 유효 격자 호출 시나리오가 본 스프린트 범위 외 (DEF-003과 동일) | DEF-003 해결 시 F1 mock/통합 테스트로 L40 커버 | **Open** |
| DEF-006 | Low | AC-FR-01-01 / UX-01 | PRD §13 `ERR_INVALID_DIMENSION` vs RED SSOT `INVALID_SIZE` 대조 | 단일 오류 코드 SSOT (Report/02·PRD 정합) | QA RED는 `INVALID_SIZE`, PRD 표는 `ERR_INVALID_DIMENSION` (message는 동일) | Dual-Track RED 배치에서 QA 별칭 선적용, Report/02 재정합 전 | GREEN/REFACTOR에서 `ERR_*` ↔ `INVALID_SIZE` 매핑표 확정·문서 갱신 | **Open** |

---

## 재현 명령 (공통)

```powershell
cd c:\DVV\MagicSquare_XX
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# 전체 회귀
python -m pytest tests/ -v

# DEF-001 재현 (구현 제거 시 — 의도적 RED)
# → ModuleNotFoundError at tests/boundary/conftest.py

# DEF-003 재현 (유효 4×4, resolver 실구현)
python -c "from magicsquare.boundary.ui.magic_square_boundary import MagicSquareBoundary; g=[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]; MagicSquareBoundary().solve(g)"

# 커버리지 (DEF-004/005)
python -m pytest tests/ --cov=magicsquare --cov-report=term-missing --cov-report=html
```

---

## 추적성

| Defect ID | RED / UI ID | 테스트 파일 |
|-----------|-------------|-------------|
| DEF-001 | RED-BND-VAL-001, UI-P0-01 | `tests/boundary/test_ac_fr_01_01_dimension_validation.py` |
| DEF-002 | (메타) TestScopeRestriction | 동일 |
| DEF-003 | UI-P0-07, RED-INT-F1-001 (예정) | `tests/integration/` (미착수) |
| DEF-004 | SP-01, SP-02, SP-04 (test_plan §5) | 후속 RED |
| DEF-005 | FR-05 성공 경로 | 동일 |
| DEF-006 | UX-01 | `docs/test_plan.md` §2 |

---

## 변경 이력

| 날짜 | 변경 |
|------|------|
| 2026-05-29 | 초안 작성 — RED ImportError, Scope 메타 실패, Track B 미구현, cov 갭, SSOT 불일치 기록 |
