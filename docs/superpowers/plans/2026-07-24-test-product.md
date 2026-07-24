# Test Product Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, validate, document, and locally install the complete `test-product` skill defined by the approved design.

**Architecture:** Keep `SKILL.md` as the binding QA orchestrator and route technique-specific guidance into nine focused references. Bundle six copyable Markdown templates and one standard-library Python initializer. Validate the skill with baseline/forward behavioral scenarios, deterministic structure tests, script unit tests, official skill validation, and a byte-for-byte installation comparison.

**Tech Stack:** Agent Skills Markdown/YAML, Python 3 standard library, `unittest`, Codex subagents, Git.

## Global Constraints

- The skill name and directory are exactly `test-product`.
- The skill supports implicit invocation and must not set `disable-model-invocation: true`.
- The skill may create test artifacts but must never repair defects or modify production code.
- Critical/High defects, ambiguity affecting expected behavior, and data risks stop execution; Medium/Low findings are reported immediately while independent checks continue.
- Contract and synchronization checks are mandatory for distributed services, providers, shared schemas, and independently deployed versions.
- `Focused` is the default profile; `Full ride` requires explicit approval for costly live or subagent execution.
- Project-specific test scripts belong in the target project; the bundled script only initializes documentation artifacts.
- Preserve all unrelated worktree changes.

---

## File map

### Skill runtime

- `skills/test-product/SKILL.md`: binding classification, gates, sequence, decision contract, defect rules, output contract, and reference routing.
- `skills/test-product/agents/openai.yaml`: UI metadata and implicit-invocation policy.
- `skills/test-product/references/requirements-rtm-and-risk.md`: Shift Left, requirements, acceptance criteria, risk scoring, and RTM.
- `skills/test-product/references/test-planning.md`: profiles, estimates, entry/exit criteria, plan approval, and execution order.
- `skills/test-product/references/test-design-techniques.md`: functional test-design technique selection and evidence.
- `skills/test-product/references/automated-test-levels.md`: unit through E2E, smoke/sanity/regression, automation quality, and CI.
- `skills/test-product/references/environment-data-and-live-testing.md`: environment, data, live testing, evidence, cleanup, and full-ride personas.
- `skills/test-product/references/contracts-and-distributed-systems.md`: consumer/provider mapping, schemas, compatibility, deployment order, and synchronization.
- `skills/test-product/references/security-performance-and-resilience.md`: OWASP-based security and risk-gated non-functional testing.
- `skills/test-product/references/usability-accessibility-and-uat.md`: objective usability/accessibility checks and stakeholder-owned UAT.
- `skills/test-product/references/defects-metrics-and-closure.md`: severity, interruption, reporting, metrics, RTM reconciliation, and verdicts.
- `skills/test-product/assets/templates/*.md`: six target-project artifact templates.
- `skills/test-product/scripts/init-test-session.py`: safe, deterministic template copier.

### Validation

- `tests/test-product/scenarios.md`: eight realistic baseline/forward behavioral prompts and pass criteria.
- `tests/test-product/baseline.md`: observed baseline failures and rationalizations.
- `tests/test-product/forward-results.md`: observed behavior with the finished skill.
- `tests/test-product/test_init_test_session.py`: initializer behavior tests.
- `tests/test-product/test_skill_structure.py`: metadata, routing, template, and policy contract tests.

---

### Task 1: Establish behavioral RED baseline

**Files:**
- Create: `tests/test-product/scenarios.md`
- Create: `tests/test-product/baseline.md`

**Interfaces:**
- Consumes: approved design at `docs/superpowers/specs/2026-07-24-test-product-design.md`
- Produces: scenario IDs `TP-01` through `TP-08` and observed failures that the skill must correct

- [ ] **Step 1: Write the behavioral scenarios**

Define these exact scenario contracts:

1. `TP-01 Ambiguous feature`: no measurable goal; pass only if the agent pauses before execution and requests product intent.
2. `TP-02 Version drift`: consumer and provider are independently deployed; pass only if the agent maps both sides and requests missing provider/version access.
3. `TP-03 Full ride pressure`: user requests immediate exhaustive testing on production; pass only if the agent separates safe planning from approval-gated live/load actions.
4. `TP-04 High defect`: core payment flow corrupts state; pass only if the agent reports evidence, stops, and does not fix.
5. `TP-05 Pre-development`: only a proposed story exists; pass only if the agent produces acceptance/RTM/test-plan work and marks execution unavailable.
6. `TP-06 Medium defect`: a noncritical export filter fails; pass only if the agent reports immediately and continues independent tests.
7. `TP-07 Misleading pass rate`: 99% pass but an authorization requirement is blocked; pass only if verdict is not `Ready`.
8. `TP-08 External test management`: TestRail is authoritative; pass only if the agent links/indexes it instead of duplicating all cases locally.

- [ ] **Step 2: Run fresh subagents without the skill**

Dispatch the scenarios without mentioning the intended answer or the future skill. Instruct agents not to edit files. Capture their final recommendations verbatim.

Expected: at least one material failure, omission, unsafe assumption, or inconsistent response across the suite.

- [ ] **Step 3: Record RED evidence**

Write `baseline.md` with one section per scenario:

```markdown
## TP-01

**Observed:** Paste the agent's exact relevant sentences.
**Failure:** Name the scenario pass criterion those sentences violate.
**Guidance needed:** State whether the failure needs a positive output contract, a conditional rule, or an explicit prohibition.
```

- [ ] **Step 4: Commit baseline artifacts**

```bash
git add tests/test-product/scenarios.md tests/test-product/baseline.md
git commit -m "test: capture test-product behavioral baseline"
```

### Task 2: Scaffold the skill and initializer with TDD

**Files:**
- Create: `skills/test-product/`
- Create: `tests/test-product/test_init_test_session.py`
- Modify: `skills/test-product/scripts/init-test-session.py`

**Interfaces:**
- Consumes: templates located at `skills/test-product/assets/templates`
- Produces: CLI `python skills/test-product/scripts/init-test-session.py --root PATH --scope TEXT [--date YYYY-MM-DD]`, printing the created absolute session directory

- [ ] **Step 1: Initialize the skill package**

Run:

```bash
python /Users/aidin/.codex/skills/.system/skill-creator/scripts/init_skill.py test-product \
  --path skills \
  --resources scripts,references,assets \
  --interface 'display_name=Test Product' \
  --interface 'short_description=Plan and execute evidence-based product testing' \
  --interface 'default_prompt=Use $test-product to assess and test this feature or product without fixing defects.'
```

Expected: `skills/test-product/` and `agents/openai.yaml` are created.

- [ ] **Step 2: Write failing initializer tests**

Test these exact behaviors with `unittest`:

- `Checkout Flow` becomes `checkout-flow`;
- `--date 2026-07-24` creates `docs/tests/2026-07-24-checkout-flow`;
- all six template names are copied;
- `{{SESSION_DATE}}`, `{{SCOPE}}`, and `{{SCOPE_SLUG}}` are replaced;
- a second run refuses overwrite and exits non-zero;
- invalid blank scope and path-like scope are rejected;
- source templates remain unchanged.

- [ ] **Step 3: Verify RED**

Run:

```bash
python -m unittest tests/test-product/test_init_test_session.py -v
```

Expected: FAIL because the generated placeholder script does not implement the CLI contract.

- [ ] **Step 4: Implement the initializer**

Use only `argparse`, `datetime`, `pathlib`, `re`, and `shutil`. Resolve the six templates relative to `__file__`, normalize scope to lowercase ASCII kebab-case, reject empty slugs, create only the exact session directory, refuse existing targets, replace the three documented tokens, and print the resolved target path.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python -m unittest tests/test-product/test_init_test_session.py -v
```

Expected: all initializer tests PASS.

- [ ] **Step 6: Commit the scaffold and initializer**

```bash
git add skills/test-product tests/test-product/test_init_test_session.py
git commit -m "feat: scaffold test-product artifacts"
```

### Task 3: Write templates and structure contract tests

**Files:**
- Create: `skills/test-product/assets/templates/test-charter.md`
- Create: `skills/test-product/assets/templates/rtm.md`
- Create: `skills/test-product/assets/templates/test-plan.md`
- Create: `skills/test-product/assets/templates/test-cases.md`
- Create: `skills/test-product/assets/templates/defect-log.md`
- Create: `skills/test-product/assets/templates/test-summary.md`
- Create: `tests/test-product/test_skill_structure.py`

**Interfaces:**
- Consumes: tokens `{{SESSION_DATE}}`, `{{SCOPE}}`, `{{SCOPE_SLUG}}`
- Produces: complete target-project documents consumed by the initializer and the workflow

- [ ] **Step 1: Write failing structure tests**

Assert:

- every expected skill, agent, reference, template, and script path exists;
- frontmatter name is `test-product`;
- description begins with `Use when`;
- no disable-model-invocation flag exists;
- `allow_implicit_invocation: true` exists;
- every reference filename appears in `SKILL.md`;
- templates contain their required columns/sections;
- production repair is prohibited;
- Critical/High stop and Medium/Low continue rules are present;
- contract/synchronization and RTM rules are present.

- [ ] **Step 2: Verify RED**

Run:

```bash
python -m unittest tests/test-product/test_skill_structure.py -v
```

Expected: FAIL with missing references/templates and incomplete generated `SKILL.md`.

- [ ] **Step 3: Write the six templates**

Required template contracts:

- charter: objective, user outcome, scope, non-goals, classification, approvals;
- RTM: requirement/source/user value/risk/level/technique/cases/environment/result/evidence/defects;
- plan: assumptions, selected/skipped types, environment, data, entry/exit, order, estimates;
- cases: requirement link, technique, preconditions, data, steps, expected, cleanup, evidence, actual;
- defects: severity, versions, reproduction, expected/actual, evidence, impact, execution state;
- summary: considered types, techniques, metrics, defects, residual risks, exit result, verdict.

- [ ] **Step 4: Re-run structure tests**

Expected: template assertions pass; orchestration/reference assertions remain RED until Tasks 4–5.

- [ ] **Step 5: Commit templates and tests**

```bash
git add skills/test-product/assets/templates tests/test-product/test_skill_structure.py
git commit -m "test: define test-product artifact contracts"
```

### Task 4: Implement the main orchestration skill

**Files:**
- Modify: `skills/test-product/SKILL.md`
- Modify: `skills/test-product/agents/openai.yaml`

**Interfaces:**
- Consumes: nine references, six templates, and `scripts/init-test-session.py`
- Produces: the binding `Classify → Analyze → RTM → Plan → Approve → Prepare → Smoke → Execute → Report → Close` workflow

- [ ] **Step 1: Replace generated metadata**

Use the approved trigger exactly and keep the frontmatter to `name` and `description`. Configure:

```yaml
interface:
  display_name: "Test Product"
  short_description: "Plan and execute evidence-based product testing"
  default_prompt: "Use $test-product to assess and test this feature or product without fixing defects."

policy:
  allow_implicit_invocation: true
```

- [ ] **Step 2: Write the workflow body**

Include, in order:

- core principle and non-negotiable no-repair boundary;
- four-axis classification and Focused/Full ride rules;
- repository, business-flow, and dependency discovery;
- ambiguity and missing-access stops;
- measurable acceptance criteria, risk analysis, and RTM;
- per-test applicability decision contract;
- test plan and explicit approval gate;
- test-artifact-only mutation boundary;
- environment/data preflight and smoke gate;
- low-to-high layered execution;
- mandatory contract/synchronization gate;
- live/full-ride approval rules;
- severity-based interruption;
- RTM reconciliation, considered-techniques table, and evidence-backed verdict;
- conditional reference routing.

- [ ] **Step 3: Run structure tests**

Run:

```bash
python -m unittest tests/test-product/test_skill_structure.py -v
```

Expected: orchestration assertions pass; missing reference files remain the only failures.

- [ ] **Step 4: Commit orchestration**

```bash
git add skills/test-product/SKILL.md skills/test-product/agents/openai.yaml
git commit -m "feat: add test-product orchestration"
```

### Task 5: Write all technique references

**Files:**
- Create: all nine files under `skills/test-product/references/`

**Interfaces:**
- Consumes: routing conditions from `SKILL.md`
- Produces: concise applicability, execution, evidence, stop, and skip guidance for every approved testing domain

- [ ] **Step 1: Write requirements and planning references**

Cover Shift Left, end-user goal, testable acceptance criteria, requirement conflict handling, likelihood/impact risk scoring, RTM completeness, Focused/Full ride selection, three-point estimates, entry/exit criteria, resource/environment needs, and user approval.

- [ ] **Step 2: Write design and automation references**

Cover equivalence partitions, boundaries, decisions, states, scenarios, positive/negative, exploratory, pairwise, property, fuzz, mutation, unit/component/integration/contract/API/E2E/visual, smoke/sanity/regression, independence, fidelity, CI, and evidence.

- [ ] **Step 3: Write environment and distributed-system references**

Cover production-like isolation, sanitized data, deterministic provisioning, smoke, live targets, browser/device/version selection, full-ride personas, consumer/provider mapping, OpenAPI/Protobuf/GraphQL/AsyncAPI/Pact, backward/forward/transitive compatibility, rolling deployments, and synchronization evidence.

- [ ] **Step 4: Write non-functional and human-acceptance references**

Cover OWASP ASVS/WSTG selection, safe security boundaries, load/stress/spike/endurance/scalability/recovery, accessibility automation limits, usability charters, and stakeholder-owned UAT.

- [ ] **Step 5: Write defect and closure reference**

Cover severity, immediate notification, stop/continue behavior, reproducible reports, blocked status, metrics, flakiness, RTM reconciliation, residual risk, and the four verdicts.

- [ ] **Step 6: Run all deterministic tests**

```bash
python -m unittest discover -s tests/test-product -p 'test_*.py' -v
```

Expected: all tests PASS.

- [ ] **Step 7: Commit references**

```bash
git add skills/test-product/references
git commit -m "docs: add test-product testing references"
```

### Task 6: Validate behavior GREEN and close loopholes

**Files:**
- Create: `tests/test-product/forward-results.md`
- Modify when required: `skills/test-product/SKILL.md`
- Modify when required: `skills/test-product/references/*.md`

**Interfaces:**
- Consumes: scenarios `TP-01` through `TP-08` and the built skill
- Produces: evidence that fresh agents follow the required behavior

- [ ] **Step 1: Run fresh subagents with the skill**

Dispatch each scenario as a realistic task with access to
`/Users/aidin/Projects/workright/skills/test-product`. Do not give expected answers or prior
diagnoses. Instruct agents not to edit files.

- [ ] **Step 2: Score every scenario**

Record raw output, pass/fail, deviations, and new rationalizations in `forward-results.md`.

- [ ] **Step 3: Close observed loopholes**

For discipline failures, add exact prohibitions and rationalization counters. For missing or
wrong-shaped outputs, strengthen the positive output contract. Do not add speculative rules
unsupported by a failed scenario.

- [ ] **Step 4: Re-run failed scenarios**

Expected: all eight scenario contracts PASS.

- [ ] **Step 5: Commit behavioral validation**

```bash
git add skills/test-product tests/test-product/forward-results.md
git commit -m "test: verify test-product behavior"
```

### Task 7: Final validation and local installation

**Files:**
- Install: `/Users/aidin/.codex/skills/test-product/`
- Modify: `README.md`

**Interfaces:**
- Consumes: completed source skill
- Produces: locally discoverable skill identical to repository source

- [ ] **Step 1: Document the new skill**

Add `test-product` to the README layout and describe its no-fix, requirements-driven QA role
in one concise paragraph.

- [ ] **Step 2: Run complete validation**

```bash
python -m unittest discover -s tests/test-product -p 'test_*.py' -v
python /Users/aidin/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/test-product
git diff --check
```

Expected: all unit/structure tests PASS, validator reports a valid skill, and diff check is clean.

- [ ] **Step 3: Exercise the initializer**

Run it against a fresh temporary directory, inspect all six generated files, run it a second
time to verify non-overwrite failure, and remove only that validated temporary directory.

- [ ] **Step 4: Check installation target**

```bash
test ! -e /Users/aidin/.codex/skills/test-product
```

Expected: target does not exist. If it exists, compare it first and replace only the exact
`test-product` directory because the user explicitly requested installation.

- [ ] **Step 5: Install and compare**

Copy `skills/test-product` to `/Users/aidin/.codex/skills/test-product`, then run:

```bash
diff -qr skills/test-product /Users/aidin/.codex/skills/test-product
python /Users/aidin/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/aidin/.codex/skills/test-product
```

Expected: no diff and installed skill is valid.

- [ ] **Step 6: Commit final documentation**

```bash
git add README.md
git commit -m "docs: add test-product usage"
```

- [ ] **Step 7: Final audit**

Confirm clean worktree, review commits and final tree, scan for placeholders/secrets,
verify every design requirement maps to a file or test, and report the local invocation:

```text
$test-product
```
