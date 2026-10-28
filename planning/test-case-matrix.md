# Test Case Matrix

Planned test cases mapped to the threat-model scenarios. "Expected result"
describes what a secure application *should* do. "Actual result" and "Evidence"
stay `Pending` until the team runs the test in its own lab and records real
output — never fill them with assumed results.

| Test ID | Use case | Tool/method | Expected result (secure behavior) | Actual result | Evidence | Owner | Status |
|---|---|---|---|---|---|---|---|
| TC-001 | S1: Attack-surface discovery | Nmap `-sV` against `127.0.0.1:3000`; ZAP passive crawl | Only the intended app port is exposed; no unexpected services | Pending | Pending (`EV-00x-nmap-local-baseline.txt`) | Member 3 | Planned |
| TC-002 | S2: Broken access control / IDOR | Two synthetic accounts; replay a request for another user's object with Burp/ZAP | Server rejects access to objects the user does not own (403/empty) | Pending | Pending (`WA-001-*`) | Member 3 | Planned |
| TC-003 | S3: Cross-site scripting | Submit a harmless marker payload into a user input; observe rendering | Input is encoded/escaped and does not execute as script | Pending | Pending (`WA-002-*`) | Member 3 | Planned |
| TC-004 | S4: Misconfiguration / info disclosure | ZAP + optional Nikto; inspect response headers and error pages | No sensitive version/stack/error disclosure; expected security headers present | Pending | Pending (`WA-003-*`) | Member 3 | Planned |
| TC-005 (optional) | S5: Authentication / session review | Browser dev tools; ZAP passive inspection of cookies/JWT | Secure cookie flags, sensible token lifetime, proper logout/invalidation | Pending | Pending | Member 3 | Planned |

Every "marker payload" must be the smallest non-destructive proof (for example a
harmless string), never anything that alters or deletes data.
