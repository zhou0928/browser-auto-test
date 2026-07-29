#!/usr/bin/env python3
"""Start a local dev server and wait for it to become ready.

Usage:
    python scripts/test_env.py                     # default port 5173
    python scripts/test_env.py --port 3000
    python scripts/test_env.py --port 8080 --cmd "npm start"
"""

import argparse
import socket
import subprocess
import sys
import time


def port_ready(port: int) -> bool:
    """Check if something is listening on localhost:port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Start dev server and wait for port")
    parser.add_argument("--port", type=int, default=5173, help="Port to wait on")
    parser.add_argument("--cmd", type=str, default="npm run dev", help="Dev server command")
    args = parser.parse_args()

    print(f"Starting dev server on port {args.port}...", file=sys.stderr)
    print(f"Command: {args.cmd}", file=sys.stderr)

    proc = subprocess.Popen(args.cmd, shell=True)

    for _ in range(30):
        if port_ready(args.port):
            print(f"http://localhost:{args.port}")
            return
        time.sleep(1)

    print("ERROR: Server did not start within 30 seconds", file=sys.stderr)
    proc.kill()
    sys.exit(1)


if __name__ == "__main__":
    main()
