# Defects, Metrics, and Closure

Read when any defect, blocker, flaky result, or final verdict is reported.

## Classify impact

| Status | Use when | Execution |
|---|---|---|
| Critical | Data loss/corruption, exploitable security, major outage, irreversible effect | Report immediately; stop |
| High | Core goal/critical flow fails, serious contract break, no reasonable workaround | Report immediately; stop |
| Medium | Material partial failure; independent evidence remains valid | Report immediately; continue independent tests |
| Low | Minor functional/cosmetic/usability issue | Record; continue |
| Blocked | Access, environment, data, dependency, or authority is missing | Report affected RTM rows and residual risk |

Severity describes product impact. `Blocked` and flaky/test-defect/environment-failure are
execution classifications, not product defects.

## Report a defect

Use:

```text
DEF-003 — High — Old consumer cannot parse new payment event
Requirement/Test: REQ-012 / TC-CONTRACT-007
Environment/Versions: staging; producer 2.4.0; consumer 2.2.1
Preconditions: rolling deployment with old consumer
Reproduction: exact bounded steps or command
Expected: old consumer processes event during supported rollout
Actual: deserialization rejects new required field
Reproducibility: 5/5
Evidence: sanitized schema diff and correlation/log reference
Impact: payment state stops synchronizing
Execution: paused; dependent business-flow tests not run
```

Keep title, reproduction, expected/actual, versions, evidence, and user impact concrete. Redact
secrets and personal data.

Never fix the product, weaken the test, or ask to repair it inside this workflow. State:
“Remediation requires a separate task.”

## Handle flakiness

Do not hide a failure with retries. Record:

- pass/fail sequence and retry policy;
- seed, timing, machine, versions, and resource conditions;
- whether isolation, ordering, shared state, network, clocks, or race behavior is implicated;
- confidence lost and affected RTM rows.

Use `Inconclusive` or residual risk when nondeterminism prevents a reliable claim.

## Report meaningful metrics

Include:

- requirements total and Passed/Failed/Blocked/Not run/Not applicable;
- test cases by result and level;
- defects by severity and requirement;
- RTM coverage;
- flaky/non-deterministic count;
- code/branch/mutation coverage only when measured;
- performance/security/compatibility metrics only when applicable;
- skipped/blocked types and residual risk.

Do not use defect density without defining denominator and period. Do not equate zero found
defects with zero defects.

## Reconcile and close

For every RTM row, confirm test IDs, result, evidence, and defect IDs. For every considered test
type, show selected/skipped/blocked reason. For every used technique, show why, cases, and
findings.

Choose one verdict:

- `Ready`: all critical exit criteria met; no open Critical/High; residual risk acceptable;
- `Ready with concerns`: exit criteria allow release and named noncritical risks remain;
- `Not ready`: critical criterion failed, open Critical/High exists, or safety threshold failed;
- `Inconclusive`: missing or unreliable evidence prevents a defensible decision.

Aggregate pass rate never overrides a failed or blocked critical requirement.

Archive RTM, plan, cases, defect log, summary, reusable scripts, sanitized data, and evidence
indexes. Run a short retrospective: what increased confidence, what caused delay/flakiness, and
what durable test/process improvement is justified.
