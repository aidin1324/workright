# Requirements, Oracles, Risk, and RTM

Use this reference before test planning in every session. Its output is a test basis,
atomic acceptance criteria, calibrated risks, selected modeling direction, and an RTM that
can later derive a defensible verdict.

## Contents

1. Establish the test basis
2. Convert intent into atomic criteria and oracles
3. Apply Shift Left
4. Score and route risk
5. Build and maintain the RTM
6. Worked example
7. Completion gate

## 1. Establish the test basis

### Inventory sources

Record source ID, location, owner, version/date, scope, and authority for:

- user request and product decision;
- approved ticket, specification, user story, or contract;
- business rules, policy, legal or regulatory requirement;
- API/event/schema and architecture documents;
- design and content specification;
- tests and prior defect reports;
- current production behavior and current implementation.

Treat tests and implementation as evidence of current behavior, not automatic proof of
intended behavior.

### Resolve source conflicts

Use project-defined governance first. If none exists, propose this precedence and ask the
decision owner to confirm any material conflict:

1. current explicit product or regulatory decision;
2. approved versioned contract/specification;
3. accepted story and acceptance criteria;
4. design/content specification within its domain;
5. documented existing behavior;
6. tests;
7. implementation.

Do not silently choose a source when the choice changes user-visible behavior, permissions,
money, data, compatibility, or a pass/fail result. Record the conflict, affected criteria,
options, recommended interpretation, owner, and decision. Block only affected scope.

### Baseline the test basis

Give the accepted set a baseline ID or timestamp. For every later change, record:

`source changed → criteria affected → risk changed → cases/RTM affected → regression added
or retired → decision owner`

Never overwrite history in a way that makes earlier evidence appear to prove a changed
requirement.

## 2. Convert intent into atomic criteria and oracles

### Start from the user's outcome

Write:

`For <actor>, <capability> must produce <observable outcome> under <conditions>, within
<tolerance/deadline>, without <forbidden effect>.`

Identify actors, roles, data ownership, initial state, trigger, result, side effects, forbidden
effects, failure handling, time, and system boundaries.

### Use criteria shapes deliberately

| Requirement shape | Criterion form | Typical model |
|---|---|---|
| Scenario | Given/When/Then plus forbidden effects | Use case + lower-level rules |
| Business rule | Conditions and resulting actions | Decision table |
| Range/limit | Domain, inclusivity, units, errors | Equivalence + boundaries |
| Lifecycle | State, event, guard, next state | State-transition model |
| Cross-system flow | Per-system invariant and convergence deadline | Contract + state reconciliation |
| Performance | Metric, percentile, workload, window, threshold | Performance run model |
| Security | Asset, actor, action, control, denial/audit outcome | Threat/abuse case |
| Human task | User group, task, context, completion/error target | Usability/UAT protocol |

Split compound wording. One atomic criterion should have one primary pass/fail proposition.
Different roles, modes, failure outcomes, or thresholds usually deserve separate criterion IDs.

### Define a complete oracle

For each criterion record:

- **source:** authoritative rule and version;
- **trigger:** exact action/event/input;
- **observable output:** value, state, response, message, or rendered behavior;
- **required side effects:** durable writes, events, notifications, logs, or downstream state;
- **forbidden effects:** data leakage, duplicate charge, partial write, unauthorized mutation;
- **deadline/tolerance:** exact value or justified interval, percentile, timezone, rounding rule;
- **observation point:** UI, API, database read model, event, metrics, or external sandbox;
- **eventual rule:** polling condition and maximum convergence time, never an arbitrary sleep.

Oracle precedence is the accepted test basis. When exact output is unavailable, use one of:

- **metamorphic oracle:** a defined input change must preserve or change a property;
- **differential oracle:** compare with an approved independent implementation/reference;
- **invariant oracle:** conservation, idempotency, monotonicity, uniqueness, or authorization;
- **review oracle:** named human owner approves a visual/content/UAT outcome.

State the limitation; a fallback oracle must not be presented as stronger proof than it is.

### Replace vague wording

| Vague term | Required clarification |
|---|---|
| easy | named users, task, context, completion/error/assistance target |
| fast | workload, environment, percentile, threshold, observation window |
| secure | asset/threat/control and expected denial, no-side-effect, audit behavior |
| synchronized | systems, canonical state, allowed interim state, convergence deadline |
| compatible | consumer/provider versions, direction, contract and semantic invariants |
| correct | explicit examples, rules, invariants, tolerances, and forbidden outcomes |

If material clarification is unavailable, set affected criteria `Blocked` or `Not run` and
report why. Do not invent a product decision to keep testing.

## 3. Apply Shift Left

Review each criterion before implementation for:

- actor/role/tenant and permission completeness;
- happy, alternate, negative, boundary, and forbidden paths;
- state, retry, timeout, cancellation, duplicate, ordering, and partial success;
- data ownership, retention, privacy, migration, and cleanup;
- observability: how success, failure, and final state will be proven;
- external contracts, supported versions, rollout and rollback;
- security abuse, rate/resource limits, accessibility, usability, and operability;
- testability: controllable inputs, observable outputs, deterministic hooks, safe environment.

Classify every observation as:

- `Ambiguity`: more than one plausible expected behavior;
- `Conflict`: sources prescribe incompatible behavior;
- `Untestable`: outcome cannot be controlled or observed;
- `Missing requirement`: material behavior is unspecified;
- `Product risk`: requirement is clear but failure matters.

Provide a concise proposed resolution and owner. For pre-development runtime work use
`Result: Not run`, `Reason: implementation absent`; keep design-review evidence separate.

## 4. Score and route risk

Use the project's approved model when available. Otherwise use inherent product risk:

`Exposure = Likelihood × Impact`, each from 1 to 5.

### Likelihood anchors

| Score | Anchor |
|---:|---|
| 1 | exceptional conditions; mature unchanged control; no relevant history |
| 2 | uncommon but credible; narrow exposure |
| 3 | plausible in ordinary edge/failure conditions |
| 4 | likely under normal variation, load, rollout, or known defect cluster |
| 5 | expected/frequent, already observed, or directly exercised by most users |

### Impact anchors

| Score | Anchor |
|---:|---|
| 1 | negligible inconvenience; no durable effect |
| 2 | minor degradation with easy workaround |
| 3 | material feature failure, limited users/data, recoverable |
| 4 | core-flow loss, serious financial/data/contract impact, difficult recovery |
| 5 | safety, major outage, unauthorized sensitive access, irreversible loss/corruption |

### Exposure bands and overrides

| Score | Band |
|---:|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

Raise to at least `High` for authorization/tenant isolation, payment correctness,
irreversible actions, sensitive-data boundaries, destructive migration, or a supported
contract rollout when failure reaches real users. Raise to `Critical` when the credible
impact is catastrophic even if occurrence is rare. Document every override.

Track:

- inherent risk before controls/testing;
- evidence and controls that reduce uncertainty;
- residual risk after testing;
- risk owner and acceptance owner.

Testing may reduce uncertainty; it does not automatically reduce the underlying impact.

Define the numeric weight used in metrics:

`Effective risk weight = max(Likelihood × Impact, floor of final band)`

Band floors are Low `1`, Medium `5`, High `10`, and Critical `17`. This makes a band override
change the weight instead of leaving a Critical override numerically below Medium. Record
base exposure, final band, override, and effective weight separately.

### Route risk to depth

| Risk | Default profile and minimum response |
|---|---|
| Low | Focused; one primary technique/layer, sanity, direct regression around change |
| Medium | Focused; positive/negative/boundary or state/rule coverage, targeted regression |
| High | Full ride recommended; multiple complementary techniques, integration/E2E where needed, explicit failure/recovery and exit gate |
| Critical | Full ride; independent evidence for critical invariant, broad relevant regression, required non-functional/contract gate, zero unknown critical rows |

Profile is adjusted by scope and evidence. A whole-product release with many Medium risks may
still require Full ride. A Full ride does not make an irrelevant test type applicable.

## 5. Build and maintain the RTM

Use separate IDs:

- `REQ-*`: source requirement;
- `AC-*`: atomic acceptance criterion;
- `RISK-*`: product risk;
- `TC-*`: test case;
- `DEF-*`: defect.

Recommended columns:

| AC ID | REQ ID | Source/baseline | Atomic criterion/oracle | User value | Risk ID/band/weight | Applicability | Selection | Technique | Level | Case/coverage IDs and role | Environment/build | Result | Reason/blocker | Evidence IDs | Defect IDs | Owner/waiver |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Rules:

1. Every applicable AC has one or more cases or an explicit `Deferred/Skipped` decision and
   residual risk.
2. Every case traces to at least one AC or named risk.
3. Mark each case/coverage item `Required` or `Supporting`. Required items are necessary to
   establish the AC in approved scope. Supporting items add confidence but are not required
   for a pass. A valid failure from either role that directly disproves the AC is dispositive.
4. `Not applicable` is both applicability and final result only when justified.
5. `Blocked` means execution could not produce a valid result; name the owner and unblock need.
6. `Not run` means applicable/selected but not executed; state why.
7. Derive the AC result in this exact order:
   - any valid linked result that directly disproves the AC → `Failed`;
   - otherwise any Required item `Blocked` → `Blocked`;
   - otherwise any Required item `Not run`, Deferred, or Skipped → `Not run`;
   - otherwise every Required item is `Passed` with valid evidence → `Passed`;
   - no Required item for an applicable AC → `Not run`;
   - `Not applicable` only when the AC itself is not applicable.
8. Shared cases may support multiple criteria, but evidence must show each oracle.
9. Record build/version/timestamp in evidence so stale results cannot prove a new build.
10. Reconcile orphan requirements, orphan tests, blank results, and evidence-less passes.

`Flaky`, test defect, and environment failure are classifications, not result values. An
unresolved flaky result uses `Result: Blocked`, `Reason/classification: Flaky`.

Independent evidence for a Critical invariant means at least two proofs whose likely failure
is not fully correlated. They must differ in a material dimension such as technique, test
level/boundary, observation source, or independently implemented oracle, and must not depend
on the same mock/test double for the invariant. Different agents running the same assertion
are not independent evidence.

Coverage formulas:

- requirement coverage =
  `applicable ACs with defensible terminal evidence / all applicable ACs`;
- risk coverage =
  `effective risk weight of ACs with valid Passed or Failed evidence / effective risk weight
  of all applicable ACs`;
- execution completion =
  `selected applicable cases with Passed or Failed result / all selected applicable cases`;
  Blocked and Not run remain outside the numerator.

Report numerator, denominator, exclusions, and criticality segments. Deferred, skipped,
blocked, not-run, and waived applicable ACs remain in the denominator; a waiver does not
create evidence. Never aggregate away a Critical/High gap.

## 6. Worked example

Request: “Make invoice export correct and fast.”

1. Discover policy says selected date range is inclusive in account timezone; SLO says p95
   below 3 s for 10,000 rows at 5 concurrent exports.
2. Create:
   - `AC-001`: records whose local date is within `[from,to]` appear exactly once;
   - `AC-002`: records outside the range never appear;
   - `AC-003`: p95 completion <3 s under the named workload/environment;
   - `AC-004`: one tenant cannot export another tenant's records.
3. Oracles include CSV record set, duplicate-free invariant, no cross-tenant IDs, workload,
   percentile, and observation window.
4. Risk:
   - AC-001/2 impact 3 × likelihood 3 = Medium;
   - AC-003 impact 2 × likelihood 3 = Medium;
   - AC-004 impact 5 × likelihood 2 = 10, overridden/retained High for tenant isolation.
5. Techniques:
   - date partitions + boundaries around midnight/timezone;
   - property check for exact set/no duplicates;
   - performance workload model;
   - actor × tenant authorization decision table.
6. RTM maps lower-level date/authorization cases, API integration, one E2E export journey, and
   performance evidence. High security failure closes readiness regardless of aggregate pass.

## 7. Completion gate

Do not proceed to planning until:

- the test basis and baseline are named;
- all material ambiguities/conflicts are resolved or explicitly blocked;
- criteria are atomic and have complete oracles;
- risks have anchored likelihood, impact, band, overrides, and owners;
- technique/layer directions exist;
- RTM has no unexplained applicable criterion.

Research basis: ISTQB CTFL 4.0.1 and CTAL Test Management 3.0 for test basis,
traceability, risk-based testing, monitoring, and completion. The procedures above are local
operational rules; the sources are supporting standards, not required reading:
<https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf> and
<https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTAL-TM_Syllabus_v3.0_zKjKsaN.pdf>.
