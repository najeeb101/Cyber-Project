# Q&A Preparation Sheet

Likely assessor questions and concise, honest answers grounded in this project's evidence.
Every team member should be able to answer any of these. Keep answers short; point to the
evidence file when asked for proof.

---

## A. Scope, safety and methodology

**Q1. What exactly did you test, and how did you keep it safe?**
A single intentionally vulnerable app, OWASP Juice Shop 20.3.0, in Docker bound to
`127.0.0.1:3000` only. Nothing public was touched. We used synthetic accounts
(`synth.a@lab.test`, `synth.b@lab.test`), no real data, no DoS, no destructive payloads.
Isolation is evidenced in `evidence/environment/isolation-check.txt`.

**Q2. Which methodology did you follow?**
OWASP WSTG for test selection and PTES phases (scope → recon → scanning → manual
verification → reporting). Scope and authorization are in `planning/scope-and-authorization.md`;
the test cases are in `planning/test-case-matrix.md`.

**Q3. How did you decide which findings to report?**
We only reported findings we could manually reproduce. Scanner alerts were treated as leads,
not confirmed vulnerabilities, until verified by hand. We selected four across two OWASP 2025
categories (A01 Broken Access Control, A02 Security Misconfiguration).

**Q4. How do you know the target was really isolated?**
The container is published to `127.0.0.1:3000`, not `0.0.0.0`, so it is not reachable from
the LAN. We recommend (and partly verified) a second-device check that the host IP:3000 does
not respond — noted as a limitation in the isolation record.

---

## B. The findings

**Q5. Walk me through your strongest finding.**
WA-003: an unauthenticated GET to `/ftp` returns a directory listing of 11 internal files,
including backup files and a KeePass credential store (`incident-support.kdbx`), all
downloadable without login. CVSS v3.1 ~7.5 (High). We deliberately did **not** copy the file
contents into evidence. See `findings/WA-003.md`.

**Q6. Explain the IDOR (WA-004). How did you prove it?**
We created two synthetic accounts. Logged in as user B (holding B's own valid JWT), we
requested `GET /rest/basket/6` — the basket belonging to user A — by changing the id in the
URL. The server returned HTTP 200 and A's basket (`"UserId":25`) to B (`"UserId":26`). So the
endpoint authenticates the caller but does not authorize them against the specific object.
Evidence: `evidence/manual-tests/WA-004-idor-basket.txt`.

**Q7. Why is "missing CSP" (WA-001) a finding if it is not directly exploitable?**
It is a defense-in-depth gap: on its own it has no direct impact, but it removes a control
that would limit the damage of any injection flaw. We rated it Low–Medium and were explicit
that its risk depends on a separate XSS existing. It is also the finding we remediated.

**Q8. Is the CORS finding (WA-002) actually serious?**
We rated it Low. The wildcard `Access-Control-Allow-Origin: *` means any site can read
responses, but browsers will not send credentials with a wildcard origin, so only
non-sensitive, non-credentialed data is exposed. We did not demonstrate a credentialed
cross-origin read, and we say so — we did not overclaim it.

**Q9. Did your scanner find all of these?**
No. ZAP flagged the CSP and CORS issues (WA-001, WA-002). The `/ftp` exposure and the IDOR
(WA-003, WA-004) came from manual testing based on app behaviour — the scanner did not report
them in the quick scan. This is our automated-vs-manual comparison point.

---

## C. Risk, CVSS and remediation

**Q10. How did you score severity?**
CVSS v3.1 base scores with the full vector recorded (reproducible), plus a qualitative
Likelihood × Impact rating for this training context. Where they differ (WA-001, WA-002) we
showed both and explained the downward adjustment rather than changing the vector. See
`report/risk-register-and-cvss.md`.

**Q11. Show me a fix that actually works.**
WA-001. We put an nginx reverse proxy in front of Juice Shop on loopback that injects a
restrictive `Content-Security-Policy` header. Before (`:3000`): no CSP. After (`:8080`): CSP
present, same page served (`Content-Length` unchanged, so the app still works). Evidence:
`evidence/05-remediation-retest/` (before/after `.txt` and `.png`, plus `retest-record.md`).

**Q12. Why fix it at a reverse proxy instead of in the app?**
The Juice Shop image is prebuilt; editing it for a demo is fragile. In production, security
headers are commonly added at the web tier (reverse proxy / WAF / middleware), so this mirrors
a realistic fix and is fully reversible for the lab.

**Q13. What is the limitation of your fix?**
It enforces CSP only for traffic through the proxy (`:8080`); the direct port (`:3000`) still
lacks it because we keep both open for a clear before/after. In production the app would only
be reachable through the proxy. We state this in the retest record.

---

## D. Limitations and integrity

**Q14. What did you NOT test or prove?**
IDOR write/tamper paths and other object types (only `GET /rest/basket/:id` was confirmed);
credentialed cross-origin reads for CORS; the contents or crackability of the `/ftp` files.
These are listed as limitations in each finding and are not claimed as confirmed.

**Q15. How did you avoid false positives?**
Every reported finding was reproduced manually with a recorded request/response. Scanner-only
alerts that we could not reproduce were not promoted to findings.

**Q16. How did you handle sensitive data in evidence?**
Synthetic accounts only; JWTs redacted in captures; `/ftp` file contents never stored. The
sanitization status of each evidence item is tracked in `evidence/findings-index.md`.

---

## E. Teamwork and process

**Q17. Who did what?**
Member 1 methodology/coordination, Member 2 lab/environment, Member 3 testing/evidence,
Member 4 risk/remediation/report/media. Ownership and reviewers are in the finding-ownership
matrix (`TEAM_TASKS.md` §10); decisions are logged in §11.

**Q18. If you had more time, what next?**
Remediate and retest WA-003 and WA-004 (highest risk), add a cross-origin PoC for CORS, and
complete the second-device isolation check.

---

## F. Quick-reference numbers

| Item | Value |
|---|---|
| Target | OWASP Juice Shop 20.3.0, Docker, `127.0.0.1:3000` |
| Findings | 4 (WA-001..004), 2 High / 1 Low–Medium / 1 Low |
| Tools | Nmap 7.993, OWASP ZAP 2.17.0, browser dev tools, curl |
| Remediated + retested | WA-001 (missing CSP) |
| Highest severity | WA-003 `/ftp` exposure, CVSS ~7.5 |
