#!/usr/bin/env bash
# Regenerate the three public PDFs (company brochure, AX portfolio, course proposal) from sanitized Markdown sources.
# md-to-pdf prints HTML as text, so the generator markers (<!-- ... -->) are stripped into a temporary clean copy first.
# The program tables inside the docs are generated — refresh them first with: python3 scripts/sync-programs.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

build() {  # build <source.md> <output.pdf> <title>
	local clean="$TMP/$(basename "$1")"
	grep -v '^<!--.*-->$' "$1" > "$clean"
	if grep -q '<!--' "$clean"; then
		echo "❌ HTML comment left in $1 after cleaning — it would print as text" >&2
		exit 1
	fi
	python3 ~/.claude/skills/md-to-pdf/scripts/md_to_pdf.py "$clean" "$2" --theme report --title "$3"
}

build "$ROOT/docs/cmdspace-brochure.md"        "$ROOT/assets/downloads/cmdspace-brochure.pdf"        "CMDSPACE 회사 소개"
build "$ROOT/docs/yohan-ax-portfolio.md"       "$ROOT/assets/downloads/yohan-ax-portfolio.pdf"       "구요한 AX 포트폴리오"
build "$ROOT/docs/cmdspace-course-proposal.md" "$ROOT/assets/downloads/cmdspace-course-proposal.pdf" "CMDSPACE 교육·코칭·컨설팅 과정 제안서"

echo ""
echo "Next: ./deploy.sh"
