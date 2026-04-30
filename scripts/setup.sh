#!/usr/bin/env bash
# mini-harness one-shot setup
# Idempotent: safe to re-run.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

bold() { printf "\033[1m%s\033[0m\n" "$*"; }
ok()   { printf "  \033[32m✓\033[0m %s\n" "$*"; }
warn() { printf "  \033[33m!\033[0m %s\n" "$*"; }

bold "[1/5] Checking tools"
for cmd in uv git python3; do
  if ! command -v "$cmd" >/dev/null; then
    echo "  missing: $cmd" >&2; exit 1
  fi
  ok "$cmd: $(command -v $cmd)"
done

bold "[2/5] Bootstrapping .env"
if [[ ! -f .env ]]; then
  cp .env.example .env
  ok "created .env from .env.example  (fill in your API keys)"
else
  ok ".env already exists"
fi

bold "[3/5] Creating Python venv (.venv) with uv"
# Pin to 3.12 for ecosystem compat (some libs lag behind 3.14)
uv venv --python 3.12 --quiet
ok ".venv ready ($(.venv/bin/python --version))"

bold "[4/5] Installing dependencies"
uv sync --extra dev --quiet
ok "deps installed"

bold "[5/5] Smoke test"
.venv/bin/python - <<'PY'
import anthropic, openai, httpx, pydantic, structlog, rich
print(f"  anthropic={anthropic.__version__}  openai={openai.__version__}  pydantic={pydantic.VERSION}")
PY
ok "imports OK"

echo
bold "Next steps:"
cat <<EOF
  1. Edit .env and fill in at least ANTHROPIC_API_KEY or DEEPSEEK_API_KEY
  2. Activate the venv:   source .venv/bin/activate
  3. Run Day 1 script:    python experiments/day01_react_from_scratch.py "What is 17 * 23 + 5?"
EOF
