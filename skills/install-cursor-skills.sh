#!/usr/bin/env bash
# macOS / Linux wrapper for the cross-platform Python installer.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$DIR/install-cursor-skills.py"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$SCRIPT" "$@"
elif command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT" "$@"
fi

echo "Python 3 is required to install skills." >&2
exit 1
