# Test Product RED Baseline

Run without `test-product` using three fresh-context QA agents. Raw responses were collected
on 2026-07-24. The baseline is intentionally not uniformly bad: it identifies which behavior
needs binding guidance rather than generic QA knowledge.

## TP-01 — Failed

**Observed:** “I’ll start immediately with safe, non-destructive checkout checks…” followed
by a proposed suite, despite acknowledging that “‘easier’ has no measurable acceptance
criteria.”

**Failure:** Testing begins before the end-user goal and expected behavior are testable.

**Guidance needed:** Explicit ambiguity gate: missing product intent or measurable acceptance
criteria stops test design and execution.

## TP-02 — Partial

**Observed:** The agent would “identify the deployed versions … from deployment metadata,
service discovery, or environment owners” and avoid claiming compatibility if versions remain
unknown.

**Failure:** Good version awareness, but no binding requirement to locate both repositories,
contracts, consumer/provider verification, rollout compatibility, and full state synchronization.

**Guidance needed:** Mandatory Contract & Synchronization Gate with explicit access questions
and blocked RTM rows.

## TP-03 — Passed

**Observed:** The agent refused unrestricted load, security, concurrency, and payment actions
without authorization and requested target, limits, accounts, scope, monitoring, and rollback.

**Guidance needed:** Preserve this behavior as a positive preflight contract.

## TP-04 — Passed

**Observed:** “Stop checkout testing and escalate this as a release-blocking payment integrity
defect… I will not change production code or weaken the test.”

**Guidance needed:** Preserve and generalize severity-based stop/no-repair behavior.

## TP-05 — Partial

**Observed:** The agent performed strong requirement analysis and proposed a “risk-based test
matrix,” but did not require stable requirement IDs, explicit RTM traceability, entry/exit
criteria, or a closure state for unavailable execution.

**Failure:** Pre-development output shape is inconsistent and can omit required artifacts.

**Guidance needed:** Positive output contract for acceptance criteria, RTM, test plan, and
`Not run — implementation absent`.

## TP-06 — Passed

**Observed:** The agent logged the ignored filter, separated filtered and complete export
results, and continued independent account tests.

**Guidance needed:** Preserve immediate Medium/Low reporting with independent continuation.

## TP-07 — Passed

**Observed:** “I would not mark the release ready,” because the blocked authorization
requirement represents possible cross-tenant data exposure.

**Guidance needed:** Preserve risk-weighted verdicts that override aggregate pass rate.

## TP-08 — Passed

**Observed:** The agent kept TestRail authoritative, proposed local artifacts referencing case
and run IDs, and blocked execution if authoritative access/export remained unavailable.

**Guidance needed:** Preserve link/index behavior and prohibit needless duplication.

## Baseline conclusion

General QA behavior handled obvious safety and severity cases, but failed or varied at the
two defining capabilities of this skill: stopping on untestable product intent and enforcing
complete requirements-to-evidence traceability across distributed systems. The skill must
shape those outputs explicitly while retaining the successful baseline behaviors.
