# cmdspace.work — Landing

Apex landing for the **CMDSPACE** ecosystem. Single static page (vanilla HTML/CSS/JS, no build) that:

1. Introduces the brand (positioning + operator)
2. Headlines & details 구요한's education/consulting history
3. Hubs all public `*.cmdspace.work` subdomains

Data is loaded client-side from `./data/activities.csv` and updated **weekly** from the vault.

## Structure

```
cmdspace-main/
├── index.html                 # single-file landing
├── data/
│   ├── activities.csv         # 구요한 이력 (weekly-updated)
│   └── gallery.json           # gallery manifest (auto-generated)
├── assets/
│   ├── logos/                 # round favicon + typo lockups (light/dark)
│   ├── og/og-landing.png      # 1200×630 OG card + HTML template
│   ├── profile/
│   │   ├── yhn-profile.png    # circular crop (480×480)
│   │   └── yhn-profile@2x.png # retina (960×960)
│   └── gallery/               # lecture/event photos (.jpg/.png)
├── scripts/
│   ├── build-og.sh            # regenerate OG image
│   └── build-gallery.sh       # rescan gallery + regenerate manifest
├── sync-activities.sh         # vault → DEV CSV sync
└── README.md
```

## Weekly update flow (activities CSV)

```bash
# 1. Update the CSV inside the vault:
#    "/Users/yohankoo/Local Obsidian_MBP/CMDSPACE_Local_MBP/70. Outputs/74. Projects/구요한 이력 DB/"

# 2. Sync into this project
cd /Users/yohankoo/DEV/cmdspace-main
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
period,host,display_title,start_at,duration_hours,affiliation,topic,activity_type
```

> 볼트 원본 DB에는 `UID`·`details`·`is_completed` 컬럼이 더 있지만, `details` 는 PII 성격이라 공개 CSV 에서 의도적으로 제외됩니다. 위 8컬럼이 `sync-activities.sh` 가 실제로 내보내는 공개 스키마입니다. 프론트는 미래 `start_at` 행을 로드 시점에 필터링합니다.

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

`bio.cmdspace.work` (레포 `/Users/yohankoo/DEV/cmds-bio`) 와 프로필 직함(차의과학대학교 겸임교수 · KIRD 객원교수)·대표 수치(활동 450+ / 노트 10,000+ / LG 900명)·링크 자산을 공유합니다.

이 레포에서 위 정보를 변경하면 **cmds-bio 도 함께 갱신**해야 합니다. cmds-bio 쪽 변경 기록은 해당 레포의 `docs/06-worklog.md` 를 참조하세요. 반대 방향(이 레포로의 참조)은 cmds-bio README 에 반영되어 있습니다.
