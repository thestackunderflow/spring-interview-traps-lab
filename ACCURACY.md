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

## Episode 2

| Shown in the video | Source |
|---|---|
| `@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)` | `ep2-prototype/src/main/java/lab/Ticket.java` L10 |
| trap field / call `private final Ticket ticket;` / `return ticket.describe(call);` | `ep2-prototype/src/main/java/lab/trap/TicketCounter.java` L13, L20 |
| fix `ObjectProvider<Ticket> tickets` / `tickets.getObject().describe(call)` | `ep2-prototype/src/main/java/lab/fix/TicketCounter.java` L13, L20 |
| trap `LAB: Ticket #1 constructed` | `ep2-prototype/evidence/replays/ep2-trap/run.jsonl` L13 |
| trap `LAB: bean-factory TRACE logging on from here` | ep2-trap L15 |
| trap calls 1-3, `Ticket #1, identityHashCode 71c905a3` | ep2-trap L16, L17, L18 |
| fix `Creating instance of bean 'ticket'` | `ep2-prototype/evidence/replays/ep2-fix/run.jsonl` L15, L19, L23 |
| fix calls: `#1 67a056f1`, `#2 72ed9aad`, `#3 4690f583` | ep2-fix L18, L22, L26 |
| docs quote "The prototype instance is the sole instance that is ever supplied to the singleton-scoped bean." | https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html (fetched 22 Oct 2026) |
| follow-up: destruction callbacks of prototypes are not called | same page: "in the case of prototypes, configured destruction lifecycle callbacks are not called" |
