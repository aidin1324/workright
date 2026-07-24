# Test Design Techniques

Choose techniques from the requirement shape. Combine techniques when they cover distinct
risks; do not generate cases mechanically.

| Technique | Use when | Design rule | Evidence |
|---|---|---|---|
| Equivalence partitioning | Inputs form behaviorally equivalent groups | Test each valid/invalid partition, not every value | Partition map and representative cases |
| Boundary value analysis | Limits, ranges, sizes, dates, pagination | Test boundary and immediate neighbors; add far invalid values when behavior differs | Values and expected outcomes |
| Decision tables | Conditions/roles/flags combine into rules | Model conditions and actions; cover each feasible high-risk rule | Table columns linked to cases |
| State transitions | Status/lifecycle/retry/payment workflow | Cover valid transitions, forbidden transitions, guards, repeated events, recovery | State model and event sequences |
| Use-case scenarios | End-user or business journey | Assert the goal and side effects through public interfaces | Journey, assertions, evidence |
| Positive/negative | Any material behavior | Pair successful use with invalid input/action and safe rejection | Expected success and denial |
| Error guessing | Project has known failure patterns | Add experience-based cases after systematic design | Named heuristic and finding |
| Exploratory | Unknown risk, UI, new workflow | Use a time-boxed charter, notes, evidence, and debrief | Charter and observations |
| Checklist-based | Repeated standard/control | Version the checklist; require evidence, not just a check mark | Version and evidence link |
| Pairwise/combinatorial | Many roles/browsers/flags/configs | Cover interactions economically; always add critical combinations explicitly | Combination matrix |
| Property/invariant | Parsers, transforms, calculations, domain laws | Generate inputs and assert an invariant, round trip, monotonicity, or conservation rule | Seed, property, minimized failure |
| Fuzz | Parsers, uploads, APIs, hostile inputs | Bound time/resources; preserve seed and minimized reproducer | Corpus/seed and crash/error |
| Mutation | Critical logic has superficially high coverage | Introduce controlled mutations and require tests to kill meaningful changes | Mutation score and survivors |

## Technique selection examples

- numeric minimum/maximum → equivalence partitions + boundaries;
- role × account state × feature flag → decision table, then pairwise for lower-risk variants;
- order/payment lifecycle → state transitions + idempotency scenarios;
- import parser → partitions + boundaries + property/fuzz;
- checkout goal → use-case/E2E for wiring, lower-level cases for rules and errors;
- unfamiliar interface → scripted acceptance cases + exploratory charter.

## Case quality

Each case records requirement IDs, risk, technique, preconditions, owned data, action,
expected observable result, cleanup, evidence, and actual result.

Keep cases:

- independent and runnable in any order;
- deterministic unless explicitly testing nondeterminism;
- focused on one behavior/risk;
- clear enough to diagnose a failure;
- free from real personal data and secrets;
- resistant to implementation-only changes.

Avoid:

- cases derived only from current code;
- one giant scenario with many unrelated assertions;
- random inputs without seeds or reproducibility;
- redundant upper-layer coverage;
- mocks that merely confirm their own setup;
- snapshots without a reviewed oracle.

The ISTQB CTFL syllabus defines equivalence partitioning, boundary value analysis, decision
tables, state transitions, white-box, exploratory, error-guessing, and checklist-based
techniques: <https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf>.
