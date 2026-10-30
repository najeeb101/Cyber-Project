# Safe Vulnerability Assessment of an Intentionally Vulnerable Web Application (OWASP Juice Shop)

> **Draft — Markdown.** Convert to MS Word for submission. Keep the main body (sections 2–11)
> at or below **3,500 words**; the current draft is ~3,150. The Appendix has no word limit.
> `TODO` markers flag the few items only the team can supply (approval dates, reflections).

---

## 1. Cover page *(excluded from word count)*

- **Title:** Safe Vulnerability Assessment of an Intentionally Vulnerable Web Application (OWASP Juice Shop)
- **Course / semester:** CMPS 380 Cybersecurity Fundamentals — Fall 2026
- **Group ID:** G02
- **Members:**
  - Najeeb Abdi — 202307172 — 25%
  - Mohanad Elhabash — 202314448 — 25%
  - Moaaz Mohamed — 202207862 — 25%
  - Ahmed Hari — 202203669 — 25%
- **Contribution total:** 100%
- **Main-report word count:** `TODO: fill after final edit`
- **Submission date:** `TODO` (deadline: 14 November 2026)

---

## 2. Introduction and motivation

Web applications are among the most exposed components of modern systems: they are reachable
over the network, process untrusted input, and mediate access to user data. The OWASP Top
10:2025 continues to rank Broken Access Control (A01) and Security Misconfiguration (A02)
among the most prevalent risk categories, with Security Misconfiguration rising to second
place this edition [1]. Because a single control failure can expose many users, assessing web
applications before and during deployment is a core defensive practice.

No single technique finds every weakness. Automated scanners quickly surface broad classes of
issue but produce false positives and miss logic flaws; manual testing confirms real impact
but is slower. A layered assessment — reconnaissance, automated scanning, and manual
verification — therefore gives more reliable results than any one method alone, and lets a
team separate confirmed vulnerabilities from unverified scanner alerts.

The problem this project addresses is practical: given a realistic vulnerable web application,
can a small team safely identify, verify, prioritise, and remediate real weaknesses using
industry methodology, while producing defensible evidence? To do this ethically we worked only
inside an isolated local lab against a deliberately vulnerable training target, OWASP Juice
Shop [2], using synthetic accounts and non-destructive techniques. No public, university, or
third-party system was touched. This controlled-lab context is what makes offensive techniques
appropriate here: the activity is authorised, contained, and reversible.

## 3. Objectives and research question

**Main objective:** perform a safe, methodical security assessment of OWASP Juice Shop in an
isolated lab and demonstrate the full cycle from discovery to remediation and retest.

**Sub-objectives (measurable):**

1. Build and verify an isolated, reproducible lab bound to loopback only.
2. Use at least two assessment approaches (automated and manual).
3. Reproduce three to five findings manually, each with sanitized evidence.
4. Prioritise findings using CVSS-informed reasoning.
5. Remediate and retest at least one finding with before/after evidence.

**Research question:** *Can a layered, safe assessment of an intentionally vulnerable web
application reliably distinguish confirmed, reproducible vulnerabilities from automated-scanner
noise, and demonstrate an effective remediation?*

**Success criteria:** an isolated lab; ≥2 approaches; ≥3 verified findings with evidence and a
reviewer; ≥1 remediated-and-retested finding; and an honest statement of limitations.

## 4. Application, use cases, and threat model

**Why Juice Shop.** OWASP Juice Shop is a widely used, deliberately insecure application built
for security training [2]. It contains realistic modern vulnerabilities, ships with synthetic
data, and can run fully offline in Docker, which makes it ideal for a safe, authorised
assessment.

**Synthetic roles and assets.** We modelled four actors — unauthenticated visitor, normal
synthetic user, privileged synthetic user, and authorised tester — and the assets they touch:
synthetic accounts, session tokens (JWT), test order/basket data, and application integrity and
availability. Trust boundaries are: browser → application; one user → another user's objects;
normal user → privileged functions; and application → local data store.

**Selected scenarios.** From the threat model we defined five scenarios, each mapped to a test
case and a finding record: S1 attack-surface discovery, S2 broken access control / IDOR, S3
cross-site scripting / input validation, S4 security misconfiguration / information disclosure,
and S5 (optional) authentication/session review. Scenarios define what we looked for; only
reproduced results are reported as findings.

**Scope and authorization.** All activity was limited to `http://127.0.0.1:3000`, using
synthetic accounts and non-destructive proof-of-concept steps. Out of scope: any public,
university, or cloud system; real data; denial-of-service; credential theft; malware; and
container escape. The full scope, isolation controls, and the team authorization statement are
in the project's scope document and are summarised in §6.

## 5. Methodology

We followed a layered process aligned with the OWASP Web Security Testing Guide (WSTG) [3] and
the phases of the Penetration Testing Execution Standard (PTES) [4]:

1. **Scope and authorization** — fix the target, boundaries, and safety rules before any test.
2. **Reconnaissance** — safe local service/version discovery to map the attack surface.
3. **Automated scanning** — a controlled OWASP ZAP baseline scan to surface candidate issues.
4. **Manual verification** — reproduce each candidate by hand with recorded request/response
   pairs; discard what cannot be reproduced.
5. **Risk analysis** — score confirmed findings with CVSS v3.1 plus a qualitative risk rating.
6. **Remediation and retest** — apply a defensive fix and repeat the test for before/after.

Two safety controls ran throughout: the target was bound to loopback only, and every captured
artefact was sanitized (synthetic accounts, redacted tokens, no sensitive file contents
copied). Scanner alerts were treated as leads, never as confirmed vulnerabilities, until
manually verified — the core of our automated-versus-manual comparison.

## 6. Lab environment and tools

The lab ran on Windows 11 Pro (build 10.0.26300) with Docker Engine 29.9.1. The target was
OWASP Juice Shop 20.3.0 (`bkimminich/juice-shop`, digest `sha256:4284…53f4`), published to
`127.0.0.1:3000` only. Testing tools were Nmap 7.993 (with Npcap 1.90) for discovery, OWASP ZAP
2.17.0 for automated scanning, Google Chrome 156 developer tools and `curl` for manual
verification, and a small custom Python script for evidence handling. Burp Suite and Nikto were
available but not needed, so they are recorded as "not used" rather than claimed.

**Why these tools.** Nmap confirms which ports/services are exposed; ZAP gives broad automated
coverage of common web issues; browser dev tools and `curl` give precise, scriptable manual
control for proof-of-concept. Each has limits: Nmap may misfingerprint an app (it reported our
HTTP service as `ppp?`); ZAP produces false positives and misses logic flaws; manual testing is
narrow by design. Using them together offsets these individual weaknesses.

**Isolation controls.** We verified three things on 2026-10-28: the container publishes to
`3000/tcp -> 127.0.0.1:3000` (loopback, not `0.0.0.0`); the app answers `HTTP/1.1 200 OK` on
loopback; and a request to the host's LAN IP (`192.168.199.1:3000`) failed (HTTP 000), showing
the target was not reachable off-host. A confirmatory check from a second physical device
remains recommended and is noted as a limitation.

## 7. Verified findings and proof of concepts

Four findings were reproduced manually. Long console output is in the Appendix; each finding
below references its sanitized evidence file.

| ID | Finding | OWASP 2025 | CVSS v3.1 | Overall risk | Status |
|---|---|---|---|---|---|
| WA-003 | Unauthenticated `/ftp` directory listing exposes internal files | A02 (also A01) | 7.5 High | High | Open |
| WA-004 | IDOR on `/rest/basket/:id` — read another user's basket | A01 | 6.5 Medium | High | Open |
| WA-001 | Missing Content-Security-Policy header | A02 | 4.3 (indicative) | Low–Medium | **Remediated + retested** |
| WA-002 | Overly permissive CORS (`Access-Control-Allow-Origin: *`) | A02 | 5.3 base | Low | Open |

**WA-003 — Unauthenticated `/ftp` directory listing.** An unauthenticated `GET /ftp` returns
an HTTP 200 directory listing of 11 internal files, including backup files and a KeePass
credential store (`incident-support.kdbx`); files download without any login (HTTP 200 on
`/ftp/acquisitions.md`). We deliberately did **not** copy file contents into evidence. Expected
behaviour: internal/backup/credential files are not web-served and listing is disabled. This is
our highest-impact finding. *Evidence: `WA-003-ftp-exposure.txt`.*

**WA-004 — IDOR on `/rest/basket/:id`.** Using two independently created synthetic accounts, we
logged in as user B (basket 7) and requested `GET /rest/basket/6`, user A's basket, by
substituting the id. The server returned HTTP 200 and A's basket object (`"UserId":25`) to B
(`"UserId":26`). A request with no/invalid token is correctly rejected with 401, so the
endpoint authenticates the caller but does not authorise them against the requested object —
a textbook insecure direct object reference [5]. Ids were low sequential integers, making
enumeration trivial. *Evidence: `WA-004-idor-basket.txt`.*

**WA-001 — Missing Content-Security-Policy header.** HTTP responses omit a `Content-Security-
Policy` header, so the browser applies no policy restricting where scripts may load from [6].
Alone this is a defense-in-depth gap rather than a direct exploit; its risk is that it would
amplify any injection flaw. This is the finding we remediated (§9). *Evidence:
`WA-001-csp-headers.txt`.*

**WA-002 — Overly permissive CORS.** The server returns `Access-Control-Allow-Origin: *`,
including for a request carrying a foreign `Origin` header [7]. Because browsers do not send
credentials with a wildcard origin, only non-credentialed, non-sensitive data is cross-origin
readable, so we rated this Low and did not overclaim it. *Evidence: `WA-002-cors-headers.txt`.*

**Automated vs manual.** ZAP flagged WA-001 and WA-002. WA-003 and WA-004 were found by manual
testing and were not reported by the ZAP quick scan — direct evidence that automated tools
alone would have missed our two highest-risk findings.

## 8. Risk analysis and CVSS reasoning

Each finding was scored with a CVSS v3.1 base vector (reproducible) and a qualitative
Likelihood × Impact rating for this training context; where the two differ we show both rather
than bending the vector to a label [8].

- **WA-003** `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` = **7.5 High.** Trivial, unauthenticated;
  exposes sensitive internal files. Likelihood High × Impact High → High.
- **WA-004** `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` = **6.5 Medium.** Any authenticated user can
  read another's object; ids are guessable. Integrity scored None because write/tamper paths
  were not tested. Likelihood High × Impact Medium–High → High overall.
- **WA-001** indicative `…/UI:R/…/C:L/I:N/A:N` ≈ **4.3.** No direct impact alone; a purist
  scoring is Informational until an XSS is confirmed. Qualitative Low–Medium as an amplifier.
- **WA-002** `…/C:L/I:N/A:N` base **5.3**, adjusted down to qualitative **Low** because no
  credentialed cross-origin read was demonstrated.

The full per-metric justification is in the project risk register. Technical severity (CVSS)
and business risk can diverge: WA-001 scores "Medium" mechanically but carries little
standalone business risk, whereas WA-003's exposure of a credential store is a real business
concern consistent with its High score.

## 9. Remediation and retesting

We remediated **WA-001**. Rather than modify the prebuilt image, we placed an nginx reverse
proxy in front of Juice Shop on loopback that injects a restrictive policy:
`default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;
frame-ancestors 'self'; object-src 'none'`. This mirrors how security headers are added in
production (web tier / WAF / middleware) and is fully reversible.

**Before/after.** Direct access (`:3000`) returned no CSP header; access through the proxy
(`:8080`) returned the policy above, with the same page served (`Content-Length` 9984 unchanged)
confirming the application still worked. Evidence: before/after `curl` captures and response-
header images in `evidence/05-remediation-retest/`, with a signed retest record.

**Residual risk.** The policy uses `style-src 'unsafe-inline'` because Juice Shop's Angular
front end relies on inline styles; a greenfield app would use nonces or hashes. The fix also
enforces CSP only for traffic through the proxy — acceptable in the lab, where both ports stay
open for comparison, and in production the app would be reachable only via the proxy.

## 10. Impact, learning outcomes, and limitations

**Impact on security practice.** The project shows, end to end, how a small team can safely
convert a vulnerable application into verified findings, prioritised risk, and a demonstrated
fix. The clearest lesson for developers is defence in depth: WA-001 (missing CSP) has no direct
impact yet would magnify any injection bug, so controls should be layered, not relied on singly.

**Benefit to stakeholders.** Developers learn to enforce server-side authorization on every
object request (WA-004) and to keep backup and credential files out of any web-served path
(WA-003). Testers gain a repeatable, evidence-first workflow. Users ultimately benefit from the
reduced exposure of their data.

**Possible misuse and safeguards.** The same techniques could be abused against systems without
permission. Our safeguards were strict scope, loopback-only isolation, synthetic data, non-
destructive proofs, and refusal to store sensitive file contents — the controls that separate
authorised assessment from attack.

**What others can learn / novelty.** The novel element is not the vulnerabilities (expected in
a training app) but the disciplined separation of *confirmed* findings from scanner noise, and
a remediation chosen to be realistic and reversible. Two of our four findings were manual-only,
making the automated-versus-manual contrast concrete.

**Honest limitations.** Scores are indicative, from a training app with synthetic data, not a
production risk assessment. We confirmed only the specific paths tested: IDOR write/tamper and
other object types were not tested; no credentialed cross-origin CORS read was demonstrated; the
contents/crackability of the `/ftp` files were not analysed. The planned XSS scenario (S3) was
not reproduced and so is reported as untested, not as a finding. The second-device isolation
check is still recommended. These are stated so nothing is overclaimed.

## 11. Conclusion

A layered, safe assessment reliably separated confirmed, reproducible vulnerabilities from
scanner noise: four findings were manually verified, two of them (the highest-risk) found only
by hand, and one was remediated and retested with clear before/after evidence — answering the
research question affirmatively. The strongest evidence is the reproduced `/ftp` exposure and
the two-account IDOR proof. In a real authorised engagement the team would next remediate and
retest WA-003 and WA-004, add a cross-origin proof-of-concept for the CORS issue, and complete
independent isolation verification before widening scope.

## 12. References

1. OWASP. *OWASP Top 10:2025.* https://top10.owasp.org/2025/
2. OWASP. *OWASP Juice Shop Project.* https://owasp.org/www-project-juice-shop/
3. OWASP. *Web Security Testing Guide (WSTG).* https://owasp.org/www-project-web-security-testing-guide/
4. Penetration Testing Execution Standard (PTES). http://www.pentest-standard.org/
5. OWASP. *Insecure Direct Object Reference Prevention Cheat Sheet.* https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
6. MDN Web Docs. *Content-Security-Policy.* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
7. MDN Web Docs. *Cross-Origin Resource Sharing (CORS).* https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
8. FIRST. *CVSS v3.1 Specification Document.* https://www.first.org/cvss/v3.1/specification-document

> Verify every URL and access date before submission, and match each in-text `[n]` to this list.

---

## Appendix (no word limit)

- **Appendix A: Individual reflections** — one distinct section per member (name, QUID, role,
  tasks done, a problem faced and how it was solved, what was learned, honest %). **`TODO`: each
  member writes their own; reflections must differ and describe real work.**
- **Appendix B: User manual** — see `environment/setup-commands.md` and `environment/troubleshooting.md`.
- **Appendix C: Commands and environment setup** — `environment/` (inventory, setup commands).
- **Appendix D: Source code and attribution** — `source/custom-script/` (custom evidence toolkit) and the Docker run command in §6.
- **Appendix E: Screenshots, logs, and evidence index** — `evidence/findings-index.md`.
- **Appendix F: Similarity and attribution log** — `TODO`: source, date accessed, what was reused, where cited, what was rewritten (seed from `references.md`).
