# Magic Square 4×4 — 테스트 계획서 (Track A: FR-01 구조 검증)

| 항목 | 내용 |
|------|------|
| **문서 ID** | `docs/test_plan.md` |
| **기준 SSOT** | [`docs/PRD_MagicSquare.md`](PRD_MagicSquare.md), [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](../Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
| **앵커 샘플** | **AC-FR-01-01** — `grid = None` → `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` |
| **PRD 매핑** | FR-01 · AC-01 · AC-05 · BR-01 · ES-01 · §12.1 · §13 |
| **기술 스택** | Python 3.11+, pytest ≥7.4, pytest-cov ≥4.1, pydantic (`FailureResult`), `unittest.mock` |
| **대상 레이어** | Boundary (`BoundaryValidator`, `MagicSquareBoundary`) |
| **작성 관점** | 시니어 QA Lead — Contract-first, Dual-Track Track A |

---

## 1. 목적 및 범위

본 계획서는 **FR-01 Input Verification** 중 **구조·차원 선행 검증**(AC-FR-01-01 / PRD AC-01)과 **Domain resolver 미호출**(PRD AC-05)을 pytest 단위 테스트로 고정한다.

| 구분 | 내용 |
|------|------|
| **In-Scope** | `None`·빈 리스트·행/열 불일치·비정방 행렬 → `INVALID_SIZE` + Domain `resolve()` 0회 |
| **Out-of-Scope** | 4×4 **정상** 입력(F1/F2), 값 범위·빈칸·중복(AC-02~04), Domain Track B, 통합 E2E(실 Domain) |

---

## 2. 앵커 샘플 및 오류 계약

| 항목 | 값 |
|------|-----|
| **AC ID (QA)** | AC-FR-01-01 (= PRD AC-01 + AC-05) |
| **FR** | FR-01 Input Verification |
| **입력** | `grid = None` |
| **기대 출력** | `code = "INVALID_SIZE"`, `message = "Grid must be 4x4."` |
| **반환 타입** | `FailureResult` (pydantic `BaseModel`: `code: str`, `message: str`) |
| **PRD §13 대응** | `ERR_INVALID_DIMENSION` — message 동일; RED 배치 `code`는 `INVALID_SIZE` 고정 |

> GREEN/REFACTOR 단계에서 Report/02 `ERR_NULL_GRID` 분리 여부는 SSOT 재정합 후 별도 문서화한다. **본 RED 배치**에서는 구조 실패 전건 동일 `(INVALID_SIZE, Grid must be 4x4.)` 를 사용한다.

---

## 3. pytest 단위 테스트 범위 및 우선순위

### 3.1 디렉터리 구조

```
tests/
├── boundary/
│   ├── conftest.py                              # mock resolver, 계약 상수
│   └── test_ac_fr_01_01_dimension_validation.py # 본 계획 P0
├── domain/                                        # Track B (별도 계획)
├── integration/                                   # F1/F2 (본 계획 제외)
└── conftest.py                                    # (선택) 공통 픽스처
```

### 3.2 SUT·호출 경로

| 역할 | 심볼 | 비고 |
|------|------|------|
| **SUT** | `MagicSquareBoundary.solve(grid)` | Boundary 공개 API 단일 진입 |
| **검증 협력** | `BoundaryValidator` (내부) | 차원 분기 — cov 대상 |
| **격리 대상** | `SolveTwoBlankPuzzle.resolve()` (또는 주입 `resolver`) | **mock only**, 0회 호출 |

### 3.3 우선순위 매트릭스

| 우선순위 | RED / UI ID | 범위 | 실행 시점 | AC |
|----------|-------------|------|-----------|-----|
| **P0** | `RED-BND-VAL-001`, `UI-P0-01` | `grid is None` — 실패 계약 + `resolve()` 0회 | Track A RED 1차 | AC-FR-01-01, AC-05 |
| **P0** | `RED-BND-VAL-004`, `UI-P0-02` | `[]`, `[[]]*4`, 3×4, 4×3, 5×5 + `resolve()` 0회 | Track A RED 1차 | AC-01, AC-05 |
| **P1** | `UI-X-01` | message 바이트 일치 (P0 전건) | GREEN 직후 | UX-01 |
| **P2** | — | 동일 입력 2회 → 동일 `(code, message)` | REFACTOR | BR-14, NFR-03 |
| **— (금지)** | `UI-P0-07`, F1/F2 | 4×4 **정상** 격자 | Integration / 별도 RED | 범위 외 |

### 3.4 설계 원칙

- **AAA** (Arrange–Act–Assert), Given-When-Then 주석, 테스트마다 `# AC-FR-01-01`
- **Contract-first:** Boundary만 실제 호출; Domain은 **항상** `unittest.mock` 주입
- **ECB:** `tests/boundary/`에서 `magicsquare.entity` solver **직접 호출 금지**
- **금지:** `print()`, assert 완화, `skip`/`xfail`로 GREEN, 4×4 정상 케이스 혼입

### 3.5 테스트 클래스·건수 (목표 25 RED)

| 클래스 | 건수 | 초점 |
|--------|------|------|
| `TestFailureReturnOnNoneGrid` | 5 | `None` → `FailureResult` 계약 |
| `TestBoundaryDimensionValues` | 5+ | BV-02~06 구조 실패 |
| `TestDomainResolverIsolation` | 5+ | `resolve()` 미호출 |
| `TestMessageExactMatch` | 5 | message 바이트 일치 |
| `TestScopeRestriction` | 5 | F1/F2·AC-02~04 소스 게이트 |

---

## 4. 경계값 케이스 목록

### 4.1 포함 케이스 (필수)

| Case ID | 입력 `grid` | 설명 | 기대 `code` | 기대 `message` | `resolve()` |
|---------|---------------|------|-------------|----------------|-------------|
| **BV-01** | `None` | 명시적 `None` | `INVALID_SIZE` | `Grid must be 4x4.` | **0** |
| **BV-02** | `[]` | 빈 리스트 (행 0) | `INVALID_SIZE` | `Grid must be 4x4.` | **0** |
| **BV-03** | `[[]] * 4` | 행 4개, 각 행 열 0 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** |
| **BV-04** | 3×4 (`GRID_3X4`) | 행 수 불일치 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** |
| **BV-05** | 4×3 (`GRID_4X3`) | 열 수 불일치 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** |
| **BV-06** | 5×5 (`GRID_5X5`) | 양방 초과 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** |
| **BV-07** | 2×2 `[[1,2],[3,4]]` | 양방 미만 (PRD TD-03) | `INVALID_SIZE` | `Grid must be 4x4.` | **0** |

### 4.2 픽스처 (구조만 검증, 셀 값 무관)

```python
GRID_3X4 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

GRID_4X3 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]

GRID_5X5 = [[i * 5 + j + 1 for j in range(5)] for i in range(5)]

GRID_FOUR_EMPTY_ROWS = [[] for _ in range(4)]  # BV-03: [[]]*4 동치 권장
```

### 4.3 명시적 제외 — 4×4 정상 입력 (포함 금지)

| Case ID | 입력 | 제외 사유 | 후속 추적 |
|---------|------|-----------|-----------|
| **EX-01** | F1 `[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]` | 4×4 구조 **통과** — AC-FR-01-01 범위 외 | `tests/integration/`, `RED-INT-F1-001` |
| **EX-02** | F2 `[[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]` | 동일 | `RED-INT-F2-001` |
| **EX-03** | 빈칸 1/3개, 중복, 값 17 등 | FR-01 AC-02~04 | `AC-FR-01-02`~`05` 별도 RED |

**게이트:** `test_ac_fr_01_01_dimension_validation.py` 소스에 F1/F2 리터럴·`ERR_BLANK_COUNT`·`ERR_DUPLICATE_VALUE`·`UNSOLVABLE` 기대 assert **없음** (`TestScopeRestriction`).

---

## 5. 예외·특이 케이스 목록

| Case ID | 유형 | 입력/조건 | 기대 동작 | 검증 포인트 |
|---------|------|-----------|-----------|-------------|
| **SP-01** | 타입 혼입 | `grid = "not a grid"` | `INVALID_SIZE` (또는 구현 확정 후 단일 code) | Boundary 조기 종료, `resolve()` 0회 |
| **SP-02** | 비리스트 | `grid = 123` | 동일 | `resolve()` 0회 |
| **SP-03** | `None` vs `[]` | 서로 다른 입력 | **동일** `INVALID_SIZE` + 동일 message | Domain 0회; GREEN 후 null 전용 code 분리 검토 |
| **SP-04** | jagged row | `[[1,2,3,4],[5,6],[7,8,9,10],[11,12,13,14]]` | `INVALID_SIZE` | `len(row)!=4` 분기, Domain 0회 |
| **SP-05** | `None` 행 원소 | `[None, [1,2,3,4], ...]` (4행) | `INVALID_SIZE` (구조 우선 정책) | Domain 0회; SSOT 1회 확정 |
| **SP-06** | `[[]] * 4` 참조 | 동일 `list` 객체 4행 공유 | `INVALID_SIZE` (열 길이 0) | 행 **동일성**은 본 AC 비목표 |
| **SP-07** | 입력 불변성 | BV 실행 전후 | `grid` 내용·id 불변 | NFR-04, BR-15 |
| **SP-08** | 이중 호출 | 동일 BV 2회 `solve()` | 동일 `(code, message)` | `resolve().call_count` 누적 0 |
| **SP-09** | message 엄격성 | P0 전건 | `Grid must be 4x4.` | 공백·이중 마침표·`null` 문구 없음 |

---

## 6. Domain resolver 호출 횟수 검증 전략 (mock/spy)

### 6.1 검증 대상

| 레이어 | 진입점 | AC-FR-01-01 기대 호출 수 |
|--------|--------|--------------------------|
| Boundary | `MagicSquareBoundary.solve(grid)` | **1** (SUT) |
| Control/Domain | `resolver.resolve(grid)` (주입 mock) | **0** |

### 6.2 Fixture·주입 패턴

```python
@pytest.fixture
def mock_resolver() -> MagicMock:
    return MagicMock(spec=SolveTwoBlankPuzzle)

@pytest.fixture
def boundary(mock_resolver: MagicMock) -> MagicSquareBoundary:
    return MagicSquareBoundary(resolver=mock_resolver)

@pytest.fixture
def mock_resolve(mock_resolver: MagicMock) -> MagicMock:
    return mock_resolver.resolve
```

### 6.3 Assert 패턴

| 기법 | 용도 | Assert |
|------|------|--------|
| `MagicMock(spec=SolveTwoBlankPuzzle)` | 타입 안전 주입 | — |
| `mock_resolve.assert_not_called()` | P0 격리 (BV-01~07) | 호출 없음 |
| `mock_resolve.call_count == 0` | 명시적 카운트 | `== 0` |
| `@pytest.mark.parametrize` | BV 전건 격리 | 케이스별 `assert_not_called()` |

### 6.4 시나리오별 기대

| 입력 | `resolve()` | `solve()` 반환 |
|------|-------------|----------------|
| BV-01 ~ BV-07 | **0** | `FailureResult(INVALID_SIZE, …)` |
| EX-01 F1 (별도 파일·통합) | **1** (mock success 시) | `list[int]` 길이 6 |

### 6.5 ECB 체크리스트

- [ ] `tests/boundary/`에서 Domain solver **실구현** import·호출 없음
- [ ] 구조 실패 테스트에 `BlankFinder` / `Solver` 내부 로직 assert 없음
- [ ] 실 Domain은 `tests/integration/`만 허용

---

## 7. 커버리지 목표

| 레이어 | NFR | Branch 목표 | 본 계획 기여 |
|--------|-----|-------------|--------------|
| **Boundary** | NFR-02 | **≥ 85%** | `BoundaryValidator` 차원 분기, `solve` 조기 return |
| **Domain** | NFR-01 | **≥ 95%** | **본 계획 미기여** (mock으로 Domain 미실행) |

### 7.1 Boundary — 본 계획으로 닫히는 분기

- `grid is None`
- `len(grid) != 4`
- `any len(row) != 4` (3×4, 4×3, jagged, `[[]]*4`)
- 검증 실패 시 `resolver.resolve` **미호출**

### 7.2 Domain 95%+ 달성 경로

- `tests/domain/` Track B (`RED-DOM-*`) 별도 실행·합산
- Boundary-only cov에서 Domain % **0%는 정상** — §8.2 분리 실행 필수

---

## 8. pytest-cov 측정 전략

### 8.1 설치

```bash
pip install pytest-cov
```

또는 개발 의존성 일괄 설치:

```bash
pip install -e ".[dev]"
```

### 8.2 실행 명령

```bash
# CI / 전체 스모크
pytest --cov=src --cov-report=term-missing

# 본 계획 — Boundary FR-01 구조 검증만
pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py \
  --cov=magicsquare.boundary \
  --cov-report=term-missing \
  --cov-fail-under=85

# Domain Track B — 별도 게이트 (본 계획과 분리)
pytest tests/domain \
  --cov=magicsquare.entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 8.3 측정·해석 규칙

| 규칙 | 설명 |
|------|------|
| **레이어 분리** | Domain 95% / Boundary 85%를 단일 `fail_under`로 동시 강제하지 않음 |
| **소스 경로** | `[tool.coverage.run] source = ["magicsquare"]` (`pyproject.toml`) |
| **mock 실행** | Boundary RED는 Domain 라인 미실행 → Domain cov는 `tests/domain`으로만 측정 |
| **범위 위반** | 4×4 정상 케이스를 boundary 파일에 넣으면 NFR-02 왜곡 — **금지** |

### 8.4 `pyproject.toml` 참고 (선택 보강)

```toml
[tool.coverage.run]
source = ["magicsquare"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
show_missing = true
```

---

## 9. RED 실행·완료 기준

### 9.1 RED 확인

```bash
pytest tests/boundary/test_ac_fr_01_01_dimension_validation.py -v
```

| RED 유형 | 원인 | 허용 |
|----------|------|------|
| Collection / Import error | `magicsquare.boundary.*` 미존재 | ✅ |
| Assertion error | SUT 미구현 | ✅ |
| `TestScopeRestriction` GREEN | 소스 정책만 충족 | ✅ (기능 RED와 분리 판정) |

### 9.2 Definition of Done

- [ ] BV-01~07 전건: `INVALID_SIZE` + message 바이트 일치
- [ ] BV-01~07 전건: `mock_resolve.assert_not_called()` 또는 `call_count == 0`
- [ ] EX-01/02 (F1/F2) **미포함** — 소스 게이트 통과
- [ ] Boundary `--cov=magicsquare.boundary --cov-fail-under=85` 통과
- [ ] TDD: RED 기록 후 최소 GREEN — assert 완화·skip 없음

---

## 10. 추적성

| Concept | BR | FR | PRD AC | QA AC | Test Case | RED ID |
|---------|----|----|--------|-------|-----------|--------|
| 4×4 구조 실패 | BR-01 | FR-01 | AC-01, AC-05 | AC-FR-01-01 | BV-01~07 | RED-BND-VAL-001, 004 |
| Domain 미호출 | — | FR-01 | AC-05 | AC-FR-01-01 | §6 mock | UI-P0-01, 02 |
| 4×4 정상 제외 | BR-01 | FR-01 | — | — | EX-01, EX-02 | — |
| 오류 문구 고정 | UX-01 | FR-01 | §13 | — | SP-09, P1 | UI-X-01 |

---

## 11. 참고

- PRD Scenario C: 4×4 아님 → Boundary 즉시 실패, Domain 미호출
- 프로젝트 규칙: `.cursor/rules/magicsquare-forbidden.mdc`, `magicsquare-tdd-testing.mdc`
- README RED 체크리스트: [`README.md`](../README.md)
