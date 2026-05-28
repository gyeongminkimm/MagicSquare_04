# MagicSquare_XX

4×4 마방진(Magic Square)을 다루는 학습·실습 프로젝트입니다.  
현재 단계는 **구현 이전의 문제 인식·정의**(STEP 1–5)이며, 소스 코드는 아직 없습니다.

---

## 프로젝트 목적

**4×4 격자**에 **1부터 16**까지를 각 칸에 한 번씩 배치했을 때, 합의한 **관심 선**(행·열·대각선)마다 합이 같아지는 배치를 **일관된 기준으로 판별**하고, 필요하면 그 조건을 만족하는 배치를 **반복·검증·공유 가능한 형태**로 다루는 것이 목표입니다.

단순히 “마방진 프로그램을 만든다”가 아니라, **규칙·불변 조건·판별과 생성의 분리·명확한 입출력 계약**을 훈련하는 것이 핵심입니다.

### 한 줄 정의

> 4×4에 1~16을 한 번씩 배치할 때, **합의된 선들의 합 일치와 숫자 집합 조건**을 명확히 정의하고 일관되게 판별하며, 필요 시 그 조건을 만족하는 배치를 얻는 과정을 **반복·검증·공유 가능하게** 다룬다.

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| 문제 인식·정의 (STEP 1–5) | 완료 |
| 문제 정의 보고서 | [`Report/01_MagicSquare_ProblemDefinition_Report.md`](Report/01_MagicSquare_ProblemDefinition_Report.md) |
| Dual-Track TDD / Clean Architecture 설계 | 완료 — [`Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
| Cursor Rules (모듈형 `.mdc`) | 완료 — [`Report/04_MagicSquare_Modular_CursorRules_Report.md`](Report/04_MagicSquare_Modular_CursorRules_Report.md) |
| 구현·테스트 코드 | 미착수 |

---

## 도메인 요약

| 항목 | 내용 |
|------|------|
| 격자 | 4×4 (16칸) |
| 숫자 | 1 ~ 16, 각 값 1회 |
| 마법합 | 34 (행·열·대각선 기준) |
| 유효성 정책 (현재 가정) | 4행 + 4열 + 2대각선, 합 모두 34 |
| 성공 기준 | 교과서 예시와 **동일한 격자**가 아니라 **규칙 충족** (해는 여러 개 존재) |

---

## 핵심 Invariant (요약)

완성된 유효 배치에서 성립해야 하는 조건입니다. 상세는 보고서 STEP 5를 참고하세요.

- **구조·집합:** 16칸, 값 집합 = {1,…,16}, 중복·누락·범위 밖 없음  
- **합:** 관심하는 모든 선의 합 = 34  
- **판별:** 동일 격자·동일 규칙 → 항상 같은 유효/무효 판단  
- **생성 계약:** 조건을 만족하는 배치를 얻는 결과는 합의된 검사를 통과해야 함  

---

## 문제 정의 워크숍 (STEP 1–5)

| STEP | 주제 | 요지 |
|------|------|------|
| **1** | Observation | 4×4·합 제약과 소프트웨어 목표 사이의 간극 관찰 |
| **2** | Why #1 | “완성”의 의미, 다해, 생성/검증/퍼즐 역할 혼동 주의 |
| **3** | Why #2 | 반복 가능성, 검증 자동화, 오류 방지, 규칙 기반 사고 |
| **4** | Why #3 | TDD로 규칙·역할·불변식·입출력을 설계 전에 고정 |
| **5** | 진짜 문제 정의 | 표면 정의 vs 개선 정의, Invariant, 훈련 사고 능력 |

### 표면 정의 vs 개선 정의

| | 표면 (피할 표현) | 개선 (정확한 초점) |
|---|------------------|---------------------|
| 초점 | 프로그램·출력물 | 규칙·판별·재현 가능한 판단 |
| 성공 | 격자를 만듦 | 합의된 불변 조건 충족 |
| 범위 | 생성만 | 판별 우선, 생성·부분 상태는 선택 |

---

## 설계 원칙 (문제 정의 단계에서 확정한 방향)

1. **판별과 생성 분리** — “맞는지 확인”과 “맞는 배치를 얻기”는 다른 책임  
2. **규칙을 먼저 고정** — 어떤 선까지 검사할지 정책으로 합의  
3. **TDD 친화** — 불변 조건을 관찰 가능한 명세·테스트로 옮길 수 있어야 함  
4. **다해 수용** — 하나의 예시 격자에 과적합하지 않음  

---

## 설계 단계에서 확정한 것 (02 보고서)

- **1순위 시나리오:** 2칸 퍼즐 완성 → `int[6]` 반환  
- **검증 범위:** 행·열·대각선 포함, 마법합 34  
- **입력 표현:** `int[4][4]`, `0`=빈칸(정확히 2개)  
- **아키텍처:** Dual-Track (Domain ∥ UI Boundary) + Clean Architecture + Repository(메모리 1차)

## 아직 구현 전인 것

- Domain / UI / Data / Integration **테스트 코드**  
- F3(UNSOLVABLE) 픽스처 숫자 고정  
- File 기반 Repository (2차)

---

## 디렉터리 구조

```
MagicSquare_XX/
├── README.md
├── .cursorrules                          # Rules 인덱스
├── .cursor/rules/                        # magicsquare-*.mdc (5종)
├── Report/
│   ├── 01_MagicSquare_ProblemDefinition_Report.md
│   ├── 02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md
│   ├── 03_MagicSquare_CursorRules_And_InitialImplementation_Report.md
│   └── 04_MagicSquare_Modular_CursorRules_Report.md
├── Prompt/
│   ├── 02_MagicSquare_DualTrack_TDD_Design_Prompt.md
│   ├── 03_MagicSquare_CursorRules_UserEntity_Prompt.md
│   └── 04_MagicSquare_Modular_CursorRules_Prompt.md
└── Prompting/
    └── 01_MagicSquare_ProblemDefinition_Report_Prompt.md
```

---

## 문서

- **문제 정의:** [Report/01_...](Report/01_MagicSquare_ProblemDefinition_Report.md) — STEP 1–5, Invariant  
- **TDD 설계:** [Report/02_...](Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) — Domain/UI/Data/통합, RED 목록, Traceability  
- **Cursor Rules (초기·User):** [Report/03_...](Report/03_MagicSquare_CursorRules_And_InitialImplementation_Report.md)  
- **Cursor Rules (모듈형 `.mdc`):** [Report/04_...](Report/04_MagicSquare_Modular_CursorRules_Report.md)  
- **프롬프트 Export:** [Prompt/02_...](Prompt/02_MagicSquare_DualTrack_TDD_Design_Prompt.md), [Prompt/03_...](Prompt/03_MagicSquare_CursorRules_UserEntity_Prompt.md), [Prompt/04_...](Prompt/04_MagicSquare_Modular_CursorRules_Prompt.md)

---

## 다음 단계 (권장 순서)

1. 02 보고서 **DOM-P0 / UI-P0** RED부터 Dual-Track TDD  
2. F3(UNSOLVABLE) 픽스처 확정  
3. INT-N-01 E2E 통과 후 Data·File Repository 확장  

---

## 라이선스 / 기여

(미정 — 필요 시 추가)
