# 05 Agent Profiles And Transcript Export Prompt

## 메타

- 목적: 현재 세션의 프롬프트/응답 흐름을 대화형 transcript로 보관
- 범위: `code-reviewer` 에이전트 생성 요청부터 본 export 요청까지
- 형식: User/Assistant 순차 기록 (핵심 도구 실행 포함)

---

## 대화형 Transcript

### Turn 1 - User

`.cursor/agents/code-reviewer.md` 생성 요청  
(frontmatter: `name`, `description`, `model: inherit`, `readonly: true`; 본문에 코드 리뷰 지침)

### Turn 2 - Assistant

프로젝트 규칙을 확인하고 `code-reviewer.md`를 생성함.

### Turn 3 - User

`/code-reviewer @app/main.py` 리뷰 요청

### Turn 4 - Assistant

`app/main.py`를 찾지 못해 리뷰 불가 안내, 대체 파일 리뷰 제안.

### Turn 5 - User

`.cursor/agents/system-optimization-engineer-agent.md` 생성 요청  
(성능 병목 분석/개선 책임, 작업 방식, 금지, 출력 형식, 안전 규칙 포함)

### Turn 6 - Assistant

`system-optimization-engineer-agent.md` 생성 완료.

### Turn 7 - User

`.cursor/agents/ux-design-advisor.md` 생성 요청  
(UX 디자이너 지침: 화면/버튼/에러 메시지 개선)

### Turn 8 - Assistant

UX/에러 메시지 계약(Report 규칙) 반영해 `ux-design-advisor.md` 생성 완료.

### Turn 9 - User

`code-bug-analyzer` → `performance-optimizer` → `ux-design-advisor` 순 실행, 앱 실행/브라우저 확인, 백업/복원 요청

### Turn 10 - Assistant

코드 구조 점검 및 테스트 실행(`pytest -q` 통과) 후 실행 준비.  
이후 사용자 지시에 따라 실행형 작업에서 문서 생성 작업으로 전환.

### Turn 11 - User

"위와 같은 `.md`를 짜달라"는 재지시

### Turn 12 - Assistant

아래 에이전트 파일들을 순차 생성:

- `.cursor/agents/code-bug-analyzer.md`
- `.cursor/agents/performance-optimizer.md`

### Turn 13 - User

`.cursor/agents/product-planning-manager.md` 생성 요청

### Turn 14 - Assistant

`product-planning-manager.md` 생성 완료.

### Turn 15 - User

`.cursor/agents/backend-developer.md` 생성 요청

### Turn 16 - Assistant

`backend-developer.md` 생성 완료.

### Turn 17 - User

`.cursor/agents/frontend-developer.md` 생성 요청

### Turn 18 - Assistant

`frontend-developer.md` 생성 완료.

### Turn 19 - User

`.cursor/agents/quality-assurance-engineer.md` 생성 요청

### Turn 20 - Assistant

`quality-assurance-engineer.md` 생성 완료.

### Turn 21 - User

`.cursor/agents/ai-integration-expert.md` 생성 요청  
(OpenRouter + DeepSeek 연동 중심)

### Turn 22 - Assistant

`ai-integration-expert.md` 생성 완료.

### Turn 23 - User

보고서/기록/GitHub 관리를 위한 `backup-agent` 생성 요청  
루틴:  
[1] `Report/xx_*_Report.md`  
[2] `Prompt/xx_*_Prompt.md`

### Turn 24 - Assistant

`.cursor/agents/backup-agent.md` 생성 완료.

### Turn 25 - User

다음 순서 실행 요청:

1. `Report` 폴더에 보고서 생성
2. 현재까지 프롬프트 전체를 `Prompt` 폴더에 대화형 transcript로 export

### Turn 26 - Assistant (현재 작업)

기존 번호 확인 후 `05` 번호로 산출물 생성:

- `Report/05_Agent_Profiles_And_Transcript_Export_Report.md`
- `Prompt/05_Agent_Profiles_And_Transcript_Export_Prompt.md` (본 파일)

---

## 실행 명령/점검 요약

- 파일 패턴 점검: `Report/*_Report.md`, `Prompt/*_Prompt.md`
- 번호 결정: 기존 최대 `04` 확인 후 `05` 할당
- 산출물 생성: 보고서 + transcript export 동시 생성

## 비고

- 본 transcript는 세션의 핵심 요청/응답 흐름을 대화형으로 정리한 export 기록이다.
