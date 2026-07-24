# Automated Test Levels and Suite Engineering

Use this reference to choose where tests belong, construct smoke/sanity/regression suites,
design maintainable automation, and produce reproducible evidence.

## Contents

1. Choose the lowest adequate level
2. Level-specific models
3. Smoke, sanity, and regression runbooks
4. Automation architecture and doubles
5. Determinism, isolation, and flakiness
6. CI/CD placement
7. Evidence contract
8. Completion gate

## 1. Choose the lowest adequate level

Ask what must be observed:

| Required proof | Lowest usual level |
|---|---|
| pure rule/calculation/validation | unit |
| module behavior through public API | component |
| database/queue/filesystem/adapter semantics | integration |
| consumer-provider compatibility | contract |
| transport/auth/error/pagination/idempotency | API/service |
| deployed health and critical wiring | smoke |
| coherent changed feature/flow | sanity |
| real user goal across stack | system/E2E |
| rendering/interaction/accessibility tree | browser/visual/manual |

Add an upper layer only when the lower one cannot expose configuration, serialization,
authorization propagation, deployment, third-party, browser, or cross-service risk. Keep rule
combinations low; keep E2E journeys few and diagnostic.

Do not enforce a universal pyramid/trophy. A pure library should be unit-heavy; a service with
database/queues needs meaningful integration; independently deployed services need contracts;
a UI product needs a small critical E2E layer.

## 2. Level-specific models

### Static and review checks

Use compiler/type checker, lint, schema validation, secret/dependency/config scanning, diff
review, and maintainability hotspot review. Record tool/config/version and scope. Static
findings are hypotheses until validated when the tool can false-positive.

### Unit tests

Prove local behavior with deterministic inputs and no real process/network dependency.

- call public behavior where practical;
- control clock, randomness, locale, and IDs;
- use table-driven cases for partitions/rules;
- assert outputs and state, not internal call sequence unless interaction itself is contract;
- keep execution fast enough for commit feedback;
- include failure and boundary behavior, not only examples.

### Component tests

Exercise a cohesive module/service in-process through its public interface while replacing
external systems. Use real internal collaborators and realistic serialization/configuration.
Assert observable component contract. This is often the best layer for HTTP handlers,
authorization middleware, and service workflows without network deployment.

### Integration tests

Use real technology for the risk being proven: actual database engine/schema, broker
semantics, filesystem, cache, or adapter sandbox.

Protocol:

1. provision version-pinned dependency;
2. create unique owned data/schema/topic namespace;
3. run migration/health precondition;
4. execute through public adapter;
5. assert result, durable state, emitted effects, and transaction behavior;
6. drain asynchronous work with bounded condition waits;
7. teardown idempotently and verify no residue.

An in-memory substitute cannot prove vendor-specific SQL, locking, transaction, encoding, or
queue semantics.

### Contract tests

Prove an interaction expected by a consumer is accepted by the provider. Generate consumer
expectations from behavior, publish/version the contract, set provider states, replay against
the provider implementation, and publish verification result. Contract tests do not prove a
whole business flow; use the distributed-systems reference for version and convergence work.

### API/service tests

Cover:

- schema/content type/status and error body;
- authentication, actor/resource/tenant authorization;
- required/optional/default/null/unknown fields;
- pagination/filter/sort/timezone/locale;
- idempotency, retries, concurrency, conditional requests;
- rate limit and safe failure behavior;
- required and forbidden durable effects.

Do not stop at response shape. Observe state and audit/side effects where material.

### System/E2E browser tests

Keep one case per critical user outcome plus upper-layer-only alternate paths.

- interact via user-visible roles, labels, text, or explicit stable test IDs;
- use browser framework auto-waiting and web-first assertions;
- wait on business state, not fixed sleeps;
- isolate account/session/data per test/worker;
- avoid third-party UI when an approved sandbox/API boundary proves the integration;
- capture trace/screenshot/console/network and correlation IDs according to evidence policy;
- select browsers/devices from supported usage and risk.

An E2E pass proves one configured journey, not every rule or real concurrency.

### Visual tests

Stabilize viewport, browser/OS, fonts, locale, data, animations, and clock. Define mask rules
and tolerance. Baseline changes require a named human review of the intended diff. A blindly
updated snapshot is not an oracle.

## 3. Smoke, sanity, and regression runbooks

### Smoke: is this target testable?

Prerequisites: exact build/versions deployed, target and credentials known, health dependencies
identified, no prohibited mutation.

Minimum probes:

1. process/service and required dependency health;
2. configuration/version endpoint or observable build identity;
3. authentication/session creation if the product requires it;
4. one read path and one safe critical write path when approved;
5. persistence/queue/worker round-trip for infrastructure required by dependent suites;
6. basic observability and cleanup.

Oracle: every selected probe reaches expected observable state within a bounded deadline, no
unexpected external effect, and created data is cleaned.

On failure: the smoke case is `Failed`; dependent cases are `Blocked`. Preserve target/version,
probe, timestamps, logs/correlation, actual state, and cleanup result. Stop target-dependent
execution.

Pass evidence: command/run ID, exit/result, exact build, target, time, probe summary, and
cleanup. Smoke is not feature acceptance.

### Sanity: does the requested change work coherently?

Build from the change's atomic criteria:

1. primary actor happy path;
2. highest-risk negative/denial path;
3. material boundaries and state transitions;
4. required side effects and forbidden effects;
5. changed integration/contract;
6. one recovery/retry path where relevant.

Run lower-level cases first, then one public flow if required. Sanity passes only when every
Critical/High criterion in the requested scope has defensible evidence and no selected core
case fails. It does not require unrelated full regression.

### Targeted regression: did the blast radius remain sound?

Derive from:

`diff → changed symbols/config/schema → callers/shared state → contracts → affected flows →
prior defects`

Select existing cases covering each node; add only uncovered risks. Include tests for the
original defect when testing a repair, neighboring boundaries/rules, and rollback/data
compatibility. Record excluded surfaces.

### Full regression: does the broader supported product remain sound?

Use for releases/broad/high-risk changes when suite reliability and cost are acceptable.
Prerequisites: smoke and sanity pass; known failures are baselined with owners. Run in
risk-priority shards. Aggregate by requirement/criticality, not just case count. A Critical
failure stops dependent/broader work according to plan.

Full regression is complete when selected suites finish, invalid/flaky results are reconciled,
all failures are attributed/classified, and coverage gaps are explicit.

## 4. Automation architecture and doubles

Structure test code into:

1. **intent layer:** cases and domain language;
2. **workflow/fixture layer:** builders, actors, data lifecycle;
3. **adapter layer:** API/UI/database/provider clients;
4. **driver/tool layer:** framework-specific details;
5. **evidence layer:** standardized run metadata and artifacts.

Keep assertions near domain intent. Centralize volatile selectors/protocol plumbing without
creating a generic framework that hides the test.

Use fixtures/builders with meaningful defaults and explicit overrides. Avoid shared mutable
global fixtures. Setup must fail clearly; teardown must be idempotent and failure-safe.

### Test doubles

| Double | Use |
|---|---|
| Dummy | required argument never used |
| Stub | returns controlled value/state |
| Spy | records interaction for later assertion |
| Mock | preprogrammed interaction expectation |
| Fake | working lightweight implementation, e.g. in-memory repository |

Prefer real implementation or high-fidelity fake when small and deterministic. Use a
stub/mock to trigger rare/unsafe failures or isolate an owned boundary. Do not mock the very
contract under test, restate implementation calls, or let a consumer mock stand in for
provider verification.

## 5. Determinism, isolation, and flakiness

### Isolation model

Allocate `run ID × worker ID × case ID` namespaces for:

- user/account/tenant;
- database/schema/table prefix;
- queue/topic/consumer group;
- object/file path and cache key;
- idempotency/correlation key;
- feature-flag/config scope;
- third-party sandbox record.

Never clean with a broad wildcard. Keep a cleanup ledger of created resources, attempt
teardown after failure, wait for asynchronous drains, and verify residue. Protect pre-existing
live data.

Control clock/timezone, random seed, locale, concurrency, environment variables, dependency
versions, and network behavior. Use bounded condition polling; fixed sleeps both waste time
and conceal races.

### Flaky-result protocol

A retry may gather evidence; it never converts the original failure into a clean pass.

1. preserve first failure and run metadata;
2. repeat under the defined diagnostic policy;
3. record sequence, seed, timing, machine, load, order, and shared state;
4. classify product nondeterminism, test defect, environment failure, or unresolved flake;
5. link affected criteria and confidence loss;
6. quarantine only with issue, owner, reason, expiry, and non-critical scope;
7. mark the affected row `Blocked` with flaky classification; use session verdict
   `Inconclusive` when this prevents a defensible critical result.

Never quarantine a Critical/High criterion merely to make a pipeline green.

## 6. CI/CD placement

Inspect the existing pipeline and timings before recommending changes.

| Trigger | Typical gate |
|---|---|
| local/commit | formatting, static, fast unit |
| pull request | unit, component, selected integration/contract, targeted regression |
| deployed test environment | smoke, sanity, E2E |
| release | broader regression, compatibility, required security/accessibility |
| schedule/manual | long E2E, dependency scans, performance/soak/fuzz/mutation |

Separate a quality gate from a diagnostic job. Gate only on reliable evidence and named
thresholds. Publish reports, versions, and artifacts. Do not modify CI without approval.

## 7. Evidence contract

Every run has an evidence manifest:

```text
Evidence ID
criterion/case IDs
command or CI job/run URL
start/end timestamp and exit code
source commit/build and component versions
target/environment/config/feature flags
sanitized test data and run/worker IDs
expected and observed result
artifact paths/URLs and optional integrity hash
correlation/trace IDs
collector/tool versions
redaction and cleanup status
```

Minimum pass evidence:

- unit/static: command/job, exit, tool/config, commit, result summary;
- integration/contract: above plus dependency/schema/provider versions and state/contract
  evidence;
- E2E/live: above plus target, data identity, user-visible outcome, relevant state/correlation;
- visual/accessibility: environment matrix, reviewed artifact/result;
- performance/security: domain-specific protocol and sanitized raw/summary evidence.

Evidence must be sufficient to identify what was proven. Saving every screenshot is not
useful if none links to an oracle.

## 8. Completion gate

Automation is acceptable when:

- each case belongs at the lowest adequate level;
- suites have explicit purpose, entry, oracle, evidence, and failure semantics;
- setup/data/teardown are isolated and repeatable;
- no fixed sleeps or hidden retries manufacture passes;
- known failures and quarantines are governed;
- CI placement matches speed, reliability, and risk;
- pass and failure evidence identifies the exact build and target.

Research basis: ISTQB Test Automation Engineering 2.0 for automation architecture,
CI/CD, configuration, maintainability, reporting, and continuous improvement; Playwright
official best practices for isolation, user-facing locators, web-first assertions, and traces:
<https://www.istqb.org/certifications/test-automation-engineering> and
<https://playwright.dev/docs/best-practices>.
