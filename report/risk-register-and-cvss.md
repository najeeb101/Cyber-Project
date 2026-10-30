# Risk Register and CVSS Reasoning

**Owner:** Member 4 (risk and remediation)  
**Reviewers:** Member 3 (technical accuracy), Member 1 (risk/limitations accuracy)  
**Scope:** Four verified findings against OWASP Juice Shop 20.3.0 in the isolated local lab
(`127.0.0.1:3000`). Synthetic data only. See `findings/` for the full records.

---

## 1. Method

Two complementary scores are given for each finding:

1. **CVSS v3.1 base score** — a technical, context-free severity (0.0–10.0). Computed with
   the standard base formula; the full vector is shown so the score can be reproduced.
2. **Qualitative risk rating** — Likelihood × Impact *in this training context*, which may
   differ from the raw CVSS where practical exploitability or data sensitivity is lower than
   the worst case. Where the two differ, the reason is stated so nothing is overclaimed.

Severity bands (CVSS v3.1): None 0.0 · Low 0.1–3.9 · Medium 4.0–6.9 · High 7.0–8.9 ·
Critical 9.0–10.0.

Likelihood/Impact bands: Low / Medium / High, combined into an overall risk below.

| Likelihood ↓ / Impact → | Low | Medium | High |
|---|---|---|---|
| **High** | Medium | High | High |
| **Medium** | Low | Medium | High |
| **Low** | Low | Low | Medium |

---

## 2. Risk register

| ID | Finding | OWASP (2025) | Likelihood | Impact | Overall risk | CVSS v3.1 | Status |
|---|---|---|---|---|---|---|---|
| WA-003 | Unauthenticated `/ftp` directory listing exposes internal files | A05 Security Misconfiguration / A01 Broken Access Control | High | High | **High** | 7.5 (High) | Open |
| WA-004 | IDOR on `/rest/basket/:id` (read another user's basket) | A01 Broken Access Control | High | Medium–High | **High** | 6.5 (Medium) | Open |
| WA-001 | Missing Content-Security-Policy header | A05 Security Misconfiguration | Low | Low–Medium | **Low–Medium** | 4.3* (Medium) | **Remediated + retested 2026-10-30** |
| WA-002 | Overly permissive CORS (`Access-Control-Allow-Origin: *`) | A05 Security Misconfiguration | Medium | Low | **Low** | 5.3* (Medium) | Open |

Ordered by overall risk (highest first). `*` = see the per-finding reasoning in §3 for why
the qualitative rating sits below the raw CVSS base.

> OWASP note: the 2025 Top 10 places Security Misconfiguration at **A05** and Broken Access
> Control at **A01**. The finding records label misconfiguration as "A02"; align both to the
> published 2025 list before submission, or cite the exact source used for the numbering.

---

## 3. CVSS reasoning (per finding)

Each vector uses CVSS v3.1. Metric keys: AV attack vector, AC attack complexity,
PR privileges required, UI user interaction, S scope, C/I/A confidentiality/integrity/
availability impact.

### WA-003 — `/ftp` directory listing — CVSS 7.5 (High)

`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`

| Metric | Value | Justification |
|---|---|---|
| AV | Network | Reachable over HTTP. |
| AC | Low | A single unauthenticated GET; no special conditions. |
| PR | None | No account required. |
| UI | None | No victim interaction. |
| S | Unchanged | Stays within the web app's authority. |
| C | High | Backup/config files and a credential store (`.kdbx`) are downloadable. |
| I / A | None | Read-only exposure; no modification or outage. |

**Rating:** Likelihood High (trivial, unauthenticated), Impact High (sensitive internal
files) → **High**, consistent with the 7.5 base. Highest priority.

### WA-004 — IDOR on `/rest/basket/:id` — CVSS 6.5 (Medium)

`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`

| Metric | Value | Justification |
|---|---|---|
| AV | Network | API over HTTP. |
| AC | Low | Increment/substitute a small integer id. |
| PR | Low | Requires any one valid user session (confirmed with two synthetic accounts). |
| UI | None | No victim interaction. |
| S | Unchanged | Within the app. |
| C | High | A user can read another user's basket object. |
| I / A | None (confirmed path) | Only `GET` was tested; write/tamper not confirmed. |

**Rating:** Likelihood High (any authenticated user, ids are low sequential integers),
Impact Medium–High (confirmed read of another user's object; write path plausible but
untested) → **High** overall. CVSS base is 6.5 because PR:Low lowers exploitability versus
WA-003. Integrity is scored None since basket *modification* across users was not tested —
do not claim it without evidence.

### WA-001 — Missing CSP header — CVSS 4.3 indicative (Medium) / qualitative Low–Medium

`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N`

| Metric | Value | Justification |
|---|---|---|
| AV | Network | HTTP responses. |
| AC | Low | Header is simply absent. |
| PR | None | Affects all visitors. |
| UI | Required | Harm requires a victim to load a page carrying injected script. |
| C | Low | No direct exposure; CSP is a *mitigating control*, so its absence only amplifies a separate injection flaw. |
| I / A | None | No direct effect alone. |

**Rating:** On its own a missing CSP has **no direct** confidentiality/integrity impact — it
is defense-in-depth. The 4.3 base treats the latent XSS-amplification as a Low C impact; a
purist scoring would record it as Informational (0.0) until an XSS is confirmed in the same
app. Qualitative risk **Low–Medium**: Likelihood Low (needs a separate injection point),
Impact Low–Medium (would worsen any such flaw). **Status: remediated and retested** via a
loopback reverse proxy that injects the header (see `evidence/05-remediation-retest/`).

### WA-002 — Permissive CORS `*` — CVSS 5.3 base (Medium) / qualitative Low

`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`

| Metric | Value | Justification |
|---|---|---|
| AV | Network | HTTP responses. |
| AC | Low | Wildcard returned to any origin. |
| PR | None | No account required. |
| UI | None | Automatable from a foreign page. |
| C | Low | Browsers do **not** send credentials with a wildcard origin, so only non-credentialed, non-sensitive data is cross-origin readable. |
| I / A | None | No modification or outage. |

**Rating:** The 5.3 base follows mechanically from C:Low. The team's **qualitative rating is
Low** because practical impact was not demonstrated (no cross-origin browser PoC) and no
sensitive credentialed endpoint was shown to be readable. If a later test shows an
`Authorization`-protected endpoint is readable cross-origin, re-rate upward. Stated as a
transparent downward adjustment, not a vector change.

---

## 4. Prioritised remediation order

1. **WA-003 (High)** — remove the `/ftp` route or require authentication; take backup/config
   files and the credential store out of any served path. Highest impact, trivially exploitable.
2. **WA-004 (High)** — enforce server-side ownership checks on `/rest/basket/:id` (and other
   per-user objects); return 403 on mismatch.
3. **WA-002 (Low)** — replace the wildcard with an explicit trusted-origin allow-list; scope
   allowed methods/headers; disable CORS where unneeded.
4. **WA-001 (done)** — restrictive CSP header; **already remediated and retested**. Serves as
   the project's demonstrated before/after fix.

---

## 5. Limitations

- Scores are **indicative**, produced for a deliberately vulnerable training app with
  **synthetic data**; they are not a production risk assessment.
- Only the explicitly reproduced paths are scored. Untested write paths (WA-004) and
  cross-origin credentialed reads (WA-002) are noted but **not** counted in the impact.
- CVSS v3.1 is used throughout for consistency with the finding records. CVSS v4.0 vectors can
  be added if the rubric requires them; the qualitative ratings above would not change.
- OWASP 2025 category numbering must be reconciled (see note in §2) before the final report.
