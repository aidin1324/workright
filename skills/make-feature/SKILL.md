---
name: make-feature
description: Build an approved feature end to end without breaking the existing product.
---

# Make Feature

Deliver the approved outcome with evidence for every acceptance criterion.

`Classify → Discover → Clarify → Contract → Implement → Verify → Report`

For discovery, proposal, or review requests, stop at the requested deliverable.
Implementation starts after explicit contract approval. Remote actions follow repository
policy and their applicable authority; local implementation approval does not authorize delivery.

## Contract continuity

At entry, resume, handoff, or workflow change, recover the goal, approved contract, decisions,
authority, unfinished obligations, and next step. Check current repository/environment identity
before reusing earlier evidence. Explicit approval for the same contract counts; slices,
compaction, and QA do not reset it. Ask only for missing decisions or material changes.
Silence is not approval. Keep authority scoped to action, target, effects, and limits.

At material milestones, update a compact checkpoint: contract revision, decisions/authority
with sources, code/environment revision, criterion results, pending work, next action.
Use existing records or chat; persistent files require a user request or project requirement.

## Boundaries

- Preserve unrelated user changes and behavior outside the approved scope.
- Use the smallest coherent implementation; defer speculative abstractions and infrastructure.
- Inspect architecture, commands, and sources of truth before proposing changes.
- Claim checks passed only from successful runs; separate baseline failures from regressions
  and observed facts from hypotheses.
- Request missing credentials directly when needed. Keep values in the approved credential
  mechanism; never echo or persist them in code, commits, shell history, output, evidence, or reports.

## 0. Classify

| Impact | Discovery depth |
|---|---|
| Light | Local, reversible; no material business-flow, schema, public-contract, authorization, integration, or infrastructure change. Inspect affected surface. |
| Medium | Cross-module behavior, API/data flow, dependency, migration, or background task. Trace callers and consumers. |
| Heavy | Critical flow, auth, payments, destructive data work, infrastructure, multiple services, concurrency, or external systems. Trace failure, rollout, and recovery. |

State the class and factual reason briefly. Reclassify when exposure changes and record why.
Light work reduces research/communication depth while retaining contract and verification gates.

**Exit:** impact and discovery depth are justified by known facts.

## 1. Discover

Complete three passes over the relevant surface:

1. **Map:** read applicable `AGENTS.md` and project contracts; inspect status/diff, modules,
   configuration, manifests/lockfiles, persistence/migrations, tests, CI and deployment tooling.
   Identify actual format, lint, type, build, test/run commands and the sync/async model.
2. **Trace:** follow entry → validation/permissions → domain logic → persistence/integrations →
   effects → consumer/user output. Locate analogous implementations, insertion point,
   expected files, sources/destinations, compatibility constraints, and relevant coverage.
3. **Verify:** check indirect callers, shared rules, failure paths, and the file list against
   code, tests, docs, and instructions. Resolve material conflicts through authoritative
   sources; ask the owner when intended behavior remains unclear.

When identity, deduplication, lifecycle, or similar objects affect the change, identify the
business object, owner, key, lifecycle, and consumer. Check a nearby counterexample before
proposing a new identifier, field, or abstraction.

**Exit:** current behavior, complete affected flow, insertion point, sources, consumers,
conventions, conflicts, and verification commands are known; unresolved scope is explicit.

## 2. Clarify

State: `For <actor>, <scope> must achieve <observable outcome> under <conditions>, without
<forbidden effects>.`

Establish current/desired behavior, testable criteria, non-goals, ownership, inputs/outputs,
permissions, effects, and material failure/retry/partial-success behavior. Include compatibility,
performance, privacy/security, migration, rollout, and rollback constraints where applicable.

Reuse answers from the request, approved spec, handoff, or repository. Ask focused questions
only for decisions that change the contract; recommend technical choices from evidence.

**Exit:** one precise feature statement; every criterion has an observable oracle.

## 3. Contract

Present one concise contract:

1. Goal, behavior, criteria, non-goals, and requested completion milestone.
2. Business owner, architectural placement, and input → source → transformation → destination/
   consumer → output/effects, with evidence for sources and placement.
3. Expected changed/created files and purpose; interfaces, failures, compatibility, and
   applicable migration/rollout/rollback.
4. Material alternatives, recommendation, conflicts, and open decisions.
5. Exact checks/scenarios, criteria/evidence, baseline, and required project gates.
6. Run target, owned data, credentials by identifier, effects, limits, and cleanup.

When selecting an execution model, dependency/API, or optional future-proofing, read
[implementation-choices.md](references/implementation-choices.md).

**Exit:** explicit approval covers the contract, sources, placement, and test strategy;
no blocking choice remains. Reuse existing approval.

## 4. Implement

Follow project architecture, boundaries, language idioms, error handling, and tooling.
Implement every approved criterion with justified safeguards. Separate transport, domain,
persistence, and presentation where the project already separates them; exclude unrelated churn.

Continue on details within the contract. Stop affected work when new facts materially change
behavior/scope, source/owner/placement, API/schema/migration, permissions/security/privacy,
services, dependencies/execution model, persistent state, or verification/rollout/rollback.
Explain impact, options, and a recommended amendment; obtain the missing decision.

When another workflow performs QA, hand over criteria, exact build/target, authority, and
evidence. Keep unfinished implementation assigned. Return QA defects to a separate remediation
step under existing authority when it covers the correction; reapprove material deviations.
Retest the original failure on the new build before affected regressions.

**Exit:** code covers every approved criterion without unapproved material deviation.

## 5. Preserve durable knowledge

For discoveries useful to future work, update existing docs if authorized or propose the
update separately. Put short durable instructions in `AGENTS.md` and detailed contracts/flows
in their existing docs, linked where needed. Reconcile confirmed stale guidance; exclude
transient notes, obvious facts, duplicated rules, speculation, and secrets.

**Exit:** material discoveries are documented or visibly pending/deferred in the handoff.

## 6. Verify

Identify the nearest valid pre-change baseline, code, environment, configuration, and attribution
limits. Select applicable format/lint/type/build, unit, integration/contract, migration,
regression, and E2E checks from the changed flow and consumers. Run required project gates on
one final coherent change. After another edit, rerun the original failure and affected checks;
repeat broader checks when new changes, failures, or risks warrant it.

For every criterion record: `criterion → command/scenario → oracle → result → evidence →
code/environment revision → limitation`. Results: `Passed`, `Failed`, `Blocked`, `Not run`.
Mark affected earlier evidence stale after relevant edits; retain independent valid evidence.
A green suite does not cover an absent journey.

Verify material success, boundary/denial, failure, retry, and recovery paths. At integration
boundaries, prove the real adapter/consumer outcome and supported versions when required and
authorized; state what mocks cannot prove. Check required and forbidden effects.

Before live actions, recover the approved plan and inspect repository/owner, host, service/
Compose project, endpoint/port, running SHA/digest/config, owned data, excluded resources,
effects, limits, and cleanup. Verify rollback provenance before a rollout requiring it.
After mutation, verify the target build/behavior and preservation of excluded resources.
Ask only for missing authority/access; production and material external effects require
explicit authorization.

For unavailable checks, report attempted command/action, factual blocker, and unverified criteria.
Bound diagnostic retries by count/deadline; stop on a repeated unchanged blocker.

**Exit:** every criterion and required check has a current result; code-caused failures are
resolved and retested. External blockers and accepted gaps remain explicitly unverified;
risk acceptance never turns a missing or failed check into `Passed`.

## 7. Review and report

Review the diff against every criterion. Remove debug/dead code, accidental churn, unused
dependencies, unjustified complexity, and secret exposure; rerun affected checks. Reconcile
delegated claims against evidence, changed paths, and outstanding obligations.

Classify concrete residual risks: **Ignorable** for negligible current impact; **Medium** for
material unfinished work/decision; **Critical** for unsafe completion/release. Explain the
reachable situation, violated contract, impact, blocked stage, and next action. Resolve
code-caused Medium/Critical items; external decisions remain with their authorized owner.

Report outcome first, then behavior/files with purpose, criterion/check results with exact
commands/revisions, uncovered scope, risks, and next action. Show applicable delivery states
separately: local implementation, verification, MR/CI, deployment/environment, enabled
capabilities, and user acceptance.

Use `complete` only for the named approved milestone whose criteria are satisfied. Partial
or blocked work names uncovered criteria; waived evidence stays unverified. Local verification
does not prove deployment or acceptance. Say “no known conflict found” only within the scope
supported by discovery, diff review, and checks.
