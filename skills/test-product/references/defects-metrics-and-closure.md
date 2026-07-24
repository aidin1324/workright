# Defects, Evidence, Metrics, and Closure

Read before classifying the first finding and before issuing a final verdict. This reference
defines immediate reporting, lifecycle without automatic repair, evidence validity,
mathematical metrics, residual-risk acceptance, and deterministic verdict precedence.

## Contents

1. Distinguish finding classes
2. Severity, priority, and execution action
3. Report and manage the defect lifecycle
4. Retest and flakiness
5. Evidence validity and metrics
6. Verdict decision model
7. Closure and archive

## 1. Distinguish finding classes

| Class | Meaning | Product defect? |
|---|---|---|
| Product defect | observed behavior violates accepted oracle | yes |
| Requirement ambiguity/conflict | expected behavior is not authoritative | no; blocks oracle |
| Blocker | access, environment, data, dependency, decision, or authority missing | no |
| Test defect | test/harness/oracle implementation is wrong | no |
| Environment failure | target/infrastructure invalidates result | no |
| Flaky result | same identified conditions produce inconsistent result without explanation | unresolved |
| Maintainability risk | code structure creates elevated future defect/change risk | not functional defect unless behavior fails |
| Change request/preference | desired behavior is outside accepted baseline | no |

Do not report a scanner warning, log anomaly, or suspected issue as a confirmed product defect
until a valid oracle and evidence support it. Do report a credible Critical safety/security
risk immediately while clearly labeling validation state.

## 2. Severity, priority, and execution action

Severity is user/product impact; priority is delivery urgency chosen by product/engineering.
Never lower severity to fit a schedule.

| Severity | Calibrated impact | Execution |
|---|---|---|
| Critical | catastrophic data/security/safety/financial impact, major outage, irreversible effect | report now; global or affected-target stop |
| High | core goal/critical flow fails, serious supported contract break, no reasonable workaround | report now; stop affected branch and dependents |
| Medium | material partial failure, limited scope or workable alternative | report now; continue only independent valid tests |
| Low | minor localized functional/visual/usability impact | report/log; continue |

Factors: affected users/tenants, data sensitivity/volume, reversibility, workaround,
frequency/exposure, duration, contract/compliance, detectability, and propagation. Use the
domain-specific security/accessibility rules where applicable.

`Blocked`, test defect, environment failure, and flake are execution classifications, not
severity.

Stop handling always follows:

`contain → cancel dependent work → make safe/cleanup → preserve evidence → classify/update
RTM → report → yield if owner action is required`

## 3. Report and manage the defect lifecycle

### Minimum defect report

```text
DEF-003 — High — Old consumer rejects supported payment event
Requirement/criterion/cases: REQ-012 / AC-018 / TC-CONTRACT-007
Environment/build/versions: staging; producer 2.4.0; consumer 2.2.1
Preconditions/data: exact safe state and owned identifiers
Reproduction: minimal ordered steps or command
Expected: accepted semantic outcome and forbidden effects
Actual: observed response/state/effects
Reproducibility: 5/5 under stated conditions
Evidence: sanitized evidence IDs, timestamps, correlation IDs
Impact: user/business/technical propagation
Severity rationale: impact/exposure factors
Execution: affected tests stopped; dependent RTM rows Blocked
Status/owner: New / unassigned
```

Report every confirmed defect to the user immediately. Redact credentials, personal data,
real customer IDs, exploitable secrets, and unsafe payloads.

Never modify product code, weaken a test, or insert a workaround. Say:
“Remediation requires a separate task.”

### Lifecycle

Use:

`New → Triaged → Accepted for remediation → Ready for retest → Verified → Closed`

Alternative states:

- `Duplicate`: link canonical defect and retain affected cases;
- `Known issue`: link owner/build/scope and review date;
- `Rejected`: record evidence-based reason and decision owner;
- `Deferred/Accepted risk`: require waiver;
- `Reopened`: retest fails or regression appears.

This testing workflow may create/update test-side records when authorized, but product repair
is a separate user request. Do not mark `Closed` merely because a fix was proposed.

### Waiver/accepted risk

Require:

- defect/risk and affected criteria/scope;
- impact and evidence;
- reason and compensating control/workaround;
- named accountable acceptor;
- applicable builds/releases/environments;
- expiry or review date;
- monitoring and rollback/containment;
- limitations on the QA verdict.

A tester/agent cannot accept business/release risk for the owner.

## 4. Retest and flakiness

### Retest after separate remediation

1. identify new commit/build and exact dependency versions;
2. preserve the original defect/evidence;
3. reproduce original conditions and execute the original failing case first;
4. verify expected output, required/forbidden effects, cleanup, and no hidden workaround;
5. run targeted regression from changed area, callers, boundaries, contracts, and related
   prior defects;
6. add new evidence; never overwrite historical failure;
7. mark `Verified` only when the original oracle passes on the fixed build;
8. reopen when reproduction or affected regression fails.

If the fix changes requirements, baseline the new approved requirement before retest.

### Flaky result

Retries are diagnostic and never erase the first failure.

Record:

- ordered pass/fail sequence and retry policy;
- build, environment, worker, order, seed, clocks, load, network, and resource conditions;
- shared state/isolation evidence;
- affected criteria and confidence loss;
- classification/owner/quarantine expiry.

Flaky rate =
`tests with at least one inconsistent valid-condition outcome / tests executed in the period`.

Quarantine only non-critical work with issue, owner, rationale, expiry, and visible exclusion.
Critical/High evidence blocked by flakiness makes the verdict `Inconclusive` or `Not ready`
when a confirmed product failure exists.

## 5. Evidence validity and metrics

### Evidence validity checklist

Evidence is valid only when it identifies:

- criterion/case and oracle;
- command/action and actual observation;
- timestamp, commit/build, deployed component versions;
- target/config/feature flags and owned test data;
- exit/result and relevant correlation/trace;
- artifact location and optional integrity hash;
- collector/tool version;
- redaction, cleanup, and retention status.

Evidence is invalid when stale, from another configuration, missing its oracle, contradicted by
a current run, contaminated by environment/test defects, or unverifiable. Invalid evidence
cannot support `Passed`.

### Core metrics

Always state numerator, denominator, period/build, exclusions, and criticality segments.

- requirement coverage =
  `applicable atomic criteria with defensible terminal evidence / all applicable criteria`;
- risk-weighted coverage =
  `effective risk weight of applicable criteria with valid Passed or Failed evidence / total
  effective risk weight of all applicable criteria`; use the requirements-reference weight
  after band override; deferred/skipped/blocked/not-run/waived rows stay in the denominator;
- execution completion =
  `selected applicable cases with Passed or Failed result / selected applicable cases`;
  Blocked and Not run remain outside the numerator;
- pass rate =
  `Passed executed cases / cases with Passed or Failed result`;
- defect density =
  `confirmed defects / declared size unit` only when the size unit is meaningful;
- reopen rate =
  `reopened defects / defects previously marked Verified or Closed`;
- defect leakage =
  `defects first found after target phase/release / defects found in that defined population`;
- defect age = current/closure time minus first confirmed time, reported by severity;
- blocked age = current time minus block time, with owner;
- automation coverage =
  `automated selected stable cases / selected cases suitable for automation`;
- code coverage and mutation score use the exact tool scope and do not replace requirement
  coverage;
- compatibility/accessibility/performance/resilience metrics come from their references.

Do not compare counts across unequal periods, environments, scope, or severity. Never let a
high aggregate rate hide one failed/unknown critical criterion.

## 6. Verdict decision model

The verdict applies to a named object:

- pre-development: “requirements/test design readiness for implementation”;
- implemented/deployed: “QA evidence readiness of this build/scope for the stated goal.”

It is a QA evidence verdict, not release authorization or stakeholder UAT sign-off.

### Precedence table

Evaluate top to bottom:

| Condition | Verdict |
|---|---|
| confirmed Critical/High defect affecting the goal; critical invariant fails; unsafe/uncontrolled effect | `Not ready` |
| evidence is insufficient/invalid for any Critical/High criterion; required environment/dependency/version/UAT decision is blocked; critical flake unresolved | `Inconclusive` |
| every mandatory exit criterion passes; no open in-scope product defect or execution blocker remains; all Required criteria have current evidence; cleanup/reconciliation passes; no material residual risk or waiver remains | `Ready` |
| core goal and all Critical/High safety criteria pass, but bounded Medium/Low defects, accepted noncritical blocked/not-run work, a waiver, or another nonzero material residual risk remains with accountable acceptance | `Ready with concerns` |
| none of the above can be established | `Inconclusive` |

Rules:

- `Not ready` takes precedence over `Inconclusive` when a confirmed disqualifying failure
  exists, even if other rows are blocked.
- A blocked or not-run noncritical row may allow `Ready with concerns` only when it is outside
  mandatory exit criteria and an accountable owner accepts the bounded residual risk.
- Any open in-scope Medium/Low product defect or material accepted gap requires
  `Ready with concerns`, never plain `Ready`. An informational recommendation outside the
  accepted product requirements is not an open product defect.
- Missing stakeholder UAT yields `Inconclusive` only when UAT is a required exit gate; otherwise
  report UAT as not performed without pretending stakeholder acceptance.
- For pre-development, `Ready` means criteria and design are testable and implementation may
  begin; runtime cases remain `Not run`. `Not ready` means unresolved design conflict/risk
  prevents responsible implementation; `Inconclusive` means required product decisions are
  missing.

## 7. Closure and archive

Closure procedure:

1. reconcile every requirement, criterion, risk, case, result, defect, blocker, waiver, and
   evidence ID;
2. verify no pass lacks evidence and no final applicable row is blank;
3. evaluate each entry/exit criterion explicitly;
4. calculate metrics with denominators and criticality;
5. state untested/invalid evidence and residual risk;
6. confirm cleanup and final distributed state;
7. issue exactly one verdict with rationale and decision-object name;
8. archive artifacts with build/version identity, retention, access control, redaction, and
   integrity metadata;
9. conduct a short retrospective: useful technique, missed risk, bottleneck/flaky cause,
   artifact/suite improvement.

Archive only reproducible, sanitized value: cases/scripts, fixture definitions, evidence
manifest, summary snapshots, contract/version matrices, and defect links. Keep external
authoritative case systems authoritative.

Research basis: ISTQB CTFL 4.0.1 and CTAL Test Management 3.0 for defect reports,
traceability, monitoring metrics, exit criteria, completion, residual risk, and reporting.
All local decision rules are specified above:
<https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf> and
<https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTAL-TM_Syllabus_v3.0_zKjKsaN.pdf>.
