# Magic Square 4×4 — 모듈형 Cursor Rules 전환 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `04_MagicSquare_Modular_CursorRules_Report` |
| **전제 보고서** | [`03_MagicSquare_CursorRules_And_InitialImplementation_Report.md`](03_MagicSquare_CursorRules_And_InitialImplementation_Report.md) |
| **작성일** | 2026-05-28 |
| **상태** | `.cursor/rules/*.mdc` 5종 배치 완료, 루트 `.cursorrules`는 인덱스로 축소 |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [설계·형식 결정](#2-설계형식-결정)
3. [`.mdc` 규칙 파일 구성](#3-mdc-규칙-파일-구성)
4. [`.cursorrules` 변경](#4-cursorrules-변경)
5. [03 보고서 대비 변경점](#5-03-보고서-대비-변경점)
6. [산출물·디렉터리](#6-산출물디렉터리)
7. [검증·운영](#7-검증운영)
8. [다음 단계](#8-다음-단계)

---

## 1. 세션 요약

| 단계 | 사용자 요청 | 결과 |
|------|-------------|------|
| 1 | `.cursorrules` + `.cursor/rules/*.mdc` 구조 **방법만** 설명 (구현 금지) | 레거시 vs 모듈형, frontmatter, 5파일 분리안 안내 |
| 2 | **진행** — 실제 적용 | 5개 `.mdc` 생성, `.cursorrules` 인덱스화 |
| 3 | 보고서·프롬프트 Export | 본 문서, [`Prompt/04_...`](../Prompt/04_MagicSquare_Modular_CursorRules_Prompt.md) |

**구현 코드 변경 없음** — AI 가이드라인 파일만 변경.

---

## 2. 설계·형식 결정

### 2.1 채택 형식

| 방식 | 03 세션 | **04 세션 (현재)** |
|------|---------|-------------------|
| 루트 `.cursorrules` (YAML, 225줄) | **채택** | **인덱스만** (13줄) |
| `.cursor/rules/*.mdc` | 권장만, 미적용 | **채택** (5파일) |

### 2.2 분리 원칙

- **한 파일 = 한 관심사** (프로젝트 / ECB / TDD·테스트 / Python 스타일 / 금지)
- **항상 적용**: 프로젝트·계약·AI 절차, forbidden
- **globs 적용**: `src/**`, `tests/**`, 전역 `**/*.py`
- 03의 YAML 8키 내용은 **손실 없이** Markdown 본문으로 이전

### 2.3 frontmatter 매핑

| 파일 | `alwaysApply` | `globs` |
|------|---------------|---------|
| `magicsquare-project.mdc` | `true` | — |
| `magicsquare-forbidden.mdc` | `true` | — |
| `magicsquare-ecb-architecture.mdc` | `false` | `src/**/*.py` |
| `magicsquare-tdd-testing.mdc` | `false` | `tests/**/*.py` |
| `magicsquare-python-code-style.mdc` | `false` | `**/*.py` |

---

## 3. `.mdc` 규칙 파일 구성

### 3.1 `magicsquare-project.mdc`

| 블록 | 03 `.cursorrules` 출처 |
|------|------------------------|
| 도메인·IO 계약·F1/F2/F3 | `project` |
| 디렉터리 트리 | `file_structure` |
| before/during/after_code, violation warning | `ai_behavior` |

### 3.2 `magicsquare-ecb-architecture.mdc`

| 블록 | 출처 |
|------|------|
| entity / control / boundary 역할·must_not | `architecture.layers` |
| boundary → control → entity | `architecture.dependency_direction` |
| Dual-Track 경로 | `architecture.dual_track` |

### 3.3 `magicsquare-tdd-testing.mdc`

| 블록 | 출처 |
|------|------|
| dual_track, red/green/refactor phase | `tdd_rules` |
| pytest, AAA, coverage, fixture scope | `testing` |
| Boundary mock·ERR 메시지 | `testing.boundary_testing` |

### 3.4 `magicsquare-python-code-style.mdc`

| 블록 | 출처 |
|------|------|
| Python 3.10+, PEP8, Black, Ruff, naming | `code_style` |
| type hints·docstring 예시 | `code_style` + `ai_behavior` |

### 3.5 `magicsquare-forbidden.mdc`

| 블록 | 출처 |
|------|------|
| print, 매직 넘버, except, TDD 우회, ECB 역전 | `forbidden` (표 형식) |

---

## 4. `.cursorrules` 변경

**이전 (03):** 225줄 YAML — `project` ~ `ai_behavior` 전체 규칙 본문.

**이후 (04):** 5개 `.mdc` 경로·적용 범위 표 + Report/README 링크만 유지.

**이유:** Cursor가 `.cursor/rules`와 `.cursorrules`를 **동시에** 읽을 수 있어, 동일 규칙 이중 주입을 피하기 위함.

---

## 5. 03 보고서 대비 변경점

| 항목 | 03 | 04 |
|------|----|----|
| 규칙 저장 위치 | 루트 `.cursorrules` only | `.cursor/rules/*.mdc` + 인덱스 `.cursorrules` |
| 레이어별 주입 | 없음 (전체 항상) | `globs`로 src/tests 분리 |
| 03 §7 다음 단계 5번 | “(선택) mdc 분리” | **완료** |
| `User` entity / pytest 9건 | 03에 기록 | **변경 없음** (본 세션 비대상) |

**유지된 정책:** F1/F2, ECB 의존 방향, Dual-Track RED/GREEN/REFACTOR, forbidden 7항, coverage 80% (02 UI 85%와의 차이는 03과 동일).

---

## 6. 산출물·디렉터리

```
MagicSquare_XX/
├── .cursorrules                          # 인덱스 (13줄)
├── .cursor/rules/
│   ├── magicsquare-project.mdc           # alwaysApply
│   ├── magicsquare-forbidden.mdc         # alwaysApply
│   ├── magicsquare-ecb-architecture.mdc  # src/**/*.py
│   ├── magicsquare-tdd-testing.mdc       # tests/**/*.py
│   └── magicsquare-python-code-style.mdc # **/*.py
├── Report/
│   ├── 01_...ProblemDefinition...
│   ├── 02_...DualTrack_CleanArchitecture_TDD_Design...
│   ├── 03_...CursorRules_And_InitialImplementation...
│   └── 04_...Modular_CursorRules...      ← 본 문서
└── Prompt/
    ├── 03_...CursorRules_UserEntity_Prompt.md
    └── 04_...Modular_CursorRules_Prompt.md
```

---

## 7. 검증·운영

| 확인 항목 | 방법 |
|-----------|------|
| 규칙 등록 | Cursor **Settings → Rules** 에 5개 Project Rule 표시 |
| src 작업 시 | `src/magicsquare/entity/` 파일 열고 ECB·forbidden 준수 여부 질의 |
| tests 작업 시 | `tests/domain/` 열고 RED/GREEN phase 질의 |
| 수동 지정 | 채팅 `@magicsquare-tdd-testing` 등 |

---

## 8. 다음 단계

| 우선순위 | 작업 | 근거 |
|----------|------|------|
| 1 | 02 보고서 **DOM-P0** RED | 마방진 본편 도메인 (03·04와 독립) |
| 2 | **UI-P0** Boundary RED | Dual-Track |
| 3 | 규칙 미세 조정 | 실제 Agent 위반 패턴 발생 시 해당 `.mdc`만 수정 |
| 4 | (선택) `pyproject`에 Ruff/Black과 규칙 문구 동기화 | CI와 규칙 일치 |

---

## 부록 — 대화 Export

전체 User/Cursor 턴: [`Prompt/04_MagicSquare_Modular_CursorRules_Prompt.md`](../Prompt/04_MagicSquare_Modular_CursorRules_Prompt.md)
