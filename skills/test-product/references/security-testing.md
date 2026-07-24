# Security Testing

Read when the scope includes identity, authorization, sensitive data, money, uploads, public
input/APIs, external providers, privileged actions, deployment controls, or a security/release
gate. Selection never authorizes active exploitation.

## 1. Build the threat and control model

Use four questions:

1. What are we working on?
2. What can go wrong?
3. What controls should prevent or detect it?
4. How will we prove the control safely?

Map:

`actor → entry point → process/service → data store/provider → output`

Mark assets, roles/tenants, trust boundaries, sensitive data, secrets, privileged operations,
dependencies, and audit/monitoring. For each threat record:

```text
Threat ID / asset / actor and prerequisites
Boundary and abuse action
Impact/exposure
Control hypothesis
Safe probe
Allow/deny, required-effect, forbidden-effect, and audit oracle
Evidence and redaction
```

Use STRIDE only as a prompt: spoofing, tampering, repudiation, information disclosure,
denial of service, and elevation of privilege. Add product-specific abuse cases such as
workflow bypass, coupon replay, cross-tenant object access, double spend, or order/payment
mismatch.

## 2. Select requirements and test modes

Use the project standard first. Otherwise use OWASP ASVS as a requirement catalog, pin exact
version and IDs such as `v5.0.0-<requirement>`, select controls by the actual asset/flow, and
use WSTG procedures for relevant web/API probes. Map selected controls to the RTM. An
unselected ASVS row is not a failure; a scanner result is not a control pass.

Build an applicability inventory before selection:

| Domain | Minimum question |
|---|---|
| Architecture/config | are boundaries, defaults, exposed services, and deployment controls sound? |
| Encoding/validation | can untrusted data change code/query/path/parser meaning? |
| Files/resources | can uploads, URLs, archives, or identifiers escape intended scope? |
| Authentication | are identity proof, recovery, and anti-enumeration adequate? |
| Session/tokens | are creation, rotation, expiry, revocation, replay, and storage safe? |
| Authorization | are function/object/tenant decisions authoritative on every path? |
| Data/privacy | is sensitive data minimized and protected throughout its lifecycle? |
| Crypto/secrets | are approved primitives, key/secret sources, and rotation used correctly? |
| Communications | are transport trust, certificates, origins, and provider channels controlled? |
| Business logic | can sequence, replay, concurrency, quota, or unknown outcome break invariants? |
| API/service | are schema, mass assignment, errors, pagination, rate, and identity safe? |
| Client/browser | are output, DOM, storage, navigation, messaging, and UI boundaries safe? |
| Logging/audit | are events useful without leakage and is abuse/failure detectable? |
| Dependencies/supply chain | are versions, provenance, reachability, images, and builds governed? |
| Availability | are resource limits and abuse protections adequate for the risk? |

For every domain record applicability, source, controls, inherent risk, selection, evidence,
and residual risk. A security/release gate requires every applicable Critical/High control to
be selected and terminal. A missing normative requirement baseline blocks a broad conformance
claim; it never permits an artificially small green subset.

| Mode | Purpose | Default authority |
|---|---|---|
| Threat/architecture review | boundaries, abuse paths, missing controls | read-only |
| Code/config review | auth, validation, secrets, crypto, logs | read-only |
| SAST/secrets/IaC/container scan | candidate code/config issues | approved local tooling |
| SCA | vulnerable dependencies and reachable exposure | approved local tooling |
| Safe dynamic verification | controlled allow/deny and malformed input | approved isolated target |
| Exploitation/fuzz/DoS | validate exploitability/resource exhaustion | action-specific approval |

## 3. Derive the minimum case set

### Authentication and session

Model account/session/token states. Cover valid, invalid, expired, revoked, replayed, and
malformed credentials; enumeration; rate/lock behavior; session rotation/logout; recovery;
MFA/passkey/provider failure. Assert no secret/token leakage and correct audit.

### Authorization

Build `actor/role × tenant/ownership × resource state × action` decision table. For every
denial assert:

- denial occurs at the authoritative boundary;
- no durable mutation/downstream effect;
- no protected data in response, headers, cache, URL, error, timing detail, or log;
- audit/detection occurs as required;
- alternate/bulk/object-ID/background paths cannot bypass the rule.

Cover horizontal and vertical privilege, stale roles/sessions, indirect references, and batch
endpoints using only synthetic records.

### Input, parsing, output, and files

Use partitions/boundaries plus safely encoded malicious classes for injection, path
traversal, unsafe deserialization, SSRF, mass assignment, parser differences, and output
encoding where applicable. Test the server directly; client validation is not a boundary.

For uploads cover type/content mismatch, size/count/name/path, archive nesting, malware-scan
state, processing failure, storage permission, public access, and retention/deletion. Keep
payloads in an isolated system.

### Data, secrets, crypto, logs, and errors

Trace collection, transport, storage, cache, backup, logs, analytics, and deletion. Verify
minimum exposure, required TLS/crypto configuration, approved secret source/rotation, redacted
logs, safe errors, and tenant-scoped caching. Verify project-required algorithms/configuration;
do not improvise cryptanalysis.

### Business abuse, dependencies, and deployment

Cover skipped/repeated/reordered workflow steps, replay, concurrency, quota/rate evasion,
price/quantity/state tampering, and unknown outcomes. Assert the business invariant.

Review lock/reachability of dependencies, image/runtime support, exposed services, debug
modes, CORS/security headers, storage/network permissions, secret injection, and environment
drift.

## 4. Execute and validate safely

For each probe:

1. confirm target, scope, account/data, payload class, and prohibited effects;
2. establish an authorized control case;
3. run the smallest safe negative/abuse probe;
4. observe response, durable state, downstream effects, data exposure, and audit;
5. repeat only enough for reproducibility;
6. exclude proxy/cache/harness/config false positives;
7. preserve sanitized evidence and cleanup;
8. report immediately.

Do not retrieve real sensitive data to prove access; a synthetic cross-tenant record is
enough. Stop on real-data access, privilege escalation, uncontrolled mutation, service
degradation, or unsafe payload propagation.

## 5. Severity, evidence, and exit

Assess confidentiality/integrity/availability/safety/money impact, sensitivity, affected
scope, exploitability, prerequisites/privilege/user interaction, persistence, detectability,
recovery, and credible chaining.

Confirmed cross-tenant sensitive access, critical privilege bypass, practical secret
exposure, uncontrolled code execution, or data corruption is at least High and often
Critical. Product severity and remediation priority remain separate.

Evidence includes exact build/target, threat/control/probe ID, test identities, action,
response/state/audit, timestamps/correlation, tool/ruleset versions, reproduction, redaction,
and cleanup. Never archive credentials, personal data, real customer records, or reusable
exploit material outside the approved lab.

Security domain result is `Passed` only when every Required selected control at every severity
is Passed, material tool findings are triaged, all applicable Critical/High controls are
selected, no material applicable control is silently omitted, artifacts are redacted, and
untested controls/residual risk are explicit. A failed Medium/Low control makes the domain
result `Failed` and requires the global defect/verdict rules; it cannot produce plain Ready.
Security control coverage =
`evaluated applicable controls / all applicable controls`, segmented by risk/domain. This
never means “secure against everything.”

Research basis: OWASP ASVS 5.0.0, WSTG, and the OWASP threat-modeling four-question framework:
<https://owasp.org/www-project-application-security-verification-standard/>,
<https://owasp.org/www-project-web-security-testing-guide/latest/>, and
<https://owasp.org/www-project-threat-modeling/>. All operating rules are local above.
