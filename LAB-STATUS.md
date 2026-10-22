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

Follow-up run (`ep1-follow`, profile `follow`, added after the script gate): `placeOrder` is `@Transactional`,
`saveAndCharge` is `@Transactional(propagation = REQUIRES_NEW)`, called with `this.`. Exactly one
`Creating new transaction with name [lab.follow.Checkout.placeOrder]` (L18), no `Suspending current transaction`,
`LAB: at the insert, transaction active = true`, `Initiating transaction rollback`, `LAB: orders after failure = 0`.
Captured with the same jar code for trap and fix (only the new `follow` class was added; trap/fix captures kept).

## Episode 2: prototype bean injected into a singleton (`ep2-prototype/`)

**State: DONE, 22 Oct 2026.** Tests: 4 JUnit + 8 evidence tests green. The lab turns on Spring's own TRACE logging for
`org.springframework.beans.factory.support.DefaultListableBeanFactory` after startup (Boot `LoggingSystem`) and says so
in a `LAB:` line, so the log shows each bean created during the calls without the startup flood.

| | Expected | Measured |
|---|---|---|
| trap: Tickets built | 1, at startup | `LAB: Ticket #1 constructed` (ep2-trap L13), before the TRACE switch (L15) |
| trap: the 3 calls | same Ticket, same identity | L16-18: `Ticket #1, identityHashCode 71c905a3` three times |
| trap: `Creating instance of bean 'ticket'` during the calls | 0 | 0 |
| fix: Tickets built | 3, one per call | `Creating instance of bean 'ticket'` (L15, L19, L23) then `LAB: Ticket #1/#2/#3 constructed` |
| fix: the 3 calls | 3 Tickets, 3 identities | L18 `#1 67a056f1`, L22 `#2 72ed9aad`, L26 `#3 4690f583` |
| A/B shape | field, constructor, call | JUnit `VariantShapeTest`: exactly those 4 rows differ in the class body |

## Episode 3: @Configuration vs @Component, lite mode (`ep3-configuration/`)

**State: DONE, 22 Oct 2026.** Tests: 4 JUnit + 9 evidence tests green. Logging: DEBUG
`org.springframework.beans.factory.support.DefaultListableBeanFactory` (one "Creating shared instance of singleton
bean" per singleton), TRACE `org.springframework.context.annotation.ConfigurationClassEnhancer`.

| | Expected (acc M3) | Measured |
|---|---|---|
| `Creating shared instance of singleton bean 'auditLog'` | once in both runs | ep3-trap L36, ep3-fix L37: once each |
| AuditLog constructor runs | trap 2, fix 1 | trap L38 `#1`, L40 `#2`; fix L39 `#1` only |
| `Successfully enhanced lab.fix.AppBeans; enhanced class name is: lab.fix.AppBeans$$SpringCGLIB$$0` | fix only | ep3-fix L15; absent in the trap |
| same object? | trap false, fix true | trap L85 `false` (identityHashCode 247667dd vs 6f099cef), fix L85 `true` (4d74c3ba twice) |
| one change | `@Component` -> `@Configuration` | JUnit `VariantShapeTest`: only the annotation row and the profile row differ in the class |
