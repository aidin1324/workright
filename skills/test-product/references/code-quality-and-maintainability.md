# Code Quality, Correctness, and Maintainability Review

Use when implementation exists. Review only the requested change and its credible blast
radius unless the user asks for a whole-product audit. The goal is to find correctness risks,
project-convention violations, tangled hotspots, and changes likely to create future defects.
Do not refactor or fix them in this testing workflow.

## Contents

1. Establish project-specific standards
2. Trace correctness and side effects
3. Review structure and maintainability
4. Review concurrency, data, integrations, and operability
5. Validate findings and report
6. Completion gate

## 1. Establish project-specific standards

Inspect before judging:

- repository instructions and architecture decisions;
- language/framework versions and official current guidance;
- formatter, linter, type checker, compiler, static-analysis configuration;
- module/package boundaries, dependency direction, naming/error/logging conventions;
- neighboring accepted code implementing a similar responsibility;
- CI quality gates, coverage/mutation rules, and existing waivers;
- change diff, blame/history, prior defects/incidents, and hotspots.

Use precedence:

`explicit project rule → approved architecture/design → configured tool rule → official
version-matched framework practice → established local pattern → general preference`

Do not call a style preference a defect. If local patterns conflict with official guidance,
explain the concrete failure/maintenance risk and classify it as a recommendation unless
accepted requirements are violated.

For a library/framework-specific judgment, verify the installed version and consult its
official current documentation. Never apply a best practice from a different version blindly.
The procedures in this reference remain complete without external tutorials; versioned
documentation is normative test-basis data only for an API, guarantee, or configured
convention specific to that dependency. If that fact cannot be verified, label the conclusion
blocked or conditional instead of guessing.

## 2. Trace correctness and side effects

Follow the changed behavior end to end:

`input → parse/validate → authorize → domain rule/state transition → transaction/persistence →
event/provider → response/read model → cleanup/recovery`

At each step ask:

- what assumptions are made and where are they enforced?
- are invalid/unauthorized inputs rejected before side effects?
- are default/null/empty/overflow/timezone/locale cases explicit?
- does every branch return the right error and preserve invariants?
- can a partial failure leave durable inconsistent state?
- can retry, duplication, cancellation, or concurrency repeat an effect?
- are resources/locks/transactions released on every path?
- does observability distinguish success, rejection, retry, and terminal failure?

Correlate review concerns with an acceptance criterion/risk and derive a test when executable.
Code reading alone may identify a definite defect only when accepted semantics are clear and
the violating path is certain; otherwise report a risk/hypothesis and its validation step.

## 3. Review structure and maintainability

### Responsibility and cohesion

A module/function/class should have a coherent reason to change. Flag when unrelated
validation, persistence, provider orchestration, formatting, and policy are interleaved so
that a small rule change affects many branches. Explain the actual change/defect risk; do not
enforce arbitrary line limits.

### Coupling and boundaries

Check:

- dependency direction follows project architecture;
- domain logic does not depend on UI/transport/storage details without an accepted pattern;
- shared mutable/global state is controlled;
- public interfaces are small and intention-revealing;
- provider/framework details are isolated enough to test failure behavior;
- duplicated business rules cannot drift across callers/services.

### Complexity and “spaghetti” hotspots

Use repository tooling where available. Otherwise identify:

- deeply nested decisions and long mixed-responsibility flows;
- boolean flag combinations with implicit state machines;
- hidden control flow through callbacks/events/global state;
- copy-pasted branches with subtle differences;
- many callers changing for one rule;
- temporal coupling (“must call A before B” but API does not enforce it);
- comments explaining *what* tangled code does instead of a clear model;
- conditionals that should be an explicit decision table/state transition.

Quantitative complexity/duplication is a locator, not automatic severity. Confirm whether the
hotspot is touched, defect-prone, weakly tested, and expensive to reason about.

### Abstraction quality

Flag:

- premature generic frameworks with one use;
- leaky abstractions requiring callers to know internals;
- wrapper layers that add no invariant or policy;
- ambiguous names hiding units, ownership, state, or side effects;
- primitive/stringly typed values where the project normally uses domain types;
- dead compatibility paths and obsolete feature flags.

Also flag under-abstraction when the same critical rule is implemented independently in
multiple places. Recommend the smallest project-consistent direction; do not redesign outside
the testing task.

### Error handling

Verify errors:

- retain causal context without leaking secrets;
- distinguish user validation, authorization, retryable dependency failure, unknown outcome,
  and terminal internal failure;
- are not silently swallowed or converted to success;
- map consistently at public boundaries;
- trigger rollback/compensation/cleanup as required;
- remain observable and testable.

## 4. Concurrency, data, integrations, and operability

### Data and transactions

Review migrations for forward/backward compatibility, locks, defaults/backfill, rollback,
large-table behavior, and mixed old/new application versions. Review queries for missing
scope/tenant filters, N+1/unbounded scans, unstable pagination, race-prone read-modify-write,
and inconsistent transaction boundaries.

### Concurrency and idempotency

Identify shared state, atomicity assumptions, lock ordering, optimistic version checks,
idempotency keys, unique constraints, retry loops, and cancellation. Derive interleaving tests
for check-then-act, duplicate submission, stale writes, timeout after commit, and worker retry.

### Integration boundaries

Verify timeouts, bounded retry/backoff/jitter, circuit/rate behavior, response/schema/error
mapping, unknown outcome, authentication propagation, and cleanup. Apply the contract
reference when another deployable/provider is involved.

### Performance and scalability risks

Inspect complexity relative to realistic volume, unbounded collection/loading, repeated
serialization/calls, synchronous work in hot paths, contention, cache invalidation, queue
backlog, and missing pagination/batching. Code review raises a hypothesis; performance claims
require the performance protocol.

### Security and privacy

Look for missing authoritative authorization, tenant scoping, unsafe interpolation/parsing,
secret/personal data in logs/errors/cache, dangerous defaults, insecure file/path handling,
and broad infrastructure permissions. Apply the security playbook for validation.

### Testability and observability

Critical behavior should allow controlled inputs, deterministic time/randomness, observable
state, correlation, and safe failure simulation. Flag hidden clocks, hard-coded provider
clients, nondeterministic global state, or absent business metrics when they prevent
defensible testing/operations.

## 5. Validate findings and report

Use this format:

```text
CQ-004 — Maintainability/Correctness risk — <title>
Location and scope
Project rule or accepted invariant
Observed code/data flow
Concrete failure/change scenario
Evidence and confidence
Affected criteria/risks/callers
Validation test or analysis
Impact if confirmed
Suggested direction (no implementation)
```

Classify:

- **confirmed product defect:** accepted behavior is demonstrably violated; use defect
  severity and stop rules;
- **probable correctness risk:** plausible path needs execution/access to confirm;
- **maintainability hotspot:** elevated future change/diagnosis risk;
- **project-convention violation:** configured/explicit rule is broken;
- **recommendation:** improvement without current requirement/risk violation.

Do not inflate cosmetic structure concerns to High severity. Raise priority when the hotspot
combines critical logic, high churn, high complexity/coupling, poor observability, and weak
tests.

## 6. Completion gate

Review is complete when:

- project/version-specific rules were discovered rather than assumed;
- the changed behavior and credible callers/side effects were traced;
- correctness, authorization, transactions, failure/retry, concurrency, and cleanup were
  assessed where applicable;
- complexity/coupling/duplication findings include a concrete risk, not taste;
- executable hypotheses became cases or explicit blockers;
- confirmed defects were reported immediately and not fixed;
- the report distinguishes defects, risks, hotspots, rule violations, and recommendations.
