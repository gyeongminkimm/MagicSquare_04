# Magic Square 4×4 — User Journey Level 1–5 검증 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `06_MagicSquare_UserJourney_Level1-5_Verification_Report` |
| **전제 보고서** | [`01_MagicSquare_ProblemDefinition_Report.md`](01_MagicSquare_ProblemDefinition_Report.md), [`02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
| **작성일** | 2026-05-28 |
| **상태** | 명세·검증 완료 (구현·테스트 코드 미포함) |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [산출물 계층 개요](#2-산출물-계층-개요)
3. [Level 1 Epic 요약](#3-level-1-epic-요약)
4. [Level 2 User Journey 요약](#4-level-2-user-journey-요약)
5. [Level 3 User Stories 요약](#5-level-3-user-stories-요약)
6. [Level 4 Technical Scenarios 요약](#6-level-4-technical-scenarios-요약)
7. [Level 5 검증 결과](#7-level-5-검증-결과)
8. [추적성 매트릭스](#8-추적성-매트릭스)
9. [누락·보강 항목](#9-누락보강-항목)
10. [다음 단계](#10-다음-단계)

---

## 1. 세션 요약

| 단계 | 사용자 요청 | 결과 |
|------|-------------|------|
| 1 | Level 1 Epic (비즈니스·학습 목표만) | Epic 「불변식 기반 사고 훈련 시스템 구축」 정의 |
| 2 | Level 2 User Journey (5 Stage) | Persona·Journey Goal·Stage 1~5·Story 매핑 |
| 3 | Level 3 User Stories (Story 1~5, AC) | Boundary 1 + Domain 4, 테스트 가능 AC |
| 4 | Level 4 Technical Scenarios | SC-DOM-SOL-001, SC-BND-VAL-001~003 |
| 5 | Level 5 Scenario Verification | 적합성 7.4/10, 일부 수정 필요 판정 |
| 6 | Report·Prompting Export | 본 문서, [`Prompting/06_...`](../Prompting/06_MagicSquare_UserJourney_Level1-5_Transcript_Prompt.md) |

**구현·테스트 코드 변경 없음** — Epic → Journey → Story → Scenario 명세·검증만 수행.

---

## 2. 산출물 계층 개요

```
Epic (Level 1)
  └─ User Journey (Level 2) — 5 Stage
       └─ User Stories (Level 3) — US-B-01, US-D-01~04
            └─ Technical Scenarios (Level 4) — 4 scenarios
                 └─ Verification (Level 5) — 추적성·커버리지 검증
                      └─ (다음) RED Test ID / Implementation Task
```

| Level | 산출물 | 식별자 예 |
|-------|--------|-----------|
| 1 | Epic | 「불변식 기반 사고 훈련 시스템 구축」 |
| 2 | User Journey | Stage 1~5 |
| 3 | User Story | US-B-01, US-D-01~04 |
| 4 | Technical Scenario | SC-DOM-SOL-001, SC-BND-VAL-001~003 |
| 5 | Verification | 본 보고서 §7 |

---

## 3. Level 1 Epic 요약

| 항목 | 내용 |
|------|------|
| **제목** | 불변식 기반 사고 훈련 시스템 구축 |
| **비즈니스 목표** | 2칸 퍼즐 완성, 판별·생성 분리, 외부 I/O 계약 고정, Dual-Track 품질 게이트 |
| **학습 목표** | Invariant 중심 설계, Dual-Track TDD, Concept→Invariant→Contract→Test 추적 |
| **성공 기준** | Domain 커버리지 ≥95%, Boundary 입력 계약 100%, named constant, Invariant–테스트 추적, 리팩터 후 계약 불변 |
| **후보 User Story (L2)** | US-L2-01~14 (상수·PuzzleGrid·Validator·Solver·Boundary·회귀 등) |

---

## 4. Level 2 User Journey 요약

| Stage | 목적 | 핵심 학습 성과 |
|-------|------|----------------|
| 1 Problem Recognition | 알고리즘 과제 → 불변식 훈련 과제로 재정의 | I-1, I-4, I-11, I-12 선언 |
| 2 Contract Definition | 입력·출력·오류 계약 선행 | UI-IN/OUT, Error Contract |
| 3 Domain Separation | Blank/Missing/Validate/Solve 분리 | I-P1, I-P2, I-5~I-7, I-O1~O2 |
| 4 Dual-Track TDD | UI RED vs Logic RED 분리 | 최소 GREEN, 안전 REFACTOR |
| 5 Regression Protection | 정상·오류·경계·포맷 회귀 | F1/F2·UNSOLVABLE·ERR 매핑 |

**Persona:** TDD·Clean Architecture 학습자, 정답보다 설계·계약·테스트·리팩토링 흐름 훈련.

---

## 5. Level 3 User Stories 요약

| Story ID | 이름 | Layer | 보호 Contract / Invariant |
|----------|------|-------|---------------------------|
| **US-B-01** | 입력 검증 | Boundary | UI-IN-01~06, Domain 미호출 |
| **US-D-01** | 빈칸 좌표 탐색 | Domain | I-P1, I-11 |
| **US-D-02** | 누락 숫자 탐색 | Domain | I-P2, I-12 |
| **US-D-03** | 마방진 검증 | Domain | I-2~I-8, MAGIC_CONSTANT |
| **US-D-04** | 두 가지 조합 시도 | Domain | I-O1, I-O2, UI-OUT-01~06 |

**픽스처 정합:** F1 → `[1,2,3,2,3,11]`, F2 → `[2,2,10,3,3,7]` (Report 02).

---

## 6. Level 4 Technical Scenarios 요약

| Scenario ID | Layer | Related Story | 핵심 Then |
|-------------|-------|---------------|-----------|
| **SC-DOM-SOL-001** | Domain / Solver | US-D-04 | small-first 실패 → reverse 성공, `[3,3,6,4,4,1]` |
| **SC-BND-VAL-001** | Boundary | US-B-01 | 빈칸 1개 → 검증 실패, Domain 미호출 |
| **SC-BND-VAL-002** | Boundary | US-B-01 | 비0 중복 → 검증 실패, Domain 미호출 |
| **SC-BND-VAL-003** | Boundary | US-B-01 | 값 >16 → 검증 실패, Domain 미호출 |

| RED 후보 | TASK 후보 |
|----------|-----------|
| RED-DOM-SOL-001 | TASK-DOM-SOL-001 |
| RED-BND-VAL-001~003 | TASK-BND-VAL-001~003 |

---

## 7. Level 5 검증 결과

### 7.1 Overall Judgment

| 항목 | 값 |
|------|-----|
| **적합성 점수** | 7.4 / 10 |
| **현재 상태** | 일부 수정 필요 |
| **요약** | Epic→Journey→Story 연결은 양호. Level 4 Scenario가 Story AC 전체를 아직 닫지 못함. |

### 7.2 일관성 검증 요약

| 구간 | 판정 | 비고 |
|------|------|------|
| Epic → Journey | ✅ | 성공 기준·Dual-Track·회귀가 Stage에 반영 |
| Journey → Story | ⚠️ | Stage 1 전용 Story 없음(간접 반영) |
| Story → Scenario | ❌ | Story 2·3·4 및 일부 AC 미변환 |
| Edge Case | ⚠️ | reverse 성공·입력 오류 3종은 있음; 차원·small-first 성공·UNSOLVABLE 부재 |
| Dual-Track TDD | ✅ | Boundary/Domain 분리 가능 |
| Implementation | ✅ | 컴포넌트 분리·하드코딩 금지 원칙 준수 가능 |

### 7.3 Invariant Coverage (Level 4 기준)

| Invariant | Scenario 커버 |
|-----------|---------------|
| 빈칸 정확히 2개 | ✅ SC-BND-VAL-001 |
| 값 0 또는 1~16 | ✅ SC-BND-VAL-003 |
| 비0 중복 금지 | ✅ SC-BND-VAL-002 |
| 행/열/대각선 합 34 | ✅ SC-DOM-SOL-001 (2차 성공) |
| int[6], 1-index | ✅ SC-DOM-SOL-001 |
| 입력 4×4 | ❌ 시나리오 없음 |
| 누락 2개·오름차순 | ❌ 시나리오 없음 |

---

## 8. 추적성 매트릭스

| Epic Goal | Journey Stage | User Story | Technical Scenario | RED (후보) | TASK (후보) |
|-----------|---------------|------------|-------------------|------------|-------------|
| 계약 우선 입력 방어 | Stage 2 | US-B-01 | SC-BND-VAL-001~003 | RED-BND-VAL-001~003 | TASK-BND-VAL-001~003 |
| 조합 시도 규칙 | Stage 3~4 | US-D-04 | SC-DOM-SOL-001 | RED-DOM-SOL-001 | TASK-DOM-SOL-001 |
| 마방진 불변식 | Stage 3 | US-D-03 | SC-DOM-SOL-001 (부분) | RED-DOM-VAL-001 (추가) | TASK-DOM-VAL-001 (추가) |
| 빈칸·누락 도출 | Stage 3 | US-D-01, US-D-02 | (미작성) | RED-DOM-BLK/MISS (추가) | TASK-DOM-BLK/MISS (추가) |
| 회귀 보호 | Stage 5 | US-B-01~US-D-04 | 일부 | RED 세트 확장 | TASK 세트 확장 |

---

## 9. 누락·보강 항목

| 항목 | 권장 조치 |
|------|-----------|
| 4×4 차원 오류 | `SC-BND-VAL-004` + `RED-BND-VAL-004` |
| BlankFinder row-major | `SC-DOM-BLK-001` (F1/F2 좌표) |
| MissingNumber 오름차순 | `SC-DOM-MISS-001` (F1: 3,11 / F2: 7,10) |
| Validator 단독 | `SC-DOM-VAL-001` (완성 true), `SC-DOM-VAL-002` (대각선 false) |
| small-first 즉시 성공 | `SC-DOM-SOL-002` (F1) |
| 양쪽 조합 실패 | `SC-DOM-SOL-003` + F3 UNSOLVABLE |
| Stage 1 Story | 문제 재정의·용어 합의 스토리 1개 (선택) |

**Level 4 시나리오 보강 후** RED 상세 분해 및 TDD 구현 착수 권장.

---

## 10. 다음 단계

1. §9 보강 시나리오를 Level 4 문서에 추가.
2. `RED-*` / `TASK-*`를 Report 02의 `DOM-*`, `UI-*` ID 체계와 매핑.
3. Boundary RED: Domain mock, Logic RED: 실 Domain — Dual-Track 순서 고정.
4. F1/F2/F3 픽스처로 GREEN 후 refactor; 외부 계약·ERR 메시지 변경 금지.

---

## 부록: 관련 파일

| 유형 | 경로 |
|------|------|
| Transcript | [`Prompting/06_MagicSquare_UserJourney_Level1-5_Transcript_Prompt.md`](../Prompting/06_MagicSquare_UserJourney_Level1-5_Transcript_Prompt.md) |
| 설계 | [`02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md) |
