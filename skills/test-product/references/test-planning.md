# Test Planning

Read after requirements and risk are stable enough to choose coverage.

## Contents

- Choose the profile
- Define entry and exit criteria
- Select and order tests
- Estimate honestly
- Approval contract

## Choose the profile

### Focused

Use by default. Include applicable requirement review, RTM, baseline/static checks, sanity,
targeted unit/integration/contract checks, positive/negative/boundary paths, and risk-targeted
regression. Add a narrow E2E only when lower layers cannot prove the user outcome.

### Full ride

Recommend for critical business flows, releases, broad changes, weak existing coverage,
distributed version changes, or explicit requests. Add applicable broad regression, approved
E2E/live exploration, compatibility matrices, security, performance/resilience,
accessibility, and isolated user simulations.

Full ride is an applicability decision, not permission to run unsafe tests.

## Define entry criteria

Examples:

- approved acceptance criteria and RTM;
- identified build/commit and component versions;
- approved environment and credentials;
- deployed dependencies healthy;
- test data seeded and cleanup tested;
- monitoring available for load/resilience work;
- smoke suite passing;
- external effects and limits approved.

If an entry criterion fails, mark affected work `Blocked`; do not silently substitute a
weaker environment.

## Define exit criteria

Tie exit to risk:

- every critical requirement has a non-empty RTM result and evidence;
- zero open Critical/High defects for a ready verdict;
- required suites and user journeys pass;
- contract/version combinations meet the approved compatibility policy;
- security/performance thresholds meet named requirements;
- no unexplained flaky results;
- residual risks are explicit and accepted by the proper stakeholder.

Do not use a percentage alone. Ninety-nine percent passing is not enough when the missing one
percent is cross-tenant authorization.

## Select and order tests

For each type, state:

`requirement/risk → applicability → technique → layer → environment → cost → approval →
evidence`

Order for fast feedback:

1. requirement/static review;
2. focused unit/component;
3. integration/contract/API;
4. environment smoke;
5. feature/flow sanity;
6. targeted then full regression;
7. E2E/live;
8. applicable security/performance/resilience;
9. stakeholder UAT support.

Parallelize only independent tests with isolated data.

## Estimate honestly

Use repository evidence and include setup, data, execution, investigation, reruns, evidence,
and reporting. When uncertainty matters, use three-point estimation:

`estimate = (optimistic + 4 × most likely + pessimistic) / 6`

Show both Focused and Full ride with:

- wall-clock range;
- tools/environments/people;
- token and subagent cost;
- main confidence gained;
- deferred risks.

Explain the technique in one sentence; do not teach project management theory.

## Approval contract

Obtain explicit approval for:

- profile and test plan;
- files to create or modify;
- live/E2E target and accounts;
- production-safe actions;
- external calls and data mutations;
- load/concurrency ceilings;
- active security testing;
- subagent/user simulations;
- cleanup and rollback.

Silence is not approval for an external effect.
