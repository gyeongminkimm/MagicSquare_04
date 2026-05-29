# 08 Magic Square AC-FR-01-01 테스트·QA Transcript Export

## 메타

| 항목 | 내용 |
|------|------|
| **목적** | FR-01 구조 검증(AC-FR-01-01) 테스트 계획·RED·GREEN·결함·커버리지 세션의 프롬프트/응답 흐름 보관 |
| **범위** | 앵커 샘플 선택 → test_plan → RED 테스트 → 실행 가이드 → defect_list → Report/Prompting Export |
| **형식** | User / Assistant 순차 기록 (핵심 산출·판단 포함) |
| **대응 보고서** | [`Report/08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md`](../Report/08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md) |
| **SSOT** | [`docs/test_plan.md`](../docs/test_plan.md), [`docs/PRD_MagicSquare.md`](../docs/PRD_MagicSquare.md), [`defect_list.md`](../defect_list.md) |

---

## 대화형 Transcript

### Turn 1 — User

**테스트 플랜 앵커 샘플 선택** (코드 작성 금지, 문서만).

- 기준: FR-01 선행 입력 검증, `grid=None` → `INVALID_SIZE`, Boundary+Domain 격리
- 산출: AC ID, PRD 번호, 입출력 예, 선택 이유 2줄

### Turn 2 — Assistant

**AC-FR-01-01** 선택 문서 출력.

- `grid=None` → `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }`
- PRD FR-01 · AC-01 · AC-05 · §12.1 · §13
- QA `INVALID_SIZE` vs PRD `ERR_INVALID_DIMENSION` (message 동일) 정합 표기

---

### Turn 3 — User

**시니어 QA — `test_plan.md` 작성** (pytest, 경계값, mock/spy, cov 95/85, pytest-cov 명령).

### Turn 4 — Assistant

[`docs/test_plan.md`](../docs/test_plan.md) 저장.

- BV-01~07 (`None`, `[]`, `[[]]*4`, 3×4, 4×3, 5×5; F1/F2 제외)
- 25건 RED 클래스 구조, Domain `resolve()` 0회 전략
- `pytest --cov=src --cov-report=term-missing`

---

### Turn 5 — User

**README에 RED 단계 To-Do 리스트** 삽입 (기존 내용 유지).

### Turn 6 — Assistant

`README.md`에 Track A/B, 커버리지, 결함 연결 체크리스트 추가.

---

### Turn 7 — User

**AC-FR-01-01 RED 테스트** 작성 (타입별 ≥5, GWT, AC 주석, RED 실패 상태).

### Turn 8 — Assistant

`tests/boundary/` 생성.

- `test_ac_fr_01_01_dimension_validation.py` (29 tests)
- `conftest.py` — mock `SolveTwoBlankPuzzle`, `INVALID_SIZE_*`
- `src` 미구현 → **ImportError RED** (의도)

---

### Turn 9 — User

**가상환경 기준** 테스트 실행 방법 안내 요청.

### Turn 10 — Assistant

venv 생성·`pip install -e ".[dev]"`·`pytest tests/boundary/ -v` 가이드. RED 시 `ModuleNotFoundError` 정상 설명.

---

### Turn 11 — User

**ImportError** (`magicsquare.boundary`) — 고쳐줘.

### Turn 12 — Assistant

GREEN 최소 구현 추가.

- `boundary/`: `FailureResult`, `BoundaryValidator`, `MagicSquareBoundary`
- `control/`: `SolveTwoBlankPuzzle.resolve` stub
- **29 passed**; Scope 메타 테스트 문자열 분리 수정

---

### Turn 13 — User

테스트 실패가 RED로 **정상**이었음 — **수정 전으로 되돌려줘**.

### Turn 14 — Assistant

`src/boundary`, `src/control` 삭제, `pyproject` dependencies 복구, Scope 테스트 원복 → **ImportError RED** 복귀.

---

### Turn 15 — User

**커버리지 HTML** 생성 요청.

### Turn 16 — Assistant

Boundary 재구현 + `pytest --cov=magicsquare --cov-report=html` → `htmlcov/`. `pyproject` `[tool.coverage.html]` 설정. 38 passed, TOTAL 94%.

---

### Turn 17 — User

**`defect_list.md`** 작성 + README 결함 체크박스 업데이트.

### Turn 18 — Assistant

[`defect_list.md`](../defect_list.md) — DEF-001~006 (Closed 2 / Open 4). README: defect_list [x], 전체 수정 [ ].

---

### Turn 19 — User

**Report** 보고서 생성, **Prompting** Transcript Export.

### Turn 20 — Assistant (현재 작업)

Report 최대 번호 `07` → **`08`** 할당:

- `Report/08_MagicSquare_AC_FR_01_01_Testing_And_QA_Report.md`
- `Prompting/08_MagicSquare_AC_FR_01_01_Testing_Transcript_Prompt.md` (본 파일)

---

## 실행 명령·점검 요약

| 점검 | 결과 |
|------|------|
| Report 번호 | `01`~`07` 존재 → **`08`** 할당 |
| Prompting | `07` 참조 패턴 → **`08`** 신규 |
| 회귀 (최종) | `pytest tests/` → 38 passed |
| Open 결함 | DEF-003, 004, 005, 006 |

---

## 세션 산출물 인덱스

| Phase | 산출물 | 저장 위치 |
|-------|--------|-----------|
| 1 | 앵커 샘플 선택 | 채팅 (Report 08 §3) |
| 2 | 테스트 계획 | `docs/test_plan.md` |
| 3 | README RED To-Do | `README.md` |
| 4 | Boundary RED 테스트 | `tests/boundary/` |
| 5 | 실행·HTML cov 가이드 | 채팅 + `htmlcov/` |
| 6 | 결함 목록 | `defect_list.md` |
| 7 | Report 08 + Prompting 08 | Turn 20 |

---

## 식별자 부록 (AC-FR-01-01)

| 구분 | ID / 상수 |
|------|-----------|
| QA AC | AC-FR-01-01 |
| PRD AC | AC-01, AC-05 |
| RED code | `INVALID_SIZE` |
| Message | `Grid must be 4x4.` |
| 테스트 파일 | `test_ac_fr_01_01_dimension_validation.py` |
| 결함 | DEF-001 ~ DEF-006 |

---

## 비고

- 본 transcript는 세션 핵심 요청·응답·TDD RED/GREEN 전환을 대화형으로 정리한 export 기록이다.
- 테스트·계획 SSOT는 `docs/test_plan.md`; 결함 SSOT는 `defect_list.md`.
- 다음 백업 시 Report/Prompting 번호 **`09`** 사용.
