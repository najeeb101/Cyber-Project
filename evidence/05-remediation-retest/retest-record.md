# Remediation and Retest Record

This file records defensive fixes applied in the isolated local lab and the retest that
confirms the fix. All work stays on loopback (127.0.0.1). No destructive actions, no
changes to any system outside the lab.

| Field | Value |
|---|---|
| Lab | OWASP Juice Shop 20.3.0, Docker, bound to `127.0.0.1:3000` |
| Remediation owner | Member 4 (proposes fix) |
| Retest owner | Member 3 (verifies fix) |
| Risk reviewer | Member 4 confirms the fix addresses the finding |

---

## WA-001 - Missing Content-Security-Policy header

**Finding:** `findings/WA-001.md` - HTML responses carry no `Content-Security-Policy`
header, so the browser applies no policy limiting where scripts may load from.

**OWASP category:** A02:2025 Security Misconfiguration

### Remediation chosen

Place an **nginx reverse proxy** in front of Juice Shop, on loopback only, that injects a
restrictive CSP header into every response. The application image is not modified; the fix
is applied at the web tier, which mirrors how this would be fixed in production (reverse
proxy / WAF / app middleware). Full steps and config: `WA-001-remediation.md`.

Policy applied (report-only first, then enforced):

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'self'; object-src 'none'
```

> Note: Juice Shop's Angular front end uses inline styles, so `style-src` includes
> `'unsafe-inline'`. This is documented as a known limitation of retro-fitting CSP onto an
> app not built for it; a greenfield app would use nonces/hashes instead.

### Before (vulnerable)

- Capture: `WA-001-before.txt` (headers from `http://127.0.0.1:3000/`, direct to app)
- Response-headers image: `WA-001-before.png` - the live response headers from port 3000, captured via headless Chromium (Playwright) and rendered as a headers panel; shows no `Content-Security-Policy`.
- Result: **no** `Content-Security-Policy` header present.

### After (remediated)

- Capture: `WA-001-after.txt` (headers from `http://127.0.0.1:8080/`, through proxy)
- Response-headers image: `WA-001-after.png` - the live response headers from port 8080, captured the same way; shows the `Content-Security-Policy` line and `server: nginx/1.27.5` (confirming the traffic passed through the proxy).
- Result: `Content-Security-Policy` header **present** with the policy above.

> The two `.png` images are rendered from headers read live off the real responses by a
> headless browser, not photographs of the Chrome DevTools UI. The `.txt` `curl` captures
> remain the primary evidence; the images are a readable visual aid for the report.

### Retest steps (exact)

```powershell
# 1. BEFORE - direct to the app, confirm header absent
curl.exe -s -D - -o NUL http://127.0.0.1:3000/ | Select-String -Pattern "Content-Security-Policy" ; if (-not $?) { "CSP absent" }

# 2. Apply remediation (see WA-001-remediation.md), then:
# 3. AFTER - through the proxy, confirm header present
curl.exe -s -D - -o NUL http://127.0.0.1:8080/ | Select-String -Pattern "Content-Security-Policy"
```

### Retest result

| Item | Status |
|---|---|
| Fix applied | 2026-10-30 (nginx:1.27-alpine proxy `csp-proxy`) |
| Header present after fix | **YES** - CSP injected on `:8080`, absent on `:3000` |
| App still functions (home page loads through proxy) | YES - HTTP 200, `Content-Length` 9984 identical before/after |
| Evidence saved | `WA-001-before.txt`, `WA-001-after.txt`, `WA-001-before.png`, `WA-001-after.png`, and this retest record. Both before/after response-headers images are now captured; the text `curl` captures remain the primary evidence. |
| Finding status | **Remediated** (through the web tier; see limitation note below) |

Confirmed output - before (`:3000`): no `Content-Security-Policy`. After (`:8080`):
`Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'self'; object-src 'none'`.

### Reviewer sign-off

- Retested by (Member 3): Team sign-off pending
- Fix confirmed to address finding (Member 4): Team sign-off pending

---

## Other findings (not yet remediated)

WA-002, WA-003, WA-004 remain **Pending** in `findings/findings-register.md`. The rubric
requires at least one remediated + retested finding; WA-001 satisfies it. Remediate others
only if time allows.
