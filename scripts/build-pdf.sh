#!/usr/bin/env bash
# Regenerate cmdspace-brochure.pdf from docs/cmdspace-brochure.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 ~/.claude/skills/md-to-pdf/scripts/md_to_pdf.py \
  "$ROOT/docs/cmdspace-brochure.md" \
  "$ROOT/assets/downloads/cmdspace-brochure.pdf" \
  --theme report --title "CMDSPACE 소개자료"
echo ""
echo "Next: vercel deploy --prod --yes"
