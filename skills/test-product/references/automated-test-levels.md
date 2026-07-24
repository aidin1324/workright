# Automated Test Levels

Use the lowest layer that can prove the risk, then add only the integration confidence missing
below it.

| Level | Proves | Best practices |
|---|---|---|
| Unit | Local domain behavior | Fast, deterministic, no network/filesystem; real code; minimal mocks |
| Component | Module through public interface | Isolate external systems; verify observable contract |
| Integration | Components/DB/queue/files work together | Real schemas and adapters; clean setup/teardown |
| Contract | Consumer and provider remain compatible | Verify consumer expectations against actual provider |
| API | Transport and service semantics | Schema, status, errors, auth, idempotency, pagination, concurrency |
| System/E2E | End-user goal works across the stack | Few critical journeys; stable user-visible locators; controlled data |
| Visual | Meaningful rendered appearance | Stable browser/OS/fonts/data; human review of diffs |

Prefer high-fidelity fakes or real implementations when they remain small and safe. Use mocks
for hard-to-trigger failures or expensive/unsafe boundaries, not to restate implementation.

## Smoke, sanity, and regression

- **Smoke:** prove the build/environment is testable. Run after provisioning/deployment and
  before dependent suites.
- **Sanity:** prove the requested feature/flow coherently works after the change. This is the
  primary `test-product` execution goal.
- **Targeted regression:** cover likely blast radius, shared rules, callers, contracts, and
  prior defects.
- **Full regression:** run for release/high-risk/full-ride needs after faster feedback.

If smoke fails, stop dependent suites. If sanity finds High/Critical impact, stop according to
the defect policy.

## Automation quality

- Arrange/Given: create owned state and data.
- Act/When: use public behavior.
- Assert/Then: check meaningful output, side effects, and forbidden effects.
- Clean up in teardown that still runs after failure.
- Avoid fixed sleeps; wait on observable conditions with bounded timeouts.
- Preserve random seeds and exact versions.
- Distinguish product failure, test defect, environment failure, and flaky result.
- Do not convert a failure to pass with retries; label it flaky and investigate evidence.

For browser E2E:

- test user-visible behavior;
- isolate browser/session/data per test;
- prefer role/label/text/test-id contracts over CSS/XPath structure;
- use web-first assertions and automatic waiting;
- collect trace/screenshot/network evidence on failure;
- select browsers/devices from supported users and risk, not “all” blindly.

Official Playwright guidance: <https://playwright.dev/docs/best-practices>.

## CI/CD

Inspect existing pipelines before changing them. Recommend:

- fast static/unit checks on commits;
- integration/contract checks on pull requests;
- smoke after deployment;
- E2E/regression at risk-appropriate gates;
- scheduled security/performance/soak work when too expensive per PR.

Do not modify CI configuration without user approval. Record the local command and CI job that
produced each result.

## Coverage

Measure statement/branch/path coverage only when the project supports it. Coverage identifies
unexercised code; it does not prove correct assertions or requirement coverage. Report it beside
RTM coverage, mutation results when used, and residual risk.
