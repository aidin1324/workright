# Usability, Accessibility, and User Acceptance Testing

Use for human-facing behavior. Keep three claims separate:

- usability: representative users can complete tasks effectively, efficiently, and
  satisfactorily in context;
- accessibility: scoped content meets named technical criteria and works with selected access
  methods;
- UAT: accountable stakeholders accept business fitness for the named scope.

An agent may prepare and facilitate these activities; it cannot impersonate real users with
disabilities or accept business/release risk for stakeholders.

## Contents

1. Applicability and target definition
2. Usability protocol
3. Accessibility protocol
4. UAT protocol
5. Severity, evidence, privacy, and closure

## 1. Applicability and target definition

Record:

- target users/roles, capabilities, prior knowledge, language, and context;
- critical tasks and business outcomes;
- supported devices/browsers/input/assistive technologies;
- accepted design system/content/product conventions;
- accessibility standard/version/level or project/regulatory target;
- UAT decision owner and release context;
- environment, data, consent, recording, retention, and privacy limits.

If a regulatory/contractual target exists, use it. Otherwise recommend the current project
target; for web products, WCAG 2.2 Level AA is a common risk-based proposal but requires owner
confirmation. Record the exact standard and date. Do not silently claim full conformance from
a sample.

# Part A — Usability

## 2.1 Choose the method

| Method | Best for | Limitation |
|---|---|---|
| Expert heuristic review | fast detection of known interaction problems | not evidence of real-user success |
| Cognitive walkthrough | first-use learnability through a task | depends on modeled user knowledge |
| Moderated task test | observed user behavior and reasoning | requires participants/facilitation |
| Unmoderated task test | broader quantitative sample | less diagnostic/context control |
| Exploratory persona simulation | early QA variation | agent simulation is not user research |

Use expert review for Focused QA. Recommend representative-user sessions when preference,
learnability, disability context, or product acceptance materially affects the decision.

## 2.2 Build a task model

For every critical task define:

```text
Task ID and user group
Realistic starting state/context
Goal phrased without revealing controls
Success state and critical errors
Allowed assistance
Target or baseline for time/steps/errors
Data and cleanup
Observation/recording method
Stop/invalid-session rule
```

Do not tell participants exactly where to click. Avoid leading questions and defending the
design. If assistance is given, record its level; assisted completion is not unassisted
success.

## 2.3 Expert/cognitive review

For each task walk through:

1. can the user discover the next action?
2. does wording match the user's goal and domain?
3. is system status/feedback timely and perceivable?
4. are consequences, constraints, and destructive actions clear?
5. are errors prevented, explained, and recoverable?
6. can the user interrupt, return, undo, or safely retry?
7. is the pattern consistent with the product?
8. can novices learn it and experienced users act efficiently?

Turn each observation into:

`task step → observed evidence → affected user/outcome → expected product convention or
criterion → severity/confidence`

Personal dislike without criterion, task impact, or user evidence is feedback—not a defect.

## 2.4 Representative-user session protocol

1. recruit users matching the role/context; record inclusion criteria, not unnecessary
   personal data;
2. obtain informed consent for participation/recording and retention;
3. verify equipment/environment and give neutral orientation;
4. present one task at a time without hints;
5. capture completion, critical errors, noncritical errors, assistance, abandonment, time,
   path, and participant comments;
6. ask neutral follow-up: “What did you expect?” and “What made that difficult?”;
7. debrief, sanitize, and link observations to task/criterion.

Invalidate or qualify a session when the environment fails, facilitator reveals the solution,
participant does not match target group, or recording/measurement is materially incomplete.

Metrics:

- task success = `unassisted successful participants / valid participants`;
- critical-error rate = `participants with a critical task error / valid participants`;
- assistance rate = `participants requiring help / valid participants`;
- time-on-task distribution compared with predeclared target/baseline;
- satisfaction score only with a named instrument/question and sample size.

Small samples reveal problems but do not justify precise population claims. Report counts and
confidence limits qualitatively.

### Decide sample sufficiency before sessions

Choose:

- **Formative/discovery:** find important problems and improve design. As a default planning
  heuristic, run at least five valid sessions for the primary group and at least three for
  each materially different high-risk group, then continue until two consecutive valid
  sessions per group reveal no new Critical/High task failure. Saturation supports discovery,
  not a population success-rate claim.
- **Summative/readiness:** prove a task-success/error threshold. Predeclare target proportion,
  confidence, margin of error or hypothesis/power, expected proportion, and segment quotas.
  Calculate sample size with an accepted method; for an approximate proportion,
  `n ≈ z² × p × (1-p) / e²` before finite-population and attrition adjustments. Without a
  decision threshold or adequate sample, report descriptive evidence and mark the summative
  cases `Blocked` by insufficient evidence and the summative readiness verdict
  `Inconclusive`.

Increase the sample for heterogeneous roles, rare critical failures, high consequence, or
large dropout. Never stop early only because results look favorable.

# Part B — Accessibility

## 3.1 Define representative scope

Inventory page/component templates, critical journeys, roles, and dynamic states. Sample to
include:

- home/navigation and shared layout;
- critical forms, tables, dialogs, menus, notifications;
- error, empty, loading, success, timeout, and disabled states;
- authentication/recovery and time-limited steps;
- every distinct component pattern;
- responsive/zoomed state and media where applicable.

Create:

| Page/component/state | Critical task | Applicable criteria | Method | Browser/AT/input | Result/evidence |
|---|---|---|---|---|---|

For full conformance, follow the accepted evaluation methodology and complete the required
scope; a risk sample supports only a sampled assessment.

### Full conformance gate

Pin the exact WCAG/contract version and claimed level. A scoped conformance claim requires:

- every in-scope **full page**, including responsive and dynamic states, meets every applicable
  success criterion at the claimed level;
- every page in each in-scope **complete process** conforms, not only selected steps;
- relied-upon technologies are accessibility-supported in the declared user environment;
- a conforming alternative version conforms at the level, has the same information/function
  and language, is equally current, and is either reachable from the nonconforming page by an
  accessibility-supported mechanism, the only gateway to that page, or linked by the
  conforming gateway through which the nonconforming page is reached;
- nonconforming content does not interfere with keyboard access, timing, flashing, or use of
  the rest of the page;
- the claim records date, guideline/version, level, exact page/process scope, and relied-upon
  technologies.

The versioned success-criterion catalog is normative test-basis data. If it is unavailable or
unapproved, mark conformance `Blocked`; do not downgrade it to a vague best-practice claim.
A sampled evaluation must say “sampled assessment,” never full conformance.

## 3.2 Layer the evaluation

### Automated

Run validated scanners/linters for detectable failures such as missing names, certain
structure/ARIA issues, and some contrast errors. Pin tool/ruleset/version. Validate material
findings and false positives manually. A zero-issue scan is not conformance.

### Keyboard and focus

For every critical route:

- all actions reachable/operable without pointer;
- logical focus order and visible focus;
- no keyboard trap;
- dialogs/menus manage focus and return it correctly;
- skip/navigation mechanisms work;
- shortcuts and drag/pointer alternatives follow the target standard.

### Semantics, text, errors, and dynamic state

Verify programmatic name/role/value/state; headings/landmarks/labels/instructions; error
identification and association; status/live-region behavior; link/button purpose; language;
table/list relationships. Inspect the accessibility tree, not only the DOM.

### Perception and adaptation

Verify contrast under named method, text resize/zoom/reflow, orientation, non-color cues,
reduced motion, content on hover/focus, target size/spacing where applicable, and no loss of
information/function.

### Assistive technology

Choose browser/AT/input combinations from supported users and risk. Execute critical tasks,
not random element reading. Record announcements, navigation, forms, errors, dialogs, and
dynamic updates.

If required expertise/tool/access is unavailable, mark affected criteria `Blocked` or
`Not run` with a reason; do not silently remove them or claim conformance.

## 3.3 Criterion results and severity

Use per criterion/page/state:

- `Passed`: method and evidence demonstrate the criterion;
- `Failed`: reproducible violation;
- `Blocked`: required environment/expertise/content unavailable;
- `Not run`: applicable but outside executed scope, with reason;
- `Not applicable`: criterion truly does not apply, with reason.

Accessibility impact:

- Critical/High: blocks a critical task for an affected access method with no reasonable
  alternative, exposes data, or prevents authentication/payment/safety action;
- Medium: material barrier with difficult alternative or repeated broad pattern;
- Low: localized friction with effective alternative.

Consider affected population and pervasiveness, but never lower severity because fewer users
are affected.

Metrics:

- criterion coverage =
  `evaluated applicable criterion instances / scoped applicable instances`;
- task accessibility =
  `critical tasks completed with selected access method / selected critical tasks`;
- failure count segmented by criterion, component pattern, task, and severity.

Do not average repeated violations into a misleading conformance percentage.

# Part C — UAT

## 4.1 Entry criteria

UAT begins only when:

- business scope, rules, and acceptance owner are named;
- stable candidate build/environment is identified;
- blocking system/sanity defects are resolved or disclosed;
- scenarios, roles, data, expected business outcomes, and evidence are prepared;
- privacy/external effects/cleanup are approved;
- decision states and waiver authority are agreed.

Prefer staging, preview, beta, or feature flag. Never deploy/update production to enable UAT
without a separate release/deployment request.

## 4.2 Derive business scenarios

Trace each scenario from a business process/rule and RTM:

```text
UAT scenario ID / business owner
Business purpose and actor
Preconditions and realistic sanitized data
Business steps/outcome, not implementation detail
Policy/contractual rule
Expected final business state and external effects
Evidence
Decision: Accepted / Rejected / Deferred / Blocked
Comments, issue IDs, waiver owner/expiry
```

Cover primary process, high-impact alternate/exception, role/policy, end-of-period or other
material business timing, external document/report, and regulatory/contract requirement.

## 4.3 Facilitate and route outcomes

The stakeholder executes or directly observes acceptance-critical work. The agent records
evidence and separates:

- product defect: clear accepted rule is violated;
- change request: new behavior desired beyond baseline;
- preference/design feedback: subjective choice needing product owner;
- training/documentation issue;
- environment/test-data issue;
- unresolved requirement decision.

Rejected/blocked scenarios link to issue and owner. After a separate remediation, identify
the new build, repeat the original scenario, and run affected UAT regression. A waiver records
scope, risk, rationale, accepting owner, expiry/review date, and limitations.

## 4.4 UAT closure

UAT closure requires:

- every planned scenario has a decision state and evidence;
- rejected/blocked/deferred items have owner and effect on acceptance;
- waivers are explicit and current;
- data/external effects are reconciled and cleaned;
- the accountable stakeholder signs the decision record.

UAT acceptance =
`Accepted executed scenarios / executed scenarios`, segmented by criticality. The ratio cannot
override a rejected critical scenario.

The agent reports the stakeholder decision; it does not sign on their behalf.

## 5. Evidence, privacy, and overall closure

Record task/criterion/scenario IDs, target users and scope, environment/build, method,
facilitator/evaluator, tool/browser/AT versions, date, data, expected/actual, sanitized
artifact, assistance, limitations, and result.

For human sessions obtain consent, minimize participant data, restrict access, define
recording/transcript retention, and remove identifiers from tracked artifacts. Never publish
raw recordings by default.

Overall closure states separately:

- expert usability assessment vs representative-user evidence;
- sampled accessibility assessment vs conformance evaluation;
- technical QA verdict vs stakeholder UAT decision.

Research basis:

- W3C WCAG-EM/conformance guidance requires a defined scope and combines automated and
  knowledgeable human evaluation:
  <https://www.w3.org/WAI/test-evaluate/conformance/>.
- WCAG 2.2 conformance requires all applicable success criteria at the claimed level and
  recommends involving users with disabilities:
  <https://www.w3.org/WAI/WCAG22/Understanding/conformance.html>.
- ISTQB Acceptance Testing covers business-process/rule-derived tests, UAT, contractual/
  regulatory acceptance, usability, alpha, and beta:
  <https://www.istqb.org/wp-content/uploads/2024/11/ISTQB-CT-AcT_Syllabus-v1.0_2019.pdf>.

All required local procedures are contained above.
