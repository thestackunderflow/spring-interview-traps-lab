#!/usr/bin/env bash
# Episode 2: build (JUnit runs in the Maven image), then capture the trap run and the fixed run, one container each,
# with logcap (docker logs --timestamps). The jar is baked into the image, so the recorded docker args hold no host path.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
EP=ep2-prototype
[ "${SKIP_BUILD:-0}" = 1 ] || build_ep "$EP"
capture "$EP" ep2-trap --spring.profiles.active=trap
capture "$EP" ep2-fix --spring.profiles.active=fix
log "captured: $(wc -l < "$EP/evidence/replays/ep2-trap/run.jsonl") trap lines, $(wc -l < "$EP/evidence/replays/ep2-fix/run.jsonl") fix lines"
