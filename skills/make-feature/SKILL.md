---
name: make-feature
description: Build an approved feature end to end without breaking the existing product.
disable-model-invocation: true
---

# Make Feature

Build features through an explicit, evidence-based workflow:

`Classify -> Discover -> Clarify -> Propose -> Approve -> Implement -> Verify -> Report`

Keep the work transparent. Explain material findings, decisions, conflicts, and deviations to the user as they arise. Do not implement before the approval gate.

## Non-negotiable rules

- Understand the user's actual goal and the feature's business fit before designing the code.
- Inspect the project instead of guessing its architecture, conventions, commands, or source of truth.
- Preserve existing behavior unless the user explicitly approves a change.
- Preserve unrelated working-tree changes. Never overwrite or clean up user work outside the approved scope.
- Use the smallest coherent implementation. Avoid speculative abstractions, columns, metadata, identifiers, indexes, dependencies, and infrastructure.
- Recommend useful future-proofing when evidence supports it, but implement it only after approval.
- Ask the user before changing an approved data source, placement, contract, schema, dependency strategy, or test plan.
- Never claim a check passed unless it was run successfully. Distinguish pre-existing failures from regressions.
- Never hide uncertainty behind confident language. Report only concrete conflicts and risks supported by evidence.

Credentials and secrets may be requested and provided directly in the chat when required. Never write them into source code, committed files, commits, commit messages, logs, test output, documentation, or reports. Never echo a secret back to the user. Keep it only in the project's approved credential mechanism and prevent commands or tools from printing it.

## 0. Classify the feature

Classify the request before broad discovery:

- **Light**: local and reversible; no meaningful change to business flow, database schema, public contract, authorization, external integration, or infrastructure.
- **Medium**: crosses modules or changes an API, data flow, dependency, migration, background task, or established business behavior.
- **Heavy**: affects a critical business flow, authentication, authorization, payments, destructive data work, infrastructure, multiple services, concurrency-sensitive behavior, or external systems.

Tell the user the classification and the concrete reasons for it. Treat it as provisional. Stop and reclassify if discovery reveals a larger impact.

For a light feature, compress the communication and inspect only the relevant project surface. Still complete discovery, clarification, proposal, explicit approval, implementation, and verification. Do not skip a gate merely because the change looks easy.

Complete this step when the impact class and discovery depth are justified by known facts.

## 1. Discover the project in three passes

Inspect before asking questions whose answers are available in the repository.

### Pass 1: Map

- Read every applicable `AGENTS.md`, project instruction, and relevant documentation file.
- Inspect the repository status and existing diff before editing.
- Map the relevant packages, modules, entry points, configuration, dependency manifests, lockfiles, database layer, migrations, test layout, and build or deployment tooling.
- Identify the project's formatter, linter, type checker, test commands, and local run path.
- Identify the architecture, naming conventions, error handling, logging, and sync/async execution model.

### Pass 2: Trace

- Trace the current business flow from its entry point through validation, permissions, domain logic, persistence, integrations, side effects, and user-visible output.
- Locate analogous features and established implementation patterns.
- Identify the proposed feature's exact insertion point and every likely file to modify or create.
- Trace each required datum to its current source of truth and destination.
- Check public contracts, database constraints, migrations, jobs, caches, events, authorization, observability, and external integrations that may be affected.
- Locate relevant unit, integration, contract, regression, and end-to-end coverage.

### Pass 3: Verify

- Re-check the proposed flow against code, tests, documentation, and project instructions.
- Search for indirect callers, duplicated business rules, compatibility constraints, deprecated APIs, and failure paths missed in the first trace.
- Compare documentation and `AGENTS.md` with actual behavior. Do not automatically assume either the code or documentation is correct when they disagree; show the conflict and ask which behavior is intended.
- Revisit the likely file list and confirm that it accounts for the full flow without unrelated scope.

Complete discovery only when you can explain the current business behavior, full data flow, precise integration point, affected surfaces, relevant conventions, known conflicts, and verification commands.

## 2. Clarify the outcome

Ask focused questions until the feature is unambiguous. Recommend technical choices with evidence; ask the user to decide product intent, business rules, and genuine trade-offs. Do not offload repository research to the user.

Establish all of the following:

- the user or system that needs the feature;
- the problem and business outcome;
- current behavior and desired behavior;
- observable acceptance criteria;
- explicit non-goals;
- authoritative data sources and destinations;
- inputs, outputs, actions, permissions, and side effects;
- edge cases, failure behavior, retries, and partial-success behavior where relevant;
- compatibility, performance, privacy, security, rollout, migration, and rollback constraints where relevant.

Keep asking when an answer changes the business flow, source of truth, placement, public behavior, or acceptance criteria. Bundle related questions into small, readable groups.

Complete clarification only when you can state the feature in one precise sentence and every acceptance criterion can be tested.

## 3. Propose an implementation contract

Present a concise contract before writing code:

1. Restate the goal, user-visible behavior, acceptance criteria, and non-goals.
2. Explain why the feature belongs in the identified business flow and architecture location.
3. List each input, action, data source, transformation, destination, output, and side effect. Ask the user to confirm that every source and placement is correct.
4. List every file expected to be modified or created and the purpose of each change.
5. Describe the implementation, interfaces, error behavior, compatibility strategy, and migration or rollout when applicable.
6. List alternatives and real trade-offs. Make a direct recommendation.
7. Propose the exact unit, integration, contract, regression, and end-to-end coverage appropriate to the project. Ask the user to approve the test strategy.
8. Explain how to run the feature locally or in an approved server environment. Identify required credentials, test data, external effects, cleanup, and rollback.
9. List concrete conflicts or open decisions. Do not invent risks for completeness.

### Prefer async

Attempt an asynchronous implementation first. Use synchronous code only when the surrounding project or execution path is synchronous, async would add disproportionate complexity or defects, or async provides no practical benefit. Explain the concrete reason and warn the user before proceeding synchronously.

Do not introduce isolated async code that cannot be used correctly by the surrounding execution model. Preserve cancellation, timeout, resource-lifetime, and error-propagation behavior where relevant.

### Prefer current dependencies and APIs

- Inspect current official documentation, stable releases, recommended methods, project compatibility, lockfiles, and deprecated usage.
- Compare credible alternatives before choosing a new package or API.
- Prefer current stable packages and recommended APIs when they are compatible and useful.
- Propose upgrades to relevant packages, describe the expected compatibility impact, and ask for approval before changing dependencies or lockfiles.
- Retain the existing version when an upgrade conflicts with project constraints, depends on deprecated project usage that cannot safely change in scope, or creates more risk than value. Explain the evidence.
- Never promise that an upgrade is safe before build and test evidence confirms it.

### Propose justified future-proofing

When a refactor, index, dependency, column, metadata field, idempotency mechanism, abstraction, or infrastructure change would materially help scale or likely future work, present it separately:

1. Name the concrete current or future problem.
2. Explain why the minimal feature implementation does not solve it.
3. State the implementation and maintenance cost.
4. Recommend doing it now or deferring it.

Do not implement the proposal without explicit approval.

Wait for explicit approval of the implementation contract. Treat silence or an unrelated response as no approval.

Complete this step only when the user has approved the contract and resolved every blocking choice.

## 4. Implement the approved contract

- Follow the existing architecture, module boundaries, naming, error handling, style, formatter, linter, type rules, and framework conventions.
- Keep code simple, readable, and direct. Apply the project's language philosophy; for Python, favor clarity, explicitness, and established Python idioms.
- Separate responsibilities according to the project's existing structure. Do not place the entire feature in one file when the architecture separates transport, domain logic, persistence, and presentation.
- Implement only the approved behavior and justified safeguards. Avoid overengineering disguised as safety or future-proofing.
- Avoid unrelated refactors, formatting churn, dependency upgrades, or opportunistic fixes.
- Keep the user informed of material progress and nuances without flooding them with routine coding details.

Stop implementation immediately when new information materially changes any of the following:

- business behavior, acceptance criteria, or scope;
- source of truth, data ownership, or feature placement;
- public API, schema, migration, permissions, privacy, or security;
- affected services or major files;
- dependency or async strategy;
- need for a refactor, index, metadata, infrastructure, or additional persistent state;
- approved test, E2E, rollout, or rollback plan;
- an unresolved conflict between code, tests, documentation, and intended behavior.

Explain the finding, its impact, alternatives, and recommendation. Ask for a decision and wait. Continue independently on minor implementation details that remain within the approved contract.

Complete implementation only when the code matches every approved acceptance criterion and no unapproved material deviation remains.

## 5. Maintain durable project knowledge

When implementation reveals a fact that would materially help future features or fixes, propose a documentation update. Add it only after approval.

- Put short, durable agent instructions in the applicable `AGENTS.md`.
- Put detailed architecture, business flows, operational procedures, or contracts in the appropriate existing documentation.
- Link from `AGENTS.md` to detailed documentation when agents need that reference to enter the project quickly.
- Reconcile stale instructions with confirmed project behavior.
- Do not add temporary implementation notes, obvious facts, duplicated guidance, speculation, or secrets.

Complete this step when durable discoveries are either documented consistently or explicitly declined by the user.

## 6. Verify from baseline to live behavior

Establish the relevant baseline before changes when practical. After implementation, use the project's real commands and run every applicable layer:

- formatter and formatting check;
- linter and static analysis;
- type checker;
- build or compilation;
- focused unit tests;
- integration and contract tests;
- migration validation;
- relevant regression suite;
- end-to-end testing.

Test success paths, meaningful edge cases, permission boundaries, failure behavior, and compatibility with the existing business flow. Attribute failures to the new change or the baseline using evidence.

### Live end-to-end testing

Ask how to run the project locally or on a server, which environment is approved, and which credentials are required. Before testing, state:

- the environment and target;
- the user journey and assertions;
- test data to create or modify;
- external calls and side effects;
- cleanup or rollback steps.

Request missing credentials directly when needed. Accept them in chat, but keep them out of code, files, commits, shell history where avoidable, command output, logs, screenshots, test output, documentation, and reports. Redact accidental exposure immediately. Never use production or cause material external effects without explicit authorization.

If an applicable check cannot run, state the exact command or action attempted, the factual blocker, and what remains unverified. Do not silently substitute a weaker check.

Complete verification only when all applicable checks pass, or when a non-code business decision or external blocker has been presented to and resolved by the user.

## 7. Review and report

Review the final diff against the approved contract. Remove debug code, dead code, accidental churn, unused dependencies, and unjustified complexity. Confirm that no secret is present in tracked files, diffs, commits, logs, documentation, or reports. Re-run checks affected by cleanup.

Classify only evidence-backed remaining risks:

- **Ignorable**: a concrete limitation with negligible current impact that can safely remain.
- **Medium**: requires a user decision or more work before normal completion.
- **Critical**: blocks safe completion or release.

Resolve every code-caused medium or critical risk before declaring completion. Leave a medium or critical item open only when it depends on a business decision or external authority, and stop for that decision. If no risk was found, say so and cite the checks supporting that conclusion.

Report concisely with:

1. A numbered list of what was implemented.
2. A separate numbered list of every changed or created file and its purpose.
3. The exact checks and end-to-end scenarios run, with results.
4. A short explanation of why the feature fits the business flow and existing architecture without known conflict.
5. Known limitations and only factual residual risks, classified as Ignorable, Medium, or Critical.

Never say the feature cannot conflict. Say that no known conflict was found only when discovery, diff review, and verification support it.
