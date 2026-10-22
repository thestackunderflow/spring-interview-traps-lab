# Lab status

## Episode 1: @Transactional self-invocation (`ep1-transactional/`)

**State: DONE, 22 Oct 2026.** Spring Boot 4.1.2 (released 22 Oct 2026), Spring Framework 7.0.10, H2 2.4.240, Java
21.0.12.1. Tests: 6 JUnit + 11 Python evidence tests green (`tests/out/green-phase.log`); red phase first
(`tests/out/red-phase.log`).

| | Expected (plan rev 2) | Measured (captures, `docker logs --timestamps`) |
|---|---|---|
| trap: transaction line before the insert | none | none (`Creating new transaction`, `Getting transaction for`, `Initiating transaction rollback` all absent) |
| trap: lab probe at the insert | `transaction active = false` | `LAB: at the insert, transaction active = false` (ep1-trap L20) |
| trap: rows after the failure | 1 | `LAB: orders after failure = 1` (ep1-trap L24) |
| fix: transaction begin | `Creating new transaction with name [...]` from `JdbcTransactionManager` | `Creating new transaction with name [lab.fix.OrderWriter.saveAndCharge]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT` (ep1-fix L18), logger `o.s.jdbc.support.JdbcTransactionManager` |
| fix: order of lines | Creating -> Acquired/Switching -> Getting transaction -> insert -> Completing -> rollback | as predicted (L18, L19-20, L21, L22, L25, L70); plus a TRACE `MethodRollbackEvent` line with the exception's stack trace (L26-68), new in this version, not predicted |
| fix: lab probe | `true` | `LAB: at the insert, transaction active = true` (ep1-fix L24) |
| fix: rows after the failure | 0 | `LAB: orders after failure = 0` (ep1-fix L75) |
| the trap bean is still proxied | yes (acc M2) | JUnit `theBeanIsProxiedAnywayOnlyTheInnerCallSkipsIt`: `AopUtils.isCglibProxy(shop)` true |
| one change between trap and fix | the call target only | JUnit `VariantShapeTest`: `saveAndCharge` byte-identical in `trap/Checkout.java` and `fix/OrderWriter.java`; `placeOrder` differs in one row |

Exit code 0 in both runs. No redactions by logcap. Runs: one container each, image `traps-lab-ep1-transactional:1.0`
(jar baked in, no bind mount).
