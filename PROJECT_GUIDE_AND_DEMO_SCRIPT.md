# Project Guide and Live Demo Script

**CMPS 380 Cybersecurity Fundamentals, Fall 2026, Group G02**
**Project:** Web Application Security Assessment of OWASP Juice Shop in an isolated local lab

| Member | Name | QUID | Role |
|---|---|---|---|
| 1 | Najeeb Abdi | 202307172 | Project coordinator and methodology (submission owner) |
| 2 | Mohanad Elhabash | 202314448 | Lab and environment engineer |
| 3 | Moaaz Mohamed | 202207862 | Security tester and evidence owner |
| 4 | Ahmed Hari | 202203669 | Risk, remediation, report, and media |

This document has two parts:

- **Part A (sections 1 to 11)** explains the whole project: what it is, the scope, what we built, what we found, how we scored it, what we fixed, and what is still open. Every member should read it so they can answer any question.
- **Part B (sections 12 to 17)** is the live demo: what to prepare, the exact commands, a timed script with words to say, a backup plan, and the gaps to close before presenting.

Every fact in this file comes from the files in this repository. Each section names the file it comes from, so you can open that file if an assessor asks for proof.

---

# PART A: THE PROJECT

## 1. The project in one paragraph

We built a small, isolated lab on one Windows laptop. Inside it we ran **OWASP Juice Shop 20.3.0**, a web shop that OWASP deliberately built with security flaws for training. Juice Shop ran in a Docker container that only the laptop itself could reach (`127.0.0.1:3000`). We assessed it the way a professional penetration tester would. First, **Nmap** mapped what was exposed. Then **OWASP ZAP** scanned it automatically. We **manually verified** every finding with `curl` and two test accounts, scored each one with **CVSS v3.1** plus a likelihood × impact rating, and **fixed one finding and retested it** to prove the fix worked. We report **four verified findings** (WA-001 to WA-004). WA-001 is the one we remediated and retested.

## 2. Why this project matters (the "so what")

- Web applications are the most common way organisations get breached. Broken access control is #1 and security misconfiguration is #2 in the **OWASP Top 10:2025**, and our findings fall into exactly those two categories.
- Many teams run a scanner and paste its output into a report. **Our point is that a scanner alone is not enough.** ZAP found 2 of our 4 findings. The 2 most serious ones (`/ftp` exposure and the IDOR) were found **only by manual testing**.
- Finding a problem is half the job. Showing that a fix works, with before and after evidence, is what makes an assessment useful.

**Research question** (from [kickoff.md](kickoff.md)):
> How effectively can a layered penetration-testing workflow identify, verify, prioritize, and communicate web-application security weaknesses in a controlled training application, and how does retesting demonstrate the value of remediation?

**Short answer, based on our evidence:** the layers complement each other. Nmap defined the attack surface (one HTTP service). ZAP quickly flagged header and configuration issues. Manual testing found the high-impact access-control problems that the scanner missed. CVSS gave us a defensible priority order. The retest proved the CSP fix changed the server's behaviour without breaking the app.

## 3. Scope, authorization and safety

Source: [planning/scope-and-authorization.md](planning/scope-and-authorization.md), [kickoff.md](kickoff.md) §3

| Item | Value |
|---|---|
| Authorized target | OWASP Juice Shop at `http://127.0.0.1:3000` (later also the fix proxy at `http://127.0.0.1:8080`) |
| Testing period | 28 Oct 2026 to 10 Nov 2026 |
| Environment | Docker Desktop on the project laptop |
| Data | Synthetic only: `synth.a@lab.test`, `synth.b@lab.test` |
| Testers | The four group members |

**In scope:** local service discovery, normal browsing, a controlled ZAP scan, manual verification with curl and browser dev tools, non-destructive proofs of concept, remediation and retest.

**Out of scope (what we did not and must not do):** public websites, university or cloud systems, real credentials or personal data, denial of service, destructive payloads, password spraying or phishing, malware or persistence, container escape, and storing or publishing sensitive data.

**Safety controls we actually applied:**
1. The container is published only on loopback: `-p 127.0.0.1:3000:3000`, not `0.0.0.0`.
2. Isolation was verified: `docker port juice-shop` shows `127.0.0.1:3000`, and a request to the laptop's LAN IP `192.168.199.1:3000` failed (HTTP code 000). Evidence: [evidence/environment/isolation-check.txt](evidence/environment/isolation-check.txt).
3. Only synthetic accounts were used, and JWTs are redacted in the evidence.
4. The contents of `/ftp` files were **deliberately not copied** into evidence. Only the listing and the HTTP status were recorded.
5. The fix proxy also listens only on loopback (`127.0.0.1:8080`).

## 4. Lab architecture

```text
                    Project laptop (Windows 11 Pro), isolated lab
 ┌──────────────────────────────────────────────────────────────────────┐
 │  Analyst tools: Chrome 156, curl, Nmap 7.993, OWASP ZAP 2.17.0,       │
 │                 PowerShell, Python 3.14 (team script)                 │
 │                          │                                            │
 │          127.0.0.1 only (loopback, not reachable from the LAN)        │
 │              │                                   │                    │
 │   BEFORE: :3000 direct                AFTER: :8080 via proxy          │
 │              │                                   ▼                    │
 │              │                     ┌────────────────────────────┐    │
 │              │                     │ Docker: csp-proxy           │    │
 │              │                     │ nginx:1.27-alpine           │    │
 │              │                     │ adds Content-Security-Policy│    │
 │              │                     └─────────────┬──────────────┘    │
 │              ▼                                   ▼                    │
 │       ┌──────────────────────────────────────────────────┐           │
 │       │ Docker: juice-shop  (OWASP Juice Shop 20.3.0)     │           │
 │       │ Node.js + Angular, in-container SQLite DB,         │           │
 │       │ synthetic data only                                │           │
 │       └──────────────────────────────────────────────────┘           │
 └──────────────────────────────────────────────────────────────────────┘
          LAN IP 192.168.199.1:3000 → connection fails (verified)
```

**Threat model** (source: [planning/threat-model.md](planning/threat-model.md)):

| Element | Contents |
|---|---|
| Assets | Synthetic user accounts, session data (JWTs), basket/order data, application integrity and availability |
| Actors | Unauthenticated visitor, normal synthetic user, privileged synthetic user, authorized tester |
| Trust boundaries | (1) Browser to app, (2) user to user-owned objects, (3) normal user to privileged functions, (4) app to data store |
| Objectives | Confidentiality, integrity, availability, authentication, authorization, accountability |

Two of our findings each cross a trust boundary. WA-003 crosses boundary 1, because an anonymous visitor reaches internal files. WA-004 crosses boundary 2, because user B reads user A's object.

## 5. Environment and tools

Source: [environment/environment-inventory.md](environment/environment-inventory.md)

| Component | Version |
|---|---|
| OS | Windows 11 Pro 10.0.26300.9711 |
| Docker Engine / Compose | 29.9.1 / v5.6.0 |
| Target | OWASP Juice Shop 20.3.0 (`bkimminich/juice-shop`, digest `sha256:42843723…53f4`, pulled 2026-10-28) |
| Nmap | 7.993 (Npcap 1.90) |
| OWASP ZAP | 2.17.0 (Temurin 17 JRE) |
| Browser | Google Chrome 156.0.8078.48 |
| Python | 3.14.0 (team script) |
| Fix proxy | nginx 1.27-alpine (reports `nginx/1.27.5`) |
| Not used | Burp Suite and Nikto. Be ready to say why (see §9). |

**Why each tool (say this in the demo, because the rubric requires tool rationale):**

| Tool | Why we used it | Its limitation |
|---|---|---|
| Docker | A reproducible, resettable lab with one-command rebuild and loopback binding | Container isolation is not a complete security boundary |
| Juice Shop | Legally safe, realistic modern app (Angular SPA + REST API + JWT auth) | Training app, so findings don't prove anything about a real production system |
| Nmap | Confirms what is exposed before we attack anything | An open port doesn't prove a vulnerability. It even misidentified the service as `ppp?` |
| OWASP ZAP | Free, open-source spider + passive/active scanner, good at header/config issues | Missed both access-control findings, can't understand business logic |
| curl / PowerShell | Exact, repeatable, scriptable requests that make clean text evidence | Depends on what the tester thinks to test |
| Browser DevTools | Shows response headers and app behaviour visually | Manual and coverage depends on the tester |
| CVSS v3.1 | A standard, reproducible way to express technical severity | It is not business risk, so we added a likelihood × impact rating |
| nginx | A realistic way to add security headers at the web tier without modifying the app | Only protects traffic that goes through it |
| Team Python script | Triage of scanner JSON and checks evidence for leaked secrets | Pattern-based secret detection is an aid, not a guarantee |

## 6. Methodology: what we did, step by step

We followed **OWASP WSTG** for the test ideas and **PTES-style phases** for the order of work:

```text
 Scope & authorize → Build & baseline lab → Recon (Nmap) → Automated scan (ZAP)
      → Manual verification (curl, 2 accounts) → Risk scoring (CVSS + L×I)
      → Remediate (nginx CSP proxy) → Retest (same command) → Report & evidence
```

**Phase 1: Build and baseline (28 Oct).** We pulled Juice Shop, ran it bound to `127.0.0.1:3000`, and confirmed HTTP 200 with the container up. Evidence: [baseline-health.txt](evidence/environment/baseline-health.txt), [isolation-check.txt](evidence/environment/isolation-check.txt).

**Phase 2: Reconnaissance (28 Oct).** We ran `nmap -sT -sV -Pn -p 3000 127.0.0.1`. Port 3000/tcp is open. Nmap labelled the service `ppp?`, which is a **fingerprint miss**: the raw response Nmap captured is clearly `HTTP/1.1 200 OK` with the Juice Shop HTML. Even so, the Nmap output already leaked useful details: `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET,HEAD,PUT,PATCH,POST,DELETE`, and an `X-Recruiting` header. Evidence: [EV-001-nmap-local-baseline.txt](evidence/reconnaissance/EV-001-nmap-local-baseline.txt).
> **Talking point:** we scanned only port 3000 on loopback on purpose, because that is the only authorized target. We did not do a broad port sweep.

**Phase 3: Automated scan (28 Oct).** We ran a ZAP quick scan (`zap -cmd -quickurl http://127.0.0.1:3000`), which uses the traditional spider and then an active scan. Results: **0 High, 2 Medium, 0 Low, 3 Informational, 0 false positives flagged by ZAP**.

| ZAP alert | Risk | What we did with it |
|---|---|---|
| Content Security Policy (CSP) Header Not Set | Medium | Manually verified, became **WA-001** |
| Cross-Domain Misconfiguration | Medium | Manually verified, became **WA-002** |
| Information Disclosure – Suspicious Comments | Info | Not promoted (comments in minified JS, not shown to be sensitive) |
| Modern Web Application | Info | Not a vulnerability. It tells you to use the AJAX spider because this is a SPA |
| User Agent Fuzzer | Info | Not a vulnerability (behaviour differences by user agent) |

Evidence: [EV-002-zap-scan-raw.html](evidence/automated-scans/EV-002-zap-scan-raw.html), [zap-console.log](evidence/automated-scans/zap-console.log).
> **Talking point:** the "Modern Web Application" alert explains part of why ZAP missed things. Juice Shop is an Angular single-page app, and the traditional spider doesn't see routes that are built by JavaScript. That's a real tool limitation we observed.

**Phase 4: Manual verification (28 Oct).** We reproduced every candidate with `curl.exe` and saved the exact command and response. We also used manual exploration to find issues the scanner didn't report: `/ftp` and the basket IDOR. For the IDOR we created **two synthetic accounts** so that we could prove cross-user access without touching anyone's real data.

**Phase 5: Risk scoring (30 Oct).** Each finding got a CVSS v3.1 vector and a likelihood × impact rating. Where the two disagree, we explain why instead of quietly changing the vector. Source: [report/risk-register-and-cvss.md](report/risk-register-and-cvss.md).

**Phase 6: Remediation and retest (30 Oct).** We fixed WA-001 with an nginx reverse proxy that injects a CSP header, then re-ran the **same curl command** on both ports. Source: [evidence/05-remediation-retest/](evidence/05-remediation-retest/).

## 7. The four verified findings in detail

Summary (source: [findings/findings-register.md](findings/findings-register.md)):

| ID | Finding | OWASP 2025 | Found by | CVSS v3.1 | Overall risk | Status |
|---|---|---|---|---|---|---|
| WA-003 | Unauthenticated `/ftp` directory listing | A02 / A01 | **Manual** | 7.5 High | **High** | Open |
| WA-004 | IDOR on `/rest/basket/:id` | A01 | **Manual** | 6.5 Medium | **High** | Open |
| WA-001 | Missing Content-Security-Policy | A02 | ZAP + manual | 4.3 Medium | Low–Medium | **Fixed + retested** |
| WA-002 | CORS `Access-Control-Allow-Origin: *` | A02 | ZAP + manual | 5.3 Medium | Low | Open |

### WA-001: Missing Content-Security-Policy header

- **What CSP is, in plain words:** a response header that tells the browser "only run scripts and load content from these places." If an attacker manages to inject a `<script>` (XSS), a good CSP stops the browser from running it.
- **How we found it:** ZAP alert 10038, then confirmed with `curl.exe -s -D - -o NUL http://127.0.0.1:3000/`.
- **What we saw:** HTTP 200 with `X-Content-Type-Options`, `X-Frame-Options`, and `Feature-Policy` present, but **no `Content-Security-Policy`**.
- **Expected:** a restrictive CSP on HTML responses.
- **Impact:** **indirect.** It doesn't leak anything by itself. It removes a safety net, so any XSS becomes more damaging. That's why we rate it Low–Medium even though CVSS gives 4.3.
- **CVSS:** `AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N` = 4.3. We openly note that a purist would score it 0.0 (informational) until an XSS is confirmed.
- **Limitation:** we checked `/` only, not every route.
- **Evidence:** [WA-001-csp-headers.txt](evidence/manual-tests/WA-001-csp-headers.txt), ZAP report.
- **Status:** fixed and retested (see §8).

### WA-002: Overly permissive CORS (`Access-Control-Allow-Origin: *`)

- **What CORS is, in plain words:** browsers normally stop site X's JavaScript from reading responses from site Y. CORS headers are how site Y says "it's OK for these other sites to read me." `*` means **any website** may read the response.
- **How we found it:** ZAP "Cross-Domain Misconfiguration", then confirmed by sending a fake foreign origin:
  `curl.exe -s -D - -o NUL -H "Origin: http://evil.example" "http://127.0.0.1:3000/rest/products/search?q=apple"`
- **What we saw:** `Access-Control-Allow-Origin: *` even for `http://evil.example`. There is no allow-list.
- **Why we only rate it Low:** browsers **refuse to send cookies or credentials** when the origin is `*`. That means only data that is already readable without logging in is exposed. We did **not** build a malicious cross-origin page, and we did **not** test credentialed API reads, so we don't claim more.
- **CVSS:** `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` = 5.3 mechanically. Our qualitative rating is **Low**, and we state the downward adjustment openly.
- **Fix:** an explicit allow-list of trusted origins, restricted methods and headers, and no CORS on routes that don't need it.
- **Evidence:** [WA-002-cors-headers.txt](evidence/manual-tests/WA-002-cors-headers.txt).

### WA-003: Unauthenticated `/ftp` directory listing (our most severe finding)

- **What happens:** anyone can open `http://127.0.0.1:3000/ftp` without logging in and get a **list of 11 internal files** that can all be downloaded:
  `acquisitions.md`, `announcement_encrypted.md`, `coupons_2013.md.bak`, `eastere.gg`, `encrypt.pyc`, **`incident-support.kdbx` (a KeePass password database)**, `legal.md`, `package-lock.json.bak`, `package.json.bak`, `suspicious_errors.yml`, plus a `quarantine` folder.
- **How we found it:** manual exploration. **ZAP did not report it.**
- **Proof:** the listing returns HTTP 200, and `curl.exe -s -I http://127.0.0.1:3000/ftp/acquisitions.md` returns HTTP 200 with `Content-Length: 909`.
- **Why it's serious:**
  - Backup files (`package.json.bak`) reveal exact dependency versions, which an attacker can match against known CVEs.
  - A password-vault file can be taken offline and brute-forced at leisure.
  - Business documents (`acquisitions.md`) leak confidential information.
- **CVSS:** `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` = **7.5 High**. No account is needed, it's one request, and confidentiality impact is high.
- **What we did not do:** we did not open or analyse the file contents and did not try to crack the `.kdbx`. This was deliberate, for ethics and scope.
- **Fix:** remove the `/ftp` route or put it behind authentication and authorization, disable directory listing, and keep backups and credential stores out of anything the web server serves.
- **Evidence:** [WA-003-ftp-exposure.txt](evidence/manual-tests/WA-003-ftp-exposure.txt).

### WA-004: IDOR on `/rest/basket/:id` (broken object-level access control)

- **What IDOR is, in plain words:** *Insecure Direct Object Reference.* The server checks **who you are** (authentication) but not **whether this object is yours** (authorization). If you change the number in the URL, you get someone else's data.
- **How we proved it** (two synthetic accounts):
  1. We registered `synth.a@lab.test` (user 25, basket 6) and `synth.b@lab.test` (user 26, basket 7).
  2. We logged in as B and got B's own valid JWT.
  3. Using **B's token**, we requested `GET /rest/basket/6`, which is **A's** basket.
  4. The server returned **HTTP 200** and the body `{"id":6,…,"UserId":25,…}`, so B received A's basket.
  5. Control test: the same request with **no token** returns **401**. This proves the endpoint does check authentication, but it never checks ownership.
- **Why it's serious:** basket ids are small sequential integers, so an attacker can just count 1, 2, 3… and read every user's basket.
- **CVSS:** `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` = **6.5 Medium**. PR is Low because you need any account. Our overall risk is still **High**, because likelihood is high when anyone can register an account.
- **What we did not claim:** we only tested **reading** (`GET`). Modifying another user's basket is plausible but **not tested**, so integrity is scored None. Both baskets were empty, so no product data was exposed.
- **Fix:** on every per-user object endpoint, compare the requested basket id against the `bid` and `UserId` in the verified JWT, and return **403** on mismatch.
- **Evidence:** [WA-004-idor-basket.txt](evidence/manual-tests/WA-004-idor-basket.txt) (JWTs redacted).

## 8. Remediation and retest of WA-001 (the before and after)

Source: [WA-001-remediation.md](evidence/05-remediation-retest/WA-001-remediation.md), [retest-record.md](evidence/05-remediation-retest/retest-record.md), [csp-proxy.conf](evidence/05-remediation-retest/csp-proxy.conf)

**Why a reverse proxy and not an edit to Juice Shop's code?** The Juice Shop image is prebuilt, so editing it is fragile. In real companies, security headers are commonly added at the web tier (reverse proxy, load balancer, or WAF). The fix is realistic, non-destructive, and fully reversible. Juice Shop itself was never modified.

**The fix:** an `nginx:1.27-alpine` container named `csp-proxy`, listening on `127.0.0.1:8080`, forwarding to Juice Shop on port 3000, and adding this header:

```text
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
                         img-src 'self' data:; frame-ancestors 'self'; object-src 'none'
```

What each part means:

| Directive | Meaning |
|---|---|
| `default-src 'self'` | Anything not listed below may only load from our own origin |
| `script-src 'self'` | Scripts only from our origin. No inline `<script>` and no third-party scripts, which is the main defence against XSS |
| `style-src 'self' 'unsafe-inline'` | Styles from our origin plus inline styles. This is a concession, because Angular uses inline styles |
| `img-src 'self' data:` | Images from our origin or inline `data:` images |
| `frame-ancestors 'self'` | Other sites can't put our page in an iframe (anti-clickjacking) |
| `object-src 'none'` | No Flash/plugins at all |

**Result:**

| Check | Before (`:3000` direct) | After (`:8080` via proxy) |
|---|---|---|
| `Content-Security-Policy` present | **No** | **Yes** |
| HTTP status | 200 | 200 |
| `Content-Length` | 9984 | 9984 (same page, so the app isn't broken) |
| `Server` header | (none) | `nginx/1.27.5` (proves traffic went through the proxy) |

Evidence: [WA-001-before.txt](evidence/05-remediation-retest/WA-001-before.txt), [WA-001-after.txt](evidence/05-remediation-retest/WA-001-after.txt), and the images [WA-001-before.png](evidence/05-remediation-retest/WA-001-before.png) / [WA-001-after.png](evidence/05-remediation-retest/WA-001-after.png).

**Residual risk (say this without being asked, because it shows maturity):**
1. Port 3000 is still open without CSP, on purpose, so we can show the comparison. In production, the app would only be reachable through the proxy.
2. `'unsafe-inline'` for styles weakens the policy a little. A new app would use nonces or hashes.
3. CSP is defence in depth. It doesn't remove any injection bug, it only limits the damage.
4. Note: the proxy also passes through the `Access-Control-Allow-Origin: *` header, so WA-002 is **not** fixed by this proxy.

## 9. Risk prioritisation and why we didn't use certain tools

**Our recommended fix order** (from [risk-register-and-cvss.md](report/risk-register-and-cvss.md)):
1. **WA-003 (High).** Remove `/ftp` or require auth. It's trivial to exploit and has the highest impact.
2. **WA-004 (High).** Add server-side ownership checks and return 403.
3. **WA-002 (Low).** Replace `*` with an origin allow-list.
4. **WA-001 (done).** CSP has already been added and retested.

**"Why fix the Low–Medium one first, not the High one?"** You will likely be asked this. Honest answer: the rubric requires one complete fix-and-retest cycle. CSP could be fixed safely and reversibly at the web tier without modifying the vulnerable app. WA-003 and WA-004 need changes to Juice Shop's own code or routing, and we list them as the next step. In a real engagement, WA-003 would be fixed first.

**Why no Burp Suite or Nikto?** curl gave us exact, repeatable, text-based evidence for every request, and ZAP already covered the proxy and scanner role. Burp Community would mostly have duplicated that. Nikto is a signature-based web-server scanner, and it would have overlapped heavily with ZAP's header checks on a Node.js app. The kickoff rules say not to add tools that don't answer a project question.

## 10. Creativity feature: the team's Python script

Source: [source/custom-script/](source/custom-script/)

[evidence_toolkit.py](source/custom-script/evidence_toolkit.py) is about 290 lines and uses only the standard library, read-only and with no network access. It has two commands:

- `scan-summary` turns a ZAP JSON report into a de-duplicated, risk-sorted table (with optional CSV) and reminds you that *every alert is a candidate, not a confirmed vulnerability*.
- `evidence-index` walks `evidence/`, indexes files by the `WA-###` / `EV-###` naming convention, flags badly named files, and with `--check-secrets` scans for leftover JWTs, `Authorization` headers, cookies, and passwords before submission.

Be honest about this if asked: our real ZAP output is HTML, not JSON, so `scan-summary` has so far only run on the synthetic sample `samples/zap-sample.json`. `evidence-index --check-secrets` was run on our **real** evidence folder on 30 Oct. It indexed 17 files and raised one flag on `WA-004-idor-basket.txt`, which is a false positive (the token there is the redacted placeholder `Bearer <B's JWT>`). That makes it the better command to demo, and the false positive is itself a good talking point.

## 11. Limitations (state these confidently, they earn marks)

1. **Training target.** Juice Shop is deliberately vulnerable and uses synthetic data, so our results don't measure real-world prevalence.
2. **One scan profile.** We ran one ZAP quick scan with the traditional spider. We didn't use the AJAX spider or an authenticated scan context, which partly explains what ZAP missed.
3. **Narrow tests.** IDOR was only tested for reading. CORS had no browser proof of concept. CSP was checked on `/` only. The `/ftp` file contents were not analysed.
4. **Isolation check.** It was done from the same laptop using its LAN IP. A check from a second physical device is still recommended.
5. **The fix covers one path only.** CSP is only applied through `:8080`.
6. **CVSS is technical severity, not business risk.** That's why we added likelihood × impact.
7. **Only one of four findings has been remediated.**

**Impact on society and security (for the "impact" rubric line):**
- Developers learn that access control must be enforced on the server **for every object**. Hiding IDs or relying on the UI is not enough.
- Testers learn that scanners are a starting point, not a verdict.
- The same knowledge could be misused. We reduced that risk by testing only a training app, not publishing weaponised code, redacting tokens, and not touching file contents.

---

# PART B: THE LIVE DEMO

## 12. Format and rules

- **20 minutes total: about 12 minutes of demo plus 8 minutes of Q&A.**
- **No PowerPoint.** Everything is shown live: terminal, browser, and files in VS Code.
- Show the **working proof of concept** and explain **why each tool was selected**.
- All four members should speak. The split below follows each person's role.

## 13. Before the demo (do this 30 to 60 minutes before)

**Screen setup** (increase font sizes so the room can read them):
- **Terminal:** PowerShell at the project root, font about 18pt.
- **Browser:** Chrome with two tabs, `http://127.0.0.1:3000` and `http://127.0.0.1:8080`, and DevTools docked at the bottom.
- **VS Code:** open `findings/findings-register.md`, `report/risk-register-and-cvss.md`, `evidence/05-remediation-retest/csp-proxy.conf`, and the ZAP HTML report in a browser tab.
- Close everything else: chats, email, notifications. **Turn on Do Not Disturb.**

**Start the lab fresh:**

```powershell
# 1. Fresh Juice Shop (a restart wipes its in-memory DB, so you get a clean state)
docker rm -f juice-shop
docker run --name juice-shop -d -p 127.0.0.1:3000:3000 bkimminich/juice-shop
# wait ~15-20 s for it to boot
curl.exe -sI http://127.0.0.1:3000

# 2. Start the fix proxy (run from the folder that contains csp-proxy.conf)
cd evidence\05-remediation-retest
docker rm -f csp-proxy
docker run --name csp-proxy -d -p 127.0.0.1:8080:80 -v "${PWD}/csp-proxy.conf:/etc/nginx/conf.d/default.conf:ro" nginx:1.27-alpine
cd ..\..
curl.exe -sI http://127.0.0.1:8080
```

> `docker rm -f` only removes **our two named containers**, never anything else.

**Rehearsal checks:**
- [ ] `http://127.0.0.1:3000` loads the Juice Shop home page in Chrome.
- [ ] `http://127.0.0.1:8080` loads too. **Open DevTools → Console and look for CSP errors.** If the page partly breaks through the proxy, that is not a disaster. It is a real talking point: "a strict CSP has to be tuned to the app, which is why you deploy it in report-only mode first." Know in advance which one you'll see.
- [ ] The IDOR commands in §14 Step 5 run end to end on the fresh container.
- [ ] Python runs. Python 3.14 is installed but may not be on PATH. If `py --version` fails, use the full path: `& "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe" --version`.
- [ ] Nmap and ZAP open. **Do not run a ZAP scan live.** It takes several minutes. Show the saved report instead.

## 14. The demo commands (copy-paste ready)

Copy these into a text file and keep it open during the demo.

```powershell
# ---- Step 2: isolation proof
docker ps --filter "name=juice-shop"
docker port juice-shop                      # → 3000/tcp -> 127.0.0.1:3000

# ---- Step 3: recon (fast, ~16 s)
nmap -sT -sV -Pn -p 3000 127.0.0.1

# ---- Step 4a: WA-001 missing CSP (direct)
curl.exe -s -D - -o NUL http://127.0.0.1:3000/

# ---- Step 4b: WA-002 CORS wildcard with a fake evil origin
curl.exe -s -D - -o NUL -H "Origin: http://evil.example" "http://127.0.0.1:3000/rest/products/search?q=apple"

# ---- Step 4c: WA-003 /ftp exposure (also open http://127.0.0.1:3000/ftp in the browser)
curl.exe -s -o NUL -w "HTTP %{http_code}`n" http://127.0.0.1:3000/ftp/acquisitions.md
```

**Step 5: WA-004 IDOR, live with two fresh synthetic accounts.** Use new emails, because registering the same email twice fails.

```powershell
$base = "http://127.0.0.1:3000"
$pw   = "Lab-Test-123!"

# Register two synthetic users
Invoke-RestMethod -Method Post "$base/api/Users/" -ContentType "application/json" -Body (@{email="demo.a@lab.test";password=$pw;passwordRepeat=$pw} | ConvertTo-Json) | Out-Null
Invoke-RestMethod -Method Post "$base/api/Users/" -ContentType "application/json" -Body (@{email="demo.b@lab.test";password=$pw;passwordRepeat=$pw} | ConvertTo-Json) | Out-Null

# Log in as each; keep tokens in variables (never print them)
$A = (Invoke-RestMethod -Method Post "$base/rest/user/login" -ContentType "application/json" -Body (@{email="demo.a@lab.test";password=$pw} | ConvertTo-Json)).authentication
$B = (Invoke-RestMethod -Method Post "$base/rest/user/login" -ContentType "application/json" -Body (@{email="demo.b@lab.test";password=$pw} | ConvertTo-Json)).authentication
"A's basket id = $($A.bid)    B's basket id = $($B.bid)"

# Control: no token → 401
curl.exe -s -o NUL -w "No token: HTTP %{http_code}`n" "$base/rest/basket/$($A.bid)"

# Attack: B's token, A's basket id → 200 + A's basket
Invoke-RestMethod "$base/rest/basket/$($A.bid)" -Headers @{Authorization = "Bearer $($B.token)"} | ConvertTo-Json -Depth 4
```

What you should see: `No token: HTTP 401`, then JSON with `"id"` equal to A's basket id and a `UserId` that **isn't B's**. The ids will differ from our evidence (25/26, 6/7) because the container is fresh. That's fine, and it's worth saying out loud.

```powershell
# ---- Step 6: WA-001 retest - same command, both ports
curl.exe -s -D - -o NUL http://127.0.0.1:3000/ | Select-String "Content-Security-Policy"   # nothing
curl.exe -s -D - -o NUL http://127.0.0.1:8080/ | Select-String "Content-Security-Policy","Server:","Content-Length"

# ---- Optional: team script on real evidence (use the full python.exe path if `py` is not found)
py source\custom-script\evidence_toolkit.py evidence-index --dir evidence --check-secrets
# Expect: 17 files, 1 flag on WA-004-idor-basket.txt, a false positive (redacted placeholder "Bearer <B's JWT>")
```

## 15. The 12-minute script (what to do and what to say)

The time markers are targets. **Speak to the audience, not to the screen.** Text in quotes is suggested wording, so make it your own and don't read it word for word.

### 0:00–1:00 · Opening, objective and safety (Najeeb, Member 1)
**Screen:** the README or this file, top section, showing the group ID and names.

> "Good morning. We're Group G02: Najeeb, Mohanad, Moaaz and Ahmed. Our project is a web application security assessment. We took OWASP Juice Shop, an online shop that OWASP deliberately built with vulnerabilities for training, and assessed it the way a penetration tester would. We mapped it, scanned it, manually verified what we found, scored the risk, fixed one issue, and retested it.
>
> Our research question was: how well does a *layered* workflow (recon, automated scanning, manual testing, and retest) find and communicate real weaknesses, compared with just running a scanner?
>
> Safety came first. Everything runs on this laptop only, bound to 127.0.0.1. We used only synthetic accounts, no real data, nothing destructive, and our written scope is in `planning/scope-and-authorization.md`."

### 1:00–2:30 · The lab and isolation (Mohanad, Member 2)
**Screen:** terminal, then the browser on `:3000`.
**Run:** `docker ps --filter "name=juice-shop"` and `docker port juice-shop`

> "Here's the lab. Juice Shop version 20.3.0 runs in a Docker container. The key line is this one: port 3000 is published to **127.0.0.1**, not 0.0.0.0. That means only this machine can reach it, not the Wi-Fi or anyone else on the network. We verified that: a request to the laptop's own LAN address on port 3000 fails, and that check is saved in `evidence/environment/isolation-check.txt`.
>
> We chose Docker because the lab is reproducible: one command rebuilds a clean copy, and a restart resets all data. Here's the app running normally: a regular online shop with login, basket, and checkout. That's important, because it means the vulnerabilities we show are in a realistic modern stack: an Angular front end, a Node.js REST API, and JWT login tokens."

### 2:30–3:30 · Reconnaissance with Nmap (Moaaz, Member 3)
**Run:** `nmap -sT -sV -Pn -p 3000 127.0.0.1`

> "Before attacking anything, you find out what's exposed. That's Nmap's job. We only scanned port 3000 on loopback, because that's the only thing we're authorized to touch.
>
> Port 3000 is open. Interestingly, Nmap guesses the service is `ppp?`, which is wrong. If you look at the raw fingerprint, it's clearly an HTTP 200 response from Juice Shop. That's our first lesson about tools: **a tool's output has to be interpreted, not trusted blindly.** Nmap also already leaks a hint for later: `Access-Control-Allow-Origin: *`."

### 3:30–4:30 · Automated scan with OWASP ZAP (Moaaz)
**Screen:** the saved ZAP report `EV-002-zap-scan-raw.html`, showing the Summary of Alerts table.

> "Next, automated scanning with OWASP ZAP, a free and open-source web scanner and proxy. We ran a quick scan, which spiders the site and then actively probes it. A full scan takes several minutes, so here's the saved report.
>
> ZAP found 2 Medium alerts (missing Content-Security-Policy and a cross-domain misconfiguration) plus 3 Informational ones. We treat every alert as a **hypothesis**, not a finding. The two Mediums we manually confirmed and they became WA-001 and WA-002. The informational ones we reviewed and didn't promote. One of them, 'Modern Web Application', is actually ZAP telling us *it* may be missing things because this is a JavaScript single-page app. Keep that in mind, because it matters in a minute."

### 4:30–5:30 · WA-001 and WA-002: verifying the scanner's findings (Moaaz)
**Run:** the Step 4a and 4b commands.

> "Manual verification of WA-001. I request the home page and print the headers. We see X-Frame-Options and X-Content-Type-Options, but **no Content-Security-Policy**. CSP is the header that tells the browser which scripts it's allowed to run. Without it, if an attacker ever injects a script, the browser will happily run it. On its own it doesn't leak anything, so we rated it Low to Medium, but it removes an important safety net.
>
> WA-002: I pretend to be a malicious site by sending `Origin: evil.example`. The server answers `Access-Control-Allow-Origin: *`, meaning *any* website may read this response. We rated it only **Low**, and here's why: browsers won't send login cookies with a wildcard, so only public data is exposed. We didn't prove more than that, so we don't claim more."

### 5:30–6:45 · WA-003: unauthenticated `/ftp` (Moaaz), our highest-severity finding
**Screen:** browser on `http://127.0.0.1:3000/ftp`, then **Run:** the Step 4c command.

> "Now the findings the scanner **missed**. I'm not logged in. I just open `/ftp`, and the server shows me a directory listing of eleven internal files: backup files like `package.json.bak`, an `acquisitions.md` business document, and a KeePass password database, `incident-support.kdbx`. And they download: HTTP 200, no login.
>
> This is our most severe finding, CVSS 7.5 High. There's no account needed, it takes one request, and confidentiality impact is high. Backup files reveal exact library versions an attacker can match to known CVEs, and a password vault can be cracked offline. For ethics and scope reasons, **we deliberately did not open or crack any of these files.** We only recorded that they're exposed. ZAP's quick scan never reported this."

### 6:45–8:30 · WA-004: IDOR live with two accounts (Moaaz)
**Run:** the Step 5 block, one command at a time.

> "WA-004 is broken access control, OWASP's number one risk. I'm going to create two brand-new synthetic users, A and B, and log in as both. The server gives each a token and a basket ID. Here they are. The IDs are different from our saved evidence because this is a freshly reset container.
>
> First the control test: if I ask for A's basket with **no** token, I get 401 Unauthorized. So the server does check *who you are*.
>
> Now I'm user B. I use **B's own valid token**, but I put **A's basket ID** in the URL… and I get 200 and A's basket, with A's user ID in it. The server checks that I'm logged in, but never checks that **this basket is mine**. That's an IDOR, an Insecure Direct Object Reference. Because basket IDs are small sequential numbers, an attacker could just count upward and read every customer's basket.
>
> CVSS 6.5, but we rate the overall risk High, because anyone can register an account. To be precise: we only tested *reading*. Changing someone else's basket is likely possible, but we didn't test it, so we don't claim it. The fix is a server-side ownership check: compare the basket ID with the one in the user's token, and return 403 if they don't match."

### 8:30–9:30 · Risk prioritisation (Ahmed, Member 4)
**Screen:** `report/risk-register-and-cvss.md`, section 2 table.

> "To prioritise, we used two lenses. First, a CVSS v3.1 base score with the full vector written out, so anyone can recompute it. Second, a likelihood × impact rating for this context. When they disagree, we say why instead of fudging the vector. For example, CORS is 5.3 in CVSS but Low in our rating, because the practical impact wasn't demonstrated.
>
> So the fix order is: `/ftp` first, then the IDOR (both High), then CORS. CSP is already done."

### 9:30–11:00 · Remediation and retest of WA-001 (Ahmed)
**Screen:** `csp-proxy.conf`, then **Run:** the Step 6 commands, then the browser on `:8080` with DevTools → Network → document → Response Headers.

> "The rubric asks us to fix something and prove it. We fixed WA-001. Rather than hack the Juice Shop image, we did what companies actually do: put a reverse proxy in front of the app. This is nginx, also bound to localhost, on port 8080, and this one line adds a Content-Security-Policy. `script-src 'self'` means only scripts from our own site may run, which blocks injected scripts. `frame-ancestors 'self'` stops other sites from framing us, and `object-src 'none'` blocks plugins.
>
> Now the retest, with **the same command as before**. Port 3000, direct: no CSP. Port 8080, through the proxy: CSP is present. The `Server: nginx` line proves the traffic went through the proxy, and the Content-Length is identical (9984 bytes), so it's the same page and we didn't break the app. You can see it here in the browser's response headers too.
>
> Residual risk, honestly: port 3000 is still open without CSP so we can compare. In production the app would only be reachable through the proxy. We allow inline styles because Angular needs them. And CSP limits the damage of an XSS but doesn't fix the XSS itself."

### 11:00–12:00 · Limitations and conclusion (Najeeb)
**Screen:** `findings/findings-register.md`.

> "To wrap up. We verified **four** findings across OWASP's top two 2025 categories: Broken Access Control and Security Misconfiguration. We fixed and retested one.
>
> The answer to our research question: **the layers really are complementary.** ZAP found two issues quickly, but the two most serious ones, the `/ftp` exposure and the IDOR, were found only by manual testing. A team that only ran the scanner would have missed its biggest risks.
>
> Our limitations: it's a training app with synthetic data, we ran one scan profile, the IDOR was tested read-only, and only one fix was applied. With more time, we'd fix and retest `/ftp` and the IDOR next.
>
> All our evidence is in the repository with stable IDs. Every claim we made today maps to a file. Thank you, and we're happy to take questions."

## 16. If something breaks live (backup plan)

| Problem | What to do and say |
|---|---|
| Docker or the container won't start | "The lab is reproducible, but let's not waste your time." Open the saved evidence `.txt` files for each step. They contain the exact command and output. |
| IDOR registration fails ("email must be unique") | Change the emails (`demo2.a@lab.test`), or `docker restart juice-shop` and wait 20 s. |
| `/rest/basket` returns 401 for B | The login body was wrong, so check `$B.token` isn't empty. Fall back to [WA-004-idor-basket.txt](evidence/manual-tests/WA-004-idor-basket.txt). |
| `:8080` doesn't respond | `docker logs csp-proxy`. If Docker Desktop's `host.docker.internal` fails, show [WA-001-before/after.txt and .png](evidence/05-remediation-retest/). |
| Nmap is slow or blocked | Show [EV-001-nmap-local-baseline.txt](evidence/reconnaissance/EV-001-nmap-local-baseline.txt). |
| Running out of time | Skip the browser views and keep to the curl commands. **Never skip the retest (Step 6)** because it's a rubric requirement. |

**Never** "improvise" by testing a public site to fill time. Explain the failure honestly and show the evidence.

## 17. Status of the repo gaps (updated 30 Oct 2026)

**Fixed:**

| # | Gap | Where | What was done |
|---|---|---|---|
| 1 | Scope approval table was `TODO` | [planning/scope-and-authorization.md](planning/scope-and-authorization.md) | Names, QUIDs, and approval date (28 Oct, from the decision log) filled in |
| 2 | Meeting log was empty | [planning/meeting-log.md](planning/meeting-log.md) | 28 Oct and 30 Oct entries added from the decision log and commit history. **Add any other meetings you held.** |
| 3 | References cited OWASP Top 10:**2021** | [references.md](references.md) | Ref [2] is now OWASP Top 10:2025 |
| 4 | Test-case matrix out of date and mislabelled | [planning/test-case-matrix.md](planning/test-case-matrix.md) | TC-001 and TC-004 marked done with evidence. TC-003 (XSS) and TC-005 honestly marked "Not executed" |
| 5 | Demo run sheet was `TODO` | [video/live-demo-run-sheet.md](video/live-demo-run-sheet.md) | Timed segments, presenters, backups, and recovery plan added |
| 6 | Video script was `TODO` | [video/video-script.md](video/video-script.md) | Full narration added (about 10.5 min), plus the opening-frame text |
| 7 | Troubleshooting table was empty | [environment/troubleshooting.md](environment/troubleshooting.md) | 8 real issues added |
| 9 | `scan-summary` validation status unclear | [source/custom-script/README.md](source/custom-script/README.md) | Validation status documented (real-data run for `evidence-index`, sample-only for `scan-summary`) |
| 10 | Python not on PATH | [troubleshooting.md](environment/troubleshooting.md), script README | Full-path workaround documented. The script was run successfully with Python 3.14.0 |
| 11 | Leftover "reconcile numbering" bullet | [report/risk-register-and-cvss.md](report/risk-register-and-cvss.md) | Removed |
| 12 | Findings lacked the final CVSS vectors | `findings/WA-00x.md` | Final vectors and scores copied from the risk register |

**Still needs a human:**

| # | Item | Why it wasn't filled in automatically |
|---|---|---|
| 8 | Retest sign-off in [retest-record.md](evidence/05-remediation-retest/retest-record.md) | Moaaz and Ahmed have to sign and date it themselves. The names are filled in and the signature and date lines are left blank. |
| — | ZAP JSON export | Needs ZAP to re-export the report, if you want `scan-summary` to run on real data. Optional. |
| — | Second-device isolation check | Needs a second physical device on the LAN. Optional, and already listed as a limitation. |
| — | `TODO` lines in [references.md](references.md) (ref 9 and the AI-tool acknowledgment) | Only the team knows which extra sources were read and whether the AI statement is accurate. |

**Deadlines:** report (MS Word, ≤ 3,500 words excluding the Appendix) and video (< 12 min) are due on Blackboard by **midnight, 14 November 2026**. The live demo is in Weeks 12–13.

For the Q&A, everyone should read [video/q-and-a.md](video/q-and-a.md). It has 18 prepared questions with answers tied to evidence files. Extra questions likely to come up based on this walkthrough:

- *"Why did Nmap say `ppp?`?"* It's a fingerprint miss. Nmap didn't recognise Juice Shop's response pattern, but the captured raw response is clearly HTTP 200 HTML.
- *"Why did you fix the least severe issue?"* See §9. Rubric, safety, and reversibility. In a real job, WA-003 goes first.
- *"Why did ZAP miss `/ftp` and the IDOR?"* An IDOR needs two identities and an understanding of ownership, which no scanner has. We also used the traditional spider without an authenticated context, and ZAP itself warned this is a modern JS app.
- *"Is `incident-support.kdbx` crackable?"* We don't know and deliberately didn't try. That was outside our ethical scope.
- *"Does the proxy fix CORS too?"* No. The `after` capture still shows `Access-Control-Allow-Origin: *`. WA-002 is still open.
