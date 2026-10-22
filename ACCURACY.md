# ACCURACY: every number and log line the videos show, mapped to the file and line it comes from

Line numbers are 1-based lines of `run.jsonl` (one JSON object per captured physical line, `text` = the line as
`docker logs --timestamps` received it, timestamp prefix removed by logcap and kept in `tRecvMs`).

## Episode 1

| Shown in the video | Source |
|---|---|
| Spring Boot 4.1.2 | `ep1-transactional/evidence/replays/ep1-trap/run.jsonl` L9 (banner), `run.meta.json` `versions.springBoot` |
| Java 21.0.12.1 | ep1-trap L11 |
| `this.saveAndCharge(item);` (trap) | `ep1-transactional/src/main/java/lab/trap/Checkout.java` L22 |
| `writer.saveAndCharge(item);` (fix) | `ep1-transactional/src/main/java/lab/fix/Checkout.java` L22 |
| `@Transactional` / `public void saveAndCharge(String item)` | trap/Checkout.java L25-26; fix/OrderWriter.java L20-21 |
| trap: `Executing prepared SQL update`, no transaction line above it | ep1-trap L18 (L17 is the lab's call line) |
| trap: `LAB: at the insert, transaction active = false` | ep1-trap L20 |
| trap: `LAB: placeOrder threw PaymentDeclinedException: card declined for book` | ep1-trap L21 |
| trap: `LAB: orders after failure = 1` | ep1-trap L24 |
| fix: `Creating new transaction with name [lab.fix.OrderWriter.saveAndCharge]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT` | `ep1-transactional/evidence/replays/ep1-fix/run.jsonl` L18 |
| fix: `Getting transaction for [lab.fix.OrderWriter.saveAndCharge]` | ep1-fix L21 |
| fix: `Executing prepared SQL update` | ep1-fix L22 |
| fix: `LAB: at the insert, transaction active = true` | ep1-fix L24 |
| fix: `Initiating transaction rollback` | ep1-fix L69 |
| fix: `Rolling back JDBC transaction on Connection [...]` | ep1-fix L70 |
| fix: `LAB: orders after failure = 0` | ep1-fix L75 |
| before/after panel rows | `ep1-transactional/video/before-after-panel.txt` (every row checked against the captures by `tests/test_ep1.py`) |
| outcome panel rows | `ep1-transactional/video/outcome-panel.txt` (same test) |
| docs quote "only external method calls coming in through the proxy are intercepted" | https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html (fetched 22 Oct 2026) |
