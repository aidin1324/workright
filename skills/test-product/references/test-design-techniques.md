# Test Design Techniques

Use this reference after acceptance criteria and risk are known. A technique is a repeatable
way to build a model, derive cases, measure coverage, and decide when enough cases exist. Do
not merely name a technique in a report.

## Contents

1. Selection algorithm
2. Oracle and case contract
3. Black-box techniques
4. White-box techniques
5. Experience-based techniques
6. Generative and fault-detection techniques
7. Combining and deduplicating
8. Worked example and completion gate

## 1. Selection algorithm

For each atomic criterion:

1. **Model the risk:** list likely failure modes, historical defects, changed code/data, and
   impact.
2. **Choose by shape:** range → partitions/boundaries; rule combinations → decision table;
   lifecycle → state transitions; journey → scenario; combinatorial configuration → pairwise;
   invariant → property testing; hostile parser/input → bounded fuzzing.
3. **Generate a minimum systematic set:** satisfy the declared coverage rule below.
4. **Add risk cases:** critical combinations, past defects, forbidden actions, failure and
   recovery paths even when a combinatorial generator omits them.
5. **Choose the lowest observable layer:** then add only the cross-boundary proof missing
   below.
6. **Deduplicate:** merge cases only when preconditions, action, oracle, layer, and diagnostic
   value remain clear.
7. **Define escalation:** a lower-layer mismatch, integration risk, or unknown behavior may
   trigger a broader test; do not broaden automatically.
8. **Stop:** when all selected model coverage items and named risks have valid cases and
   additional cases add no distinct behavior/risk within the approved scope.

Selection must account for risk, change impact, oracle strength, controllability, cost,
historical defects, architecture boundaries, concurrency, and evidence quality.

## 2. Oracle and case contract

Every case records:

```text
ID / title / criterion and risk IDs
Technique and coverage item
Level and environment/build
Preconditions and owned data
Action or command
Expected output
Required side effects
Forbidden effects
Tolerance or eventual deadline
Cleanup
Minimum pass/fail evidence
Actual result / timestamp / evidence IDs / defect IDs
```

An expected HTTP status alone is rarely a complete oracle. Include durable state, downstream
effects, non-occurrence, authorization, and user-visible outcome where relevant.

## 3. Black-box techniques

### Equivalence partitioning

Use when values, states, roles, or configurations divide into groups expected to behave the
same.

Procedure:

1. Name the input/output/state variable and its domain.
2. Derive non-overlapping, non-empty valid and invalid partitions from requirements.
3. Include special semantic classes, not only data types: known/unknown user, owned/foreign
   tenant, active/suspended account.
4. Select one representative per partition; select more only when internal heterogeneity or
   risk makes the equivalence assumption weak.
5. Map each representative to its expected result and evidence.

Coverage = `partitions exercised / identified applicable partitions`.

Example for quantity `1..99`: valid `1..99`; invalid `<1`; invalid `>99`; invalid non-integer;
missing. Representatives might be 50, 0, 100, 1.5, and absent. Do not call 1 and 99 separate
partitions unless behavior differs.

Common errors: overlapping classes, forgetting invalid/output partitions, deriving from code
instead of requirement, assuming every value in a broad class is equivalent.

### Boundary value analysis

Use for ordered ranges, sizes, dates, pagination, timeouts, thresholds, and capacity limits.

Procedure:

1. State boundaries, inclusivity, units, timezone/rounding, and representable domain.
2. Use **2-value BVA** for ordinary risk: each boundary and nearest value on the other side.
3. Use **3-value BVA** for higher risk or fragile validation: value immediately below, at, and
   immediately above each boundary.
4. Add far-invalid or representation cases only when they exercise different handling.
5. Apply BVA to transition guards and outputs as well as input fields.

For inclusive `1..99`, 3-value candidates are `0,1,2,98,99,100`. For a date range, define
whether “immediately” means date, second, millisecond, or database precision.

Coverage = `required boundary sides/points exercised / identified boundary sides/points`.

Common errors: testing only min/max, ignoring precision/overflow/timezone, multiplying all
boundaries across parameters instead of combining economically.

### Decision-table testing

Use when several conditions determine actions, permissions, pricing, validation, or feature
behavior.

Procedure:

1. List independent conditions with finite values and actions/outputs.
2. Create columns as rules; each column is one meaningful condition combination.
3. Mark impossible combinations and document the constraint/source.
4. Collapse columns only when the omitted condition provably cannot change any action.
5. Ensure every rule has a unique expected action set, including no-action/denial/audit.
6. Create at least one case per feasible high-risk rule; pairwise may sample lower-risk rules
   only when explicitly approved.

Example authorization table:

| Rule | Authenticated | Own tenant | Has permission | Action |
|---|---|---|---|---|
| R1 | yes | yes | yes | allow + audit |
| R2 | yes | yes | no | deny; no mutation + audit denial |
| R3 | yes | no | any | deny; disclose no resource data |
| R4 | no | any | any | challenge; no mutation |

Coverage = `feasible rules tested / feasible rules selected`. For authorization and money,
cover all material feasible rules, not just pairwise.

Common errors: conditions that are actually outputs, missing “else,” treating impossible
combinations as skipped without proof, asserting only the happy response.

### State-transition testing

Use for order/payment/account lifecycles, retries, workflows, sessions, and protocols.

Procedure:

1. Enumerate stable states, initial state, terminal states, events, guards, actions, and errors.
2. Build `current state × event/guard → next state + effects`.
3. Add valid transitions, forbidden transitions, self-transitions, repeated events, timeout,
   restart/recovery, and competing events.
4. Choose coverage:
   - **all states** for low risk;
   - **all valid transitions** for ordinary workflows;
   - **all valid + material invalid transitions** for high risk;
   - **transition pairs/sequences** when bugs depend on preceding state.
5. Assert next state, transition effects, forbidden effects, audit/event emission, and
   idempotency.

Coverage states the selected criterion explicitly; “state coverage” alone is ambiguous.

Common errors: modeling UI screens rather than business state, omitting guards, forcing state
through private storage in E2E, ignoring duplicate/late events and recovery.

### Scenario and business-process testing

Use to prove a user goal or end-to-end business outcome through public interfaces.

Procedure:

1. Name actor, goal, trigger, precondition, primary path, alternate paths, and postcondition.
2. Link each step to underlying rules instead of hiding all assertions in one giant case.
3. Keep one primary journey case; move combinatorial rule detail to lower layers.
4. Add alternate E2E only when wiring, authorization, external effect, or recovery cannot be
   proven below.
5. Assert user-visible outcome plus durable cross-system state and forbidden effects.

Coverage = business-process steps/alternate flows selected by risk, not number of clicks.

### Pairwise and combinatorial testing

Use when parameters such as browser, role, locale, flag, and backend mode create too many
combinations and most defects are expected from low-order interactions.

Procedure:

1. List parameters and discrete values after partitioning.
2. Add constraints for impossible combinations and verify them with the product owner/code.
3. Generate pairwise by default; use 3-way or explicit combinations where history/risk shows
   higher-order interaction.
4. Always inject must-test combinations: production default, most-used path, every Critical
   combination, past defects, and rollout pairs.
5. Review the generated set for missing semantic rules; tools optimize combinations, not
   product meaning.

Evidence includes input model, constraints, generator/version or algorithm, generated matrix,
and explicit additions. Coverage is `t-way interactions covered / feasible t-way
interactions`, plus named must-test combinations.

## 4. White-box techniques

Use only when implementation structure is part of the test basis. White-box coverage finds
untested structure; it does not prove correct behavior.

### Statement and branch coverage

1. Identify changed/high-risk units.
2. Run the project coverage tool with the exact build/config.
3. For statement coverage, find unexecuted executable statements.
4. For branch/decision coverage, require each decision outcome at least once.
5. Add cases only when the uncovered structure represents meaningful risk; inspect whether
   dead/unreachable code is itself a finding.
6. Keep behavioral assertions; a line executed without an oracle is weak evidence.

Prefer branch over statement coverage for rule-heavy code because 100% statements can still
miss a decision outcome. Use condition/MC/DC only when project safety/regulatory rules require
it; define the required standard rather than improvising.

### Data-flow and path-focused review

For defect-prone code, trace definitions to uses, error paths, resource acquisition/release,
and transaction boundaries. Full path coverage is usually infeasible; select paths by risk,
cyclomatic complexity, change diff, and historical failures. Report untestable “hot spots”
such as deeply nested decisions, hidden global state, or tangled side effects as quality
risks—not as functional defects without failing behavior.

## 5. Experience-based techniques

### Error guessing

Use after systematic techniques. Build a named heuristic from:

- prior defects and production incidents;
- common project-specific failure patterns;
- language/framework hazards;
- integration/provider failure history;
- suspicious complexity, comments, or change hotspots.

For each guessed failure, record the heuristic and expected observable failure prevention.
Do not use “try weird things” as a case design.

### Checklist-based testing

Use for repeatable standards or release controls.

1. Version the checklist and name its source/scope.
2. Remove non-applicable entries with a reason.
3. Turn every item into `probe → oracle → evidence → status`.
4. Review periodically against defects and changed standards.

A checked box without evidence is not a pass.

### Session-based exploratory testing

Use for unfamiliar behavior, interactions difficult to enumerate, visual/usability concerns,
or residual risk after scripted cases.

Charter:

```text
Explore <target>
with <resources/data/persona>
to discover <risks/questions>
for <time box>
without <prohibited effects>
```

Protocol:

1. Set 30–120 minute time box and specific risk charter.
2. Record setup, path, observations, data, questions, and evidence as testing occurs.
3. Separate product defect, requirement question, test/environment issue, and idea.
4. Preserve exact reproduction for findings.
5. Debrief: coverage achieved, risks remaining, new scripted cases, defects, blockers.

Exploration complements systematic coverage; it does not replace missing acceptance criteria.

## 6. Generative and fault-detection techniques

### Property-based testing

Use when many inputs share an invariant.

1. Define generators that produce valid and intentionally invalid partitions.
2. State the property independently of implementation: round-trip, conservation,
   idempotency, monotonicity, commutativity, normalization, or authorization.
3. Bound size and runtime; preserve seed.
4. Shrink/minimize failures and record the minimal counterexample.
5. Include example-based cases for important known values and boundaries.

Avoid tautological properties that call the same implementation to calculate expected output.

### Metamorphic testing

Use when exact expected output is hard to compute but relations are known. Define a
transformation and relation, for example: reordering independent inputs does not change a
total; adding an irrelevant field does not change authorization; retrying with the same
idempotency key creates no second effect. Record both executions and the relation oracle.

### Fuzz testing

Use for parsers, protocols, uploads, serialization, public APIs, and hostile input.

1. Define scope, allowed payload classes, resource/time budget, and prohibited targets.
2. Seed the corpus with valid, boundary, malformed, historical, and protocol-specific cases.
3. Instrument crashes, hangs, memory/resource growth, uncaught errors, and invariant breaks.
4. Isolate process/data and enforce time/memory/output limits.
5. Preserve seed/corpus/tool version and minimize the reproducer.
6. Validate that a crash is in the product rather than harness/environment.

Fuzzing production or a real provider requires explicit authorization and bounded effects.

### Mutation testing

Use when critical logic has high ordinary coverage but assertion strength is uncertain.

1. Scope to stable critical units; exclude generated code and equivalent/noisy mutations.
2. Run baseline tests first.
3. Apply controlled semantic mutations: condition inversion, boundary change, omitted call,
   altered return.
4. A killed mutant proves some test detects it; a survivor requires analysis, not automatic
   test creation.
5. Classify survivors as missing assertion, uncovered behavior, equivalent mutant, unreachable
   code, or out of scope.

Mutation score =
`killed non-equivalent mutants / all executed non-equivalent mutants`.
Report exclusions and survivors; never optimize the percentage by hiding difficult mutants.

## 7. Combining and deduplicating

Typical combinations:

- range-controlled state guard: partitions + BVA + state transitions;
- role × tenant × flag: decision table + explicit critical combinations + pairwise remainder;
- import/parser: partitions + boundaries + example cases + properties + bounded fuzzing;
- checkout: decision/state models below + one public journey + contract/failure cases;
- distributed idempotency: state transitions + metamorphic retry property + integration.

Do not repeat every boundary at unit, API, and UI. Keep detailed rules low, cross-boundary
semantics at integration/contract, and a few business outcomes at E2E.

## 8. Worked example and completion gate

Requirement: “A password reset token works once, expires after 15 minutes, and cannot reset
another account.”

1. Partitions: correct/other account; valid/malformed/unknown token.
2. Boundaries: just before, exactly at, and just after the approved expiry rule.
3. State model: issued → consumed or expired; repeated consume forbidden.
4. Decision table: authenticated state is irrelevant; token ownership, validity, and expiry
   determine reset/denial.
5. Metamorphic property: retry with consumed token creates no further password/session change.
6. Cases assert response, password state, session revocation policy, no other-account change,
   audit outcome, and no token leakage.
7. Detailed cases run at service/integration level; one E2E proves delivery-to-reset wiring.

Design is complete when every selected criterion/risk has:

- a named model and coverage rule;
- cases covering the model and explicit risk additions;
- a complete oracle, owned data, cleanup, and evidence contract;
- a justified level;
- an escalation/stop rule;
- no unexplained duplicate or omitted coverage item.

Research basis: ISTQB CTFL 4.0.1 and CTAL Test Analyst 4.0 define black-box,
white-box, and experience-based techniques and recommend combining them by risk and test
basis. This file contains the complete local procedure:
<https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf> and
<https://www.istqb.org/wp-content/uploads/sdm-uploads/ISTQB-CTAL-TA-Syllabus-v4.0-EN.pdf>.
