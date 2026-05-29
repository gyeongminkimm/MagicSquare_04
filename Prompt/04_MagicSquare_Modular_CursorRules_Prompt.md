# Magic Square 4×4 — 모듈형 Cursor Rules (대화형 프롬프트 Export)

_Exported on 2026-05-28 from Cursor — MagicSquare_XX `.cursor/rules/*.mdc` 전환 세션_

**산출물 링크**

| 산출물 | 경로 |
|--------|------|
| 모듈형 Cursor Rules 보고서 | [`Report/04_MagicSquare_Modular_CursorRules_Report.md`](../Report/04_MagicSquare_Modular_CursorRules_Report.md) |
| Cursor Rules 인덱스 | [`.cursorrules`](../.cursorrules) |
| 모듈 규칙 (5종) | [`.cursor/rules/`](../.cursor/rules/) |
| 이전 Rules·User Entity 세션 | [`Report/03_...`](../Report/03_MagicSquare_CursorRules_And_InitialImplementation_Report.md), [`Prompt/03_...`](03_MagicSquare_CursorRules_UserEntity_Prompt.md) |
| TDD 설계 (전제) | [`Report/02_...`](../Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |

---

**User**

(이미지: `.cursorrules` + `.cursor/rules/` 아래 5개 `magicsquare-*.mdc` 구조)

와 같이 커서룰을 만들고 싶은데 방법을 알려줘. 구현은 하지마

---

**Cursor**

(구현·파일 생성 없음 — 방법만 설명)

**요약**

1. **두 방식 공존:** 루트 `.cursorrules`(레거시) vs `.cursor/rules/*.mdc`(권장·모듈형).
2. **폴더:** `.cursor/rules/이름.mdc` — YAML frontmatter + Markdown 본문.
3. **frontmatter:** `description`, `alwaysApply: true` 또는 `globs: **/*.py`, `alwaysApply: false`.
4. **MagicSquare 5파일 분리안:**
   - `magicsquare-project.mdc` — project, file_structure, ai_behavior → alwaysApply
   - `magicsquare-ecb-architecture.mdc` — architecture → `src/**/*.py`
   - `magicsquare-tdd-testing.mdc` — tdd_rules, testing → `tests/**/*.py`
   - `magicsquare-python-code-style.mdc` — code_style → `**/*.py`
   - `magicsquare-forbidden.mdc` — forbidden → alwaysApply
5. **작업 순서:** 폴더 생성 → .mdc 작성 → 기존 `.cursorrules` 이전·중복 제거 → Settings에서 확인.
6. **UI:** Cursor Settings → Rules → Add Rule.

---

**User**

진행

---

**Cursor**

기존 `.cursorrules`(225줄 YAML) 내용을 5개 `.mdc`로 분할·이전.

| 생성 파일 | alwaysApply | globs |
|-----------|-------------|-------|
| `magicsquare-project.mdc` | true | — |
| `magicsquare-forbidden.mdc` | true | — |
| `magicsquare-ecb-architecture.mdc` | false | `src/**/*.py` |
| `magicsquare-tdd-testing.mdc` | false | `tests/**/*.py` |
| `magicsquare-python-code-style.mdc` | false | `**/*.py` |

`.cursorrules`는 5개 파일 안내 표만 남김(중복 주입 방지).

---

**User**

보고서를보내주는 것과 프롬프트 저장을 해줘

---

**Cursor**

1. **`Report/04_MagicSquare_Modular_CursorRules_Report.md`** 생성.
2. **`Prompt/04_MagicSquare_Modular_CursorRules_Prompt.md`** (본 파일) — 세션 Export.
3. **`README.md`** 문서·디렉터리 목록 갱신.

---

## 재실행용 단일 프롬프트 (요약)

아래를 새 채팅에 붙이면 **모듈형 Cursor Rules만** 다시 구성할 수 있다.

```markdown
`Report/03_MagicSquare_CursorRules_And_InitialImplementation_Report.md`와
루트 `.cursorrules`(또는 백업 YAML)를 읽은 뒤,
구현 코드는 변경하지 말고 `.cursor/rules/`에 모듈형 규칙을 만든다.

## 산출물

1. `.cursor/rules/magicsquare-project.mdc` — alwaysApply: 프로젝트·F1/F2·디렉터리·AI 절차
2. `.cursor/rules/magicsquare-forbidden.mdc` — alwaysApply: forbidden 표
3. `.cursor/rules/magicsquare-ecb-architecture.mdc` — globs: src/**/*.py
4. `.cursor/rules/magicsquare-tdd-testing.mdc` — globs: tests/**/*.py
5. `.cursor/rules/magicsquare-python-code-style.mdc` — globs: **/*.py
6. `.cursorrules` — 5개 .mdc 인덱스만 (본문 중복 금지)
7. `Report/04_MagicSquare_Modular_CursorRules_Report.md`
8. `Prompt/04_MagicSquare_Modular_CursorRules_Prompt.md` — 대화 Export

## frontmatter 예시

---
description: ...
alwaysApply: true
---

또는

---
description: ...
globs: tests/**/*.py
alwaysApply: false
---

03 보고서의 ECB·Dual-Track·RED/GREEN/REFACTOR·forbidden 내용을 빠짐없이 이전할 것.
```

---

## 부록 A — 방법 안내 요청 시 사용한 프롬프트 (원문)

```markdown
(이미지: .cursorrules + .cursor/rules/*.mdc 구조)

와 같이 커서룰을 만들고 싶은데 방법을 알려줘. 구현은 하지마
```

---

## 부록 B — 구현 진행 프롬프트 (원문)

```markdown
진행
```

---

## 부록 C — Export 요청 프롬프트 (원문)

```markdown
보고서를보내주는 것과 프롬프트 저장을 해줘
```

---

## 부록 D — 03 세션 `.cursorrules` YAML (이전 SSOT, 참고용)

> 04 세션에서 본문은 `.mdc`로 이전됨. 복원 시 `Prompt/03_...` 부록 또는 git history 참고.

최상위 키: `project`, `code_style`, `architecture`, `tdd_rules`, `testing`, `forbidden`, `file_structure`, `ai_behavior` (225줄).
