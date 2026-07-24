# Environment, Data, and Live Testing

Read before creating or using a runtime environment.

## Select the target

Prefer in order:

1. existing isolated test harness;
2. dedicated local/container environment;
3. staging/test server close to production;
4. production only for explicitly approved safe observations/actions.

State which production characteristics are mirrored and which are not. Do not infer production
performance, compatibility, or resilience from an unrepresentative environment.

## Preflight

Record:

- repository commit/build and every component version;
- URLs, regions, feature flags, schemas, and configuration;
- accounts/roles and credential source without printing secrets;
- test data, mutations, external calls, notifications, payments, and quotas;
- monitoring, logs, evidence path, cleanup, and rollback;
- concurrency/load/security limits;
- approved actions and forbidden actions.

Provision predictably using existing Docker/IaC/project scripts when available. Do not invent
new infrastructure before inspecting project conventions.

## Test data

- use sanitized production-like shape, not real personal data;
- create unique session-owned records;
- include valid, invalid, boundary, historical, and conflicting states as required;
- keep clocks, random seeds, locales, and time zones controllable;
- clean up even after failure;
- verify cleanup rather than assuming it;
- never put secrets or sensitive payloads in tracked fixtures, logs, screenshots, or traces.

## Smoke gate

After deployment/provisioning, verify service health, dependency reachability, schema/migration
state, basic authentication, one critical read/write flow, observability, and cleanup. A failed
smoke makes dependent results untrustworthy; report `Blocked`.

## Live testing

Obtain approval for target, journey, roles, data, side effects, browser/device/version matrix,
and cleanup. Test:

- main user goals;
- critical edge/failure paths;
- permission boundaries;
- supported routes and entry points;
- interruption, refresh, retry, timeout, and duplicate actions;
- supported browsers/devices/locales based on actual users;
- cross-service state and asynchronous completion.

Collect screenshots, traces, console/network logs, API evidence, and resulting state on failure.
Redact credentials, tokens, personal data, and internal secrets.

## Full ride simulations

Use only after explicit approval. Give each isolated agent/persona one bounded charter and clean
state:

- new user;
- experienced user;
- restricted-role user;
- invalid/hostile-input user;
- slow/interrupted-network user;
- accessibility-oriented user;
- concurrent user when concurrency is material.

Require observations, steps, expected/actual behavior, and evidence. Agents never repair code
or share mutable test state. Prefer staging. If Computer Use is necessary, recommend local or
staging where side effects and credentials are controllable.

## Cleanup and archive

Remove session data and temporary resources; verify removal. Keep reusable scripts, sanitized
datasets, configuration, RTM, and report snapshots. Store large raw evidence in the project's
ignored test-results/artifact location and link it from documentation.
