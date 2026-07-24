# Environment, Test Data, Live Testing, and Full Ride

Read before provisioning, mutating, or claiming anything about a running target. The goal is
not to copy production blindly; it is to make each environment dimension adequate for the
claim and make every side effect owned, bounded, observable, and reversible.

## Contents

1. Environment claim and fidelity model
2. Reproducible provisioning and qualification
3. Test-data lifecycle and parallel isolation
4. Live-testing runbook
5. Full-ride model and persona simulation
6. Production preflight and abort protocol
7. Completion gate

## 1. Environment claim and fidelity model

For each planned test record:

| Dimension | Required fidelity | Actual target | Gap and effect on claim |
|---|---|---|---|
| source/build and feature flags |  |  |  |
| OS/runtime/container |  |  |  |
| database/cache/broker versions |  |  |  |
| schemas/migrations/data volume |  |  |  |
| services/providers/contracts |  |  |  |
| network/TLS/DNS/proxy |  |  |  |
| identity/roles/tenant policy |  |  |  |
| browser/device/locale/timezone |  |  |  |
| topology/capacity/autoscaling |  |  |  |
| monitoring/logging/tracing |  |  |  |

Examples:

- a hermetic unit test needs code/runtime fidelity, not production topology;
- a migration test needs the real database engine, schema history, and representative volume;
- contract verification needs the exact provider implementation and states, not production
  data;
- capacity/scalability claims need representative topology and observability;
- browser support claims need the approved browser/device matrix.

If a material gap remains, mark affected RTM rows `Blocked`; when it prevents the named
readiness claim, the session verdict is `Inconclusive`. “Works locally” does not establish
“ready in production.”

Prefer in order:

1. isolated local/container for deterministic component work;
2. ephemeral integration environment for real dependencies;
3. shared staging/test server with data namespaces;
4. dedicated production-like performance/security environment;
5. production only for explicitly approved bounded observation/action.

## 2. Reproducible provisioning and qualification

### Provision

- use repository-supported IaC/container/fixture tooling;
- pin source, images, dependencies, schemas, configuration, and feature flags;
- record secrets by identifier, never value;
- make setup idempotent or fail before partial mutation;
- detect configuration drift against declared target;
- use unique session/run ID.

If the environment is manually provisioned, record exact steps and deviations so another
agent can reproduce it.

### Qualification sequence

1. identify target and exact deployed versions;
2. verify required endpoint/process/dependency health;
3. verify schema/migration and feature-flag state;
4. verify credentials, role, tenant, and test-account isolation;
5. verify monitoring, clock, storage, queue, and external sandbox access as applicable;
6. seed minimal owned data;
7. run smoke probes from the automated-levels reference;
8. verify cleanup using the minimal data;
9. publish environment qualification evidence.

Health endpoints alone are insufficient if the planned flow depends on persistence, workers,
or providers. A failed qualification probe blocks only work relying on that capability unless
the target is generally contaminated or unsafe.

## 3. Test-data lifecycle and parallel isolation

### Design production-like, sanitized data

Build from partitions and states, not a random database dump:

- smallest valid object;
- typical realistic object;
- boundary sizes/values/dates;
- invalid and forbidden values;
- each role/account/tenant/state;
- historical regression shape;
- required relationship/cardinality and asynchronous state.

Use synthetic data by default. If production-derived data is necessary, obtain authority,
minimize fields, irreversibly sanitize, document provenance/retention, and verify it cannot be
re-identified. Never put personal data, secrets, real tokens, or raw customer payloads into
tracked fixtures.

### Ownership and namespace

Use:

`session ID / run ID / worker ID / case ID`

in all created resources. Allocate separate:

- users, accounts, tenants, roles;
- database schema/row keys;
- topics, consumer groups, queues, DLQs;
- object storage/file paths/cache keys;
- idempotency and correlation keys;
- email/SMS/payment/provider sandbox destinations.

Record each resource in a cleanup ledger with create time, owner case, delete/reconcile
action, and final state.

### Setup and teardown

Each test owns its setup, or consumes an immutable declared fixture. Teardown must:

1. run after pass/failure/abort where safe;
2. be idempotent;
3. avoid broad globs or deleting pre-existing data;
4. drain/cancel asynchronous jobs or wait for a bounded terminal state;
5. remove external sandbox objects when supported;
6. verify no residue and record exceptions.

If cleanup fails, report environment contamination. Do not continue tests whose evidence or
data isolation may be compromised.

## 4. Live-testing runbook

Live testing means interacting with a running application through real public interfaces. It
does not automatically mean production.

### Preflight

Record:

- target URL/environment and exact versions;
- account/role/tenant and test-data namespace;
- approved actions and prohibited actions;
- external providers and real-world consequences;
- monitoring/log/trace access;
- per-action and total rate/concurrency limits;
- stop/abort thresholds;
- cleanup and rollback;
- evidence capture and redaction;
- operator/owner contacts when an incident is possible.

No approved target/effect/cleanup means no mutating live test.

### Coverage matrix

Build only applicable dimensions:

| User goal/route | Role/tenant | State/data | Browser/device | Expected final state | Case/evidence |
|---|---|---|---|---|---|

Cover:

1. critical route discovery/navigation;
2. primary goal;
3. highest-risk denial/permission path;
4. material validation/boundary;
5. interruption/retry/recovery;
6. required external effect in sandbox;
7. logout/session/cleanup;
8. final state through UI and authoritative system.

“All routes” means all routes in the approved route inventory, not crawling or mutating
unknown endpoints blindly.

### Execution

1. confirm environment qualification and smoke are current;
2. start narrow read-only/safe cases;
3. allocate unique data for each case/persona;
4. record correlation IDs and timestamps during action;
5. wait on observable conditions with deadline;
6. assert output, required effects, forbidden effects, and final state;
7. capture evidence for pass and failure;
8. cleanup and verify;
9. update RTM before the next risk tier.

On a defect, follow stop/contain/report rules. Do not repair or rerun against a modified
product without a separate remediation and identified build.

## 5. Full-ride model and persona simulation

Full ride has two parts:

1. **required:** every test layer and quality characteristic applicable to the approved scope
   and risk;
2. **optional/costly:** multiple isolated subagent/persona explorations that simulate
   different real-user goals and usage patterns.

Persona simulation requires explicit approval. It is useful for independent exploration,
workflow variation, and usability observations. It is not proof of real user research, load,
accessibility conformance, or concurrency.

### Build the matrix

| Requirement/risk | Layer/technique | Persona/role | Environment/data | Owner | Result/evidence |
|---|---|---|---|---|---|

Choose personas from actual roles and risks, for example:

- first-time user completing the primary goal;
- experienced user optimizing the workflow;
- constrained/invalid actor testing recovery;
- admin/support role;
- attacker/unauthorized role using safe security probes;
- old/new client or service version.

Give each a bounded charter, isolated account/data, prohibited actions, required evidence, and
time box. Deduplicate findings by behavior/root symptom while preserving every reproducer and
affected persona.

### Completion

Full ride is complete when:

- all applicable requirement × risk × layer rows are terminal;
- every approved persona charter is debriefed;
- duplicate findings are reconciled;
- no persona evidence is overstated;
- Critical/High rows and cross-system final states are independently evidenced;
- cleanup and environment integrity are verified.

## 6. Production preflight and abort protocol

Production is not the default test environment. Prefer staging, preview, sandbox, canary, or
shadow/read-only observation.

Before any production action require:

- named approver and exact action list;
- test account/tenant/data and safeguards against real users;
- known external effects and financial/notification consequences;
- rate, concurrency, duration, geographic and data-scope ceilings;
- live dashboards/logs and operator;
- kill switch/abort mechanism;
- rollback/compensation and incident path;
- cleanup and retention plan.

Start at one minimal action. Increase only within the approved plan after health remains
normal. Abort immediately on unexpected customer impact, data-integrity risk, security
exposure, error/latency/resource threshold, runaway jobs/notifications, evidence loss, or
cleanup failure.

After abort:

1. stop load/actions;
2. preserve evidence and exact state;
3. trigger approved rollback/compensation;
4. verify user/data/system integrity;
5. report and do not resume without new explicit approval and requalified entry criteria.

Never improvise a production rollback.

## 7. Completion gate

Environment/live work is complete only when:

- fidelity is mapped to each claim and every gap is disclosed;
- build/config/dependency identity is recorded;
- test data is synthetic/sanitized, owned, and isolated;
- smoke and required qualification probes pass;
- external effects and limits are approved;
- pass/failure evidence includes target, time, data, action, and final state;
- cleanup ledger is reconciled;
- no uncontrolled production action occurred.

Research basis: ISTQB test-management and performance guidance for representative
environments, explicit entry criteria, monitoring, and controlled execution; Playwright for
browser isolation and evidence. The runbooks above are complete local guidance.
