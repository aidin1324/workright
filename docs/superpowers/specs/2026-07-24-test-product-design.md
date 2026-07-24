# Test Product Skill Design

## Status

Approved in conversation on 2026-07-24. This document defines the design of
`test-product`; it does not authorize implementation changes beyond this specification.

## Purpose

`test-product` is a requirements-driven quality-assurance orchestrator for a feature,
business flow, release, integration, or whole software product. It may run before
development, after implementation, or against an approved deployed environment.

The skill must:

- understand the user's actual goal from the end user's perspective;
- analyze the repository and connected systems before selecting tests;
- expose ambiguity, conflicts, and untestable requirements early;
- create measurable acceptance criteria and a Requirement Traceability Matrix (RTM);
- recommend a fast focused run or a more expensive full ride;
- create and execute only applicable tests;
- report every defect with evidence;
- stop on critical findings without repairing production code;
- leave an auditable test plan, RTM, defect log, and closure report.

Quality and feedback speed are co-primary goals. Completeness means covering all
applicable risks, not mechanically running every known test type.

## Non-goals

The skill must not:

- fix defects or modify production code;
- deploy, update, or repair production;
- choose product intent when requirements conflict;
- claim complete quality or compatibility without evidence;
- run destructive security, performance, or production tests without explicit approval;
- treat pass rate or code coverage alone as proof of release readiness;
- duplicate an established external test-management source of truth.

Defect remediation is always a separate user-requested task.

## Skill name and invocation

The skill name and directory are `test-product`.

It supports explicit invocation and automatic model invocation. Do not set
`disable-model-invocation: true`.

Proposed trigger:

```yaml
---
name: test-product
description: Use when a feature, business flow, release, integration, or whole software product needs requirements-based test planning, quality assessment, or testing before development or after implementation or deployment.
---
```

## Classification model

Before broad testing, classify the request along four independent dimensions:

| Dimension | Values |
|---|---|
| Lifecycle | `Pre-development`, `Implemented`, `Deployed` |
| Scope | `Feature`, `Business flow`, `Change or release`, `Whole product` |
| Risk | `Low`, `Medium`, `High or critical` |
| Profile | `Focused`, `Full ride` |

Explain the provisional classification and its concrete reasons. Reclassify when
repository discovery reveals broader impact.

### Profiles

`Focused` is the default recommendation. It is fast but not superficial: requirement
analysis, RTM, baseline checks, sanity testing, risk-targeted unit/integration coverage,
positive and negative paths, boundary cases, and targeted regression remain mandatory
when applicable.

`Full ride` adds the applicable expensive confidence layers: broad regression, approved
E2E and live testing, exploratory testing, compatibility matrices, security, performance,
resilience, accessibility, and independent user simulations. It does not require irrelevant
tests.

`Pre-development` ends after Shift Left analysis, acceptance criteria, RTM, and a test
plan. Execution rows are marked `Not run — implementation absent`, not silently omitted.

## Mandatory workflow

The main `SKILL.md` must prescribe this order:

```text
Intent
→ Repository discovery
→ Scope and lifecycle classification
→ Requirement analysis
→ Ambiguity gate
→ Acceptance criteria
→ Risk analysis
→ RTM
→ Profile recommendation
→ Test plan
→ User approval
→ Artifact creation
→ Environment validation
→ Smoke gate
→ Layered execution
→ Defect handling
→ RTM reconciliation
→ Closure report
```

The order is binding. The agent retains discretion only in selecting applicable techniques,
tools, and depth inside the approved scope.

## Decision contract

Do not require the agent to disclose private chain-of-thought. Require a concise,
observable decision record instead.

For every considered test type, record:

```text
Test type
→ Requirement or risk covered
→ Applicable, skipped, or blocked and why
→ Technique
→ Environment
→ Cost
→ Required approval
→ Expected evidence
```

Decision rules:

1. Do not run a test merely because it exists in the catalog.
2. Do not skip an applicable test without a factual reason.
3. Start at the fastest, lowest layer that can provide the required confidence.
4. Move upward only for behavior a lower layer cannot prove.
5. Avoid duplicating identical assertions across layers.
6. Cover positive, negative, boundary, and failure paths for every material requirement.
7. Keep tests independent, repeatable, order-independent, and in control of their data.
8. Establish the existing-test and environment baseline before attributing failures.
9. Support every `Passed`, `Failed`, `Blocked`, and `Not run` result with evidence.
10. Update the RTM throughout execution rather than only during planning.

## Repository and requirement discovery

Inspect instructions, documentation, status and diffs, architecture, manifests, lockfiles,
test layout, CI/CD, deployment configuration, existing test reports, and local run commands.
Trace the requested flow through validation, authorization, domain logic, persistence,
integrations, side effects, and user-visible results.

Identify:

- the end user and business outcome;
- current and intended behavior;
- measurable acceptance criteria;
- non-goals;
- sources of truth;
- inputs, outputs, permissions, and side effects;
- edge cases and failure behavior;
- privacy, security, performance, rollout, and rollback constraints;
- connected repositories, services, providers, schemas, and deployed versions.

Ask only questions whose answers cannot be obtained safely from the repository or approved
environment. Stop before RTM construction when a missing answer changes expected behavior.

## RTM and planning

Every testable acceptance criterion receives a stable requirement ID. Each RTM row contains:

| Field |
|---|
| Requirement ID |
| Source |
| Requirement or acceptance criterion |
| User value |
| Risk and priority |
| Test level |
| Technique |
| Test case IDs |
| Environment |
| Result |
| Evidence |
| Defect IDs |

Allowed final results are `Passed`, `Failed`, `Blocked`, `Not run`, and `Not applicable`.
No result cell may be empty at closure.

The test plan contains:

- goal, scope, and non-goals;
- classification and profile;
- assumptions, conflicts, and open questions;
- selected, skipped, and blocked test types with reasons;
- environment, component versions, and dependencies;
- test data, privacy controls, cleanup, and rollback;
- entry and exit criteria;
- ordered execution plan;
- approvals and prohibited actions;
- estimated time, resources, and token cost.

The user must approve the test plan, target environments, external effects, and proposed
artifact changes before execution.

## Test design catalog

### Requirement and static techniques

- requirement, acceptance-criteria, architecture, and data-flow review;
- project-scoped code-quality and bug-hotspot review;
- formatter, lint, type, build, and static-analysis checks;
- dependency, deprecated-API, configuration, and supply-chain review.

Code-quality findings must be tied to correctness, testability, maintainability, or a
specific defect risk. Do not report stylistic preferences as defects.

### Functional test design

Use as applicable:

- equivalence partitioning;
- boundary value analysis;
- decision tables;
- state-transition testing, including invalid transitions;
- use-case and end-user scenario testing;
- positive and negative testing;
- error guessing after systematic techniques;
- time-boxed exploratory charters;
- checklist-based testing with a versioned checklist;
- pairwise or risk-based combinatorial selection;
- property and invariant testing;
- fuzz testing with explicit resource bounds;
- mutation testing for critical logic when coverage confidence is uncertain.

### Test levels

Use the test pyramid as a selection heuristic:

- unit;
- component;
- integration;
- contract;
- API;
- system and E2E;
- visual regression.

Use many fast lower-level checks and fewer broad E2E checks. A higher-level test must add
confidence unavailable at a lower level.

### Change-confidence sequence

Run in this order where applicable:

```text
Environment health
→ Smoke
→ Sanity of requested scope
→ Targeted regression
→ Full regression when profile or risk requires
```

Smoke confirms that the environment is testable. Sanity is the core purpose of the skill:
it determines whether the requested feature or flow works coherently after a change.
Regression evaluates impact on previously working behavior.

### Security

Activate security testing for authentication, authorization, sensitive data, payments,
uploads, public inputs or APIs, external integrations, or release gates.

Cover attack-surface mapping, sessions, object-level authorization, validation and
injection, secrets and data exposure, dependency/configuration risk, safe logging, abuse
cases, rate limits, file handling, and business-logic attacks. Base web/API guidance on
OWASP ASVS and WSTG.

Active destructive checks require separate approval and are never run against production
by default.

### Performance and resilience

Select among baseline, load, stress, spike, endurance, scalability, recovery, and failover
testing only when risk and measurable requirements justify them.

Require:

- a workload model;
- a representative environment;
- measurable thresholds such as latency percentiles, throughput, errors, CPU, and memory;
- explicit permission to generate load;
- monitoring, cleanup, and recovery observation.

Stress testing must evaluate graceful degradation and post-stress recovery, not merely find
a crash threshold.

### Live testing and full ride

Prefer staging or a dedicated test server. Prefer local execution when Computer Use,
complete isolation, or controlled test data requires it. Production testing is limited to
pre-approved, safe actions against an already deployed version; the skill never deploys.

Live testing covers applicable main paths, edge paths, roles, routes, supported browsers,
devices, versions, and recovery behavior. Save screenshots, traces, logs, and network
evidence for failures without exposing secrets.

Full ride may dispatch isolated user-simulation agents for personas such as:

- new user;
- experienced user;
- restricted-role user;
- invalid or hostile-input user;
- interrupted or slow-network user;
- accessibility-oriented user;
- concurrent users when concurrency is material.

Each agent starts from clean state, performs an approved bounded charter, modifies no
production code, and returns observations and evidence. Full ride requires explicit approval
because of runtime and token cost.

### Usability, accessibility, and UAT

The agent may prepare personas, scenarios, objective usability checks, accessibility checks,
and stakeholder questions. Accessibility combines automated, manual, and, where available,
assistive-technology evaluation; an automated scanner alone cannot establish conformance.

The user or relevant stakeholder makes subjective usability and UAT decisions. The agent
must not substitute its taste for stakeholder acceptance.

## Contract and synchronization gate

This gate is mandatory when discovery finds microservices, multiple repositories,
HTTP/RPC providers, event buses, queues, shared schemas, generated clients, external
providers, webhooks, callbacks, or independently deployed versions.

Build a dependency map:

```text
Feature or flow
→ caller or consumer
→ provider or producer
→ API, event, or schema
→ persisted state
→ downstream consumers
→ deployed versions
```

Locate OpenAPI/JSON Schema, Protobuf/gRPC, GraphQL, AsyncAPI, Pact or equivalent contracts,
generated SDKs, shared migrations, integration documentation, and representative traffic.

Check:

- consumer expectations against provider behavior;
- schema and semantic compatibility;
- required and optional fields, enums, defaults, and nullability;
- status and error models;
- authentication and authorization;
- ordering, duplication, and idempotency;
- timeout, retry, and partial-failure behavior;
- backward, forward, full, and transitive compatibility as applicable;
- deployment order and rolling-version coexistence;
- end-to-end state synchronization across the business flow.

When a related service or repository is unavailable, ask whether it is local, in another
repository, accessible by URL, or deployed to an approved test environment. Ask for
permission to read its source or contract and run safe integration checks. Never mark
compatibility passed without both contract and execution evidence; mark affected RTM rows
`Blocked` and state the residual risk.

## Environment and test data

Prefer the project's existing test harness and conventions. Mirror production closely
enough for the claims being made, but isolate tests from production data and external
effects.

The agent may create or modify only approved test artifacts:

- tests under `tests/` or the project's established equivalent;
- E2E and test-support scripts under `scripts/` or the established equivalent;
- sanitized fixtures and test data;
- test-only configuration, Docker, or IaC;
- RTM, plans, cases, checklists, defect logs, evidence indexes, and reports under
  `docs/tests/` or the approved documentation location.

It must not modify production code. It must not hide a defect by weakening an assertion,
mocking away the behavior under test, or introducing a test-only workaround.

State environment, versions, credentials required, data mutations, external calls, cleanup,
and rollback before execution. Never persist or expose secrets or personal data in source,
test output, screenshots, traces, logs, or reports.

Run a smoke suite after provisioning or deployment. Do not run dependent heavy suites when
smoke fails.

## Defect handling

Severity is based on user and system impact:

| Severity | Definition | Execution behavior |
|---|---|---|
| `Critical` | Data loss/corruption, exploitable security issue, major outage, or irreversible external effect | Report immediately and stop |
| `High` | Core goal or critical flow fails, serious contract break, and no reasonable workaround exists | Report immediately and stop |
| `Medium` | Material partial failure with independent tests still runnable | Report immediately, log, and continue independent tests |
| `Low` | Minor functional, cosmetic, or usability issue | Log and continue |
| `Blocked` | Missing access, environment, data, dependency, or authority rather than a product defect | Report affected scope and RTM rows |

Ambiguous requirements, conflicting sources of truth, or dilemmas affecting expected
behavior also stop execution until the user decides.

Every defect report contains:

- stable ID, concise title, and severity;
- requirement and test case IDs;
- environment, build, and component versions;
- preconditions and reproduction steps;
- expected and actual result;
- reproducibility;
- sanitized logs, traces, screenshots, schema diffs, or other evidence;
- user/business and technical impact;
- execution status after the finding.

The skill reports findings but never asks to repair them automatically. It states that
remediation requires a separate task.

## Closure

Reconcile every requirement, test case, and defect with the RTM. The summary report includes:

1. Goal, scope, profile, environment, and versions.
2. Requirement and RTM coverage.
3. Every considered test type with selected/skipped/blocked reason, result, and evidence.
4. Every technique used with reason, test cases, and findings.
5. Passed, failed, blocked, and not-run counts.
6. Defects by severity.
7. Code coverage only when actually measured and meaningful.
8. Performance, security, compatibility, and flakiness metrics when applicable.
9. Unverified requirements and residual risks.
10. Entry/exit criteria outcome.
11. One verdict: `Ready`, `Ready with concerns`, `Not ready`, or `Inconclusive`.

A high pass rate cannot override a failed or unverified critical requirement.

## Target-project artifacts

Unless the user selects another location or the project already has a source of truth, create:

```text
docs/tests/<date>-<scope>/
├── test-charter.md
├── rtm.md
├── test-plan.md
├── test-cases.md
├── defect-log.md
└── test-summary.md
```

Large raw evidence belongs in the existing framework's report directory or an approved
ignored artifact directory. Documentation links to that evidence rather than committing
large binaries or sensitive logs.

## Skill package structure

```text
skills/test-product/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── requirements-rtm-and-risk.md
│   ├── test-planning.md
│   ├── test-design-techniques.md
│   ├── automated-test-levels.md
│   ├── environment-data-and-live-testing.md
│   ├── contracts-and-distributed-systems.md
│   ├── security-performance-and-resilience.md
│   ├── usability-accessibility-and-uat.md
│   └── defects-metrics-and-closure.md
├── assets/
│   └── templates/
│       ├── test-charter.md
│       ├── rtm.md
│       ├── test-plan.md
│       ├── test-cases.md
│       ├── defect-log.md
│       └── test-summary.md
└── scripts/
    └── init-test-session.py
```

`SKILL.md` owns the non-negotiable workflow, gates, decision rules, reference routing, and
output contract. References own detailed applicability, execution guidance, common mistakes,
and evidence requirements. Templates are copied into target projects. Do not duplicate
reference content in the main file.

`init-test-session.py` creates `docs/tests/<date>-<scope>/` from templates, substitutes
session metadata, refuses to overwrite existing files, and never touches production code.
Project-specific E2E, load, and security scripts are created in the target repository rather
than bundled generically.

## Validation strategy

Develop the skill through baseline and forward tests.

Run equivalent scenarios without and then with the skill:

1. An ambiguous feature request tempts immediate test execution without an end-user goal or RTM.
2. A multi-service flow has mismatched deployed versions and an inaccessible provider repository.
3. A full-ride request tempts unapproved live tests and excessive subagent use.
4. A high-severity defect tempts continued execution or an unsolicited repair.
5. A pre-development request has no runnable implementation.
6. A medium defect requires immediate reporting while independent tests continue.
7. A high pass rate hides one blocked critical requirement.
8. An existing external test-management system makes local artifact duplication tempting.

Capture baseline failures and rationalizations. Write the minimal guidance that corrects
observed failures, rerun the scenarios with the skill, then tighten any remaining loopholes.

Validate:

- skill metadata and directory naming;
- automatic discovery from realistic prompts;
- reference routing;
- template completeness;
- script non-overwrite behavior and portability;
- defect stop/continue behavior;
- zero production-code edits;
- RTM reconciliation and evidence-backed verdicts.

## Research basis

- [ISTQB CTFL 4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)
- [ISTQB Technical Test Analyst 4.0](https://www.istqb.org/wp-content/uploads/2024/11/ISTQB-CTAL-TTA_Syllabus_v4.0.pdf)
- [ISTQB Acceptance Testing](https://www.istqb.org/certifications/certified-tester-acceptance-testing-ct-act/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/latest/)
- [W3C accessibility evaluation](https://www.w3.org/WAI/test-evaluate/)
- [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Google Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html)
- [Playwright best practices](https://playwright.dev/docs/best-practices)
- [Pact provider verification](https://docs.pact.io/implementation_guides/javascript/docs/provider)
- [Confluent schema evolution and compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html)

