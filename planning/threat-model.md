# Threat Model

## Assets

- Synthetic user accounts
- Session data
- Test profile/order data
- Application integrity
- Application availability

## Actors

- Unauthenticated visitor
- Normal synthetic user
- Privileged synthetic lab user
- Authorized security tester

## Trust boundaries

1. Browser to web application
2. User to user-owned objects
3. Normal user to privileged functions
4. Application to local data store

## Security objectives

- Confidentiality
- Integrity
- Availability
- Authentication
- Authorization
- Accountability

## Selected scenarios

These are the planned assessment scenarios. Each maps to a finding record and a
row in the test-case matrix. The exact findings are confirmed only after the
team reproduces them in its own lab — these scenarios define what the team will
look for, not confirmed results.

| Scenario | Security question | Planned tool |
|---|---|---|
| S1 — Attack-surface discovery | What services and web entry points does the local lab expose? | Nmap service/version scan; OWASP ZAP passive crawl |
| S2 — Broken access control / IDOR | Can a normal synthetic user read or act on another user's object (e.g. basket) by changing an identifier? | Browser dev tools + Burp/ZAP request replay with two synthetic accounts |
| S3 — Cross-site scripting (input validation) | Does user-controlled input render in the page without proper output encoding? | OWASP ZAP; browser dev tools |
| S4 — Security misconfiguration / information disclosure | Does the application leak version, stack, error, or header information, or omit expected security headers? | OWASP ZAP; optional Nikto; browser dev tools |
| S5 (optional) — Authentication / session review | Are login, logout, token (JWT), and cookie attributes handled safely? | Browser dev tools; ZAP passive inspection |

Scope reminder: all scenarios run only against `http://127.0.0.1:3000` using
synthetic accounts and non-destructive steps (see
[scope-and-authorization.md](scope-and-authorization.md)).
