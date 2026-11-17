---
type: note
aliases:
  - cmdspace.work Topics & Tools
  - 커맨드스페이스 다루는 주제와 도구
description: "Source-of-truth for the Topics and Tools sections of the cmdspace.work landing page. It defines public education topics and tool groups while the company positioning and engagement model remain in the main page source."
author:
  - "[[구요한]]"
date created: 2026-04-21
date modified: 2026-11-17
tags:
  - cmdspace
  - landing
  - topics
  - tools
  - master
CMDS: "[[📚 806 Webpages]]"
related:
  - "[[2026-04-21-cmdspace-landing]]"
  - "[[CMDSPACE Brand Identity]]"
  - "[[00-AX강의-자산-인덱스]]"
  - "[[programs-by-audience]]"
status: inProgress
---

# cmdspace.work · Topics & Tools (Master)

이 문서는 `cmdspace.work` 랜딩의 **다루는 교육 주제** 와 **다루는 도구·툴** 두 섹션의 **단일 출처** 입니다. 여기를 수정한 뒤 `cmdspace-update` 스킬을 호출하면 배포 프로젝트의 HTML 이 자동으로 재생성됩니다.

> **규칙**: 프론트엔드(index.html) 를 직접 손대지 말고 이 문서를 먼저 고칠 것. 구조가 바뀌면 스킬 파서도 함께 갱신.

---

## 📚 Topics (교육 주제)

주제 카드는 10개. 순서는 조직 주제(01~03), 구축 특화 주제(04~06), 개인 지식 주제(07~08), 만들기와 교육(09~10). 각 항목은 `id · title · desc · audience` 4 필드. 근거는 [[00-AX강의-자산-인덱스|AX 강의 자산 라이브러리]]와 `50. Assets/54. Lecture Assets/`의 강의별 카드(2026-06~11). 대상별로 들을 수 있는 과정은 [[programs-by-audience|대상별 과정 카탈로그]]가 정본이다.

### 01 · AI 업무 활용 · 프롬프트에서 하네스까지

AI를 잘 쓰는 사람은 묻지 않고 맡기고, 매번 설명하지 않고, 기준을 줍니다. 프롬프트 → 컨텍스트 → 하네스 → 루프 네 층으로 ChatGPT · Claude · Gemini를 실제 업무에 붙이고, 클라우드와 로컬 중 어디에 맡길지 보안 기준까지 함께 정합니다.

- 대상: 기업·공공기관 실무자 · 전 직원 교육 · 일반 수강생

### 02 · 임원 AX · AI를 지휘하는 리더의 언어

AX는 도구 도입이 아니라 업무 재설계입니다. 에이전트의 다섯 요소(모델·도구·지식·룰·루프), AI 과제를 결재하는 여섯 질문, 위임과 판단 포기의 경계, 거버넌스와 데이터 주권을 임원의 언어로 다루고 1:1 코칭으로 잇습니다.

- 대상: CEO · 임원 · 부문장 · 대기업·금융·공공기관 리더

### 03 · AI가 읽는 조직 · AI-ready 데이터

데이터가 없는 게 아니라 AI가 읽지 못하는 형태로 쌓여 있을 뿐입니다. 보고용(PPT·PDF)·교환용(마크다운·JSON)·원문 세 층과 메타데이터 일곱 칸으로 부서 지식을 정본으로 만들고, NotebookLM 같은 근거형 AI를 기관 문서에 들이는 기준을 세웁니다.

- 대상: DX·AI 조직 · 지식·데이터 담당 · 공공기관 · 임원

### 04 · 사내 에이전트 · 일을 맡기는 워크플로 설계

에이전트 교육은 도구 사용법이 아니라 일을 맡기는 설계입니다. 작업 계약, 컨텍스트 팩, 스킬, 단계와 상태, 검증과 복구를 차례로 세워 업무 한 건을 끝까지 맡기고, 작성자와 검증자, 사람 결재를 나눈 멀티 에이전트 흐름까지 다룹니다.

- 대상: AX 전담 조직 · 개발·DX 팀 · 에이전트를 업무에 붙이려는 실무자

### 05 · 하네스 구축 · 조직의 AI 작업 환경

프롬프트 다음은 컨텍스트, 그다음은 하네스입니다. 시스템 파일과 공용 규칙, 스킬, 훅, 권한으로 AI가 회사의 규칙과 문체, 금기를 스스로 따르게 하고, 검증 루프와 성숙도 진단으로 운영 수준을 올립니다.

- 대상: AX 전담 조직 · 팀 리더 · 사내 AI 운영 담당

### 06 · 팀 LLM Wiki · 쌓일수록 쓸모 있는 지식 베이스

Karpathy의 LLM Wiki 패턴을 팀 단위로 옮깁니다. 원천 자료를 AI가 위키 카드로 소화하고(Ingest), 묻고(Query), 점검하며(Lint), 스키마와 갱신 책임을 먼저 정하고 qmd 인덱스로 수천 개 노트를 찾게 합니다. 모은 수가 아니라 소화한 수로 세는 개인·팀 지식 베이스.

- 대상: 연구팀 · 부서 지식관리 담당 · 팀 리더 · 지식노동자

### 07 · 옵시디언 PKM · 에이전트를 위한 볼트 설계

BASB·제텔카스텐·LYT를 한국 실무에 맞게 재구성한 CMDS 프로세스. 분류 체계, 프로퍼티 스키마, Bases, 위키링크로 개인 지식을 사람과 AI 에이전트가 함께 읽고 쓰는 구조로 만듭니다. Obsidian 101 기초부터 월간 옵시디언 심화까지.

- 대상: 지식노동자 · 연구자 · 학생 · 콘텐츠 크리에이터

### 08 · 연구자의 세컨드 브레인

문헌 수집부터 읽기·인용·집필까지 연구 과정을 AI와 다시 짭니다. Zotero 서재를 에이전트가 함께 읽게 하고, pandoc 인용으로 Word 원고까지 잇고, 연구 데이터 분석과 보고서 작성은 근거를 남겨 검증합니다.

- 대상: 대학원생 · 교수 · 정부출연연구기관 · 병원 연구팀

### 09 · 내 도구 직접 만들기 · 바이브코딩에서 배포까지

Claude Code · Codex에 일을 맡기고 MCP와 스킬로 도구를 연결합니다. 견적 계산기·업무 앱·웹페이지를 사서 쓰지 않고 직접 만들어 배포하며, 9Yohan 멀티에이전트 운영 사례와 AKM Index로 지식·에이전트 운영 수준을 점검합니다.

- 대상: 개발자 · Power User · 반복 업무를 덜어 내려는 실무자

### 10 · 교육자를 위한 AI · 수업과 과정 설계

AI를 쓴 과제를 결과물보다 대화 기록과 구술로 평가하는 법, 기출문제와 교육과정으로 수업을 역설계하는 법까지. 중고등·대학·기업·공공기관 맞춤 실습 워크숍과 코호트 과정을 설계합니다.

- 대상: 교사 · 교수 · 교육 담당자 · L&D 팀

---

## 🧰 Tools (다루는 도구·툴)

그룹 → 툴 리스트. 각 툴은 선택적으로 `primary: true` 플래그(`●` 배지) 를 가짐. 2026-08 이후 강의·컨설팅 노트에 실제로 등장한 도구만 남겼습니다.

### AI 모델 · 에이전트

> 대화·추론·에이전트 실행

- Claude **●**
- Claude Code **●**
- Codex **●**
- ChatGPT **●**
- Gemini
- Grok
- Microsoft 365 Copilot
- Google AI Studio
- Antigravity
- OpenClaw
- MCP **●**
- Agent Skills

### 지식 베이스 · PKM

> 기록·연결·AI가 읽는 정본

- Obsidian **●**
- Obsidian Bases **●**
- qmd **●**
- Obsidian Web Clipper
- Hookmark
- Mermaid
- Notion

### 연구 · 문헌

> 수집·인용·집필·분석

- Zotero **●**
- Better BibTeX
- pandoc
- NotebookLM (Gemini Notebook)
- Semantic Scholar
- OpenAlex
- Python / Colab

### 음성 · 영상 · 이미지

> 기록·생성·라이브러리

- ElevenLabs **●**
- HeyGen
- Plaud
- Midjourney
- Suno
- Eagle

### 개발 · 배포 · 운영

> 내 도구를 만들고 내보내기

- Vercel **●**
- GitHub **●**
- Cloudflare
- Supabase
- Tailscale
- cmux
- OpenRig

---

## 🔄 편집 워크플로

1. **이 문서를 수정** — 새 주제/도구 추가, 기존 항목 수정·삭제
2. **`cmdspace-update` 스킬 호출** — "cmdspace 주제/도구 동기화" 또는 "cmdspace 랜딩 업데이트" 라고 말하면 스킬이:
	- 이 파일을 `/DEV/cmdspace-main/data/topics-tools.md` 에 복사
	- 파서가 Topics/Tools 섹션 HTML 을 재생성
	- `index.html` 의 해당 두 섹션을 덮어쓰기
	- Vercel 배포 실행
3. **검증** — `cmdspace.work` 에서 반영 확인

## 📎 파싱 규약 (스킬용)

스킬 파서가 이 문서를 읽을 때 의존하는 마크업 패턴:

**Topics**:
- `## 📚 Topics` 헤딩 하위
- `### NN · <title>` → 카드 하나
- 바로 아래 문단 → 설명
- `- 대상: <text>` → audience 라인

**Tools**:
- `## 🧰 Tools` 헤딩 하위
- `### <group-name>` → 그룹
- `> <sub-description>` → 그룹 부제
- `- <tool-name>` → 일반 툴
- `- <tool-name> **●**` → 주력 툴 (primary)

이 패턴을 유지하는 한 스킬이 깔끔하게 파싱합니다. 문서 구조를 크게 바꾸면 `~/.claude/skills/cmdspace-update/scripts/sync-topics-tools.py` 도 업데이트 필요.

## 🗓 갱신 기록

- 2026-11-17: 주제를 8개에서 10개로. 특화 주제 둘을 새로 세웠다(04 사내 에이전트, 05 하네스 구축). 06 LLM Wiki는 팀 단위 지식관리를 앞세워 고쳤고, 옛 07 「AI 에이전트 · 내 도구 직접 만들기」는 09 「내 도구 직접 만들기」로 제목만 바꿨다. 순서는 조직, 구축 특화, 개인 지식, 만들기와 교육. 대상별 과정은 새 정본 [[programs-by-audience]]로 분리했다.
- 2026-11-05: 2026년 강의 자산 기준으로 주제 8개와 도구 5그룹을 다시 씀. 주제는 하네스(01)·임원 지시언어(02)·AI-ready 데이터(03)·연구자 세컨드 브레인(04)·볼트 설계(05)·LLM Wiki(06)·에이전트로 내 도구 만들기(07)·교육자용 AI(08)로 재편하고, 옛 「데이터 분석·시각화」는 04에, 「노코드·자동화(n8n)」는 07에 흡수. 도구는 2026-08 이후 강의·컨설팅 노트에 실제로 나온 것만 남김(n8n·Make.com·Tableau·Sora·DALL-E·Stable Diffusion·Webflow·Raycast·Cursor·Hermes 등 제외, Codex·qmd·Bases·Zotero·pandoc·NotebookLM 등 추가). 파서가 섹션 구분선 `---`을 마지막 주제 설명에 붙이던 문제도 함께 고침.

## 🔗 Related

- [[2026-04-21-cmdspace-landing]] — 랜딩 프로젝트 트래킹 노트
- [[CMDSPACE Brand Identity]] — 브랜드 포지셔닝 (Hero/Pillars 카피 근거)
- [[🔖 YHN's Curriculum]] — Topics 상세 커리큘럼
- [[🔖 YHN's Lectures]] — 개별 강의 참조
- [[00-AX강의-자산-인덱스]] — 주제 카드의 근거가 된 강의 자산 라이브러리
