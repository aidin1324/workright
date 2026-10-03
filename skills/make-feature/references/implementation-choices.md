# Implementation Choices

Read when selecting an execution model, dependency/API, or optional future-proofing.
These decisions remain within the approved contract.

## Execution model

Attempt async first. Use synchronous code when the surrounding path is synchronous,
async adds disproportionate complexity/defects, or it has no practical benefit. Explain
why before proceeding; an already approved strategy remains approved.

Preserve cancellation, timeout, resource lifetime, and error propagation where relevant.
Do not introduce an isolated async path its callers cannot use correctly.

## Dependencies and APIs

Before selecting a package/API or proposing a relevant upgrade:

- check current official docs, stable releases, recommended methods, deprecations,
  compatibility, manifests, and lockfiles;
- compare credible alternatives and recommend the smallest compatible option;
- describe compatibility impact and obtain approval for dependency/lockfile changes;
- retain current versions when constraints or out-of-scope changes make an upgrade
  riskier than its demonstrated value;
- establish safety through build/test evidence, not a release label.

An ordinary fix using an unchanged supported dependency needs no new upgrade proposal.

## Future-proofing

For a proposed refactor, index, column, metadata, idempotency mechanism, abstraction, or
infrastructure addition, state the evidenced problem, why the minimal feature cannot solve
it, implementation/maintenance cost, and recommendation to include or defer it.

Keep optional proposals separate; implement only after explicit approval. Similar names
or a possible future use are insufficient grounds for new persistent state.
