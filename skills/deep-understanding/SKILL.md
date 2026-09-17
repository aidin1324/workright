---
name: deep-understanding
description: Use when deep research, unfamiliar-codebase comprehension, root-cause analysis, or durable learning would be harmed by premature synthesis, shallow reading, or unverified assumptions.
---

# Deep Understanding

Build the model before using it. Evidence precedes abstraction; the first explanation is a hypothesis.

## Start

Establish one primary goal and completion evidence; ask once if its mode is ambiguous. On every later turn, re-establish the current objective, read and use new evidence, and treat the prior model as provisional. If the mode changes, switch and retain unresolved verification as explicit uncertainty:

- **Work:** finish the task; preserve only the selected learning target.
- **Study:** optimize durable independent understanding.

## Step 0: Ground the model

### Repository

1. Inventory the repository; locate entry points, tests, configuration, generated/vendor content, and target flow.
2. Read the relevant closure completely: callers, callees, types, state, configuration, tests, and comparable implementations.
3. Record each file's role, inputs, outputs, state changes, dependencies, and invariants before constructing the abstraction.
4. Trace the mechanism end to end, form a credible alternative explanation, and try to disprove the preferred model using other paths, tests, logs, configuration, or a safe experiment.

Inventory all files, but deeply read generated/vendor content only when it participates in the mechanism. Keyword matches are not a system model.

### Research

1. Frame the question and freeze a priority set: primary studies, strong syntheses, and credible counterevidence.
2. Complete each priority source before cross-source synthesis. Record its question, method, comparison, measurement, result, proposed mechanism, limitations, and non-claims.
3. Snippets, abstracts, and secondary summaries are screening only. Mark inaccessible full texts incompletely verified; never invent unseen methods or limitations.
4. Once all records are complete, compare mechanisms, contradictions, and boundary conditions. Re-read decisive and anomalous sources and seek evidence that could falsify the synthesis.
5. Before delivery, audit every load-bearing source: retain its decisive comparison, measurement boundary, result, and validity threat. Brevity may compress wording, never decisive evidence.

## Grounding gate

Proceed when the model explains the important observations, beats credible alternatives, makes verified predictions, and states remaining uncertainty. Bound claims to observed conditions and time windows. If evidence is unavailable, narrow the claim and report the gap.

## Help the person

In **work mode**, complete the task; use at most one brief prediction before and one causal explanation after unless deeper study is requested.

In **study mode**:

- Ask for a prediction before revealing the mechanism or answer. In live tutoring, wait for the learner; an explicit lesson script may include a later answer key.
- novice: after that prediction, use a worked or partial example, then fade support;
- competent: prediction or explanation, then the smallest useful hint;
- advanced: boundaries, counterexamples, error diagnosis, and far transfer.

Use a mastery loop:

1. Begin each mastery check with the learner explaining the mechanism in their own words and recording confidence.
2. Give no hint; ask for a prediction on a far-transfer case and a similar non-example.
3. Close every check by comparing that confidence with correctness and reasoning, then have the learner revise it. After a specific failure, give the smallest useful hint, then remove it and retest unaided.
4. At the user's stated later session, repeat without notes on interleaved new cases. Advance difficulty only after repeated independent success across mechanisms, boundaries, errors, and transfer.

Do not accept “понятно” or restatement. Finish with one justified, independently executable next action; do not bundle tasks with “and” or “then”.

## Temporary notes

When needed, create one scratch directory in task `work/` or with `mktemp -d`; keep one notes file plus sources. On completion or cancellation, delete only that directory unless preservation was requested. Keep it while waiting or interrupted. Never delete repository files, deliverables, or a parent directory.
