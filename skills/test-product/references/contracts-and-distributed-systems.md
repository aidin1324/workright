# Contracts, Compatibility, and Distributed Synchronization

Read before planning whenever behavior crosses a process, service, repository, provider,
schema, generated client, event, webhook, callback, or independent deployment. Compatibility
means both sides can interact for the supported version matrix; synchronization means the
business invariant converges across all systems after success and failure.

## Contents

1. Dependency and contract inventory
2. Define semantic invariants
3. Derive the required version/rollout matrix
4. Contract verification ladder
5. Distributed failure and synchronization model
6. Safe execution, evidence, metrics, and exit
7. Worked example

## 1. Dependency and contract inventory

Trace:

`user action → caller/consumer → provider/producer → contract/schema → persistence/transaction
→ event/job/webhook → downstream consumers → read model → user-visible final state`

For every edge record:

| Edge | Owner/repo | Contract and version | Runtime/deployed versions | Environment | Compatibility policy | Access |
|---|---|---|---|---|---|---|

Locate:

- OpenAPI/JSON Schema, GraphQL schema, Protobuf/gRPC;
- AsyncAPI/event schema and registry compatibility settings;
- Pact or equivalent consumer-driven contracts;
- generated SDK/client and generation source/version;
- database migrations or shared tables;
- webhook/provider documentation and sandbox;
- topic/queue/DLQ/consumer-group configuration;
- representative sanitized request/event traces.

Ask only what discovery cannot find:

- where is the related service/contract: local path, repository, registry, or URL?
- which exact versions are current, supported, and coexisting during rollout?
- may both source/contract sides be read and may safe verification run?
- who owns compatibility policy, deployment order, and final business state?

If any required side/version is unavailable, mark only affected combinations `Blocked` and
state residual risk. Never infer compatibility from a consumer mock, schema diff, or one
deployed side.

## 2. Define semantic invariants

Schema compatibility is necessary but not sufficient. For each interaction state:

```text
Trigger and actor
Consumer assumption
Provider guarantee
Business meaning of fields/status/errors
Authorization/tenant invariant
Required writes/events/notifications
Forbidden effects
Idempotency key and duplicate rule
Ordering rule
Retryable vs terminal errors
Unknown-outcome handling
Canonical owner of state
Allowed interim states
Convergence deadline
Compensation/reconciliation outcome
```

Examples:

- accepted payment event must mean funds are captured, not merely requested;
- omitted price currency must not silently default differently across services;
- a timeout after provider commit is an unknown outcome; retry must not double charge;
- `order.paid` and billing ledger must agree within 30 seconds, or reconciliation alerts.

Include identity propagation, correlation/causation IDs, clock/timezone, encoding, default and
null semantics, enum unknown values, pagination, cancellation, and error mapping where
material.

## 3. Derive the required version/rollout matrix

### Compatibility directions

- **Backward:** new reader/consumer handles data written by old producer/schema.
- **Forward:** old reader/consumer handles data written by new producer/schema.
- **Full:** both directions.
- **Transitive:** the new version is checked against every supported prior version, not only
  the immediately previous one.

Use the project's actual definition if terminology differs.

### Minimum combinations

Always evaluate:

| Consumer | Provider/producer | Purpose |
|---|---|---|
| current | current | target steady state |
| old supported | new | provider/producer-first or rolling coexistence |
| new | old supported | consumer-first or rollback coexistence |
| each transitive supported version | new/current | declared long-lived support |

Add generated-client versions, schema-registry versions, stored historical events, and
rollback combinations when they can coexist.

### Choose rollout order from policy

- Backward event compatibility generally requires upgrading consumers before producers emit
  new data because old consumers are not guaranteed to read it.
- Forward compatibility generally requires producer-first handling under the actual platform
  semantics.
- Full compatibility permits independent order at the schema level, but semantic and
  operational behavior still need verification.
- No compatibility policy requires a coordinated stop-the-world change or explicit migration
  plan; never assume safe rolling deployment.

Record exact planned order, coexistence duration, flag activation, migration/backfill,
rollback point, and who detects incompatibility.

## 4. Contract verification ladder

Execute narrow to broad:

### 1. Static contract diff

Compare accepted baseline to candidate. Classify:

- additive optional/defaulted change;
- removal/rename/type/format/range change;
- requiredness/null/default/enum change;
- request/response/status/error/auth change;
- topic/routing/partition/ordering change;
- semantic change not expressible in schema.

Run the project compatibility tool/registry rule. A green diff proves only encoded rules.

### 2. Consumer behavior/contract

Exercise the real consumer client against a contract mock generated from consumer
expectations. Assert parsing, request construction, defaults, errors, retries, and semantic
use. Publish/version the contract when tooling supports it.

### 3. Provider verification

Create deterministic provider states and replay every relevant consumer interaction against
the actual provider implementation. Publish result for the exact provider version. Stub only
the provider's downstream dependencies, not behavior under verification.

### 4. Exact deployed-version integration

Run real serialization, transport, authentication, generated clients, schema registry, and
infrastructure for each required version combination. Assert semantic invariant and both
sides' state.

### 5. Rolling upgrade and rollback

Simulate the actual order with old/new instances coexisting. Send old and new payloads before,
during, and after flag/schema activation. Verify routing, storage, replay, monitoring, and
rollback reads historical/new data.

### 6. Failure/recovery and reconciliation

Inject only approved bounded failures. Verify unknown outcome, retry/idempotency, delayed or
duplicate delivery, DLQ/replay, compensation, and final convergence.

Do not substitute E2E alone for contract levels; it is slower, less diagnostic, and usually
samples too few versions.

## 5. Distributed failure and synchronization model

Build a state table:

| Scenario | Local commit | Publication/call | Downstream state | User state | Recovery and deadline |
|---|---|---|---|---|---|

Cover applicable scenarios:

- provider slow, unavailable, malformed, or terminal error;
- timeout before/after provider side effect;
- partial persistence before event publication;
- at-least-once duplicate; delayed or reordered event;
- stale consumer during rolling deployment;
- process restart after local commit;
- DLQ and bounded replay;
- compensating transaction/saga failure;
- reconciliation/backfill and repeated reconciliation;
- user reads before and after convergence.

### Patterns and their required tests

- **Idempotency:** same key/request repeated yields one business effect and stable response or
  documented equivalent.
- **Transactional outbox:** local state and outbox are atomic; publisher retry emits without
  lost business event; consumer deduplicates.
- **Saga/compensation:** every partial state has a compensating or manual-resolution path;
  compensation is idempotent and observable.
- **Optimistic concurrency:** stale write is rejected/merged as specified; retry preserves
  invariant.
- **Eventual consistency:** canonical state, allowed interim state, convergence condition and
  maximum time are explicit.
- **Reconciliation:** detects divergence, repairs only authorized state, is repeatable, and
  reports unrecoverable rows.

Do not test asynchronous convergence with a fixed sleep. Poll the authoritative observation
until condition or deadline and preserve timestamps.

## 6. Safe execution, evidence, metrics, and exit

### Safety

Event replay, webhook invocation, backfill, queue/DLQ mutation, schema registration, and
provider calls can duplicate irreversible effects. Require target-specific approval,
test namespace, rate limit, sandbox endpoints, known idempotency behavior, monitoring,
abort/cleanup, and replay boundary. Never publish test events to a production topic by
default.

### Evidence

Capture:

- dependency graph and owner/access map;
- contract/schema baseline and diff;
- consumer and provider verification run IDs;
- exact consumer/provider/generated-client/schema versions;
- version × rollout × scenario matrix;
- sanitized request/event and correlation/causation/idempotency IDs;
- per-system state snapshots with timestamps;
- retries, DLQ/replay/compensation evidence;
- convergence measurement and final user-visible outcome;
- cleanup/reconciliation state.

### Metrics

- compatibility coverage =
  `verified required version combinations / required combinations`;
- contract verification coverage =
  `verified applicable consumer interactions / applicable interactions`;
- convergence compliance =
  `flows converged within SLO / completed test flows`;
- duplicate-effect count and reconciliation delta must be zero unless requirement says
  otherwise;
- recovery completeness =
  `recoverable injected failures reaching correct terminal state / injected failures`.

Always provide counts, time window, versions, and exclusions.

### Exit criteria

Compatibility/synchronization passes only when:

- every supported combination and rollout/rollback combination is Passed or explicitly
  accepted outside support;
- no schema or semantic breaking change remains;
- Critical invariants pass under success, retry, duplicate, and applicable partial failure;
- convergence/recovery thresholds pass;
- no unexplained DLQ, divergence, duplicate effect, or orphan state remains;
- all sides and exact deployed versions have evidence.

Missing one side or a required combination makes affected RTM rows `Blocked` and the
compatibility/readiness verdict `Inconclusive`, not Ready.

## 7. Worked example

Flow: Order service A reserves inventory through B, then emits `OrderConfirmed`; Billing C
creates an invoice.

1. Inventory identifies A→B OpenAPI and A→C event schema plus generated client versions.
2. Invariants: one reservation and one invoice per order/idempotency key; rejected reservation
   emits no confirmation; A/B/C converge within 20 seconds.
3. Matrix: A-old/B-new, A-new/B-old for rolling API deployment; C-old/new against old/new
   event schema; current/current.
4. Static diff finds a new optional `warehouseId`; provider verification confirms old callers;
   C-old must ignore or default the new field according to event policy.
5. Integration tests timeout after B commits: A retries with same key and B reserves once.
6. Outbox test crashes A after order commit and before publish; restart publishes once,
   C deduplicates, all states converge.
7. Evidence links contract runs, exact images, order/correlation IDs, state snapshots, and
   convergence time. Any missing C repository/version blocks the end-to-end sync claim.

Research basis: Pact provider verification requires replaying consumer interactions against
the provider and publishing the result; Confluent documents backward/forward/full/transitive
compatibility and its rollout-order implications:
<https://docs.pact.io/getting_started/verifying_pacts> and
<https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html>.
