#!/usr/bin/env python3
"""Compare two screenshots (baseline vs current) using ImageMagick.

Requires ImageMagick (magick) installed.

Usage:
    python scripts/snapshot_diff.py baseline.png current.png
    python scripts/snapshot_diff.py baseline.png current.png diff.png
"""

import argparse
import os
import subprocess
import sys
import time


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two screenshots")
    parser.add_argument("baseline", help="Baseline screenshot path")
    parser.add_argument("current", help="Current screenshot path")
    parser.add_argument("output", nargs="?", default=None, help="Output diff path")
    args = parser.parse_args()

    for name, path in [("Baseline", args.baseline), ("Current", args.current)]:
        if not os.path.isfile(path):
            print(f"ERROR: {name} not found: {path}", file=sys.stderr)
            sys.exit(1)

    if subprocess.run(["which", "magick"], capture_output=True).returncode != 0:
        print("ERROR: ImageMagick not found. Install with: brew install imagemagick", file=sys.stderr)
        sys.exit(1)

    output = args.output or f"diff-{int(time.time())}.png"

    result = subprocess.run(
        ["magick", "compare", "-metric", "AE", "-highlight-color", "red",
         args.baseline, args.current, output],
        capture_output=True, text=True
    )

    baseline_size = os.path.getsize(args.baseline)
    current_size = os.path.getsize(args.current)

    print("---")
    print(f"Baseline: {args.baseline} ({baseline_size} bytes)")
    print(f"Current:  {args.current} ({current_size} bytes)")
    print(f"Diff:     {output}")
    print("---")
    print("Open the diff image to inspect visual changes.")
    print(f"If the change is expected, replace baseline: cp {args.current} {args.baseline}")


if __name__ == "__main__":
    main()
