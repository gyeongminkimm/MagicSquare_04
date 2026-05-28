# Magic Square 4×4 — PRD 작성·검토 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **문서 ID** | `07_MagicSquare_PRD_And_Review_Report` |
| **전제 보고서** | [`01_MagicSquare_ProblemDefinition_Report.md`](01_MagicSquare_ProblemDefinition_Report.md), [`02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md`](02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md), [`03_MagicSquare_CursorRules_And_InitialImplementation_Report.md`](03_MagicSquare_CursorRules_And_InitialImplementation_Report.md), [`06_MagicSquare_UserJourney_Level1-5_Verification_Report.md`](06_MagicSquare_UserJourney_Level1-5_Verification_Report.md) |
| **작성일** | 2026-05-28 |
| **상태** | PRD 본문 저장 완료, 7항목 검토 완료, 구현·테스트 코드 미포함 |

---

## 목차

1. [세션 요약](#1-세션-요약)
2. [산출물 목록](#2-산출물-목록)
3. [Phase 1 — 참고 문서 분석·매핑](#3-phase-1--참고-문서-분석매핑)
4. [Phase 2 — PRD 본문 작성](#4-phase-2--prd-본문-작성)
5. [Phase 3 — PRD 저장](#5-phase-3--prd-저장)
6. [Phase 4 — PRD 7항목 검토](#6-phase-4--prd-7항목-검토)
7. [검토 결과 요약](#7-검토-결과-요약)
8. [권장 보완 항목 (우선순위)](#8-권장-보완-항목-우선순위)
9. [Open Questions / Decision Needed](#9-open-questions--decision-needed)
10. [다음 단계](#10-다음-단계)

---

## 1. 세션 요약

| Phase | 사용자 요청 | 결과 |
|-------|-------------|------|
| 1 | PRD 작성 전 참고 문서 분석·섹션 매핑 (본문·코드·파일 수정 금지) | 8섹션 분석 보고서 (채팅 산출) |
| 2 | 구현 전 PRD 전체 작성 (23섹션 구조, Dual-Track·Traceability 필수) | PRD Markdown 본문 (채팅 산출) |
| 3 | `docs/PRD_MagicSquare.md` 파일 저장 | 저장 완료 |
| 4 | PRD 7기준 검토 (수정 금지, 문제·개선안만) | 검토 보고 (채팅 산출) |
| 5 | Report·Prompting Transcript Export | 본 문서, [`Prompting/07_...`](../Prompting/07_MagicSquare_PRD_And_Review_Transcript_Prompt.md) |

**구현·테스트 코드 변경 없음** — 문서·PRD 명세만 수행.

---

## 2. 산출물 목록

| 유형 | 경로 | 비고 |
|------|------|------|
| PRD (SSOT) | [`docs/PRD_MagicSquare.md`](../docs/PRD_MagicSquare.md) | 23섹션, FR-01~05, AC-01~20, BR-01~15 |
| 분석 보고 | 채팅 Turn 1 (미파일) | 본 Report §3에 요약 반영 |
| 검토 보고 | 채팅 Turn 4 (미파일) | 본 Report §6~§8에 요약 반영 |
| 세션 보고서 | `Report/07_MagicSquare_PRD_And_Review_Report.md` | 본 문서 |
| Transcript | `Prompting/07_MagicSquare_PRD_And_Review_Transcript_Prompt.md` | 대화형 Export |

---

## 3. Phase 1 — 참고 문서 분석·매핑

### 3.1 문서 경로 정합

| 사용자 참조명 | 저장소 실제 경로 |
|---------------|------------------|
| Report/1.ProblemDefinition | `Report/01_MagicSquare_ProblemDefinition_Report.md` |
| Report/2.CleanArchitecture... | `Report/02_MagicSquare_DualTrack_CleanArchitecture_TDD_Design.md` |
| Report/3.DevelopmentEnvironment... | `Report/03_MagicSquare_CursorRules_And_InitialImplementation_Report.md` |
| Report/4.UserJourney... | `Report/06_MagicSquare_UserJourney_Level1-5_Verification_Report.md` |
| — | `Report/04_*` = 모듈형 Cursor Rules (User Journey 아님) |

### 3.2 PRD 작성 가능 여부

| 항목 | 판정 |
|------|------|
| 작성 가능 여부 | **가능 (조건부)** |
| 1차 참고 | Report/06 (요구·검증 내러티브) + Report/02 (계약·불변식) |
| 보조 참고 | Report/01, 03, `.cursor/rules/*.mdc` |
| 누락 정보 | F3(UNSOLVABLE) 픽스처, Gherkin 전문, Control 계층 필수 여부 |

### 3.3 출처 우선순위 (확정)

| 주제 | Primary | Secondary |
|------|---------|-----------|
| 동기·Why | 01 | README |
| Epic·Journey·Story | 06 | 01 |
| I/O·Invariant·레이어 | 02 | project.mdc |
| TDD·품질·금지 | 03, `.mdc` | 02 |

---

## 4. Phase 2 — PRD 본문 작성

### 4.1 구조 준수

- 지정 23섹션 구조 준수 (Executive Summary ~ Appendix)
- FR-01~05, BR-01~15, AC-01~20, NFR-01~09
- Dual-Track: §15 Track A(Boundary) / Track B(Domain)
- Traceability Matrix §21 (Concept → BR → FR → AC → Test → Component)

### 4.2 고정 계약 반영

| 항목 | PRD 반영 |
|------|----------|
| 입력 | 4×4, `0` 빈칸 2개, `0`∪[1,16], 비0 중복 금지 |
| 출력 | `int[6]`, 1-index, `[r1,c1,n1,r2,c2,n2]` |
| 시도 순서 | small→pos1, large→pos2 (Attempt 1) → reverse (Attempt 2) |
| 마법합 | 34 |
| 실패(두 조합) | Domain `UNSOLVABLE_PUZZLE` → Boundary `ERR_UNSOLVABLE` |

### 4.3 대표 테스트 데이터 (PRD §16.4)

| Data ID | 목적 | Matrix |
|---------|------|--------|
| TD-01 | small-first (F1) | `[[16,0,2,13],[5,10,0,8],[9,6,7,12],[4,15,14,1]]` |
| TD-02 | reverse (F2) | `[[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]` |
| TD-07 | unsolvable | Decision Needed (F3 미확정) |

**Report/02 기대 출력 (PRD §16.4에 미기재 — 검토 시 지적)**

| Fixture | 기대 `int[6]` |
|---------|----------------|
| F1 | `[1,2,3,2,3,11]` |
| F2 | `[2,2,10,3,3,7]` |

---

## 5. Phase 3 — PRD 저장

| 항목 | 내용 |
|------|------|
| 경로 | `docs/PRD_MagicSquare.md` |
| 시점 | 사용자 “파일로 저장” 요청 후 |
| 상태 | 저장 완료 |

---

## 6. Phase 4 — PRD 7항목 검토

### 6.1 기준별 판정

| # | 기준 | 판정 |
|---|------|------|
| 1 | 모든 FR에 테스트 가능한 AC | 부분 충족 |
| 2 | 모든 AC가 Traceability Matrix 연결 | 미충족 |
| 3 | Boundary/Domain 책임 혼합 없음 | 부분 문제 |
| 4 | 오류 정책 미정 없음 | 부분 미정 (F3, null, ERR_INTERNAL 등) |
| 5 | small-first / reverse 데이터 구분 | 부분 충족 (행렬만, 기대 벡터 없음) |
| 6 | 1-index·row-major 누락 없음 | 부분 충족 (F1/F2 기대 좌표·내부 좌표계 미정) |
| 7 | 구현/테스트 코드 미포함 | 충족 |

### 6.2 주요 이슈 ID (검토 보고서)

| ID | 요약 |
|----|------|
| P1-01 | 출력 계약 검증 독립 FR 없음 |
| P2-01 | AC-06, AC-15~17, AC-20 등 Matrix 누락 |
| P3-01 | FR-05 Domain+Boundary 혼합 |
| P4-01 | TD-07 / F3 미확정 |
| P5-01 | TD-01/02 기대 `int[6]` 미기재 |
| P6-01 | pos2 AC·Domain 내부 좌표계 미정 |

---

## 7. 검토 결과 요약

**총평:** PRD는 Dual-Track·핵심 불변식·입력 오류 조기 차단·UNSOLVABLE 정책이 명확하여 **구현 전 기준 문서로 사용 가능**하나, **승인 전 1회 보완**이 권장된다.

| 강점 | 보완 필요 |
|------|-----------|
| FR-01~05 + AC-01~20 체계 | FR-06 Boundary 출력 검증 분리 |
| §13 Error 표 + Domain 미호출 정책 | F1/F2 기대 벡터를 AC·TD에 고정 |
| BR-05, BR-12 row-major·1-index | AC Coverage Index 또는 Matrix AC 전수 |
| TD-01/02 행렬 분리 | F3 확정 또는 ES-05 Phase 분리 |
| 코드 없음 (PRD 수준 준수) | null·ERR_INTERNAL·message exact match |

---

## 8. 권장 보완 항목 (우선순위)

| 순위 | 항목 | 근거 |
|------|------|------|
| 1 | TD-01/02 + AC-15/16에 기대 `int[6]` 연결 | P5, P6, 테스트 가능성 |
| 2 | F3(TD-07) 확정 또는 ES-05 Out-of-Scope 명시 | P4-01, AC-17 |
| 3 | FR-06 Boundary 출력 검증, FR-05 Domain 분리 | P3, P1-01, Dual-Track |
| 4 | AC Coverage Index / Matrix AC 전수 | P2 |
| 5 | null·ERR_INTERNAL·FR-04 미완성 격자·UX-01 message | P4 |

---

## 9. Open Questions / Decision Needed

PRD §22와 동일. 승인 게이트:

1. **F3 unsolvable fixture** — TD-07 확정
2. **참고 문서 표기** — Report/4 vs Report/06 단일 표준
3. **Coverage CI** — 80% 최소 vs Domain 95%/Boundary 85% 병행 여부
4. **Control 계층** — 필수 오케스트레이션 vs Boundary 직접 호출

---

## 10. 다음 단계

| 우선순위 | 작업 | 근거 |
|----------|------|------|
| 1 | PRD §8 권장 보완 반영 (docs/PRD_MagicSquare.md 개정) | 검토 P1~P6 |
| 2 | F3 픽스처 확정 후 TD-07·ES-05 폐쇄 | Report/02 INT-E-02 |
| 3 | Report/02 `DOM-*` / `UI-*` ID와 PRD RED 후보 매핑 | §23.4 |
| 4 | Dual-Track RED: Boundary mock + Domain P0 | PRD §15 |
| 5 | (선택) README에 PRD 링크 추가 | SSOT 안내 |

---

## 부록 — 대화 Export

전체 User/Cursor 턴: [`Prompting/07_MagicSquare_PRD_And_Review_Transcript_Prompt.md`](../Prompting/07_MagicSquare_PRD_And_Review_Transcript_Prompt.md)
