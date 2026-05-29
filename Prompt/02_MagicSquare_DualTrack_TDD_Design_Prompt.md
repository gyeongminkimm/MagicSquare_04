# 4×4 Magic Square — Dual-Track TDD 설계 (대화형 프롬프트 Export)
_Exported on 2026-05-28 from Cursor — MagicSquare_XX spec/design 세션_

**산출물 링크**

| 산출물 | 경로 |
|--------|------|
| Dual-Track / Clean Architecture TDD 설계 보고서 | [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](../Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
| 문제 정의 보고서 (전제) | [`Report/01_MagicSquare_ProblemDefinition_Report.md`](../Report/01_MagicSquare_ProblemDefinition_Report.md) |

---

**User**

너는 Cursor.AI용 프롬프트 설계자다.
나는 Magic Square 4x4 TDD 설계 문서를 만들기 위한 프롬프트가 필요하다.
지금 설계 문서를 만들지 말고,그 설계 문서를 만들 수 있는 실행용 프롬프트만 작성하라.

---

**Cursor**

(설계 문서는 작성하지 않음 — **실행용 프롬프트만** 제공)

아래 블록 전체를 Cursor 새 채팅에 붙여 넣어 `Report/02_MagicSquare_TDD_Design.md`를 생성하도록 실행한다.

```markdown
당신은 **4×4 Magic Square TDD 설계 문서**를 작성하는 **테스트 주도 설계(TDD) 명세 설계자**입니다.

## 이번 턴의 목표 (하나만)

**`Report/02_MagicSquare_TDD_Design.md`** 한 편의 **TDD 설계 문서**를 완성한다.

- 지금은 **구현·프로덕션 코드·테스트 코드 파일 생성 금지**
- **알고리즘·자료구조 구현 상세·클래스 다이어그램·프레임워크 설정** 금지
- **문제 인식·Why 워크숍(STEP 1–5) 재작성 금지** — 이미 완료된 내용은 **인용·정렬**만 한다

작업 전에 반드시 읽을 것:

1. `README.md`
2. `Report/01_MagicSquare_ProblemDefinition_Report.md`

(… §0~§8, RED 15개+, Invariant 매핑, 품질 바 등 전체 실행 프롬프트 본문 — 생략 없이 원문은 이 세션 첫 응답에 포함됨)

위 품질 바를 모두 만족한 뒤에만 파일을 저장하고 마친다.
```

**사용 방법:** 새 채팅 → 붙여넣기 → `Report/02_MagicSquare_TDD_Design.md` 생성.

> **참고:** 이후 세션에서는 Dual-Track 설계로 범위가 확장되어, 최종 보고서 파일명은 `02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`로 정리됨.

---

**User**

당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.
프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련
제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만
- 입력/출력은 명확히 고정
입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지
출력 계약:
- int[6]
- 좌표는 1-index
- 반환 형식: [r1,c1,n1,r2,c2,n2]
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

------------------------------------------------------------
출력 형식 (반드시 이 구조로)
------------------------------------------------------------
# 1) Logic Layer (Domain Layer) 설계
## 1.1 도메인 개념
## 1.2 도메인 불변조건(Invariants)
## 1.3 핵심 유스케이스(도메인 관점)
## 1.4 Domain API(내부 계약)
## 1.5 Domain 단위 테스트 설계(RED 우선)

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)
## 2.1 사용자/호출자 관점 시나리오
## 2.2 UI 계약(외부 계약)
## 2.3 UI 레벨 테스트(Contract-first, RED 우선)
## 2.4 UX/출력 규칙

# 3) Data Layer 설계
## 3.1 목적 정의
## 3.2 인터페이스 계약
## 3.3 구현 옵션 비교(메모리/파일)
## 3.4 Data 레이어 테스트

# 4) Integration & Verification
## 4.1 통합 경로 정의
## 4.2 통합 테스트 시나리오
## 4.3 회귀 보호 규칙
## 4.4 커버리지 목표
## 4.5 Traceability Matrix (필수)

추가 조건:
- 모호한 표현 금지
- 모든 규칙은 검증 가능해야 함
- 구현 코드 작성 금지
- 표/체크리스트 적극 사용

---

**Cursor**

Dual-Track UI + Logic TDD / Clean Architecture 설계를 **채팅 본문**으로 작성함.

**주요 고정 사항**

| 항목 | 내용 |
|------|------|
| 빈칸 순서 | 행 우선 스캔 (1,1)→…→(4,4) |
| 검증 | 행4+열4+대각2, 합 34 |
| F1 | `[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]` → `[1,2,3,2,3,11]` |
| F2 | `[[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]` → `[2,2,10,3,3,7]` |
| Domain RED | ≥20, UI ≥15, Data ≥7, INT ≥6 |
| 커버리지 | Domain 95%+, UI 85%+, Data 80%+ |

**산출:** 이후 사용자 요청에 따라 `Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`로 파일화.

---

**User**

다음의 순서로 실행해줘
1. Report 폴더에 보고서 생성해줘
2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompt 폴더에 Export transcript 해줘

---

**Cursor**

1. **`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`** 생성 완료 (F1/F2 픽스처 수치 검증 포함).
2. **`Prompt/02_MagicSquare_DualTrack_TDD_Design_Prompt.md`** (본 파일) — 세션 User/Cursor 턴 Export.

---

## 재실행용 단일 프롬프트 (요약)

아래를 새 채팅에 붙이면 **보고서만** 다시 생성할 수 있다.

```markdown
`README.md`와 `Report/01_MagicSquare_ProblemDefinition_Report.md`를 읽은 뒤,
구현 코드 없이 `Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`를 작성하라.

전제: Dual-Track UI+Logic TDD, Clean Architecture, 2-blank 퍼즐.
입력: int[4][4], 0=빈칸×2, 값 0|1~16, 비0 중복 금지.
출력: int[6] [r1,c1,n1,r2,c2,n2] 1-index; min→첫빈칸·max→둘째빈칸 유효 시 (n1,n2)=(min,max) else 반대.
빈칸 순서: 행 우선 스캔.

문서 구조: #1 Logic ~ #4 Integration (1.1~4.5 동일), Traceability Matrix 필수.
픽스처 F1→[1,2,3,2,3,11], F2→[2,2,10,3,3,7] 검증 후 명시.
```

---

## 부록 A — 턴 1 실행용 프롬프트 (TDD 설계 문서 생성, 전문)

> 이 세션에서 **설계 문서를 만들지 말고 실행용 프롬프트만** 요청했을 때의 산출물.  
> Dual-Track 설계(02 보고서) 이전 단계용. 파일명은 `Report/02_MagicSquare_TDD_Design.md` 가정.

```markdown
당신은 **4×4 Magic Square TDD 설계 문서**를 작성하는 **테스트 주도 설계(TDD) 명세 설계자**입니다.

## 이번 턴의 목표 (하나만)

**`Report/02_MagicSquare_TDD_Design.md`** 한 편의 **TDD 설계 문서**를 완성한다.

- 지금은 **구현·프로덕션 코드·테스트 코드 파일 생성 금지**
- **알고리즘·자료구조 구현 상세·클래스 다이어그램·프레임워크 설정** 금지
- **문제 인식·Why 워크숍(STEP 1–5) 재작성 금지** — `Report/01_MagicSquare_ProblemDefinition_Report.md`는 **인용·정렬**만

작업 전 필독: `README.md`, `Report/01_MagicSquare_ProblemDefinition_Report.md`

## 필수 섹션

§0 결정 로그(D-1~D-4) | §1 TDD 목적 | §2 도메인 계약·Invariant 매핑 | §3 책임 경계
§4 테스트 전략 | §5 RED 15개+(Given/When/Then) | §6 GREEN/REFACTOR | §7 백로그 | §8 체크리스트

## 품질 바

- RED ≥15, P0 3~5개, I-1~I-12 매핑, D-1~D-4 확정, 구현 코드 0줄

품질 바 충족 후 `Report/02_MagicSquare_TDD_Design.md` 저장.
```
