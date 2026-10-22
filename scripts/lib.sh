#!/usr/bin/env bash
# Shared settings for the lab scripts. Source it from the lab root: `source scripts/lib.sh`.
# Every image is pinned by tag AND digest. Nothing is installed on the host: Maven, Java and Python run in containers.
export MSYS_NO_PATHCONV=1
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAB_W="$(cd "$LAB_ROOT" && (pwd -W 2>/dev/null || pwd))"
cd "$LAB_ROOT"

MAVEN_IMAGE=maven:3.9.16-eclipse-temurin-21@sha256:99e61abcff91a9b1333463bd8451fb18495d6eba9250ac66a338b518f8278320
JDK_IMAGE=eclipse-temurin:21.0.12.1_1-jdk-noble@sha256:107215954359f1ab0be058a247d7c64ed6e69c71c1682d471d38ef751ec8e964
PYTHON_IMAGE=python:3.13-slim@sha256:70729b46c69b4f1e97c4822c1af3df53a1476cf5ddc6c087c0c10bc3a5678c2f
M2_VOLUME=traps-lab-m2
# logcap lives in the video engine repo (mcp-canvas); it writes run.jsonl + run.meta.json from `docker logs --timestamps`
LOGCAP="${LOGCAP:-$LAB_ROOT/../Refream-Canvas/mcp-canvas/tools/logcap/logcap.sh}"

log() { echo "[$(date -u +%H:%M:%S)] $*" >&2; }

free_gb() {  # host free physical memory in GB (Windows), via PowerShell
  powershell.exe -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)" | tr -d '\r'
}

ram_wait() {  # other agents share the machine: wait for >= 3 GB free
  local f
  while :; do
    f=$(free_gb)
    awk -v f="$f" 'BEGIN{exit !(f>=3)}' && return 0
    log "free RAM ${f} GB < 3 GB: waiting 120 s"; sleep 120
  done
}

mvn_ep() {  # mvn_ep <episode dir> <mvn args...>: Maven in the pinned image, cache in a named volume
  local ep=$1; shift
  docker run --rm -v "$LAB_W:/lab" -v "$M2_VOLUME:/root/.m2" -w "/lab/$ep" "$MAVEN_IMAGE" mvn -q -B "$@"
}

py() {  # python in the pinned image, lab mounted at /lab
  docker run --rm -i -v "$LAB_W:/lab" -w /lab -e PYTHONDONTWRITEBYTECODE=1 "$PYTHON_IMAGE" python "$@"
}

image_of() { echo "traps-lab-$1:1.0"; }   # the jar is baked into an image, so `docker run` args carry no host path

build_ep() {  # build_ep <episode dir>: jar in the Maven image (tests run), then the runtime image
  local ep=$1
  ram_wait
  mvn_ep "$ep" package
  docker build -q -t "$(image_of "$ep")" -f docker/Dockerfile --build-arg JAR="$ep/target/app.jar" . >/dev/null
  log "built $(image_of "$ep")"
}

capture() {  # capture <episode dir> <scenario> [app args...]: one container, logcap (docker logs --timestamps)
  local ep=$1 sc=$2; shift 2
  local out="$LAB_W/$ep/evidence/replays/$sc"   # absolute: logcap runs its node step from the engine repo
  rm -rf "$out"
  bash "$LOGCAP" --out "$out" --scenario "$sc" --timeout 120 -- --memory 768m "$(image_of "$ep")" "$@"
}
