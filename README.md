# Spring Boot Interview Traps, Proven: the lab

One folder per episode of The Stack Underflow series "Spring Boot Interview Traps, Proven". Each episode is a tiny
Spring Boot 4.1.2 app (no web server) with two Spring profiles: `trap` (the interview trap, reproduced) and `fix` (one
change, same flow). Each run prints Spring's own log lines at DEBUG/TRACE for the parts that matter, plus a few lines the
lab prints itself; those always start with `LAB:`.

Everything runs in Docker (pinned images, by digest, in `scripts/lib.sh`). Nothing is installed on the host.

| Folder | Episode | The trap | What the log shows |
|---|---|---|---|
| `ep1-transactional/` | #1 | `placeOrder()` calls `this.saveAndCharge()` (`@Transactional`) in the same class; it throws; the order row stays | trap: no `Creating new transaction`, `LAB: orders after failure = 1`; fix: `Creating new transaction ...`, `Initiating transaction rollback`, `= 0` |

## Run it

```bash
bash tests/run-tests.sh          # JUnit (in the Maven image) + Python evidence tests (in the python image)
bash scripts/ep1.sh              # build, then capture the trap and the fixed run with docker logs --timestamps
```

Captures land in `<episode>/evidence/replays/<scenario>/run.jsonl` (+ `run.meta.json`), written by the video engine's
`logcap` tool from `docker logs --timestamps`. Tests were written first (red, `tests/out/red-phase.log`), then the
app (green, `tests/out/green-phase.log`). Measured vs expected: `LAB-STATUS.md`. Every number in the videos: `ACCURACY.md`.

License: Apache-2.0.
