# Performance and Scalability Testing

Read when a named SLO, latency/resource/capacity risk, hot path, data growth, concurrency, or
release regression is material. No workload model and no measurable threshold means no valid
performance pass/fail claim.

## 1. Define the model

For every operation/journey record:

```text
Business operation and traffic mix
Environment/topology/dependency/data volume
Open arrival rate or closed concurrency
Normal, peak, and forecast level
Think time/pacing/session behavior
Warmup, ramp, steady, cooldown duration
Latency percentiles and thresholds
Throughput/completion target
Error/timeout/retry target
Resource/saturation/queue limits
Observation window/exclusions
Recovery and reconciliation target
```

Use an **open model** when arrivals must remain independent of response time, such as requests
per second. Use a **closed model** for a fixed population that waits for iterations, such as
interactive concurrent users. A closed model can hide overload by reducing arrivals as
responses slow—coordinated omission.

Derive load from production telemetry/business forecast. If unavailable, document assumptions
and call the result characterization, not production capacity.

## 2. Select the test type

| Type | Answers | Completion |
|---|---|---|
| Baseline | what is repeatable current behavior? | stable reference distribution |
| Load | does normal/peak meet SLO? | threshold at target model |
| Stress | where does degradation begin? | breakpoint, protection, integrity, recovery |
| Spike | can sudden arrivals be absorbed? | peak/backlog/recovery behavior |
| Soak | does sustained work leak/degrade? | stable long-window metrics and cleanup |
| Volume | does target data/cardinality work? | operations at target dataset |
| Scalability | how does capacity change with resources? | capacity/efficiency curve and bottleneck |

Run only types tied to a named risk. Stress/spike/soak/scalability need dedicated monitoring,
limits, and environment authority.

## 3. Prepare and calibrate

1. verify build, topology, dependencies, configuration, and data fidelity;
2. account for scheduled/background work;
3. verify clocks and client/server telemetry;
4. ensure the generator/network is not the limiting resource;
5. seed unique data and cleanup;
6. run single-user functional validation;
7. calibrate low load and reconcile client/server counts/latency;
8. set automated/manual abort thresholds and approved ceiling.

Tag operations and separate setup/auth from the measured action. Do not generate expensive
test data inside the timed path unless users do.

## 4. Execute valid runs

Phases:

1. **warmup:** cache/JIT/connection state meets a declared stable condition;
2. **ramp:** load increases smoothly unless spike is the subject;
3. **steady:** hold target long enough for sample and system dynamics;
4. **cooldown:** stop arrivals and observe drain/recovery;
5. **reconcile:** verify data integrity, backlog, external effects, cleanup.

Repeat baseline and candidate enough to understand variance; three valid repetitions is a
practical default when cost permits, not a guarantee. Keep workload, data class, config,
topology, and window equal.

Invalidate a run—with recorded reason—for generator saturation, telemetry gap, unrelated
deployment, data collision, failed setup, clock error, or changed/aborted workload. Preserve
invalid-run evidence and never cherry-pick only the fastest run.

## 5. Analyze and decide

Report:

- p50/p95/p99 latency and max when useful;
- arrival/completed throughput, backlog/dropped iterations;
- functional error/timeout/retry rate;
- CPU, memory/GC, disk/network, pools/connections/threads;
- queue depth/age, database waits/locks, cache hit, downstream latency;
- autoscaling and recovery time.

SLO passes only when every declared threshold holds for the declared steady window and
functional correctness/data integrity also pass.

For regression without absolute SLO, predeclare:

`relative change = (candidate - baseline) / baseline`

and an allowed tolerance greater than ordinary measured variance. Compare like-for-like and
show every repetition. A noisy comparison row is `Blocked` by insufficient precision; if the
comparison is required, the session verdict is `Inconclusive` until validated.

Stress succeeds only when degradation onset, error/protection behavior, integrity, and
recovery are understood. A maximum user count alone is not a result.

## 6. Safety, evidence, and exit

Abort on approved error/latency/resource threshold, unexpected customer/provider effect, data
inconsistency, runaway backlog, generator failure, or missing monitoring. Stop arrivals,
preserve state, cool down, reconcile/cleanup, and report.

Evidence includes exact build/environment, workload/config/tool version, data, phase
timestamps, thresholds, raw sanitized metrics, dashboard/query definitions, generator
health, repetitions, stop/cleanup, and final state.

Performance scope passes when runs are valid and repeatable, thresholds hold, the generator is
not limiting, system/dependency telemetry explains behavior, correctness is preserved,
recovery completes, and assumptions/variance are disclosed.

Research basis: Grafana k6 official open/closed models and thresholds, plus ISTQB performance
guidance:
<https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/>,
<https://grafana.com/docs/k6/latest/using-k6/thresholds/>, and
<https://www.istqb.org/wp-content/uploads/2024/11/ISTQB-CTAL-TTA_Syllabus_v4.0.pdf>.
