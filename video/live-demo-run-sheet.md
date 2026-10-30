# Live Demonstration Run Sheet

**Maximum demonstration time:** Approximately 12 minutes  
**Slides:** None  
**Full script with wording and commands:** `PROJECT_GUIDE_AND_DEMO_SCRIPT.md` §13–§16

| Time | Segment | Presenter | What is shown |
|---|---|---|---|
| 0:00–1:00 | Objective, research question, safety boundary | Najeeb Abdi (M1) | Group ID, scope file |
| 1:00–2:30 | Isolated lab and target startup | Mohanad Elhabash (M2) | `docker ps`, `docker port juice-shop`, app in browser |
| 2:30–3:30 | Reconnaissance (tool rationale: Nmap) | Moaaz Mohamed (M3) | Live `nmap -sT -sV -Pn -p 3000 127.0.0.1` |
| 3:30–4:30 | Automated scan (tool rationale: ZAP) | Moaaz Mohamed (M3) | Saved `EV-002` report, alert summary |
| 4:30–5:30 | WA-001 CSP and WA-002 CORS verification | Moaaz Mohamed (M3) | Live `curl.exe` header checks |
| 5:30–6:45 | WA-003 `/ftp` exposure | Moaaz Mohamed (M3) | Browser `/ftp`, `curl` HTTP 200 |
| 6:45–8:30 | WA-004 IDOR with two fresh synthetic accounts | Moaaz Mohamed (M3) | PowerShell: 401 without token, 200 with B's token on A's basket |
| 8:30–9:30 | Risk prioritisation (CVSS + likelihood × impact) | Ahmed Hari (M4) | `report/risk-register-and-cvss.md` |
| 9:30–11:00 | WA-001 remediation and retest | Ahmed Hari (M4) | `csp-proxy.conf`; same curl on `:3000` vs `:8080`; DevTools headers |
| 11:00–12:00 | Limitations and conclusion | Najeeb Abdi (M1) | `findings/findings-register.md` |
| 12:00–20:00 | Questions | All | `video/q-and-a.md` |

**Primary presenter:** Najeeb Abdi (opens, closes, keeps time)  
**Backup presenter:** All members — each can run any segment (`planning/team-info.md`). If Moaaz is unavailable, Mohanad runs the findings segments; if Ahmed is unavailable, Najeeb runs risk and retest.

**Demo recovery plan:**

1. Before the session, start a fresh lab (`docker rm -f juice-shop` then the `docker run` from `environment/setup-commands.md`) and start `csp-proxy` (see `evidence/05-remediation-retest/WA-001-remediation.md`). Rehearse every command once.
2. If a container fails live: `docker restart juice-shop` and wait about 20 seconds; if still down, continue from the saved evidence files, which contain the exact commands and outputs:
   - Recon: `evidence/reconnaissance/EV-001-nmap-local-baseline.txt`
   - WA-001 to WA-004: `evidence/manual-tests/`
   - Retest: `evidence/05-remediation-retest/WA-001-before/after.txt` and `.png`
3. If account registration fails during the IDOR step, use new emails (e.g. `demo2.a@lab.test`).
4. If short on time, skip browser views but never skip the retest segment.
5. Never test any target other than `127.0.0.1` to fill time. Explain a failure honestly.
