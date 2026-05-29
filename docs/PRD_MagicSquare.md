# PRD — Magic Square 4x4 TDD Practice

## 1. Executive Summary
Magic Square 4x4 프로젝트의 목적은 알고리즘 난이도 경쟁이 아니라, 불변식 기반 사고와 계약 기반 개발 역량을 훈련하는 것이다. 본 PRD는 구현 전에 입력/출력 계약, Boundary/Domain 책임 분리, Dual-Track UI + Logic TDD, RED-GREEN-REFACTOR 흐름, Concept-to-Code Traceability를 고정한다. 이 문서는 “정답 격자 생성”보다 “검증 가능한 규칙 충족”을 성공 기준으로 정의하며, 구현·테스트·리팩토링의 기준선으로 사용한다.

---

## 2. Background
4x4 마방진 문제는 수학 퍼즐처럼 보이지만, 실제 개발에서 학습자가 반복적으로 실패하는 지점은 규칙 자체가 아니라 규칙을 코드 계약으로 고정하는 과정이다. 학습자는 구현을 먼저 시작하고, 테스트 기준을 뒤늦게 정하며, Boundary와 Domain 책임을 섞는 경향이 있다. 결과적으로 리팩토링 이후 계약이 깨져도 원인을 추적하지 못한다. 본 프로젝트는 이 문제를 해결하기 위해 “문제 정의 → 계약 고정 → Dual-Track TDD → 회귀 보호” 순서를 강제한다.

---

## 3. Problem Statement
본 프로젝트의 문제는 “마방진을 만든다”가 아니다.  
본 프로젝트의 문제는 다음 문장으로 정의한다.

- **문제 정의:** 4x4 입력에서 고정된 불변식(값 집합, 합 규칙, 좌표 규칙, 포맷 규칙)을 항상 검증 가능하게 유지하면서, 두 빈칸 퍼즐을 결정론적으로 해결하는 계약을 완성한다.
- **핵심 관점:** 성공은 특정 격자와의 일치가 아니라 계약 충족 여부로 판단한다.
- **입출력 계약 중요성:** TDD는 관찰 가능한 계약이 있어야 RED/GREEN 판단이 가능하다. 입력 계약과 출력 계약이 고정되어야 회귀 테스트가 성립한다.

---

## 4. Why Now / Why Chain
- **Why Now:** 구현 전 기준 문서가 없으면 팀 내 요구사항 해석이 달라지고, 테스트가 명세 대신 구현 추종으로 변질된다.
- **Why #1 (완성 기준):** “완성” 정의가 불명확하면 검증 기준이 흔들린다.
- **Why #2 (프로그램화):** 반복 실행, 자동 검증, 오류 재현을 위해 프로그램화가 필요하다.
- **Why #3 (TDD):** 규칙 해석·역할 경계·다해 처리 정책을 테스트 가능한 계약으로 고정하기 위해 TDD가 필요하다.
- **닫아야 하는 문제**
  - 구현 선행으로 인한 계약 누락
  - 테스트 기준 불명확
  - Boundary/Domain 책임 혼합
  - 리팩토링 후 계약 파손

---

## 5. Target Users
- **TDD 학습자:** RED-GREEN-REFACTOR를 실전으로 훈련하려는 개발자
- **코드 리뷰어:** 계약·불변식·레이어 경계를 기준으로 리뷰하려는 개발자
- **아키텍처 학습자:** Clean Architecture + ECB 분리를 훈련하려는 개발자

**사용 환경**
- 콘솔 실행 또는 테스트 실행 중심
- UI, DB, Web 런타임 의존성 없음

---

## 6. Vision & Epic Goal
- **Vision:** 불변식 기반 사고를 코드 계약과 테스트 추적성으로 전환하는 학습 시스템을 구축한다.
- **Epic Goal:** **“불변식 기반 사고 훈련 시스템 구축”**
- **Epic Success Criteria**
  - 입력/출력 계약 위반을 Boundary에서 차단
  - Domain 불변식 검증 로직 분리
  - Dual-Track TDD 진행 기록 가능
  - Concept → Rule → Use Case → Contract → Test → Component 추적 가능

---

## 7. Persona
- TDD를 학습 중이며 RED 작성 습관이 약한 개발자
- Clean Architecture 계층 분리를 실습으로 이해하려는 개발자
- 알고리즘 정답보다 설계·계약·테스트·리팩토링 흐름을 훈련하려는 사용자

---

## 8. User Journey Summary

| Stage | 핵심 활동 | Pain Point | Learning Outcome |
|---|---|---|---|
| 1. 문제 인식 | “정답 생성”이 아닌 “규칙 검증”으로 재정의 | 목표를 구현 산출물로만 해석 | 불변식 중심 문제 정의 |
| 2. 계약 정의 | 입력/출력/오류 계약 고정 | 테스트 기준이 케이스별로 흔들림 | 계약 우선 설계 습관 |
| 3. 도메인 분리 | Blank/Missing/Validate/Solve 분리 | 책임이 한 함수에 집중 | ECB 책임 분리 이해 |
| 4. Dual-Track TDD | Track A/B RED 병렬 진행 | Domain 완성 후 Boundary 붙이기 관성 | 병렬 RED/GREEN 운영 |
| 5. 회귀 보호 | 규칙-테스트 추적성 관리 | 리팩토링 후 계약 파손 탐지 실패 | Traceability 기반 회귀 방어 |

---

## 9. Scope

### 9.1 In-Scope
- 빈칸 좌표 탐색
- 누락 숫자 탐색
- 마방진 판정
- 두 조합 시도 후 결과 반환
- Boundary 입력 검증
- 출력 계약 검증
- RED-GREEN-REFACTOR 흐름에서 테스트 가능 요구사항 명세

### 9.2 Out-of-Scope
- UI 화면 개발
- DB 저장/검색
- Web/API 서버 개발
- N×N 일반화
- 완전한 마방진 생성 알고리즘
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔
- 외부 서비스 연동

---

## 10. Functional Requirements

### FR-01 Input Verification
- **Description:** 입력 행렬의 구조·값·중복·빈칸 개수를 Boundary에서 검증한다.
- **Layer:** Boundary
- **Input:** `int[4][4]`
- **Processing Rules:**
  - 4x4 크기 확인
  - 값 범위 `0` 또는 `1..16` 확인
  - `0` 개수 정확히 2개 확인
  - `0` 제외 중복 금지 확인
- **Output:** 성공 시 Domain 전달, 실패 시 표준 오류 반환
- **Acceptance Criteria:**
  - AC-01: 4x4가 아니면 실패한다.
  - AC-02: 값 범위 위반이 있으면 실패한다.
  - AC-03: 빈칸 개수가 2가 아니면 실패한다.
  - AC-04: `0` 제외 중복이 있으면 실패한다.
  - AC-05: AC-01~04 실패 시 Domain resolver를 호출하지 않는다.
- **Error / Exception Policy:** `ERR_INVALID_DIMENSION`, `ERR_INVALID_VALUE`, `ERR_BLANK_COUNT`, `ERR_DUPLICATE_VALUE`
- **Related Business Rules:** BR-01, BR-02, BR-03, BR-04
- **Related Test Direction:** Track A 입력 검증/미호출 검증
- **Component Candidate:** `BoundaryValidator`

### FR-02 Blank Coordinate Discovery
- **Description:** row-major 순서에서 첫 번째/두 번째 빈칸 좌표를 확정한다.
- **Layer:** Domain
- **Input:** 검증 통과한 4x4 행렬
- **Processing Rules:**
  - 행 우선 스캔으로 `0` 위치 2개 추출
  - 첫 번째 발견 좌표를 `pos1`, 두 번째를 `pos2`로 고정
- **Output:** `(pos1, pos2)` (도메인 내부 좌표)
- **Acceptance Criteria:**
  - AC-06: 빈칸 좌표 2개를 순서 포함으로 반환한다.
  - AC-07: `pos1`은 row-major에서 최초 `0` 좌표다.
  - AC-08: 동일 입력에서 동일 좌표 순서를 반환한다.
- **Error / Exception Policy:** 입력 계약 위반은 FR-01에서 차단
- **Related Business Rules:** BR-05
- **Related Test Direction:** Track B 빈칸 탐색/결정론 테스트
- **Component Candidate:** `BlankFinder`

### FR-03 Missing Number Discovery
- **Description:** `1..16` 대비 누락 숫자 2개를 오름차순으로 확정한다.
- **Layer:** Domain
- **Input:** 검증 통과한 4x4 행렬
- **Processing Rules:**
  - `0` 제외 값 집합 계산
  - 누락 집합 크기 2 확인
  - 누락 숫자 오름차순 정렬
- **Output:** `(small, large)`
- **Acceptance Criteria:**
  - AC-09: 누락 숫자 2개를 반환한다.
  - AC-10: 반환 순서는 항상 오름차순이다.
  - AC-11: 동일 입력에서 동일 결과를 반환한다.
- **Error / Exception Policy:** 계약 위반은 Boundary 선차단
- **Related Business Rules:** BR-06, BR-07
- **Related Test Direction:** Track B 누락 숫자/정렬/결정론 테스트
- **Component Candidate:** `MissingNumberFinder`

### FR-04 Magic Square Validation
- **Description:** 완성 격자가 마방진 불변식을 만족하는지 판정한다.
- **Layer:** Domain
- **Input:** 0이 없는 4x4 완성 격자
- **Processing Rules:**
  - 마방진 상수 `34` 사용
  - 4개 행, 4개 열, 2개 대각선 합 검증
- **Output:** `valid` / `invalid`
- **Acceptance Criteria:**
  - AC-12: 10개 선 합이 모두 34이면 유효다.
  - AC-13: 하나라도 34가 아니면 무효다.
  - AC-14: 동일 입력에 동일 판정을 반환한다.
- **Error / Exception Policy:** 검증 대상이 완성 격자가 아니면 무효 처리 정책 적용
- **Related Business Rules:** BR-08, BR-09
- **Related Test Direction:** Track B 행/열/대각선 판정 테스트
- **Component Candidate:** `MagicSquareValidator`

### FR-05 Two-Combination Solver and Result Formatting
- **Description:** 두 조합을 순차 시도해 성공 조합을 `int[6]` 포맷으로 반환한다.
- **Layer:** Domain + Boundary(출력 계약 점검)
- **Input:** FR-01 통과 입력
- **Processing Rules:**
  - Attempt 1: `small -> pos1`, `large -> pos2`
  - Attempt 2: Attempt 1 실패 시 `large -> pos1`, `small -> pos2`
  - 성공한 첫 조합을 선택
  - 결과를 `[r1,c1,n1,r2,c2,n2]` 1-index로 반환
- **Output:** `int[6]`
- **Acceptance Criteria:**
  - AC-15: Attempt 1 유효 시 Attempt 1 결과를 반환한다.
  - AC-16: Attempt 1 무효, Attempt 2 유효 시 Attempt 2 결과를 반환한다.
  - AC-17: 두 조합 모두 무효면 정의된 실패 정책을 반환한다.
  - AC-18: 반환 배열 길이는 6이다.
  - AC-19: 좌표는 1-index 범위 `1..4`다.
  - AC-20: `n1`, `n2`는 누락 숫자 2개다.
- **Error / Exception Policy:** Domain `UNSOLVABLE_PUZZLE` 발생, Boundary `ERR_UNSOLVABLE` 변환
- **Related Business Rules:** BR-10, BR-11, BR-12, BR-13
- **Related Test Direction:** Track B 조합 성공/실패 + Track A 출력 계약
- **Component Candidate:** `Solver`, `ResultFormatter`

---

## 11. Business Rules / Domain Rules

- **BR-01:** 입력은 항상 4행 4열 정수 행렬이어야 한다.
- **BR-02:** 빈칸 값 `0`은 항상 정확히 2개여야 한다.
- **BR-03:** 각 셀 값은 항상 `0` 또는 `1..16` 범위여야 한다.
- **BR-04:** `0`을 제외한 숫자는 항상 중복되면 안 된다.
- **BR-05:** 첫 번째 빈칸은 항상 row-major 스캔에서 처음 발견된 `0`이다.
- **BR-06:** 누락 숫자 집합의 크기는 항상 2여야 한다.
- **BR-07:** 누락 숫자 쌍은 항상 오름차순 `(small, large)`로 정의한다.
- **BR-08:** 마방진 상수는 항상 `34`다.
- **BR-09:** 유효한 완성 격자는 항상 4행, 4열, 2대각선 합이 모두 `34`다.
- **BR-10:** Solver는 항상 Attempt 1을 먼저 수행해야 한다.
- **BR-11:** Attempt 1 실패 시 Solver는 항상 Attempt 2를 수행해야 한다.
- **BR-12:** 성공 결과 좌표는 항상 1-index로 반환해야 한다.
- **BR-13:** 성공 결과 형식은 항상 `int[6] = [r1,c1,n1,r2,c2,n2]`여야 한다.
- **BR-14:** 동일 입력은 항상 동일 출력 또는 동일 실패를 반환해야 한다.
- **BR-15:** 입력 행렬은 처리 전후 값이 동일해야 하며, 함수 내부에서 원본을 변경하면 안 된다.

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code 또는 Failure Policy |
|---|---|---|---|---|---|
| `grid` | `int[4][4]` | 4x4 고정 | `[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]` | `[[1,2],[3,4]]` | `ERR_INVALID_DIMENSION` |
| cell value | `int` | `0` 또는 `1..16` | `0`, `1`, `16` | `-1`, `17` | `ERR_INVALID_VALUE` |
| blank count | `int` | `0` 개수 = 2 | F1/F2 입력 | 0이 1개 또는 3개 | `ERR_BLANK_COUNT` |
| non-zero uniqueness | set rule | `0` 제외 중복 금지 | 비0 14개 고유 | `... [5,5] ...` | `ERR_DUPLICATE_VALUE` |

### 12.2 Output Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code 또는 Failure Policy |
|---|---|---|---|---|---|
| result | `int[6]` | 길이 6 | `[1,2,3,2,3,11]` | `[1,2,3]` | `ERR_INTERNAL` |
| `r1,c1,r2,c2` | `int` | 1-index `1..4` | `1,2,2,3` | `0,2,5,1` | `ERR_INTERNAL` |
| `n1,n2` | `int` | 누락 숫자 2개, 서로 다름 | `3,11` | `3,3` | `ERR_INTERNAL` |
| ordering | rule | FR-05 시도 순서 준수 | F1: Attempt 1 성공 | 순서 무시 | `ERR_INTERNAL` |

---

## 13. Error / Failure Policy

| Error Code | Message | Layer | Domain resolver 호출 여부 | Related Acceptance Criteria |
|---|---|---|---|---|
| `ERR_INVALID_DIMENSION` | `Grid must be 4x4.` | Boundary | No | AC-01, AC-05 |
| `ERR_BLANK_COUNT` | `Grid must contain exactly 2 blank cells (0).` | Boundary | No | AC-03, AC-05 |
| `ERR_INVALID_VALUE` | `Cell value must be 0 or between 1 and 16.` | Boundary | No | AC-02, AC-05 |
| `ERR_DUPLICATE_VALUE` | `Duplicate non-zero value is not allowed.` | Boundary | No | AC-04, AC-05 |
| `ERR_UNSOLVABLE` | `No valid magic square can be formed with two blanks.` | Boundary (from Domain) | Yes | AC-17 |
| `UNSOLVABLE_PUZZLE` | Domain internal failure for both attempts invalid | Domain | Yes | AC-17 |

**고정 정책**
- 입력 검증 실패는 Boundary에서 종료한다.
- 입력 검증 실패 시 Domain resolver는 호출하지 않는다.
- 두 조합 모두 실패 시 Domain은 `UNSOLVABLE_PUZZLE`을 발생시키고, Boundary는 `ERR_UNSOLVABLE`로 변환한다.

---

## 14. Non-Functional Requirements

- **NFR-01 Coverage (Domain):** Domain Logic branch coverage는 95% 이상이어야 한다.
- **NFR-02 Coverage (Boundary):** Boundary Validation branch coverage는 85% 이상이어야 한다.
- **NFR-03 Deterministic Execution:** 동일 입력은 항상 동일 출력 또는 동일 오류를 반환해야 한다.
- **NFR-04 No Side Effects:** 입력 행렬 원본은 변경하면 안 된다.
- **NFR-05 Performance:** 4x4 단일 실행은 50ms 이내여야 한다.
- **NFR-06 Maintainability:** Boundary와 Domain 책임은 분리되어야 한다.
- **NFR-07 Maintainability:** 설명 없는 매직 넘버를 금지하고 명명된 상수를 사용해야 한다.
- **NFR-08 Maintainability:** Domain은 UI/DB/Web/파일시스템에 의존하면 안 된다.
- **NFR-09 Testability:** 모든 FR은 Acceptance Criteria로 검증 가능해야 한다.

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD
- 입력 검증 테스트를 RED로 시작한다.
- 출력 형식 테스트를 RED로 시작한다.
- 실패 응답 코드/메시지 테스트를 RED로 시작한다.
- 입력 오류 시 Domain resolver 미호출 테스트를 RED로 시작한다.

### 15.2 Track B — Domain / Logic TDD
- 빈칸 탐색 테스트를 RED로 시작한다.
- 누락 숫자 탐색 테스트를 RED로 시작한다.
- 마방진 검증 테스트를 RED로 시작한다.
- small-first 성공 테스트를 RED로 시작한다.
- small-first 실패 후 reverse 성공 테스트를 RED로 시작한다.
- 두 조합 모두 실패 테스트를 RED로 시작한다.

### 15.3 Parallel Progression Rules
- UI RED와 Logic RED를 분리한다.
- UI GREEN과 Logic GREEN은 각각 최소 구현으로 완료한다.
- 구조 개선은 REFACTOR 단계에서만 수행한다.
- Domain 전량 구현 후 Boundary를 결합하는 순차 개발을 금지한다.
- 테스트 약화, 삭제, skip/xfail로 GREEN을 만드는 행위를 금지한다.

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios
- NS-01: small-first 성공
- NS-02: small-first 실패 후 reverse 성공

### 16.2 Exception Scenarios
- ES-01: 4x4가 아닌 입력
- ES-02: 빈칸 개수 오류
- ES-03: 값 범위 오류
- ES-04: 중복 숫자 오류
- ES-05: 두 조합 모두 실패

### 16.3 Boundary Scenarios
- BS-01: 최소값 1 검증
- BS-02: 최대값 16 검증
- BS-03: `0`은 빈칸으로만 처리
- BS-04: 출력 좌표 1-index 검증
- BS-05: 반환 배열 길이 6 검증

### 16.4 Representative Test Data

| Data ID | 목적 | Matrix / Value |
|---|---|---|
| TD-01 | small-first 성공(F1) | `[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]` |
| TD-02 | reverse 성공(F2) | `[[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]` |
| TD-03 | invalid size | `[[1,2],[3,4]]` |
| TD-04 | invalid blank count | `[[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]` |
| TD-05 | duplicate value | `[[16,0,2,13],[5,10,5,8],[9,6,0,12],[4,15,14,1]]` |
| TD-06 | invalid range | `[[16,0,2,13],[5,10,17,8],[9,6,0,12],[4,15,14,1]]` |
| TD-07 | unsolvable two attempts | **Decision Needed (F3 fixture 미확정)** |

---

## 17. Architecture Overview, High-Level

- **Boundary Layer**
  - 입력 검증
  - 오류 응답 코드/메시지 반환
  - 출력 포맷 검증
- **Domain Layer**
  - 빈칸 탐색
  - 누락 숫자 탐색
  - 마방진 판정
  - 두 조합 해결 로직
- **Control / Application Layer**
  - Boundary와 Domain 호출 순서 조정
  - 오류 전달 흐름 표준화

**의존 방향**
- `Boundary → Control → Domain`
- Domain은 Boundary를 알지 않는다.
- Domain은 UI, DB, Web, 파일시스템에 의존하지 않는다.

---

## 18. Component Candidates

| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| `BoundaryValidator` | 입력 계약 검증, 조기 실패 | Boundary | `int[4][4]` | valid / error | FR-01 | ES-01~04, BS-01~03 |
| `BlankFinder` | row-major 빈칸 2개 탐색 | Domain | validated grid | `pos1,pos2` | FR-02 | NS-01/02 좌표 검증 |
| `MissingNumberFinder` | 누락 숫자 2개 오름차순 계산 | Domain | validated grid | `small,large` | FR-03 | NS-01/02 누락값 검증 |
| `MagicSquareValidator` | 10개 선 합 34 판정 | Domain | completed grid | valid/invalid | FR-04 | NS-01/02, ES-05 |
| `Solver` | Attempt 1/2 실행 및 성공 선택 | Domain | validated grid | assignment or unsolvable | FR-05 | NS-01/02, ES-05 |
| `ResultFormatter` | 1-index `int[6]` 변환 | Boundary/Domain output contract | assignment | `int[6]` | FR-05 | BS-04/05 |

---

## 19. Risks & Ambiguities

| Risk | Impact | Decision / Mitigation |
|---|---|---|
| 1-index vs 0-index 혼동 | 좌표 오류, 회귀 발생 | BR-12/BR-13 고정, BS-04 필수 |
| row-major 첫 빈칸 정의 누락 | Attempt 순서가 달라짐 | BR-05 명시, FR-02 AC-07 필수 |
| small-first/reverse 데이터 혼동 | 잘못된 기대값으로 테스트 오염 | TD-01/TD-02를 기준 데이터로 고정 |
| 입력 행렬 변경 여부 불명확 | 부작용으로 테스트 불안정 | NFR-04로 원본 불변 고정 |
| 두 조합 실패 정책 누락 | 에러 처리 일관성 붕괴 | Domain `UNSOLVABLE_PUZZLE` + Boundary `ERR_UNSOLVABLE`로 확정 |
| 상수 34 하드코딩 확산 | 유지보수 난이도 증가 | BR-08 + NFR-07 적용 |
| Boundary/Domain 책임 혼합 | 테스트 추적성 붕괴 | ECB 의존 방향 강제, Track A/B 분리 운영 |

---

## 20. Engineering Principles

- PEP8 준수
- 모든 공개 함수 type hints 필수
- pytest 사용
- AAA 패턴 사용
- Coverage 목표: Domain 95%+, Boundary 85%+
- ECB 레이어 분리 준수
- RED-GREEN-REFACTOR 준수
- `print()` 디버깅 금지
- bare `except` 금지
- 테스트 약화/삭제/skip/xfail로 통과시키기 금지
- 설명 없는 magic number 금지
- Boundary 테스트에서 Domain 로직 복제 금지
- Domain 계층의 외부 의존 금지

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4x4 입력 | BR-01 | FR-01 | AC-01, AC-05 | ES-01 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | AC-03, AC-05 | ES-02 | BoundaryValidator |
| 값 범위 0 또는 1~16 | BR-03 | FR-01 | AC-02, AC-05 | ES-03, BS-01, BS-02 | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | AC-04, AC-05 | ES-04 | BoundaryValidator |
| row-major 첫 번째 빈칸 | BR-05 | FR-02 | AC-07 | NS-01/02 좌표 검증 | BlankFinder |
| 누락 숫자 2개 | BR-06 | FR-03 | AC-09 | NS-01/02 누락값 검증 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-07 | FR-03 | AC-10 | NS-01/02 정렬 검증 | MissingNumberFinder |
| 마방진 상수 34 | BR-08 | FR-04 | AC-12, AC-13 | NS-01/02, ES-05 | MagicSquareValidator |
| 행/열/대각선 합 | BR-09 | FR-04 | AC-12, AC-13 | NS-01/02, ES-05 | MagicSquareValidator |
| small-first 시도 | BR-10 | FR-05 | AC-15 | NS-01 | Solver |
| reverse 시도 | BR-11 | FR-05 | AC-16 | NS-02 | Solver |
| int[6] 반환 | BR-13 | FR-05 | AC-18, AC-20 | BS-05, NS-01/02 | ResultFormatter |
| 1-index 좌표 | BR-12 | FR-05 | AC-19 | BS-04 | ResultFormatter |
| 결정론 보장 | BR-14 | FR-02~05 | AC-08, AC-11, AC-14 | 반복 실행 동일성 | BlankFinder/MissingNumberFinder/MagicSquareValidator/Solver |
| 입력 불변성 | BR-15 | FR-01~05 | AC-05 + NFR-04 | 입력 전후 동일성 | BoundaryValidator/Solver |

---

## 22. Open Questions / Decision Needed

1. **Decision Needed — F3 unsolvable fixture 확정**
   - 두 조합 모두 실패를 재현하는 표준 입력 행렬(F3)이 아직 고정되지 않았다.
   - PRD 승인 전에 TD-07을 확정해야 ES-05가 폐쇄된다.

2. **Decision Needed — 문서 명칭 정합**
   - 참조 문서 요청명(`Report/4.UserJourney...`)과 실제 저장소 파일명(`Report/06_...`)이 다르다.
   - PRD 참고 문헌 표기에서 단일 표준명을 확정해야 한다.

3. **Decision Needed — Coverage 정책 단일 표기**
   - 일부 규칙 문서에는 최소 80%가 존재한다.
   - 본 PRD는 Domain 95%+, Boundary 85%+를 기준으로 정의한다.
   - CI 게이트를 “레이어별+전역”으로 병행할지 단일 지표로 운영할지 확정이 필요하다.

4. **Decision Needed — Control 계층 필수 여부**
   - 현재 범위에서 Control을 얇은 오케스트레이션 계층으로 둘지, Boundary가 직접 Domain을 호출할지 확정이 필요하다.

---

## 23. Appendix

### 23.1 참고 문서 목록
- `Report/01_MagicSquare_ProblemDefinition_Report.md`
- `Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`
- `Report/03_MagicSquare_CursorRules_And_InitialImplementation_Report.md`
- `Report/06_MagicSquare_UserJourney_Level1-5_Verification_Report.md` *(요청명 Report/4 대응)*
- `.cursorrules`
- `.cursor/rules/magicsquare-project.mdc`
- `.cursor/rules/magicsquare-forbidden.mdc`
- `.cursor/rules/magicsquare-ecb-architecture.mdc`
- `.cursor/rules/magicsquare-tdd-testing.mdc`
- `.cursor/rules/magicsquare-python-code-style.mdc`

### 23.2 Cursor Rules 요약
- 프로젝트 계약(F1/F2/F3, I/O, AI 절차)
- 금지 패턴(print, bare except, 테스트 약화, 매직 넘버)
- ECB 의존 방향 강제
- Dual-Track TDD 단계 규칙
- Python 스타일(type hints, docstring, naming)

### 23.3 대표 Gherkin Scenario 요약
- **Scenario A:** 유효 입력(F1)에서 small-first 조합이 성공하면 `int[6]` 반환
- **Scenario B:** 유효 입력(F2)에서 small-first 실패 후 reverse 성공하면 reverse 결과 반환
- **Scenario C:** 입력이 4x4가 아니면 Boundary가 즉시 `ERR_INVALID_DIMENSION` 반환, Domain 미호출
- **Scenario D:** 두 조합 모두 실패하면 Domain `UNSOLVABLE_PUZZLE`, Boundary `ERR_UNSOLVABLE`

### 23.4 향후 RED Test ID 후보
- **Track A (Boundary):** `RED-BND-VAL-001`~`RED-BND-VAL-005`
- **Track B (Domain):** `RED-DOM-BLK-001`, `RED-DOM-MISS-001`, `RED-DOM-VAL-001`, `RED-DOM-SOL-001`~`003`
- **Integration:** `RED-INT-F1-001`, `RED-INT-F2-001`, `RED-INT-ERR-001`
