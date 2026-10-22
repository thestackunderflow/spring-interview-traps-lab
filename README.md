# Spring Boot Interview Traps, Proven: the lab

One folder per episode of The Stack Underflow series "Spring Boot Interview Traps, Proven". Each episode is a tiny
Spring Boot 4.1.2 app (no web server) with two Spring profiles: `trap` (the interview trap, reproduced) and `fix` (one
change, same flow). Each run prints Spring's own log lines at DEBUG/TRACE for the parts that matter, plus a few lines the
lab prints itself; those always start with `LAB:`.

Everything runs in Docker (pinned images, by digest, in `scripts/lib.sh`). Nothing is installed on the host.

| Folder | Episode | The trap | What the log shows |
|---|---|---|---|
| `ep1-transactional/` | #1 | `placeOrder()` calls `this.saveAndCharge()` (`@Transactional`) in the same class; it throws; the order row stays | trap: no `Creating new transaction`, `LAB: orders after failure = 1`; fix: `Creating new transaction ...`, `Initiating transaction rollback`, `= 0` |
| `ep2-prototype/` | #2 | a prototype `Ticket` injected into a singleton `TicketCounter`; three calls get the same object | trap: one Ticket at startup, no `Creating instance of bean 'ticket'` during the calls; fix (`ObjectProvider`): that line before every call, three Tickets |
| `ep3-configuration/` | #3 | `@Bean` methods in a `@Component`: `orderService()` calls `auditLog()`; the singleton's constructor runs twice | trap: one `Creating shared instance ... 'auditLog'`, constructor `#1` and `#2`, `same object? false`; fix (`@Configuration`): `Successfully enhanced lab.fix.AppBeans`, one run, `true` |

## Run it

```bash
bash tests/run-tests.sh          # JUnit (in the Maven image) + Python evidence tests (in the python image)
bash scripts/ep1.sh              # build, then capture the trap and the fixed run with docker logs --timestamps (ep2.sh, ep3.sh likewise)
```

Captures land in `<episode>/evidence/replays/<scenario>/run.jsonl` (+ `run.meta.json`), written by the video engine's
`logcap` tool from `docker logs --timestamps`. Tests were written first (red, `tests/out/red-phase.log`), then the
app (green, `tests/out/green-phase.log`). Measured vs expected: `LAB-STATUS.md`. Every number in the videos: `ACCURACY.md`.

License: Apache-2.0.
