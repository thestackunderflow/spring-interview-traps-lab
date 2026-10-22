#!/usr/bin/env bash
# Runs every episode's JUnit tests (Maven + JDK 21 in the pinned Maven image), then the Python evidence tests (pinned
# python image). Nothing runs on the host but docker. Usage: bash tests/run-tests.sh [log-file] [unittest pattern]
# Extra private words for the privacy test: LAB_PRIVATE_WORDS="word1,word2" bash tests/run-tests.sh
set -uo pipefail
cd "$(dirname "$0")/.."
source scripts/lib.sh
LOG="${1:-tests/out/test-run.log}"
PATTERN="${2:-test_*.py}"
mkdir -p "$(dirname "$LOG")"
: > "$LOG"
for ep in ep*/; do
  ep=${ep%/}
  echo "== JUnit $ep" | tee -a "$LOG"
  mvn_ep "$ep" test 2>&1 | tail -40 | tee -a "$LOG"
  grep -ho 'tests="[0-9]*" errors="[0-9]*" skipped="[0-9]*" failures="[0-9]*"' "$ep"/target/surefire-reports/TEST-*.xml 2>/dev/null \
    | sed "s/^/JUnit $ep: /" | tee -a "$LOG"
done
echo "== Python evidence tests" | tee -a "$LOG"
docker run --rm -v "$LAB_W:/lab" -w /lab -e PYTHONDONTWRITEBYTECODE=1 -e LAB_PRIVATE_WORDS="${LAB_PRIVATE_WORDS:-}" "$PYTHON_IMAGE" \
  python -m unittest discover -s tests -p "$PATTERN" -v 2>&1 | tee -a "$LOG" | grep -E '^(FAIL|ERROR):|^Ran |^OK|^FAILED'
