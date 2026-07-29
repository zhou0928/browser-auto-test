#!/bin/bash
set -e

# snapshot-diff.sh - Compare two screenshots (baseline vs current) using ImageMagick
# Usage: bash /mnt/skills/user/browser-auto-test/scripts/snapshot-diff.sh <baseline> <current> [output-diff]

BASELINE="$1"
CURRENT="$2"
OUTPUT="${3:-diff-$(date +%s).png}"

if [ -z "$BASELINE" ] || [ -z "$CURRENT" ]; then
  echo "Usage: $0 <baseline.png> <current.png> [output-diff.png]" >&2
  exit 1
fi

if ! command -v magick &>/dev/null; then
  echo "ERROR: ImageMagick not found. Install with: brew install imagemagick" >&2
  exit 1
fi

if [ ! -f "$BASELINE" ]; then
  echo "ERROR: Baseline not found: $BASELINE" >&2
  exit 1
fi

if [ ! -f "$CURRENT" ]; then
  echo "ERROR: Current screenshot not found: $CURRENT" >&2
  exit 1
fi

# Compare and highlight differences in red
magick compare -metric AE -highlight-color red "$BASELINE" "$CURRENT" "$OUTPUT" 2>&1 || true

BASELINE_SIZE=$(stat -f%z "$BASELINE" 2>/dev/null || stat -c%s "$BASELINE" 2>/dev/null)
CURRENT_SIZE=$(stat -f%z "$CURRENT" 2>/dev/null || stat -c%s "$CURRENT" 2>/dev/null)

echo "---"
echo "Baseline: $BASELINE ($BASELINE_SIZE bytes)"
echo "Current:  $CURRENT ($CURRENT_SIZE bytes)"
echo "Diff:     $OUTPUT"
echo "---"
echo "Open the diff image to inspect visual changes."
echo "If the change is expected, replace baseline: cp $CURRENT $BASELINE"
