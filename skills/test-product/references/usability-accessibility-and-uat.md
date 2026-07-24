# Usability, Accessibility, and UAT

Use for human-facing workflows. Keep objective checks separate from stakeholder taste.

## Usability

Define target users, task, context, prior knowledge, and success measure. Evaluate:

- task completion and correctness;
- time/steps only when a baseline or target exists;
- terminology, navigation, feedback, and system status;
- prevention, clarity, and recovery from errors;
- interruption, return, and destructive-action confirmation;
- consistency with the product's established patterns;
- discoverability for new users and efficiency for experienced users.

Use scripted critical tasks plus a time-boxed exploratory charter. Record observations and user
impact; do not report personal preference as a defect.

## Accessibility

Select the applicable WCAG/project/regulatory target. Combine:

- automated checks for machine-detectable failures;
- keyboard-only navigation and visible focus;
- semantic names, roles, states, headings, labels, and errors;
- contrast, zoom/reflow, reduced motion, and non-color cues;
- screen-reader or accessibility-tree checks when tools and expertise allow;
- dynamic updates, dialogs, forms, time limits, and authentication flows;
- representative pages/states, not only the home page.

An automated scanner cannot establish full conformance. W3C requires knowledgeable human
evaluation for criteria tools cannot determine:
<https://www.w3.org/WAI/test-evaluate/>.

Record standard/version, scope, method, tools/browser/assistive technology, outcome, evidence,
and untested criteria.

## UAT

Use UAT when business fitness, workflow acceptance, policy, contractual behavior, or subjective
product acceptance needs a stakeholder decision.

The agent:

1. derives scenarios from business processes and RTM;
2. prepares realistic sanitized data and clear expected business outcomes;
3. identifies roles and decision owners;
4. facilitates execution and captures evidence/feedback;
5. distinguishes defect, change request, preference, and training/documentation issue.

The stakeholder decides acceptance. The agent must not approve taste, business policy, or
release risk on the stakeholder's behalf.

Never update production to enable UAT. Recommend staging, preview, feature flag, beta, or another
approved safe environment. Production observation requires explicit bounded approval.

ISTQB acceptance guidance covers business-process acceptance, usability/UX, performance,
security, alpha/beta, and collaboration:
<https://www.istqb.org/certifications/certified-tester-acceptance-testing-ct-act/>.
