# Magic Square 4×4 — Cursor Rules 및 초기 구현 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `03_MagicSquare_CursorRules_And_InitialImplementation_Report` |
| **전제 보고서** | [`01_MagicSquare_ProblemDefinition_Report.md`](01_MagicSquare_ProblemDefinition_Report.md), [`02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
| **작성일** | 2026-05-28 |
| **상태** | `.cursorrules` 완성, `User` entity·Domain 테스트 9건 GREEN, 본편 마방진 도메인 미착수 |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [Cursor Rules 설계 결정](#2-cursor-rules-설계-결정)
3. [`.cursorrules` 구성](#3-cursorrules-구성)
4. [`.cursorrules` 검토 (2026-05-28)](#4-cursorrules-검토-2026-05-28)
5. [초기 구현 — `User` Entity](#5-초기-구현--user-entity)
6. [산출물·디렉터리](#6-산출물디렉터리)
7. [다음 단계](#7-다음-단계)

---

## 1. 세션 요약

본 세션에서는 **구현 코드 작성 전** Cursor AI 가이드라인(`.cursorrules`)을 설계·작성·검토한 뒤, ECB **entity** 레이어의 첫 도메인 타입 **`User`** 를 TDD 스타일로 추가했다.

| 단계 | 내용 | 결과 |
|------|------|------|
| Rules 설계 | `.cursorrules` vs `.cursor/rules/*.mdc` 비교, 8~10개 분리안 | **`.cursor/rules/*.mdc` 권장**, 본 프로젝트는 사용자 요청으로 **루트 `.cursorrules`(YAML)** 채택 |
| Rules 뼈대 | 8개 최상위 키 + 80자 `#` 구분선 | 완료 |
| `tdd_rules` | RED / GREEN / REFACTOR + `dual_track` | 완료 |
| Rules 검토 | YAML·누락·충돌·`ai_behavior` | 문법 OK, 7개 섹션 공백 지적 → 이후 전 섹션 채움 |
| Rules 완성 | project ~ ai_behavior 전체 | 완료 (225줄) |
| 구현 | `User` entity + pytest | **9 passed** |

---

## 2. Cursor Rules 설계 결정

### 2.1 형식 선택

| 방식 | 채택 | 이유 |
|------|------|------|
| `.cursor/rules/*.mdc` | 권장(문서화) | `globs` / `alwaysApply`로 레이어·테스트별 주입 |
| 루트 `.cursorrules` (YAML) | **본 저장소 적용** | 사용자 지정 8키 구조, 팀이 한 파일로 관리 |

> Cursor는 `.cursorrules` 내용을 **구조화 YAML로 파싱하기보다** 문맥 텍스트로 주입하는 경우가 많다. 규칙 준수는 **명확한 Must/Must not + 예시**에 의존한다.

### 2.2 권장 분리안 (참고 — 미적용)

| 파일(안) | 역할 |
|----------|------|
| `00-project-core.mdc` | alwaysApply — 프로젝트·SSOT |
| `20-tdd-dual-track.mdc` | RED/GREEN/REFACTOR, Dual-Track |
| `31~33-ecb-*.mdc` | entity / control / boundary |
| `40-pytest-aaa.mdc` | tests/** |

---

## 3. `.cursorrules` 구성

| 섹션 | 주요 내용 |
|------|-----------|
| `project` | 4×4, 마법합 34, IO 계약, F1/F2/F3, Report 링크 |
| `code_style` | Python 3.10+, PEP8, type hints, Google docstring, Black 88 |
| `architecture` | ECB 3레이어, boundary→control→entity, Dual-Track 경로 |
| `tdd_rules` | `dual_track`, `red_phase` / `green_phase` / `refactor_phase` (description, rules, must_not) |
| `testing` | pytest, AAA, coverage 80%, `test_` 접두사, fixture scope |
| `forbidden` | print, 하드코딩 상수, bare except, RED 생략, 테스트 약화, ECB 역의존 등 |
| `file_structure` | `src/magicsquare/{entity,control,boundary}`, `tests/{domain,boundary,integration}` |
| `ai_behavior` | before/during/after_code, `tdd_violation_warning` |

### 3.1 `tdd_rules` 요약

| Phase | 핵심 |
|-------|------|
| **RED** | 테스트 선작성, pytest 실패 확인, 스킵·xfail 금지 |
| **GREEN** | 최소 구현만, 리팩터링·테스트 완화 금지 |
| **REFACTOR** | 계약 불변, 커버리지 유지 |
| **dual_track** | DOM-* ∥ UI-* / DATA-*, INT는 P0 GREEN 이후 |

---

## 4. `.cursorrules` 검토 (2026-05-28)

검토 시점(전 섹션 채우기 **이전**) 기준 이슈와 조치:

| 항목 | 당시 문제 | 조치 |
|------|-----------|------|
| YAML 문법 | 없음 | — |
| 누락 섹션 | 7개 키 공백 | **전 섹션 작성 완료** |
| `tdd_rules` ↔ `forbidden` | 직접 충돌 없음 (forbidden 비어 있음) | forbidden에 금지 항목 명시 |
| `ai_behavior` | 비어 있음 | before/during/after + violation warning 추가 |
| Dual-Track | `tdd_rules`에 없음 | `dual_track` 블록 추가 |

**잔여 참고:** 02 보고서 UI Boundary 커버리지 목표(85%)와 `.cursorrules` `testing.coverage_minimum`(80%)는 **의도적 완화** — 통합 시 `pyproject`/CI에서 레이어별 threshold 분리 권장.

---

## 5. 초기 구현 — `User` Entity

### 5.1 위치·책임

| 항목 | 내용 |
|------|------|
| **레이어** | ECB **entity** |
| **경로** | `src/magicsquare/entity/user.py` |
| **역할** | 퍼즐 저장·로드 시 Repository `id` **소유자** 정체성 (02 보고서 Data 레이어와 연계 예정) |
| **02 보고서** | `User`는 설계서에 없음 — **보조 entity**로 추가 |

### 5.2 API·불변조건

| API / 규칙 | 설명 |
|------------|------|
| `User.create(user_id, display_name)` | trim 후 검증, frozen 인스턴스 반환 |
| `user_id` | 비어 있으면 `InvalidUserError` |
| `display_name` | 1..50자 (`MAX_DISPLAY_NAME_LENGTH`) |
| `__eq__` / `__hash__` | `user_id` 기준만 |

### 5.3 테스트

| 항목 | 내용 |
|------|------|
| **경로** | `tests/domain/test_user.py` |
| **패턴** | pytest, AAA, `test_{unit}_{condition}_{expected}` |
| **결과** | **9 passed** (2026-05-28) |

| ID (관례) | 검증 |
|-----------|------|
| DOM-USER-CREATE-01 | 정상 생성 |
| DOM-USER-CREATE-02 | whitespace 정규화 |
| DOM-USER-CREATE-E01~E03 | 빈 id, 빈 name, name 길이 초과 |
| DOM-USER-EQ-01~03 | 동등성·해시 |

### 5.4 ECB 준수

- entity에 UI/I/O/boundary import **없음**
- `InvalidUserError`는 `entity/exceptions.py` (도메인 예외, UI 메시지 없음)

---

## 6. 산출물·디렉터리

```
MagicSquare_XX/
├── .cursorrules                          # AI 규칙 (YAML, 8섹션)
├── pyproject.toml                        # pytest pythonpath
├── src/magicsquare/
│   ├── __init__.py
│   └── entity/
│       ├── __init__.py
│       ├── exceptions.py
│       └── user.py
├── tests/
│   └── domain/
│       └── test_user.py
├── Report/
│   ├── 01_...ProblemDefinition...
│   ├── 02_...DualTrack_CleanArchitecture_TDD_Design...
│   └── 03_...CursorRules_And_InitialImplementation...  ← 본 문서
└── Prompt/
    └── 03_...CursorRules_UserEntity_Prompt.md          # 세션 Export
```

---

## 7. 다음 단계

| 우선순위 | 작업 | 근거 |
|----------|------|------|
| 1 | 02 보고서 **DOM-P0** RED → `PuzzleGrid`, `MagicSquareValidator` | 설계서 1순위 Domain |
| 2 | **UI-P0** Boundary RED (Domain mock) | Dual-Track |
| 3 | F3(UNSOLVABLE) 픽스처 확정 | INT-E-02 |
| 4 | `User` ↔ Repository 소유자 연계 | Data 레이어 구현 시 |
| 5 | (선택) `.cursor/rules/*.mdc`로 규칙 분리 | 토큰·레이어별 주입 |

---

## 부록 — 대화 Export

전체 User/Cursor 턴: [`Prompt/03_MagicSquare_CursorRules_UserEntity_Prompt.md`](../Prompt/03_MagicSquare_CursorRules_UserEntity_Prompt.md)
