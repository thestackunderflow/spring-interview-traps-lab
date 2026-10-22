#!/usr/bin/env bash
# Episode 1: build (JUnit runs in the Maven image), then capture the trap run and the fixed run, one container each,
# with logcap (docker logs --timestamps). The jar is baked into the image, so the recorded docker args hold no host path.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
EP=ep1-transactional
[ "${SKIP_BUILD:-0}" = 1 ] || build_ep "$EP"
capture "$EP" ep1-trap --spring.profiles.active=trap
capture "$EP" ep1-fix --spring.profiles.active=fix
log "captured: $(wc -l < "$EP/evidence/replays/ep1-trap/run.jsonl") trap lines, $(wc -l < "$EP/evidence/replays/ep1-fix/run.jsonl") fix lines"
