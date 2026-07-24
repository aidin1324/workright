---
name: test-product
description: Use when a feature, business flow, release, integration, or whole software product needs requirements-based test planning, quality assessment, or testing before development or after implementation or deployment.
---

# Test Product

Test the user's real outcome with risk-based, traceable evidence. Prefer the cheapest test
that can disprove a requirement; escalate to broader and costlier testing only when the
remaining risk justifies it.

## Non-negotiable boundaries

- Never fix a defect in this workflow. Never modify production code, weaken assertions, or add
  a test-only workaround that conceals product behavior.
- Create or modify only approved test artifacts: existing test directories, sanitized fixtures,
  test-only configuration or IaC, test scripts, and QA documentation.
- Inspect the repository and connected systems before guessing commands, architecture,
  contracts, versions, environments, or sources of truth.
- Stop before case design when the user goal or a material expected result is ambiguous.
- Report every product defect or blocker to the user as soon as it is confirmed.
- Stop all affected execution on Critical/High defects, data risk, an invalid environment, or
  a requirement conflict that changes the oracle. Continue only independent work after
  Medium/Low findings.
- Do not ask to repair the defect inside this workflow. State that remediation requires a
  separate task; the user can request it later.
- Never run destructive security tests, load, fault injection, real external side effects, or
  production mutations without action-specific approval.
- Never claim `Passed`, compatibility, coverage, or readiness without current, reproducible
  evidence.

## Operating model

Follow this sequence and do not cross a gate early:

`Intent → Discovery → Classification → Test basis → Acceptance criteria → Ambiguity gate →
Risk → Technique/layer selection → RTM → Plan → Proportional approval → Artifacts →
Environment qualification → Smoke → Execution → Immediate findings → Reconciliation →
Closure`

Keep user communication brief. For each important technique, say what was used and why in one
factual sentence. Explain a pause with the exact missing decision, access, evidence, or safety
approval.

## Invocation router

After discovery, choose one intent route:

| Route | Continue through | Do not do |
|---|---|---|
| `Shift Left / plan-only` | requirements, risk, models, RTM, plan, design-readiness closure | runtime environment or execution |
| `Read-only assessment` | inspect current evidence/quality risks, reconcile what can be proven, assessment closure | files, mutations, or implied runtime proof |
| `Focused execution` | compact plan, selected artifacts if requested, safe execution, closure | broad irrelevant suites |
| `Full execution` | complete applicable matrix, approved broad/live/non-functional work, closure | unsafe “test everything” behavior |

Choose target mode independently:

| Target mode | Meaning |
|---|---|
| `Local/hermetic` | in-process, local, containerized, or isolated dependency work |
| `Isolated live` | running staging/test/preview/sandbox target |
| `Deployed/production-like` | shared deployed or production target requiring full preflight and bounded authority |

Every route uses the same oracle, traceability, immediate-defect, evidence, and verdict rules.
A low-risk Focused run may keep a compact RTM/summary in chat when files were not requested.
`Pre-development` closes with a design-readiness verdict; it does not pretend runtime proof.

Step exit conditions:

- discovery: the behavior path, change surface, commands, dependencies, and missing access are
  known enough to classify;
- requirements/risk: material criteria have complete oracles and calibrated risk, or are
  explicitly blocked;
- design/RTM: each applicable criterion has a technique, level, case direction, and evidence
  contract;
- planning: target, order, entry/exit/stop, effects, cleanup, cost, and required approvals are
  explicit;
- environment: fidelity gaps are recorded and qualification/smoke support the intended claim;
- execution: every selected case is terminal or a stop/block is reconciled;
- closure: RTM, defects, evidence, metrics, residual risk, and verdict agree.

## 1. Discover before asking

Read applicable repository instructions and product documentation. Inspect status and diffs,
manifests, lockfiles, architecture, test layout, CI/CD, deployment configuration, prior
reports, feature flags, migrations, and real run commands. Trace the requested behavior
through input, validation, authorization, domain logic, persistence, integrations, side
effects, observability, and user-visible output.

Locate connected repositories, services, providers, schemas, events, generated clients,
deployed versions, and rollout configuration. Search before asking anything code or
documentation can answer. Preserve unrelated user changes.

## 2. Classify the request

Classify four independent dimensions and give concrete reasons:

| Dimension | Values |
|---|---|
| Lifecycle | `Pre-development`, `Implemented`, `Deployed` |
| Scope | `Feature`, `Business flow`, `Integration or contract`, `Change or release`, `Whole product` |
| Risk | `Low`, `Medium`, `High`, `Critical` |
| Profile | `Focused`, `Full ride` |

Lifecycle and scope may be final after discovery; risk and profile remain provisional until
acceptance criteria and calibrated risk scoring are complete.

Recommend `Focused` by default: requirements-complete sanity testing plus the smallest
risk-targeted regression set. Recommend `Full ride` for critical flows, releases, broad
changes, distributed-version changes, weak existing evidence, or an explicit request.
`Full ride` means every applicable layer plus approved broad or human simulation; it never
means every known test or permission for unsafe work.

Use the calibrated risk and profile rules in
[requirements-rtm-and-risk.md](references/requirements-rtm-and-risk.md) and
[test-planning.md](references/test-planning.md). Reclassify when discovery changes exposure.
Use the most advanced lifecycle state: `Deployed` when testing a running target, otherwise
`Implemented` when code exists, otherwise `Pre-development`.

## Conditional reference router

Before acceptance design, RTM, or planning, load every applicable branch:

- any cross-process/service/provider/schema/version boundary → read
  [contracts-and-distributed-systems.md](references/contracts-and-distributed-systems.md);
- any security-sensitive asset/entry point → read
  [security-testing.md](references/security-testing.md);
- any latency/load/capacity/scalability claim → read
  [performance-testing.md](references/performance-testing.md);
- any dependency/failover/recovery objective → read
  [resilience-testing.md](references/resilience-testing.md);
- any human-facing task, accessibility target, or stakeholder acceptance → read
  [usability-accessibility-and-uat.md](references/usability-accessibility-and-uat.md);
- any implemented change/code review → read
  [code-quality-and-maintainability.md](references/code-quality-and-maintainability.md);
- any running/live target or test-data mutation → read
  [environment-data-and-live-testing.md](references/environment-data-and-live-testing.md).

These references govern requirement completeness and planning even when the route is Shift
Left/plan-only and no runtime execution will occur.

## 3. Establish a testable goal and oracle

State:

`For <user/actor>, <scope> must achieve <observable outcome> under <material conditions>,
without <forbidden effects>.`

Establish current and desired behavior, source precedence, measurable acceptance criteria,
non-goals, permissions, failure behavior, compatibility, privacy, security, performance,
rollout, rollback, time/tolerance rules, and external effects where applicable.

If “better,” “easier,” “correct,” “fast,” “secure,” or “synchronized” has no measurable
oracle, stop and ask one focused product question. Do not use current implementation as the
oracle when product intent is unclear.

For `Pre-development`, perform Shift Left analysis. Produce criteria, risks, RTM, and plan.
Set runtime rows to `Result: Not run` and `Reason: implementation absent`; do not call them
failed.

Read [requirements-rtm-and-risk.md](references/requirements-rtm-and-risk.md) completely before
designing cases or assigning risk.

## 4. Select techniques and levels before building the RTM

For every atomic criterion:

1. identify failure modes and risk;
2. choose the technique that models the criterion shape;
3. choose the lowest layer that can observe the required outcome and forbidden effects;
4. add a higher layer only for integration, deployment, or user-journey confidence missing
   below;
5. define oracle, owned data, cleanup, and minimum evidence;
6. state the escalation and stopping condition.

Read [test-design-techniques.md](references/test-design-techniques.md) and
[automated-test-levels.md](references/automated-test-levels.md) now, not only during
execution.

## 5. Build and maintain the RTM

Assign separate stable IDs to requirements, atomic acceptance criteria, risks, and cases.
Map each criterion to user value, risk, technique, level, environment, cases, result,
evidence, and defects.

Keep three dimensions separate:

- applicability: `Applicable` or `Not applicable`;
- selection: `Selected`, `Deferred`, or `Skipped`;
- execution result: `Passed`, `Failed`, `Blocked`, `Not run`, or `Not applicable`.

Never create composite statuses. Record a separate reason, blocker, or waiver. A test is
`Passed` only when its current evidence satisfies its oracle; the requirement result is
derived from all linked material tests.

Mark case/coverage items `Required` or `Supporting` and use the exact aggregation precedence
in the requirements reference. Keep flaky/test/environment causes as classifications; when
they prevent a defensible result, use `Blocked` plus the classification.

For every considered test type, record:

`Type → requirement/risk → applicability/selection → reason → technique/layer →
environment → cost → approval → expected evidence`

Preserve authoritative external systems such as TestRail: create a local traceability index
with external IDs and evidence links instead of duplicating hundreds of cases.

## 6. Plan and obtain proportional approval

Read [test-planning.md](references/test-planning.md). Present:

- user goal, classification, scope, non-goals, assumptions, and unresolved conflicts;
- risk register and requirement-to-test selection;
- selected, deferred, skipped, and blocked work with reasons and residual risk;
- environment, exact versions, dependencies, data, external effects, cleanup, and rollback;
- entry, exit, stop, completion, and verdict criteria;
- ordered execution and evidence plan;
- realistic time/resources/cost only to the detail material for the decision;
- exact files to create or modify.

Read-only discovery and existing safe local tests need no artificial approval pause. Obtain
explicit approval before creating or changing artifacts, running live/E2E mutations, using
external accounts/services, exceeding ordinary local resource use, active security work,
load/fault injection, production actions, or costly subagent/persona simulations. Reapprove
when scope, target, effects, or cost materially changes.

## 7. Create test artifacts

Do this only when the user/project requests persistent artifacts. Prefer project conventions.
Otherwise initialize:

```text
docs/tests/<date>-<scope>/
├── test-charter.md
├── risk-register.md
├── rtm.md
├── test-plan.md
├── test-cases.md
├── defect-log.md
├── evidence-index.md
└── test-summary.md
```

From the installed skill directory, run
`python3 scripts/init-test-session.py --root <project-root> --scope "<scope>"`. It creates the
session atomically and refuses to overwrite an existing one. Templates live in
`assets/templates/`.

Place automated tests in the established `tests/` tree. Put project-specific E2E, security,
or load scripts in the approved `scripts/` or test-tooling directory. Never track credentials,
personal data, unsafe payloads, or sensitive raw logs.

## 8. Qualify environment and data

Use an isolated environment whose fidelity is sufficient for each claim. Prefer staging or a
dedicated test server for live testing. Use local execution when complete isolation, Computer
Use, or controlled data requires it.

Before mutations, state target, versions, credentials, data ownership, external calls,
monitoring, limits, cleanup, and rollback. Use sanitized production-like data. Make tests
order-independent and give parallel workers isolated namespaces.

Read [environment-data-and-live-testing.md](references/environment-data-and-live-testing.md).
Run target-environment health checks and smoke before any suite that depends on that target.
Static and hermetic unit work may run earlier. If a smoke case fails, record that case as
`Failed`, mark only dependent work `Blocked`, report immediately, and stop dependent suites.

## 9. Execute narrow to broad

Establish the existing baseline before attributing a new failure. Execute applicable work:

`Static/review → Unit/component → Integration/contract/API → Environment smoke → Feature/flow
sanity → Targeted regression → Full regression → E2E/live → Non-functional → UAT support`

Sanity of the requested feature or business flow is the core goal. Cover positive, negative,
boundary, invalid-action, permission, state, failure, and recovery behavior where material.
Do not duplicate the same assertion at every layer.

Use:

- [automated-test-levels.md](references/automated-test-levels.md) for suite construction,
  automation architecture, CI, flakiness, and evidence;
- [code-quality-and-maintainability.md](references/code-quality-and-maintainability.md) for
  project-specific correctness, architecture, spaghetti-code hotspots, scalability risks,
  and testability review;
- [environment-data-and-live-testing.md](references/environment-data-and-live-testing.md) for
  environment qualification, live runs, and full-ride personas;
- [security-testing.md](references/security-testing.md) for threat/control-derived security
  review and approved safe verification;
- [performance-testing.md](references/performance-testing.md) for workload, load/stress/soak,
  capacity, and scalability;
- [resilience-testing.md](references/resilience-testing.md) for approved steady-state fault
  and recovery experiments;
- [usability-accessibility-and-uat.md](references/usability-accessibility-and-uat.md) for
  human-facing quality.

## 10. Enforce the Contract & Synchronization Gate

Apply whenever scope crosses a process, service, repository, provider, event, shared schema,
generated client, webhook, callback, or independently deployed version.

Read [contracts-and-distributed-systems.md](references/contracts-and-distributed-systems.md)
before selecting compatibility cases or executing either side.

Map:

`feature/flow → consumer/caller → provider/producer → contract/schema → persisted state →
downstream consumers → deployed versions → user-visible final state`

Verify both sides, syntax and semantics, required old/new combinations, rollout order, errors,
authorization, idempotency, retry/unknown outcomes, partial failure, convergence, recovery,
and final-state reconciliation.

If a side is unavailable, ask for its local path, repository/contract URL, environment, exact
deployed version, and permission for safe verification. Mark affected rows `Blocked`; never
infer compatibility from one side alone.

## 11. Report findings immediately

Read [defects-metrics-and-closure.md](references/defects-metrics-and-closure.md) before
classifying or reporting the first finding.

| Severity/class | Meaning | Execution action |
|---|---|---|
| `Critical` | Data loss/corruption, exploitable security, major outage, irreversible effect | Report; stop all affected work |
| `High` | Core goal/flow fails, serious contract break, no reasonable workaround | Report; stop all affected work |
| `Medium` | Material partial failure; independent evidence remains valid | Report; log; continue independent work |
| `Low` | Minor functional, visual, or usability impact | Report/log; continue |
| `Blocked` | Missing access, environment, data, dependency, decision, or authority | Report affected scope |

Include defect ID, title, severity, criterion/cases, environment/build/versions, preconditions,
minimal reproduction, expected/actual, reproducibility, sanitized evidence, user/technical
impact, and execution state. Distinguish severity from delivery priority.

Never alter the product in this workflow.

## 12. Reconcile and close

Reconcile every criterion, risk, test, result, defect, waiver, and evidence item with the RTM.
Leave no applicable item unexplained. Report:

1. goal, scope, profile, environment, commit/build, and component versions;
2. requirement/risk coverage using declared denominators;
3. every considered test type and its selection/result/evidence;
4. every technique used, why, and what it found;
5. pass/fail/block/not-run, defect, flake, compatibility, and applicable quality metrics;
6. unverified requirements, invalid evidence, limitations, and residual risks;
7. each entry/exit criterion and accountable risk acceptance;
8. exactly one verdict: `Ready`, `Ready with concerns`, `Not ready`, or `Inconclusive`.

Use the precedence and closure rules in
[defects-metrics-and-closure.md](references/defects-metrics-and-closure.md). A pass percentage
never overrides a failed or blocked critical criterion. Archive sanitized scripts, datasets,
evidence manifests, and reports according to project retention rules.
