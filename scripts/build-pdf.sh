#!/usr/bin/env bash
# Regenerate public CMDSPACE and Yohan AX PDFs from sanitized Markdown sources.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 ~/.claude/skills/md-to-pdf/scripts/md_to_pdf.py \
  "$ROOT/docs/cmdspace-brochure.md" \
  "$ROOT/assets/downloads/cmdspace-brochure.pdf" \
  --theme report --title "CMDSPACE 회사 소개"

python3 ~/.claude/skills/md-to-pdf/scripts/md_to_pdf.py \
  "$ROOT/docs/yohan-ax-portfolio.md" \
  "$ROOT/assets/downloads/yohan-ax-portfolio.pdf" \
  --theme report --title "구요한 AX 포트폴리오"

echo ""
echo "Next: vercel deploy --prod --yes"
