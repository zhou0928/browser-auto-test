#!/bin/bash
set -e

# test-env.sh - Start a local dev server and open a Playwright-controlled browser
# Usage: bash /mnt/skills/user/browser-auto-test/scripts/test-env.sh [port] [dev-command]

PORT="${1:-5173}"
DEV_CMD="${2:-pnpm run dev}"

echo "Starting dev server on port $PORT..." >&2
echo "Command: $DEV_CMD" >&2

# Start dev server in background
$DEV_CMD &
DEV_PID=$!

# Wait for port to be ready
for i in $(seq 1 30); do
  if nc -z localhost "$PORT" 2>/dev/null; then
    echo "Dev server is ready on http://localhost:$PORT" >&2
    echo "http://localhost:$PORT"
    exit 0
  fi
  sleep 1
done

echo "ERROR: Server did not start within 30 seconds" >&2
kill $DEV_PID 2>/dev/null
exit 1
