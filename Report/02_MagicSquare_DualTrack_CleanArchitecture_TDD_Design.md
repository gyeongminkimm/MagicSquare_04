# Magic Square 4×4 — Dual-Track UI + Logic TDD / Clean Architecture 설계

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design` |
| **전제 보고서** | [`01_MagicSquare_ProblemDefinition_Report.md`](01_MagicSquare_ProblemDefinition_Report.md) |
| **작성일** | 2026-05-28 |
| **상태** | 구현·테스트 코드 미포함 (설계·계약·테스트·통합 계획만) |

---

## 전제 요약

- **목적:** 알고리즘 난이도보다 **레이어 분리 + 계약 기반 테스트 + 리팩토링** 훈련.
- **1순위 시나리오:** 2칸 퍼즐 완성 (입력 검증 → 누락 수 채움 → `int[6]` 반환).
- **검증 정책:** 행 4 + 열 4 + 대각선 2, 마법합 **34** (01 보고서 I-5~I-7).
- **빈칸 순서:** 행 우선 스캔 `(1,1)→(1,4)→…→(4,4)`에서 `0` 발견 순서 = 첫·둘째 빈칸.

### 외부 입출력 계약 (고정)

| 구분 | 규칙 |
|------|------|
| **입력** | `int[4][4]`, `0`=빈칸, 빈칸 **정확히 2개**, 값 ∈ {0}∪[1,16], 비0 중복 금지 |
| **출력** | `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index** |
| **출력 순서** | 누락 두 수 `min<max`. `(min→첫 빈칸, max→둘째 빈칸)` 완성 격자가 마방진이면 `(n1,n2)=(min,max)`, 아니면 `(max,min)` |

### 검증된 테스트 픽스처

| ID | 격자 (0=blank) | 기대 `int[6]` | 비고 |
|----|----------------|---------------|------|
| **F1** | `[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]` | `[1,2,3,2,3,11]` | min→첫 유효 |
| **F2** | `[[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]` | `[2,2,10,3,3,7]` | 반대 배치만 유효 (n1>n2) |
| **F3** | 구현 전 수동 구성 | — | `UNSOLVABLE_PUZZLE`용 (INT-E-02) |

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

| 종류 | 이름 | 책임 (SRP) | 금지 |
|------|------|------------|------|
| **Entity** | `PuzzleGrid` | 4×4 상태; 0/1~16 규칙; I-11·I-12 검사 지원 | UI·파일 I/O |
| **Value Object** | `CellPosition` | 1-index `(row,col)`, 경계 1~4 | 합 계산 |
| **Value Object** | `MagicConstant` | 정책상 **34** 단일 값 | n×n 일반화 |
| **Value Object** | `LineSum` | 한 선 4칸 합 | 판정 정책 변경 |
| **Value Object** | `MissingPair` | 누락 두 수 `(min,max)` | 좌표 할당 |
| **Value Object** | `FillAssignment` | `(pos1→n1, pos2→n2)` 후보 | 영속화 |
| **Value Object** | `SolutionVector` | `[r1,c1,n1,r2,c2,n2]`; 순서 규칙 캡슐화 | 에러 문구 |
| **Domain Service** | `EmptyCellLocator` | 빈칸 2개를 스캔 순서로 반환 | 입력 스키마(크기) |
| **Domain Service** | `MissingNumberResolver` | {1..16}\\비0 → 2수 | 마방진 판정 |
| **Domain Service** | `MagicSquareValidator` | 완성 격자 I-5~I-7·I-2~I-3 | 0 허용 판정 |
| **Domain Service** | `TwoBlankPuzzleSolver` | 두 배치 시도 → 출력 순서 → `SolutionVector` | 저장/로드 |

**Application (선택)**

| 이름 | 책임 |
|------|------|
| `SolveTwoBlankPuzzle` | Domain 호출 순서 고정; 실패는 도메인 코드만 (문구는 UI) |

## 1.2 도메인 불변조건(Invariants)

| ID | 불변조건 | 검증 시점 | 실패 코드 |
|----|----------|-----------|-----------|
| **I-1** | 격자 4×4 | `PuzzleGrid` | `INVALID_DIMENSION` |
| **I-2** | 완성 시 값 집합 = {1..16} | Validator | `NOT_MAGIC_SQUARE` |
| **I-3** | 완성 시 비0 중복 없음 | `PuzzleGrid`/Validator | `DUPLICATE_VALUE` |
| **I-4** | 마법합 = 34 | Validator | `NOT_MAGIC_SQUARE` |
| **I-5** | 4행 합 각 34 | Validator | `NOT_MAGIC_SQUARE` |
| **I-6** | 4열 합 각 34 | Validator | `NOT_MAGIC_SQUARE` |
| **I-7** | 2대각선 합 각 34 | Validator | `NOT_MAGIC_SQUARE` |
| **I-8** | 동일 완성 격자 → 동일 판정 | Validator | — |
| **I-11** | 빈칸 = 0만 | `PuzzleGrid` | `INVALID_CELL_VALUE` |
| **I-12** | 비0 ∈ [1,16], 비0 중복 없음 | `PuzzleGrid` | `INVALID_CELL_VALUE` / `DUPLICATE_VALUE` |
| **I-P1** | 빈칸 정확히 2개 | `EmptyCellLocator` | `BLANK_COUNT_NOT_TWO` |
| **I-P2** | 누락 수 정확히 2개 | `MissingNumberResolver` | `MISSING_COUNT_NOT_TWO` |
| **I-O1** | n1→첫 빈칸, n2→둘째 빈칸 | `TwoBlankPuzzleSolver` | — |
| **I-O2** | min→첫 유효 시 (n1,n2)=(min,max), else (max,min) | `TwoBlankPuzzleSolver` | `UNSOLVABLE_PUZZLE` |

**관심 선 (1-index)**

| 선 | 칸 |
|----|-----|
| R1~R4 | 행 i, 열 1~4 |
| C1~C4 | 열 j, 행 1~4 |
| D1 | (1,1)(2,2)(3,3)(4,4) |
| D2 | (1,4)(2,3)(3,2)(4,1) |

## 1.3 핵심 유스케이스(도메인 관점)

| UC | 이름 | 사후조건 |
|----|------|----------|
| **UC-D1** | 빈칸 찾기 | 스캔 순서로 `CellPosition` 2개 |
| **UC-D2** | 누락 숫자 찾기 | `MissingPair(min,max)`, \|집합\|=2 |
| **UC-D3** | 마방진 판정 | 10선 합=34 & I-2 |
| **UC-D4** | 두 조합 시도 | 아래 의사코드 |
| **UC-D5** | 해 반환 | `SolutionVector` → `int[6]` |

**UC-D4 의사코드**

```
pos1, pos2 := 첫·둘째 빈칸 (행 우선 스캔)
min, max := 누락 두 수 (min < max)

G1 := pos1=min, pos2=max
G2 := pos1=max, pos2=min

if MagicSquareValidator(G1): return SolutionVector(pos1, min, pos2, max)
if MagicSquareValidator(G2): return SolutionVector(pos1, max, pos2, min)
fail UNSOLVABLE_PUZZLE
```

## 1.4 Domain API(내부 계약)

| API | 입력 | 출력 | 실패 |
|-----|------|------|------|
| `PuzzleGrid.of(int[4][4])` | 4×4 | `PuzzleGrid` | `NULL_GRID`, `INVALID_DIMENSION`, `INVALID_CELL_VALUE`, `DUPLICATE_VALUE` |
| `EmptyCellLocator.locate(PuzzleGrid)` | grid | 2×`CellPosition` | `BLANK_COUNT_NOT_TWO` |
| `MissingNumberResolver.resolve(PuzzleGrid)` | grid | `MissingPair` | `MISSING_COUNT_NOT_TWO` |
| `MagicSquareValidator.isValidComplete(int[4][4])` | 0 없음 | boolean | `INCOMPLETE_GRID` |
| `TwoBlankPuzzleSolver.solve(PuzzleGrid)` | grid | `SolutionVector` | 상위 실패, `UNSOLVABLE_PUZZLE` |
| `SolutionVector.toArray()` | — | `int[6]` | — |

## 1.5 Domain 단위 테스트 설계(RED 우선)

**명명:** `{Unit}_{condition}_{expected}`

### P0

| ID | Given | When | Then | Invariant |
|----|-------|------|------|-----------|
| DOM-P0-01 | 완성 마방진 (F1 완성본) | `isValidComplete` | true | I-5~7 |
| DOM-P0-02 | 행만 맞고 D2 깨짐 격자 | `isValidComplete` | false | I-7 |
| DOM-P0-03 | F1 | `solve` | `[1,2,3,2,3,11]` | I-O1,O2 |
| DOM-P0-04 | F1 | `solve` | n1=3, n2=11 (min→첫) | I-O2 |
| DOM-P0-05 | F2 | `solve` | `[2,2,10,3,3,7]` | I-O2 반대 |

### 정상 / 비정상 / 엣지 (요약)

| 구분 | ID 예 | Then |
|------|-------|------|
| 정상 | DOM-N-01~04 | 완성 검증, F1/F2 solve, 완성 후 검증, 재현성 |
| 비정상 | DOM-E-01~08 | 차원, 빈칸≠2, 중복, 17, UNSOLVABLE |
| 엣지 | DOM-X-01~03 | (4,3)(4,4) 스캔 순서, 좌표 1-index, 완성 격자 solve 거부 |

**Domain RED:** ≥ **20개** (P0 5 + 정상 4 + 비정상 8 + 엣지 3)

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 시나리오

| Step | 행위 | 레이어 |
|------|------|--------|
| 1 | `int[4][4]` 전달 | UI Boundary |
| 2 | 입력 계약 검증 | UI Boundary |
| 3 | 실패 → Error schema | UI Boundary |
| 4 | Domain `solve` (테스트 시 Mock) | Domain |
| 5 | Domain 실패 → Error 매핑 | UI Boundary |
| 6 | 성공 → 출력 계약 검증 → `int[6]` | UI Boundary |

## 2.2 UI 계약(외부 계약)

### Input

| ID | 규칙 |
|----|------|
| UI-IN-01 | `grid != null` |
| UI-IN-02 | `grid.length == 4` |
| UI-IN-03 | 모든 행 길이 4 |
| UI-IN-04 | 값 ∈ {0}∪[1,16] |
| UI-IN-05 | 0 개수 == 2 |
| UI-IN-06 | 비0 집합 크기 == 14 |

### Output (성공)

| ID | 규칙 |
|----|------|
| UI-OUT-01 | length == 6 |
| UI-OUT-02 | r1,c1,r2,c2 ∈ [1,4] |
| UI-OUT-03 | n1,n2 ∈ [1,16], n1≠n2 |
| UI-OUT-04 | 두 좌표 상이 |
| UI-OUT-05 | 해당 칸이 0 |
| UI-OUT-06 | 비0 ∪ {n1,n2} = {1..16} |

### Error schema

| code | message (고정) |
|------|----------------|
| `ERR_NULL_GRID` | `Grid must not be null.` |
| `ERR_INVALID_DIMENSION` | `Grid must be 4x4.` |
| `ERR_INVALID_VALUE` | `Cell value must be 0 or between 1 and 16.` |
| `ERR_BLANK_COUNT` | `Grid must contain exactly 2 blank cells (0).` |
| `ERR_DUPLICATE_VALUE` | `Duplicate non-zero value is not allowed.` |
| `ERR_UNSOLVABLE` | `No valid magic square can be formed with two blanks.` |
| `ERR_INTERNAL` | `Unexpected error.` |

**Domain → UI 매핑:** `INVALID_DIMENSION`→`ERR_INVALID_DIMENSION`, `INVALID_CELL_VALUE`→`ERR_INVALID_VALUE`, `BLANK_COUNT_NOT_TWO`→`ERR_BLANK_COUNT`, `DUPLICATE_VALUE`→`ERR_DUPLICATE_VALUE`, `UNSOLVABLE_PUZZLE`→`ERR_UNSOLVABLE`, 기타→`ERR_INTERNAL`.

**Boundary API:** `MagicSquareBoundary.solve(int[4][4])` → `int[6]` | ErrorSchema

## 2.3 UI 레벨 테스트(Contract-first, Domain Mock)

| ID | Then |
|----|------|
| UI-P0-01~06 | null, 3×4, blank≠2, 17, duplicate, ERR 메시지 일치 |
| UI-P0-07 | Mock success → 기대 배열, Domain 1회 |
| UI-P0-08 | Mock UNSOLVABLE → `ERR_UNSOLVABLE` |
| UI-N-01~02 | OUT-01~06, 실패 시 Domain 미호출 |
| UI-X-01 | message 완전 일치 |

**UI RED:** ≥ **15개**

## 2.4 UX/출력 규칙

| ID | 규칙 |
|----|------|
| UX-01 | message는 표와 바이트 일치 |
| UX-02 | 성공은 숫자 배열만 |
| UX-03 | field: `grid[r][c]` (0-index 표기) |
| UX-04 | 동일 입력 → 동일 출력 |
| UX-05 | 성공/에러 필드 혼합 금지 |

---

# 3) Data Layer 설계

## 3.1 목적

| 항목 | 내용 |
|------|------|
| **왜** | 입력·해 스냅샷 재현; 저장 형식과 Domain 분리 연습 |
| **범위** | `int[4][4]`, (선택) `int[6]`, timestamp |
| **범위 밖** | DB, 동시성, 계정 |

## 3.2 인터페이스 계약

| 메서드 | 실패 |
|--------|------|
| `save(id, grid, resultOptional)` | `REPO_NULL_ID`, `REPO_INVALID_GRID` |
| `load(id)` | `REPO_NOT_FOUND`, `REPO_CORRUPT_FORMAT` |
| `exists(id)` | — |
| `delete(id)` | `REPO_NOT_FOUND` |

**SavedPuzzle:** DATA-I1 grid 4×4, DATA-I2 result 길이 6·OUT 규칙, DATA-I3 id 유일.

## 3.3 구현 옵션

| | InMemory | File JSON |
|--|----------|-----------|
| **추천 1차** | ✓ RED 속도 | 2차 어댑터 |

## 3.4 Data 테스트

| ID | Then |
|----|------|
| DATA-01~07 | save/load, result, not found, overwrite, corrupt, 5×5 거부, delete |

**Data RED:** ≥ **7개**

---

# 4) Integration & Verification

## 4.1 통합 경로

```
Caller → UI Boundary → [Application] → TwoBlankPuzzleSolver → UI Boundary → int[6]
                              ↘ MatrixRepository (선택)
```

**의존성:** UI→Domain ✓, Domain→UI/Data ✗, Data→Domain ✗.

## 4.2 통합 시나리오

| ID | 유형 | Then |
|----|------|------|
| INT-N-01 | F1 E2E | `[1,2,3,2,3,11]` |
| INT-N-02 | save/load 재호출 | 동일 결과 |
| INT-E-01 | blank 3 | `ERR_BLANK_COUNT` |
| INT-E-02 | F3 | `ERR_UNSOLVABLE` |
| INT-E-03 | unknown id | `REPO_NOT_FOUND` |
| INT-E-04 | corrupt file | `REPO_CORRUPT_FORMAT` |

## 4.3 회귀 보호

| ID | 규칙 |
|----|------|
| REG-01 | ERR message 변경 = 의도적만 |
| REG-02 | int[6] 의미 변경 금지 |
| REG-03 | Domain/UI P0 CI 필수 |
| REG-04 | 커버리지 하한 미달 merge 불가 |
| REG-05 | Repository 변경 시 DATA+INT 동시 수정 |

## 4.4 커버리지 목표

| 레이어 | 목표 |
|--------|------|
| Domain | ≥95% branch |
| UI Boundary | ≥85% branch |
| Data | ≥80% branch |

## 4.5 Traceability Matrix

| Concept | Rule | Use Case | Contract | Test | Component |
|---------|------|----------|----------|------|-----------|
| I-1 | UI-IN-02,03 | — | Input | UI-P0-02, DOM-E-01 | UI |
| I-P1 | UI-IN-05 | UC-D1 | Input | UI-P0-03,04 | UI+Locator |
| I-12 | UI-IN-04,06 | — | Input | UI-P0-05,06 | UI |
| I-5~7 | 10선 | UC-D3 | Validator | DOM-P0-01,02 | Validator |
| I-O2 | min/max | UC-D4 | Output | DOM-P0-03~05 | Solver |
| I-8 | — | UC-D5 | Output | DOM-N-04, INT-N-02 | Solver+Repo |
| UX-01 | message | — | Error | UI-P0-*, UI-X-01 | UI |

## Dual-Track 실행 순서

| Track | 순서 |
|-------|------|
| Logic | DOM-P0-01→02→04→03→05 |
| UI | UI-P0-01~06 (Mock) |
| Data | DATA-01~03 |
| Integration | INT-N-01, INT-E-01~02 |

---

## 설계 완료 체크리스트

- [x] Domain/UI/Data/Integration 4절
- [x] RED: Domain ≥18, UI ≥15, Data ≥7, INT ≥6
- [x] F1/F2 기대값 검증 완료
- [x] 구현 코드 없음
