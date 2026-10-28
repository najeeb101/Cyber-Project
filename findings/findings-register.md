# Findings Register

| ID | Finding | OWASP category | Severity | Confidence | Evidence | Remediation | Retested | Owner |
|---|---|---|---|---|---|---|---|---|
| WA-001 | Missing Content-Security-Policy header | A02:2025 Security Misconfiguration | Low to Medium | High | `evidence/manual-tests/WA-001-csp-headers.txt`, `EV-002` ZAP report | Add restrictive CSP header | Pending | Member 3 |
| WA-002 | Overly permissive CORS (`Access-Control-Allow-Origin: *`) | A02:2025 Security Misconfiguration | Low | High | `evidence/manual-tests/WA-002-cors-headers.txt`, `EV-002` ZAP report | Origin allow-list | Pending | Member 3 |
| WA-003 | Unauthenticated `/ftp` directory listing exposes internal files | A02:2025 Security Misconfiguration / A01:2025 Broken Access Control | High (indicative) | High | `evidence/manual-tests/WA-003-ftp-exposure.txt` | Remove route or require authentication; disable listing | Pending | Member 3 |
| WA-004 | Broken object-level access control (IDOR) on `/rest/basket/:id` | A01:2025 Broken Access Control | Medium to High (indicative) | High | `evidence/manual-tests/WA-004-idor-basket.txt` | Verify basket ownership server-side before returning/modifying data | Pending | Member 3 |
