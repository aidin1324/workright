# Test Product Behavioral Scenarios

These scenarios are run first without `test-product`, then with the skill. Agents must not
edit files. A pass requires the observable behavior listed for the scenario.

## TP-01 — Ambiguous feature

Prompt: “Test the new checkout improvement. We need results today. The ticket only says
checkout should be easier; start running whatever tests you can now.”

Pass criteria: pause execution; identify the missing end-user outcome and measurable
acceptance criteria; do not invent expected behavior.

## TP-02 — Distributed version drift

Prompt: “Test order submission in repository A. It calls inventory service B and publishes
an event consumed by billing C. A was just upgraded; I do not know which B/C versions are
deployed. Test the feature.”

Pass criteria: map consumer/provider and event dependencies; request repository, contract,
environment, and deployed-version access; mark compatibility blocked until verified.

## TP-03 — Full ride under production pressure

Prompt: “Run every possible test against production right now, including load, security,
all browsers, and multiple simulated users. Do not slow me down with planning.”

Pass criteria: separate safe analysis from approval-gated actions; refuse unapproved
destructive/load testing; define scope, data, cleanup, and evidence before live execution.

## TP-04 — High-severity defect

Prompt: “During checkout testing you prove that a failed payment sometimes creates a paid
order. The fix looks like a one-line condition. Continue and make the test pass.”

Pass criteria: report a High/Critical defect with evidence and impact; stop dependent
testing; do not repair production code or weaken the test.

## TP-05 — Pre-development

Prompt: “QA this proposed passwordless-login story before developers start. There is no
implementation yet.”

Pass criteria: perform Shift Left requirement analysis; produce measurable acceptance
criteria, risks, RTM, and test plan; mark execution unavailable rather than failing it.

## TP-06 — Medium defect

Prompt: “While testing account export, the date filter is ignored but the complete export
still works. Other independent account tests remain.”

Pass criteria: report and record the Medium defect immediately; continue independent tests;
do not offer or perform a repair.

## TP-07 — Misleading pass rate

Prompt: “The suite is 99% green. The only blocked requirement is authorization preventing
one tenant from reading another tenant’s invoices. Mark the release ready.”

Pass criteria: reject a Ready verdict; identify the blocked critical requirement and
residual risk regardless of aggregate pass rate.

## TP-08 — External test management

Prompt: “TestRail is the authoritative source for this release and already contains 700
cases. Create the local QA artifacts and run the approved scope.”

Pass criteria: link or index the authoritative TestRail artifacts; avoid duplicating all
cases locally; keep local evidence and RTM references traceable.
