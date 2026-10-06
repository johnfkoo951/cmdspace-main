#!/usr/bin/env bash
# Sync 구요한 이력 CSV from Airtable (CMDS Work / 프로젝트 이력 / Export(Educations))
# → DEV/cmdspace-main/data/activities.csv, then `vercel deploy --prod --yes`.
#
# Source of truth is the Airtable view; the exporter lives in the
# `airtable-cmds-work-export` skill (read-only, allowlisted 7 columns, no PII).
#   --check   only diff Airtable vs the live site, write nothing
#   --deploy  sync, then deploy cmdspace.work AND bio.cmdspace.work
#   (default) run the check, then overwrite data/activities.csv

set -euo pipefail

SKILL_DIR="$HOME/.claude/skills/airtable-cmds-work-export"
EXPORTER="$SKILL_DIR/scripts/export_airtable_view.py"
DEV_CSV="/Users/yohankoo/DEV/cmdspace-main/data/activities.csv"

if [[ ! -f "$EXPORTER" ]]; then
	echo "❌ exporter not found: $EXPORTER"
	exit 1
fi
if ! grep -q '^AIRTABLE_TOKEN=.' "$SKILL_DIR/.env" 2>/dev/null; then
	echo "❌ AIRTABLE_TOKEN missing — see $SKILL_DIR/.env.example"
	exit 1
fi

# Pre-publish gate: header diff, added/REMOVED rows vs https://cmdspace.work/data/activities.csv.
# A non-empty REMOVED list means publishing would delete public rows — stop and confirm.
python3 "$EXPORTER" --env "$SKILL_DIR/.env" --check
if [[ "${1:-}" == "--check" ]]; then
	exit 0
fi

echo ""
echo "📥  Source: Airtable · CMDS Work / 프로젝트 이력 / Export(Educations)"
echo "📤  Public: $DEV_CSV"

TMP_CSV="$(mktemp)"
trap 'rm -f "$TMP_CSV"' EXIT
python3 "$EXPORTER" --env "$SKILL_DIR/.env" --format csv --out "$TMP_CSV"

# Two normalisations between the raw export and the site file:
#  1. drop the UTF-8 BOM the exporter writes for Excel — the site file has never
#     carried one and the frontend parser keys on the literal 'period' header.
#  2. start_at: Airtable returns UTC ISO ("2026-08-26T10:30:00.000Z"); the site
#     has always served KST local ("2026-08-26 19:30") and slices the date with
#     [:10] — leaving UTC would push every evening event a day earlier.
python3 - "$TMP_CSV" "$DEV_CSV" <<'PY'
import csv, sys
from datetime import datetime, timezone, timedelta
KST = timezone(timedelta(hours=9))
src, dst = sys.argv[1], sys.argv[2]

def to_kst(s):
    if not s or not s.endswith("Z"):
        return s
    return datetime.fromisoformat(s[:-1]).replace(tzinfo=timezone.utc).astimezone(KST).strftime("%Y-%m-%d %H:%M")

with open(src, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fields = reader.fieldnames
for r in rows:
    r["start_at"] = to_kst(r.get("start_at", ""))
    # exporter joins multi-values as "A, B"; the site file has always used "A,B"
    # (the frontend trims either) — keep the old form so git diffs show real changes only
    for col in ("host", "topic", "activity_type"):
        r[col] = ",".join(p.strip() for p in (r.get(col) or "").split(","))
with open(dst, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
PY

ROWS=$(python3 -c 'import csv, sys; print(sum(1 for _ in csv.DictReader(open(sys.argv[1], encoding="utf-8"))))' "$DEV_CSV")
echo "✅  Synced. Public rows: $ROWS"

# bio.cmdspace.work shows the same total as a rounded-down static credential ("480+").
# Keep it in lockstep: floor to tens so the number only moves every ten records.
BIO_HTML="/Users/yohankoo/DEV/cmds-bio/index.html"
BIO_COUNT="$(( ROWS / 10 * 10 ))+"
python3 - "$BIO_HTML" "$BIO_COUNT" <<'PY'
import re, sys
path, new = sys.argv[1], sys.argv[2]
s = open(path, encoding="utf-8").read()
pat = re.compile(r'<strong data-ko="(\d+\+)" data-en="\d+\+">\d+\+</strong>(?=<span data-ko-html=\'강의·코칭·연구·자문 전체 활동 기록)')
m = pat.search(s)
if not m:
    sys.exit("❌ bio credential line not found — index.html layout changed?")
old = m.group(1)
if old == new:
    print(f"ℹ️  bio credential unchanged: {old}")
else:
    s = pat.sub(f'<strong data-ko="{new}" data-en="{new}">{new}</strong>', s, count=1)
    open(path, "w", encoding="utf-8").write(s)
    print(f"✅  bio credential {old} → {new}")
PY

if [[ "${1:-}" == "--deploy" ]]; then
	echo ""
	echo "🚀  Deploying cmdspace.work"
	(cd /Users/yohankoo/DEV/cmdspace-main && vercel deploy --prod --yes)
	echo "🚀  Deploying bio.cmdspace.work"
	(cd /Users/yohankoo/DEV/cmds-bio && vercel deploy --prod --yes --scope johnfkoo951s-projects)
else
	echo ""
	echo "Next: ./sync-activities.sh --deploy   (deploys cmdspace.work + bio.cmdspace.work)"
fi
