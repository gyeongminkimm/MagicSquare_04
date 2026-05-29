# MagicSquare_XX — 문서 인덱스

프로젝트 루트 [`README.md`](../README.md)와 함께 참고하는 보조 문서·체크리스트입니다.

| 문서 | 설명 |
|------|------|
| [`PRD_MagicSquare.md`](PRD_MagicSquare.md) | 제품 요구사항 (FR, AC, TD) |
| [`test_plan.md`](test_plan.md) | Boundary·Domain 테스트 계획 |
| [`defect_list.md`](defect_list.md) | 결함 추적 |
| [`golden_master_approval_design.md`](golden_master_approval_design.md) | Golden Master / Approve 패턴 설계 |
| [Report/14 — Golden Master 회귀](../Report/14_MagicSquare_Golden_Master_Regression_Report.md) | 세션 보고서 |
| [Prompt/14 — Transcript](../Prompt/14_MagicSquare_Golden_Master_Regression_Transcript_Prompt.md) | 대화 Export |

---

## RED 단계 To-Do 리스트

> AC-FR-01-01 RED/GREEN 상세 체크리스트는 루트 [`README.md` §TDD 체크리스트](../README.md#tdd-체크리스트--ac-fr-01-01-구조차원-검증)를 SSOT로 한다.

### Golden Master 회귀 안전장치

Refactoring 시작 전 구축.  
GREEN 완료 후 즉시 적용.

#### 기준 파일 생성

- [x] **GM-01:** `golden_master_expected.txt` 생성 — [`tests/golden_master_expected.txt`](../tests/golden_master_expected.txt)
- [x] **GM-02:** 정상/역순/오류 시나리오 추가 (GM-TC-01~05)
- [x] **GM-03:** `git add tests/golden_master_expected.txt`

#### 테스트 코드

- [x] **GM-04:** `test_golden_master_magic_square` 작성 — [`tests/golden_master/test_golden_master_magic_square.py`](../tests/golden_master/test_golden_master_magic_square.py)
- [x] **GM-05:** approve 패턴 적용 — [`tests/golden_master/approval.py`](../tests/golden_master/approval.py)
- [x] **GM-06:** Golden Master 테스트 PASS 확인

```powershell
cd c:\DVV\MagicSquare_XX
python -m pytest -m golden_master -v
```

#### 회귀 보호

- [x] **GM-07:** row-major 규칙 보호 — `assert_row_major_blank_order`
- [x] **GM-08:** 1-index 출력 보호 — `assert_int_six_format`
- [x] **GM-09:** reverse 조합 fallback 보호 — `assert_reverse_fallback_combination`
- [x] **GM-10:** Error Contract 보호 — `INVALID_BLANK_COUNT` / `DUPLICATE_NUMBER` / `NO_VALID_MAGIC_SQUARE`

기준 갱신(의도적 계약 변경 후):

```powershell
$env:GOLDEN_MASTER_APPROVE = "1"
python -m pytest -m golden_master -v
git add tests/golden_master_expected.txt
```
