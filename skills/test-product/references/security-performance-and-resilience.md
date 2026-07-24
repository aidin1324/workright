# Security, Performance, and Resilience

Apply only the sections justified by risk. Explain why a section is selected or skipped.

## Security

Activate for authentication, authorization, sensitive data, payments, uploads, public input or
APIs, external providers, privileged actions, or a release gate.

Map assets, actors, trust boundaries, entry points, data flows, and abuse cases. Cover as
applicable:

- authentication, session/token lifetime, logout, replay, and account enumeration;
- function/object/tenant-level authorization and privilege changes;
- validation, injection, unsafe deserialization, and file handling;
- secrets, personal data, transport/storage exposure, caching, logs, and errors;
- dependency/supply-chain and deployment/configuration risk;
- rate limits, automation abuse, business-logic abuse, and resource exhaustion;
- auditability without leaking sensitive data.

Use OWASP ASVS for verifiable web-application requirements and WSTG for execution guidance:

- <https://owasp.org/www-project-application-security-verification-standard/>
- <https://owasp.org/www-project-web-security-testing-guide/latest/>

Static scanners are inputs, not proof. Validate material findings safely. Active exploitation,
destructive payloads, denial of service, real data access, or production attacks require
separate explicit authorization.

## Performance selection

Do not run performance tests without a workload model and measurable oracle.

| Type | Question |
|---|---|
| Baseline | What are current latency, throughput, errors, and resources? |
| Load | Does the system meet thresholds at normal and expected peak load? |
| Stress | Where does graceful degradation begin, and does the system recover? |
| Spike | Can it absorb and recover from a sudden peak? |
| Endurance/soak | Does sustained operation leak or degrade? |
| Scalability | Does capacity scale up/down while meeting service objectives? |
| Recovery/failover | What happens when process/node/dependency fails and returns? |

Require:

- representative environment and data;
- traffic shape, concurrency, arrival rate, duration, and warmup;
- p50/p95/p99 latency, throughput, error rate, CPU, memory, I/O, queue depth, and saturation
  as applicable;
- approved load ceiling and stop conditions;
- monitoring and correlation IDs;
- cooldown and recovery observation;
- baseline comparison with uncertainty stated.

Stress is successful only when degradation, error behavior, data integrity, and recovery are
understood. A crash threshold alone is incomplete.

## Resilience scenarios

Use controlled fault injection only with approval. Consider:

- dependency timeout, slow response, malformed response, or outage;
- exhausted connection/thread pools;
- retry storms and circuit-breaker behavior;
- process restart, leader change, or network partition;
- duplicate/reordered events;
- storage pressure;
- recovery, reconciliation, and data consistency.

Never perform load or fault injection against production by default. Stop immediately when
approved safety thresholds or data-integrity limits are crossed.

ISTQB performance guidance emphasizes representative environments, explicit thresholds,
early bottleneck discovery, graceful degradation, and recovery:
<https://www.istqb.org/wp-content/uploads/2024/11/ISTQB-CTAL-TTA_Syllabus_v4.0.pdf>.
