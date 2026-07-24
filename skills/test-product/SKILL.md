---
name: test-product
description: Use when a feature, business flow, release, integration, or whole software product needs requirements-based test planning, quality assessment, or testing before development or after implementation or deployment.
---

# Test Product

Test the user's actual outcome with risk-based, traceable evidence. Move quickly by choosing
the cheapest test that proves each requirement; spend more only where risk justifies it.

## Non-negotiable boundaries

- Never fix defects. Never modify production code, weaken assertions, or add test-only
  workarounds that hide product behavior.
- Create or modify only user-approved test artifacts: established test directories,
  sanitized fixtures, test-only configuration/IaC, test scripts, and QA documentation.
- Inspect the repository and connected systems instead of guessing commands, architecture,
  contracts, versions, or sources of truth.
- Stop before test design when the user goal or expected behavior is materially ambiguous.
- Stop on Critical/High defects, data risk, or a conflict that changes expected behavior.
- Report Medium/Low defects immediately, record them, then continue independent tests.
- Never perform a repair automatically or treat a defect report as permission to fix.
- Never run destructive security, load, or live production actions without explicit,
  action-specific approval.
- Never claim `Passed`, compatibility, coverage, or readiness without current evidence.

## Required workflow

Follow this order. Do not skip a gate because the request sounds urgent:

`Intent → Discover → Classify → Requirements → Ambiguity gate → Acceptance criteria → Risk
→ RTM → Profile → Test plan → Approve → Artifacts → Environment → Smoke → Execute → Defects
→ Reconcile → Close`

Keep communication brief. Explain the technique used and why in one factual sentence.

## 1. Discover before asking

Read applicable instructions and documentation. Inspect repository status and diffs, manifests,
lockfiles, architecture, test layout, CI/CD, deployment configuration, prior reports, and real
run commands. Trace the requested behavior through input, validation, authorization, domain
logic, persistence, integrations, side effects, and user-visible output.

Locate connected repositories, services, providers, schemas, events, generated clients, and
deployed versions. Search the repository before asking questions that code or documentation
can answer.

Do not alter unrelated user changes.

## 2. Classify the request

Classify four independent dimensions:

| Dimension | Values |
|---|---|
| Lifecycle | `Pre-development`, `Implemented`, `Deployed` |
| Scope | `Feature`, `Business flow`, `Change or release`, `Whole product` |
| Risk | `Low`, `Medium`, `High or critical` |
| Profile | `Focused`, `Full ride` |

Tell the user the provisional classification and concrete reasons. Reclassify when discovery
shows broader impact.

Recommend `Focused` by default: fast, requirements-complete sanity testing with targeted
lower-level and regression coverage. Recommend `Full ride` for critical flows, releases,
large changes, weak coverage, or explicit requests. Full ride means every *applicable* layer,
not every known test. Obtain explicit approval before costly live or subagent simulations.

## 3. Establish testable intent

State in one sentence:

`For <user>, <scope> must achieve <observable outcome> under <material conditions>.`

Establish current behavior, desired behavior, measurable acceptance criteria, non-goals,
sources of truth, permissions, side effects, edge cases, failures, compatibility, privacy,
security, performance, rollout, and rollback constraints as applicable.

If “better,” “easier,” “correct,” “fast,” or similar wording lacks a measurable oracle, stop
and ask a focused product question. Do not begin “safe tests” against an unknown expectation.

For `Pre-development`, perform Shift Left analysis and finish with acceptance criteria, risks,
RTM, and test plan. Mark runtime rows `Not run — implementation absent`; do not report them as
failures.

Read [requirements-rtm-and-risk.md](references/requirements-rtm-and-risk.md) for requirement,
acceptance, risk, and RTM rules.

## 4. Build the Requirement Traceability Matrix

Assign a stable ID to every testable acceptance criterion. Map each requirement to user value,
risk, level, technique, test case IDs, environment, result, evidence, and defect IDs.

Use only `Passed`, `Failed`, `Blocked`, `Not run`, and `Not applicable`. Never leave a final
result blank. Preserve an authoritative external system such as TestRail or Jira: create a
local index with external IDs and evidence links rather than duplicating it.

For every considered test type, record:

`Type → requirement/risk → applicable/skipped/blocked reason → technique → environment →
cost → approval → expected evidence`

Do not run a catalog item merely because it exists. Do not skip an applicable item silently.

## 5. Plan and obtain approval

Select the lowest, fastest layer that can prove each requirement. Move upward only when a lower
layer cannot provide the needed confidence. Avoid identical assertions at every layer.

Present:

- scope, non-goals, risk, profile, and user outcome;
- requirements and unresolved conflicts;
- selected, skipped, and blocked tests with reasons;
- environment, versions, dependencies, data, external effects, and cleanup;
- entry and exit criteria;
- ordered execution and evidence plan;
- estimated time, resources, and token cost;
- exact files to create or modify;
- approvals required.

Wait for approval of the plan, live/E2E target, external effects, and test-artifact changes.
Read [test-planning.md](references/test-planning.md).

## 6. Create test artifacts

Prefer existing project conventions. Otherwise initialize:

```text
docs/tests/<date>-<scope>/
├── test-charter.md
├── rtm.md
├── test-plan.md
├── test-cases.md
├── defect-log.md
└── test-summary.md
```

Run `scripts/init-test-session.py --root <project-root> --scope "<scope>"`. It refuses to
overwrite an existing session. Templates live under `assets/templates/`.

Place automated tests in the established test tree and project-specific E2E/load/security
scripts in the project's approved `scripts/` or test tooling directory. Never put credentials,
personal data, or sensitive raw logs in tracked artifacts.

## 7. Prepare environment and data

Use an isolated, production-representative environment adequate for the claims. Prefer staging
or a dedicated test server for live testing. Use local execution when complete isolation,
Computer Use, or controlled data requires it.

Before execution, state target, versions, credentials required, test data, mutations, external
calls, monitoring, cleanup, and rollback. Use sanitized production-like data. Keep each test
independent, order-independent, repeatable, and responsible for its own cleanup.

Run environment health checks and smoke tests first. If smoke fails, report the blocker and do
not run dependent suites. Read
[environment-data-and-live-testing.md](references/environment-data-and-live-testing.md).

## 8. Execute from narrow to broad

Establish the existing baseline before attributing failures. Execute applicable layers in this
order:

`Static → Unit/component → Integration/contract/API → Smoke → Sanity → Targeted regression →
Full regression → E2E/live → Non-functional → UAT support`

Sanity of the requested feature or flow is the core purpose. Cover positive, negative,
boundary, invalid-action, permission, and failure paths for every material requirement.

Use the project framework and official current documentation. Prefer real implementations or
high-fidelity fakes over mocks when they do not increase test size or external risk.

Read:

- [test-design-techniques.md](references/test-design-techniques.md) to choose test cases;
- [automated-test-levels.md](references/automated-test-levels.md) for unit through E2E,
  smoke, sanity, regression, CI, and automation quality;
- [security-performance-and-resilience.md](references/security-performance-and-resilience.md)
  when non-functional risk applies;
- [usability-accessibility-and-uat.md](references/usability-accessibility-and-uat.md) for
  human-facing quality.

## 9. Enforce the Contract & Synchronization Gate

Apply this gate whenever the scope crosses services, repositories, providers, events, shared
schemas, generated clients, webhooks, callbacks, or independently deployed versions.

Map:

`feature/flow → consumer/caller → provider/producer → contract/schema → persisted state →
downstream consumers → deployed versions`

Verify both sides, schema and semantic compatibility, old/new coexistence, deployment order,
errors, authorization, idempotency, retries, partial failures, and end-to-end state
synchronization.

If a dependency is unavailable, ask where its repository, contract, URL, environment, and
deployed version can be accessed and whether safe verification is approved. Mark affected RTM
rows `Blocked`. Never infer compatibility from one side alone.

Read [contracts-and-distributed-systems.md](references/contracts-and-distributed-systems.md).

## 10. Handle findings immediately

| Severity | Meaning | Action |
|---|---|---|
| `Critical` | Data loss/corruption, exploitable security issue, major outage, irreversible effect | Report and stop |
| `High` | Core goal/flow fails, serious contract break, no reasonable workaround | Report and stop |
| `Medium` | Material partial failure; independent tests remain valid | Report, log, continue independent tests |
| `Low` | Minor functional, cosmetic, or usability issue | Report or log, continue |
| `Blocked` | Missing access, environment, data, dependency, or authority | Report affected RTM scope |

Include ID, title, severity, requirements/tests, environment/build/versions, preconditions,
reproduction, expected vs actual, reproducibility, sanitized evidence, impact, and execution
state.

Do not ask “should I fix it?” as part of this workflow. State that repair requires a separate
task. Read [defects-metrics-and-closure.md](references/defects-metrics-and-closure.md).

## 11. Reconcile and close

Reconcile every requirement, test, result, defect, and evidence item with the RTM. Report:

1. Goal, scope, profile, environment, and exact versions.
2. Requirement/RTM coverage.
3. Every considered test type: selected/skipped/blocked reason, result, evidence.
4. Every technique used: reason, test cases, findings.
5. Passed, failed, blocked, not-run, defect, flakiness, and applicable quality metrics.
6. Unverified requirements and residual risks.
7. Entry/exit criteria result.
8. One verdict: `Ready`, `Ready with concerns`, `Not ready`, or `Inconclusive`.

Never let aggregate pass rate override a failed or blocked critical requirement. Archive useful
scripts, sanitized data, and report snapshots using the project's conventions.
