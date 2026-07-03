#!/usr/bin/env bash
# Sync 구요한 이력 CSV from vault → DEV/cmdspace-main/data/
# Run weekly (or after any CSV update), then `vercel deploy --prod --yes`.

set -euo pipefail

VAULT_DIR="/Users/yohankoo/Local Obsidian_MBP/CMDSPACE_Local_MBP/70. Outputs/74. Projects/구요한 이력 DB"
DEV_CSV="/Users/yohankoo/DEV/cmdspace-main/data/activities.csv"

# Always pick the newest matching CSV (handles versioned filenames like _v0.2)
VAULT_CSV=$(ls -t "$VAULT_DIR"/구요한\ 이력_*.csv 2>/dev/null | head -1 || true)
if [[ -z "$VAULT_CSV" ]] || [[ ! -f "$VAULT_CSV" ]]; then
	echo "❌ Vault CSV not found. Check $VAULT_DIR"
	exit 1
fi

PRIVATE_CSV="/Users/yohankoo/DEV/cmdspace-main/data/activities-private.csv"

echo "📥  Source: $VAULT_CSV"
echo "📤  Private: $PRIVATE_CSV"
echo "📤  Public:  $DEV_CSV"

# Keep full copy as private backup
cp "$VAULT_CSV" "$PRIVATE_CSV"

# Strip PII columns for public CSV.
#   legacy schema : 'details'    (names, phone numbers, locations)
#   2026-06 schema: '제목(임의)' (original/internal title with client + person names)
# Read with utf-8-sig to drop any BOM — the frontend parser keys on header names
# (e.g. 'period'), so a BOM-prefixed first column would silently break rendering.
python3 -c "
import csv
PII = {'details', '제목(임의)'}
with open('$PRIVATE_CSV', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fields = [col for col in reader.fieldnames if col not in PII]
    with open('$DEV_CSV', 'w', encoding='utf-8', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for row in reader:
            writer.writerow(row)
"

ROWS=$(( $(wc -l < "$DEV_CSV") - 1 ))
echo "✅  Synced. Public rows: $ROWS (PII title/details column stripped)"
echo ""
echo "Next: cd $(dirname "$DEV_CSV")/.. && vercel deploy --prod --yes"
