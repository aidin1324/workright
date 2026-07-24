# Resilience and Recovery Testing

Read when behavior depends on services/providers/networks/queues/processes, failover, retry,
or recovery objectives. Fault injection is never implied by selection and is not run against
production by default.

## 1. Define the experiment

For each experiment write:

```text
Steady-state business invariant and metric
Fault hypothesis
Fault target/mechanism
Blast radius and test namespace
Expected degraded behavior
Abort condition and kill switch
Recovery action/automatic behavior
RTO/RPO/convergence/reconciliation oracle
Monitoring owner and evidence
```

Useful steady states: accepted orders stay within error SLO; no duplicate charge; every
accepted event reaches a terminal state; reads remain available; no tenant boundary breaks.

## 2. Select faults from architecture

Consider only credible risks:

- dependency timeout, latency, malformed response, reset, or outage;
- exhausted pool/connection/thread/file descriptor;
- retry storm, circuit breaker, or rate limit;
- process/pod/node restart, leader change, or zone loss;
- network partition, DNS/TLS failure, or clock skew;
- delayed/duplicate/reordered event or DLQ;
- disk/storage pressure/read-only mode;
- stale cache/read model;
- failed compensation or reconciliation.

Inject one fault first. Combined faults require a separate hypothesis and higher approval.
Do not use a fault simply because the tool exposes it.

Turn architecture behavior into a matrix:

| Failure | Injection/proxy | Expected protection | Business oracle | Recovery oracle |
|---|---|---|---|---|
| provider timeout before effect | bounded delay/drop | timeout, bounded retry | no local success/forbidden effect | request may retry safely |
| provider timeout after effect | response loss after commit | idempotency/lookup | exactly one effect | unknown outcome reconciles |
| queue duplicate | duplicate owned event | deduplication | one business transition | offset/state becomes terminal |
| consumer outage | stop isolated consumer | durable backlog | accepted work remains recoverable | backlog drains within target |
| process restart | terminate test instance | restart/readiness | committed state preserved | service and jobs resume within RTO |

For each row specify whether the fault is injected at client, proxy, dependency stub, process,
or infrastructure layer. Verify the injection actually occurred; a tool command succeeding
does not prove the target experienced the intended failure.

## 3. Execute safely

1. pass smoke and establish a valid steady-state measurement;
2. verify namespace, blast radius, monitoring, kill switch, and rollback;
3. inject at the lowest useful magnitude;
4. observe user behavior, protections, data, queues, retries, and dependencies;
5. abort at threshold;
6. remove the fault and observe recovery;
7. reconcile authoritative/downstream state and cleanup;
8. repeat only after isolation is verified.

Assert graceful error, bounded retry/backoff/jitter, circuit behavior, no amplification, no
duplicate/forbidden effect, observability, RTO/RPO, backlog drain, and final invariant.

Production experiments require separate change/incident authority, canary scope, operator,
kill switch, exact blast radius, and tested rollback.

### Abort and resume

Abort immediately on:

- data loss/corruption or authorization/privacy failure;
- blast radius beyond the test namespace/canary;
- unexpected customer/provider effect;
- retry/load amplification beyond ceiling;
- missing telemetry or failed kill switch;
- recovery/cleanup becoming unsafe.

After abort, remove the fault, stop dependent load, preserve timestamps/state, run the
approved rollback or recovery, reconcile authoritative/downstream data, and report. Do not
resume until the target is requalified, the abort cause is understood, and new explicit
approval is obtained when scope/limits change.

## 4. Metrics and interpretation

Use business and system measures:

- RTO = time from failure start to restored declared service state;
- RPO = maximum accepted data-loss point or observed loss against target;
- detection time = failure start to alert/detection;
- recovery time = fault removal or recovery trigger to steady-state restoration;
- convergence time = accepted operation to correct final distributed state;
- backlog drain time/rate;
- duplicate, lost, orphan, and unreconciled business-effect counts;
- error/latency/throughput during degraded and recovery windows;
- retry amplification = downstream attempts / original business operations.

State measurement boundaries, clocks, windows, and thresholds. A fast technical restart does
not satisfy recovery when backlog, data, or user-visible state remains wrong.

## 5. Evidence, severity, and exit

Evidence includes build/target, experiment/hypothesis, fault tool/config/version, steady
baseline, timestamps, blast radius, monitoring queries, actual degradation, abort, recovery,
RTO/RPO/convergence, reconciliation, and cleanup.

Any data/security invariant failure follows Critical/High stop rules. An uncontrolled,
mis-scoped, or unobserved experiment is `Blocked`; if required for readiness, it makes the
session verdict `Inconclusive` and may itself contaminate the environment.

Pass only when:

- steady state before fault was valid;
- the intended fault occurred within the blast radius;
- degraded behavior matched the oracle;
- no data/security invariant failed;
- recovery met RTO/RPO/convergence;
- backlog/DLQ/compensation/reconciliation reached correct terminal state;
- monitoring detected/explained the event;
- target health and cleanup were restored.

## 6. Worked example

Requirement: accepted checkout must create exactly one paid order even if the payment provider
response is lost; final status must converge within 60 seconds.

1. Steady state: normal checkout succeeds and provider/order metrics agree.
2. Hypothesis: if the provider captures payment but its response is dropped, the application
   records an unknown outcome, retries/queries with the same idempotency key, and creates one
   paid order.
3. Inject response loss only for the owned test payment in the provider sandbox.
4. Abort if any non-test transaction is affected, duplicate capture occurs, or monitoring is
   lost.
5. Observe user message, local transition, provider capture, attempts, idempotency key, events,
   reconciliation, and final state.
6. Remove fault, wait on the explicit convergence condition up to 60 seconds, verify one
   charge/order and empty unresolved queue, then cleanup.
7. Evidence includes proxy rule, transaction/correlation IDs, timelines, state snapshots,
   retry amplification, convergence, and sandbox cleanup.
