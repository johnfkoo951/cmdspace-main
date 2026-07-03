---
type: note
aliases:
  - cmdspace.work Topics & Tools
  - 커맨드스페이스 다루는 주제와 도구
description: Source-of-truth for the "Topics" and "Tools" sections of cmdspace.work landing page. When updated, sync to `/DEV/cmdspace-main/data/topics-tools.md` and trigger the `cmdspace-update` skill to regenerate the relevant HTML sections. Each topic has id/title/desc/audience fields; each tool group has a name/sub and a list of tool objects with name and primary flag.
author:
  - "[[구요한]]"
date created: 2026-04-21
date modified: 2026-04-21
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
status: inProgress
---

# cmdspace.work · Topics & Tools (Master)

이 문서는 `cmdspace.work` 랜딩의 **다루는 교육 주제** 와 **다루는 도구·툴** 두 섹션의 **단일 출처** 입니다. 여기를 수정한 뒤 `cmdspace-update` 스킬을 호출하면 배포 프로젝트의 HTML 이 자동으로 재생성됩니다.

> **규칙**: 프론트엔드(index.html) 를 직접 손대지 말고 이 문서를 먼저 고칠 것. 구조가 바뀌면 스킬 파서도 함께 갱신.

---

## 📚 Topics (교육 주제)

주제 카드는 8개. 순서는 중요도·빈도 기준. 각 항목은 `id · title · desc · audience` 4 필드.

### 01 · 생성형 AI 리터러시

언어모델 원리부터 프롬프트 엔지니어링, 유료 기능 활용, 실무 자동화까지. ChatGPT · Claude · Gemini 를 목적에 맞게 조합해 쓰는 감각을 기릅니다.

- 대상: 일반 실무자 · 임원 · 교사 · 학생 · 학부모

### 02 · 연구자용 AI

논문 탐색·읽기·쓰기·인용, AI로 데이터 정제와 분석 자동화, 나만의 연구 보조 GPT 만들기. 연구 프로세스 전 단계를 LLM과 함께 재설계합니다.

- 대상: 대학원생 · 교수 · 연구소 · 기관 연구팀

### 03 · 개인지식관리(PKM) · 세컨드브레인

티아고 포르테의 BASB, 루만의 제텔카스텐, kepano·닉 마일로의 LYT를 한국 실무 맥락에 맞게 재구성한 CMDS 프로세스. 옵시디언 기초부터 고급 플러그인·그래프 활용까지.

- 대상: 지식노동자 · 연구자 · 학생 · 콘텐츠 크리에이터

### 04 · AI 에이전트·멀티에이전트

Claude Code · OpenClaw 기반 에이전트 구축, MCP로 외부 도구 연결, Obsidian 볼트를 에이전트의 장기 기억으로 활용. 9Yohan 멀티에이전트 오케스트레이션 사례.

- 대상: 개발자 · Power User · 프로덕트 팀

### 05 · CEO · 리더십 AX 교육

LG 임원·회장단 교육, LG인화원 AX Camp(for Leaders / for CEO), CEO 1:1 코칭. AI 시대에 조직과 본인의 의사결정을 어떻게 재설계할 것인가.

- 대상: 사장 · 부사장 · 임원 · 대기업/공공기관 리더

### 06 · 데이터 분석·시각화

기초·고급 통계, 회귀·ANOVA·SEM, 머신러닝 지도·비지도학습, 토픽 모델링. Tableau로 패널데이터 스토리텔링, ESG·HR Analytics 실무 사례.

- 대상: 연구자 · HR · 마케팅 · 정책 담당자

### 07 · 교수법·커리큘럼 설계

중고등 · 대학 · 기업 · 공공기관 맞춤 학습 경험 설계. 실습 중심 Day 1~3 워크샵, 시리즈 과정, 장기 코칭 프로그램 기획.

- 대상: 교사 · 교수 · 교육 담당자 · L&D 팀

### 08 · 노코드·자동화

n8n 워크플로우로 일상 자동화, Google Sheet + GPT API 연동, 교육·HR·마케팅 자동화 설계. 코드 없이 일하는 방식을 바꾸는 레시피.

- 대상: 실무자 · 교육자 · 기획자

---

## 🧰 Tools (다루는 도구·툴)

그룹 → 툴 리스트. 각 툴은 선택적으로 `primary: true` 플래그(`●` 배지) 를 가짐.

### LLM · AI Agent

> 대화·추론·에이전트

- ChatGPT **●**
- Claude **●**
- Claude Code **●**
- Claude Agent SDK
- Gemini
- OpenClaw **●**
- Perplexity
- Hermes
- MCP

### Personal Knowledge Management

> 메모·연결·저장

- Obsidian **●**
- Notion
- DevonThink
- Excalidraw
- Zotero
- Bookends

### 연구·학습

> 논문·문헌·분석

- Elicit
- SciSpace
- ResearchRabbit
- Semantic Scholar
- Publish or Perish
- Python / Colab
- R
- Tableau

### 이미지 · 음성 · 영상 AI

> 멀티모달 생성

- Midjourney
- Stable Diffusion
- DALL-E
- Sora
- ElevenLabs **●**
- HeyGen
- Whisper

### 자동화 · 개발

> 워크플로 · 퍼블리시

- n8n **●**
- Make.com
- Cursor
- Vercel **●**
- Cloudflare
- Webflow
- Raycast

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

## 🔗 Related

- [[2026-04-21-cmdspace-landing]] — 랜딩 프로젝트 트래킹 노트
- [[CMDSPACE Brand Identity]] — 브랜드 포지셔닝 (Hero/Pillars 카피 근거)
- [[🔖 YHN's Curriculum]] — Topics 상세 커리큘럼
- [[🔖 YHN's Lectures]] — 개별 강의 참조
