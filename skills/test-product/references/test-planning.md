# Test Planning

Use after the test basis, atomic criteria, risks, and technique/layer candidates exist.
Planning turns them into a bounded, approved execution contract.

## Contents

1. Route the invocation
2. Choose Focused or Full ride
3. Consider the test-type catalog
4. Build a risk-based plan
5. Baseline and regression selection
6. Entry, stop, exit, and completion criteria
7. Estimate and schedule
8. Approval matrix
9. Plan quality gate

## 1. Route the invocation

| Intent route | Use when | Required output | Runtime execution |
|---|---|---|---|
| Shift Left / plan-only | implementation absent or user requests design | test basis, criteria, risks, RTM, plan | mark applicable runtime cases `Not run` |
| Read-only assessment | user requests review/status, no execution | findings, evidence limits, risk/coverage gaps, assessment verdict | only non-mutating checks |
| Focused execution | feature/fix/flow needs fast confidence | compact RTM/plan, evidence, defect log, summary | selected sanity + risk regression |
| Full execution | release/product/high risk | complete applicable matrix and artifacts | layered, broad, non-functional as justified |

Select target mode separately:

| Target mode | Planning addition |
|---|---|
| Local/hermetic | versioned local runtime, owned data, deterministic cleanup |
| Isolated live/staging | target preflight, accounts, effects, monitoring, cleanup |
| Deployed/production-like | exact action approval, ceilings, operator, abort, rollback, retention |

The same requirements, defect, and evidence rules apply to every route. A low-risk Focused run
may keep its compact RTM and summary in chat if the user did not request files and the project
has no artifact requirement. Do not create six documents merely to satisfy formality.

Lifecycle classification uses the most advanced state: use `Deployed` if the target is a
running deployment, otherwise `Implemented` if code exists, otherwise `Pre-development`.

## 2. Choose Focused or Full ride

### Decision table

| Condition | Focused default | Full ride default |
|---|---|---|
| Scope | narrow feature/fix/flow | release, whole product, broad shared change |
| Risk | Low/Medium with strong existing evidence | High/Critical or many correlated Medium risks |
| Architecture | local boundary or mature integration | multiple deployables/providers/version drift |
| Change | isolated, reversible | migration, auth/payment/data model, large blast radius |
| Existing evidence | reliable targeted coverage | weak/unknown/flaky coverage |
| User need | fastest defensible answer | maximum applicable confidence |

Focused includes requirement review, compact RTM, baseline, sanity, systematic positive and
negative cases, the lowest adequate layer, and targeted regression. It may include one E2E or
contract test if that is the cheapest adequate proof.

Full ride adds every risk-applicable layer: broader regression, exact version matrices,
approved E2E/live exploration, security, performance/resilience, accessibility, and optional
isolated persona simulation. It does not include irrelevant techniques.

If time or token budget is constrained, protect Critical/High criteria first and show the
deferred risk. Never lower a safety or authorization gate to meet a deadline.

## 3. Consider the test-type catalog

Consider every row, then select, defer, skip, block, or mark not applicable with a factual
reason. Do not run the catalog mechanically.

| Family | Types to consider |
|---|---|
| Test basis/static | requirements/Shift Left, architecture/code/config review, lint/type/schema, maintainability |
| Functional levels | unit, component, integration, contract, API/service, system/E2E |
| Change confidence | environment smoke, feature/flow sanity, targeted regression, full regression, original-defect retest |
| Data/state | migration/backward data, transaction/concurrency, idempotency, recovery/reconciliation |
| Compatibility | browser/device/OS, API/event/schema, provider/client, old/new deployable versions |
| Human-facing | exploratory, visual, usability, accessibility, localization, UAT |
| Security/privacy | threat/control review, SAST/SCA/secrets/IaC, dynamic/manual abuse |
| Performance | baseline, load, stress, spike, soak, volume, scalability/capacity |
| Resilience/operations | dependency failure, failover, restart, observability, backup/restore where required |
| Live/full ride | approved route/role matrix, production-like observation, optional isolated personas |

“All test types considered” means every relevant family appears in the plan/report with its
decision and residual risk. It does not mean all are executed.

## 4. Build a risk-based plan

For every considered test type record:

```text
Test/type ID
Linked criteria and risks
Applicability and selection
Technique/model and coverage target
Lowest adequate level; escalation condition
Environment/build/version
Data namespace, external effects, cleanup
Execution order/dependencies
Cost/time/resources
Approval state
Pass/fail evidence
Skip/defer/block reason and residual risk
```

### Order by feedback and dependency

1. test-basis and static review;
2. hermetic unit/component;
3. integration/contract/API;
4. target-environment qualification and smoke;
5. feature/flow sanity;
6. targeted then full regression;
7. E2E/live and exploratory;
8. approved security/performance/resilience;
9. stakeholder UAT support.

Static/unit work may precede environment smoke. Anything relying on the target waits for
target smoke. Parallelize only independent cases with isolated resources and independent stop
conditions.

### Test quadrants as a completeness check

Do not force equal coverage, but ask whether the plan addresses:

- technology-facing support: unit/component/static;
- business-facing support: examples/API/component;
- business-facing critique: E2E/exploratory/usability/UAT;
- technology-facing critique: security/performance/resilience.

Absence is acceptable only with a factual applicability/risk reason.

## 5. Baseline and regression selection

### Choose a baseline

Use the nearest valid comparator:

1. same test on the identified pre-change commit/build in the same environment;
2. last green mainline build with equivalent configuration;
3. previous supported release;
4. documented current production metric/behavior;
5. no baseline—state attribution is limited.

Never compare different data, configuration, load, or environment without identifying the
confounder.

### Build the impact graph

Trace:

`diff/config/migration → changed symbols/components → callers → shared rules/state →
contracts/providers → user flows → prior defects/incidents → deployment/rollback`

Select regression for:

- directly changed behavior;
- callers and consumers;
- shared validation/authorization/calculation;
- persistence/migration and backward data;
- integration and version combinations;
- prior defects in the touched risk cluster;
- critical neighboring flows whose invariants share the changed state.

Record excluded surface and why. A full existing suite may be cheaper and more reliable than
manual selection; run it when cost is acceptable, but do not let it replace impact analysis.

### Known failures and quarantine

Establish the existing failure set before the change. For each known failure, require issue
link, owner, first/last seen build, affected criteria, quarantine reason, and expiry/review
date. A new failure cannot be dismissed because the suite “is flaky.” Baseline reproduction
changes attribution, not user impact.

## 6. Entry, stop, exit, and completion criteria

### Entry criteria

Select only applicable items and make them binary:

- accepted test basis, criteria, and RTM baseline;
- identified commit/build and all component versions;
- adequate environment and credentials;
- dependencies healthy and exact versions known;
- isolated test data and verified cleanup;
- monitoring/correlation for load/resilience/live work;
- approved external effects and limits;
- target smoke passed.

Failed entry makes dependent scope `Blocked`. Never silently substitute a lower-fidelity
environment and retain the stronger claim.

### Stop and containment protocol

When a stop condition occurs:

1. prevent further affected actions and cancel dependent work;
2. allow already-running independent work only if it cannot worsen risk or corrupt evidence;
3. make the target safe; run failure-safe cleanup or rollback;
4. preserve logs, trace IDs, versions, timestamps, inputs, and current state;
5. classify the failing case and dependent rows;
6. update RTM/defect/evidence records;
7. report immediately and yield when user/owner action is required.

Stop the whole campaign for credible data corruption/loss, uncontrolled external effects,
environment contamination, safety/security incident, or evidence invalidation across the
campaign. Otherwise stop only the affected branch/suite/target.

Resume by cause:

| Stop/block cause | Permitted resume |
|---|---|
| Confirmed product defect | only after a separate remediation task produces a new identified build; run original reproducer, then targeted regression |
| Environment contamination/failure | same product build is allowed on a cleaned/requalified or new environment after entry gates pass |
| Missing access/data/dependency/decision | same identified build is allowed after the prerequisite exists and affected entry gates pass |
| Approval/scope/limit change | after the changed plan receives the required authority |
| Test-artifact defect | same product build is allowed after an authorized test-only correction and baseline check |

Never treat resume authority as permission to repair product code inside this workflow.

### Exit criteria

Define per session, for example:

- every Critical/High criterion has current defensible evidence;
- zero open Critical/High product defects;
- required sanity journeys and supported contract combinations pass;
- no unexplained/expired quarantines affecting the goal;
- named security/performance/accessibility thresholds pass;
- all applicable selected cases are terminal;
- blocked/not-run scope and residual risk are within an explicitly accepted allowance;
- cleanup and final-state reconciliation pass.

Do not use pass percentage alone.

### Definition of testing complete

Testing work is complete only when:

- every applicable criterion and selected case has a controlled final status;
- every pass has current evidence;
- failures/blockers/flakes are classified and linked;
- every considered test type has selection and reason;
- exit criteria are individually evaluated;
- metrics include denominators and criticality;
- residual risks have owner, rationale, scope, and acceptance state;
- artifacts and evidence are sanitized and archived;
- a QA evidence verdict is issued for the named object.

## 7. Estimate and schedule

Estimate from discovered commands, suite history, environment provisioning, and data needs.
Include setup, execution, investigation, retries required to diagnose—not hide—flakiness,
cleanup, evidence, and reporting.

When uncertainty is material, use three-point PERT:

`Expected = (optimistic + 4 × most likely + pessimistic) / 6`

Also state the range and largest uncertainty. Split work into setup, fast feedback, broad
execution, and closure; this makes a partial result interpretable.

Offer Focused vs Full ride cost only when the choice is material. Token/subagent estimates are
needed only when expensive simulations or delegation affect approval. Avoid false precision.

## 8. Approval matrix

| Action | Default authority |
|---|---|
| Read repository/docs, inspect config, run non-mutating diagnostics | proceed |
| Run existing safe local hermetic tests | proceed unless project instructions say otherwise |
| Create/modify test artifacts or tests | obtain user approval if not already requested |
| Mutate isolated local test data with verified cleanup | plan and disclose; follow project policy |
| Staging E2E/live mutation or external sandbox call | explicit target/effects/cleanup approval |
| Production observation | explicit bounded approval |
| Production mutation, active security, load, fault injection | action-specific approval, limits, monitoring, abort/rollback |
| Subagent persona/full-ride simulation | explicit cost and target approval |

Previously given explicit authority counts. Ask only for the missing material permission.
Silence never authorizes an external effect.

## 9. Plan quality gate

Before execution verify:

- every selected test traces to criterion/risk and declares technique, layer, oracle, evidence;
- entry/exit/stop/resume criteria are binary and risk-based;
- baseline and impact graph are recorded;
- target, versions, data, effects, cleanup, and approval are explicit;
- execution order respects environment smoke and dependencies;
- skipped/deferred/blocked work exposes residual risk;
- estimate includes uncertainty without unnecessary ceremony;
- exact artifact paths are named.

Research basis: ISTQB CTAL Test Management 3.0 for context-driven strategy,
risk treatment, estimates, entry/exit, monitoring/control, and completion. The Agile Testing
Quadrants are used only as a completeness lens, not a mandated coverage ratio:
<https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTAL-TM_Syllabus_v3.0_zKjKsaN.pdf>.
