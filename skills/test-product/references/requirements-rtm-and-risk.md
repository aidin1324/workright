# Requirements, RTM, and Risk

Read this reference for every invocation.

## Put the user goal first

Write one testable sentence:

`For <user>, <scope> must achieve <observable outcome> under <material conditions>.`

Separate:

- business outcome: why the behavior exists;
- user-visible behavior: what can be observed;
- implementation: how the repository currently attempts it.

Do not use implementation as the oracle when requirements are unclear.

## Inspect requirement sources

Search tickets, specifications, user stories, API/schema documents, designs, tests,
documentation, release notes, feature flags, migrations, and current behavior. Record each
source. When sources conflict, show the conflict and ask which behavior is authoritative.

Stop when missing intent affects expected behavior, permissions, source of truth, external
effects, or acceptance.

## Make acceptance criteria measurable

Prefer one of these shapes:

- scenario: `Given <state>, when <action>, then <observable result>`;
- rule: input/state/role → outcome/error/side effect;
- threshold: metric, unit, percentile, load, observation window, maximum/minimum;
- invariant: property that must remain true across many inputs or transitions.

Replace vague wording:

| Vague | Make testable |
|---|---|
| easy | target users complete named task without defined failure/friction |
| fast | percentile latency under stated workload and environment |
| secure | named threat/control and expected denial/audit behavior |
| synchronized | named systems reach the same business state within a defined window |
| compatible | old/new consumer-provider combinations and allowed schema changes |

Define non-goals to prevent accidental scope expansion.

## Apply Shift Left

Before implementation, detect:

- missing actors, roles, states, and permissions;
- undefined failure, retry, cancellation, timeout, or partial success;
- missing data ownership and retention rules;
- contradictory business rules;
- behavior that cannot be observed or measured;
- rollout, migration, compatibility, and rollback gaps;
- security, privacy, accessibility, and operability omissions.

Produce acceptance criteria, risks, RTM, test plan, and proposed test data. Mark runtime
execution `Not run — implementation absent`.

## Score risk

Use a simple, explained scale unless the project has one:

- likelihood: 1 rare → 5 expected;
- impact: 1 negligible → 5 catastrophic;
- exposure = likelihood × impact.

Raise priority independently for critical business flows, sensitive data, authorization,
payments, irreversible effects, compliance, concurrency, migrations, or distributed version
drift. Reassess when testing finds new information.

Risk determines technique, level, depth, order, and exit criteria. It does not excuse an
uncovered requirement.

## Build the RTM

Assign stable IDs such as `REQ-001` and test IDs such as `TC-UNIT-001`.

Required columns:

| Requirement ID | Source | Requirement / acceptance criterion | User value | Risk | Test level | Technique | Test case IDs | Environment | Result | Evidence | Defect IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|

Rules:

- one row may reference several tests; every test references at least one requirement/risk;
- record positive, negative, boundary, permission, and failure coverage where material;
- use `Passed`, `Failed`, `Blocked`, `Not run`, or `Not applicable`;
- explain every skipped, blocked, or not-applicable item;
- update results and evidence during execution;
- leave no final result blank;
- link external test-management IDs instead of duplicating authoritative cases.

The current ISTQB Foundation syllabus treats traceability and risk-based testing as core test
management practices: <https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf>.
