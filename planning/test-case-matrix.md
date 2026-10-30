# Test Case Matrix

Planned test cases mapped to the threat-model scenarios. "Expected result"
describes what a secure application *should* do. "Actual result" and "Evidence"
stay `Pending` until the team runs the test in its own lab and records real
output — never fill them with assumed results.

| Test ID | Use case | Tool/method | Expected result (secure behavior) | Actual result | Evidence | Owner | Status |
|---|---|---|---|---|---|---|---|
| TC-001 | S1: Attack-surface discovery | Nmap `-sT -sV -Pn -p 3000` against `127.0.0.1`; ZAP quick scan (spider + active) | Only the intended app port is exposed; no unexpected services | Port 3000/tcp open, HTTP 200 from Juice Shop (Nmap fingerprint miss reported as `ppp?`). ZAP: 0 High, 2 Medium, 3 Informational | `EV-001-nmap-local-baseline.txt`, `EV-002-zap-scan-raw.html` | Member 3 | Done |
| TC-002 | S2: Broken access control / IDOR | Two synthetic accounts; replay a request for another user's object with curl | Server rejects access to objects the user does not own (403/empty) | Confirmed vulnerable: `GET /rest/basket/:id` returns another user's basket (HTTP 200) → **WA-004** | `WA-004-idor-basket.txt` | Member 3 | Done |
| TC-003 | S3: Cross-site scripting | Submit a harmless marker payload into a user input; observe rendering | Input is encoded/escaped and does not execute as script | Not executed. ZAP's quick scan raised no XSS alert; no manual XSS test was recorded | None | Member 3 | Not executed (limitation) |
| TC-004 | S4: Misconfiguration / info disclosure | ZAP + manual curl; inspect response headers and exposed paths | No sensitive file/directory exposure; expected security headers present; CORS restricted to trusted origins | Confirmed: no CSP header → **WA-001**; `Access-Control-Allow-Origin: *` → **WA-002**; unauthenticated `/ftp` listing → **WA-003** | `WA-001-csp-headers.txt`, `WA-002-cors-headers.txt`, `WA-003-ftp-exposure.txt` | Member 3 | Done |
| TC-005 (optional) | S5: Authentication / session review | Browser dev tools; ZAP passive inspection of cookies/JWT | Secure cookie flags, sensible token lifetime, proper logout/invalidation | Not executed | None | Member 3 | Not executed (optional) |

Every "marker payload" must be the smallest non-destructive proof (for example a
harmless string), never anything that alters or deletes data.
