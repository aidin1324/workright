# Contracts and Distributed Systems

Read whenever behavior crosses a process, service, repository, provider, event, schema,
generated client, webhook, callback, or independently deployed version.

## Build the dependency map

Trace:

`user action → caller/consumer → provider/producer → contract/schema → persistence →
event/job → downstream consumer → user-visible final state`

Record owners, repositories, contracts, environments, deployed versions, and rollout order.

Ask when missing:

- Where is each related service: local path, repository URL, contract registry, or test URL?
- May its source/contract be read and may safe verification be run?
- Which versions are deployed together now and during rolling deployment?
- Which component owns the contract and compatibility policy?

Do not claim compatibility or synchronization when one side is unavailable. Mark RTM rows
`Blocked` with the exact missing access and residual risk.

## Locate contracts

Inspect OpenAPI/JSON Schema, Protobuf/gRPC, GraphQL, AsyncAPI/event schemas, Pact or equivalent
consumer contracts, generated SDKs, shared database migrations, webhook docs, topic configs,
and representative sanitized traces.

A schema-valid message can still be semantically wrong. Verify business meaning and side
effects in addition to shape.

## Verify both sides

Check:

- consumer assumptions and actual provider response;
- required/optional fields, types, enums, defaults, nullability, and unknown fields;
- status/error models and retryability;
- authentication, authorization, tenant boundaries, and identity propagation;
- timeouts, cancellation, retries, backoff, duplicate delivery, and idempotency;
- ordering, eventual consistency window, partial failure, and compensation;
- clock/version/locale/serialization differences;
- generated client version against deployed provider;
- old consumer/new provider and new consumer/old provider combinations;
- final state across every service in the business flow.

Consumer-driven contracts should be replayed against the provider; a consumer mock alone does
not verify provider behavior. Pact overview: <https://docs.pact.io/getting_started/how_pact_works>.

## Compatibility policy

Define direction:

- backward: new reader/consumer accepts old data/provider contract;
- forward: old reader/consumer accepts new data/provider contract;
- full: both directions;
- transitive: compare against all supported prior versions, not only the latest.

Test the actual rollout plan. For example, a backward-only event policy may require upgrading
consumers before producers emit the new schema. Confluent reference:
<https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html>.

## Synchronization scenarios

Cover happy path and:

- provider slow/unavailable;
- event delayed, duplicated, reordered, or rejected;
- consumer temporarily old during rolling deployment;
- partial persistence before publication;
- retry after timeout with unknown outcome;
- reconciliation/backfill;
- dead-letter and recovery;
- user reads state before and after convergence.

Evidence includes contract diffs, provider verification, exact version matrix, request/event
IDs, timestamps, state snapshots in each service, and the user-visible final outcome.
