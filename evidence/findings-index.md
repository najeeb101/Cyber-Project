# Evidence Index

All evidence captured 2026-10-28 against OWASP Juice Shop 20.3.0 on `127.0.0.1:3000` (isolated local lab). No credentials were used.

| Evidence ID | Filename | Finding/use case | What it proves | Sanitized | Owner |
|---|---|---|---|---|---|
| ENV-001 | `evidence/environment/baseline-health.txt` | Environment | Juice Shop container is running, image digest recorded, baseline response headers captured | Yes (no cookies/tokens) | Member 2 |
| ENV-002 | `evidence/environment/isolation-check.txt` | Environment | Port bound to loopback only; target unreachable via the host's LAN address. Second-device check still recommended | Yes | Member 2 |
| EV-001 | `evidence/reconnaissance/EV-001-nmap-local-baseline.txt` | Reconnaissance (TC-001) | Only port 3000 scanned on loopback; open and returning HTTP 200 from Juice Shop (Nmap fingerprint miss reported as `ppp?`) | Yes | Member 2 |
| EV-002 | `evidence/automated-scans/EV-002-zap-scan-raw.html` (+ `zap-console.log`) | Reconnaissance / WA-001, WA-002 | ZAP 2.17.0 baseline scan results; scanner output only, alerts count as confirmed only where manually verified | Raw report; no cookies, tokens, or passwords were found during the recorded keyword check; manual verification is documented separately | Member 3 |
| WA-001 evidence | `evidence/manual-tests/WA-001-csp-headers.txt` | WA-001 | `Content-Security-Policy` header is absent from `/` | Yes | Member 3 |
| WA-002 evidence | `evidence/manual-tests/WA-002-cors-headers.txt` | WA-002 | `Access-Control-Allow-Origin: *` returned for a foreign `Origin` | Yes | Member 3 |
| WA-003 evidence | `evidence/manual-tests/WA-003-ftp-exposure.txt` | WA-003 | Unauthenticated `/ftp` listing and file download headers (file contents deliberately not stored) | Yes | Member 3 |
| WA-004 evidence | `evidence/manual-tests/WA-004-idor-basket.txt` | WA-004 | Two-account IDOR test: user B's token retrieves user A's basket via `/rest/basket/:id` | Yes (JWTs redacted) | Member 3 |
| EV-003 | `evidence/05-remediation-retest/WA-001-before.txt`, `WA-001-after.txt`, `retest-record.md` | WA-001 retest | Direct access lacks CSP; proxy access returns the CSP header while preserving HTTP 200 and page length | Yes | Member 3 |
| ENV-003 | `evidence/06-screenshots/ENV-003-juice-shop-home.png` | Environment | Live capture (2026-10-30): Juice Shop healthy on `127.0.0.1:3000` | Yes (no session) | Member 2 |
| EV-002 screenshot | `evidence/06-screenshots/EV-002-zap-alert-summary.png` | WA-001, WA-002 | Capture of the saved ZAP report's alert summary (0 High, 2 Medium, 3 Informational) | Yes | Member 3 |
| WA-003 screenshot | `evidence/06-screenshots/WA-003-ftp-listing.png` | WA-003 | Live capture (2026-10-30): unauthenticated `/ftp` listing with 11 entries; no file opened | Yes | Member 3 |

Report figures in `report/figures/` render the unaltered text of the evidence files above as
terminal-style panels, and include the architecture diagram. They are produced by
`source/report-figures/capture.js`.
