# cmdspace.work — Landing

Apex landing for **CMDSPACE**, an enterprise AX and context-architecture professional-services company. The single static page (vanilla HTML/CSS/JS, no build):

1. Presents the `Discover → Diagnose → Pilot → Scale → Operate` engagement model
2. Introduces Yohan Koo's enterprise AX/context-architect role and verified activity record
3. Publishes sanitized company and AX portfolio PDFs
4. Hubs public `*.cmdspace.work` properties

Data is loaded client-side from `./data/activities.csv` and updated **weekly** from the vault.

## Structure

```
cmdspace-main/
├── index.html                 # single-file landing
├── data/
│   ├── activities.csv         # 구요한 이력 (weekly-updated)
│   └── gallery.json           # gallery manifest (auto-generated)
├── assets/
│   ├── downloads/              # sanitized public PDFs
│   ├── logos/                 # round favicon + typo lockups (light/dark)
│   ├── og/og-landing.png      # 1200×630 OG card + HTML template
│   ├── profile/
│   │   ├── yhn-profile.png    # circular crop (480×480)
│   │   └── yhn-profile@2x.png # retina (960×960)
│   └── gallery/               # lecture/event photos (.jpg/.png)
├── scripts/
│   ├── build-og.sh            # regenerate OG image
│   └── build-gallery.sh       # rescan gallery + regenerate manifest
├── sync-activities.sh         # Airtable → data/activities.csv sync
└── README.md
```

## Weekly update flow (activities CSV)

```bash
# 1. Edit records in Airtable: base "CMDS Work" → table "프로젝트 이력" → view "Export(Educations)"
#    (token lives in ~/.claude/skills/airtable-cmds-work-export/.env — never commit)

# 2. Dry-run: diff Airtable vs the live site (added / REMOVED rows, header, data health)
cd /Users/yohankoo/DEV/cmdspace-main
./sync-activities.sh --check

# 3. Write data/activities.csv (strips BOM, UTC→KST start_at, "A, B"→"A,B")
./sync-activities.sh

# 3. Deploy
vercel deploy --prod --yes
```

The filename in the vault may carry a date suffix (`구요한 이력_20260421.csv`) — if the hardcoded path misses, the script falls back to the newest matching file.

## Adding gallery photos

```bash
# Option A — drop files directly into the gallery folder (accepts .jpg/.png)
cp ~/Downloads/new-photo.jpg /Users/yohankoo/DEV/cmdspace-main/assets/gallery/
cd /Users/yohankoo/DEV/cmdspace-main
./scripts/build-gallery.sh           # rescans + regenerates manifest
vercel deploy --prod --yes

# Option B — bulk import from a source folder (auto-resizes, auto-names)
./scripts/build-gallery.sh ~/Downloads/new-lecture-photos
vercel deploy --prod --yes
```

The build script:
- Accepts `.jpg .jpeg .png .heic` (converted to JPG)
- Resizes max dim to 1800px · 84% quality · progressive
- Respects EXIF rotation
- Names sequentially: `photo-NN.jpg`
- Writes `/data/gallery.json` — the runtime reads this to render the grid

## CSV schema (must match)

```
period,host,display_title,start_at,duration_hours,topic,activity_type
```

> 공개 CSV는 위 7컬럼입니다. Airtable 뷰에 보이는 `제목(임의)`(내부 라벨)와 숨김 필드는 exporter 의 allowlist 로 제외됩니다 — Airtable `view` 파라미터는 레코드만 거르고 필드는 안 거르므로 allowlist 가 PII 방벽입니다. 프론트는 미래 `start_at` 행을 필터링합니다.

See `/Users/yohankoo/Local Obsidian_MBP/CMDSPACE_Local_MBP/70. Outputs/74. Projects/구요한 이력 DB/CMDSPACE 이력 데이터 스키마.md` for field definitions.

## Vercel

- Project: `cmdspace-main`
- Domain: `cmdspace.work` (apex)
- First-time setup: `vercel link --project cmdspace-main --yes`
- Deploy: `vercel deploy --prod --yes`

## Design

Follows **CMDS v4.3** standards — same token system as `system.cmdspace.work`:

- Light: CMDS Green `#134538` accent
- Dark: CMDS Pink `#E985A2` accent
- Apple SF Pro × Pretendard stack
- 17 OG meta tags, round logo favicon, `.accent-word` class for highlight

## Subdomain hub (public `*.cmdspace.work` only)

Excluded from the hub per existing policy:

- `lg.cmdspace.work`, `ax.cmdspace.work`, `test.cmdspace.work` — LG 고객사 페이지
- `obsidian-professional.cmdspace.work` — redirect only
- Tool endpoints (`dify`, `n8n`, `openwebui`, etc.) — not websites

## 연결 프로젝트 — cmds-bio

`bio.cmdspace.work` (레포 `/Users/yohankoo/DEV/cmds-bio`) 와 프로필 직함(`Founder & Principal Context Architect`)·대표 수치(전체 활동 기록 480+ / 1만여 개 지식 파일 / 그룹 임원 855명 대상 프로그램)·링크 자산을 공유합니다.

`docs/`는 PDF 생성용 원문이며 Vercel 배포에서 제외됩니다. 공개 산출물은 `assets/downloads/`의 비식별 PDF만 사용합니다.

이 레포에서 위 정보를 변경하면 **cmds-bio 도 함께 갱신**해야 합니다. cmds-bio 쪽 변경 기록은 해당 레포의 `docs/06-worklog.md` 를 참조하세요. 반대 방향(이 레포로의 참조)은 cmds-bio README 에 반영되어 있습니다.

## Public hub maintenance

- The vault `cmdspace-landing/hub-links.md` is the reviewed master; `data/hub-links.json` is its public deployment copy.
- Run `python3 scripts/sync-hub.py` after editing the master. For a portable rebuild, use `python3 scripts/sync-hub.py --data`.
- Never add a domain just because it responds: exclude customer pages, noindex material, research-participant forms, and individual shared notes.
- Alias pairs: `course` → `showcloud`, `files` → `system`. Keep one representative card; aliases remain active.
- 2026-09-12: 30 reviewed links in 6 groups. Added Brain, Apps, Deck, AI 백일장, CmdSync, CMDS Share, and Mobile Command Center. Updated profile education and KIRD title in llms.txt.
