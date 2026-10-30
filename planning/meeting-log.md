# Meeting Log

Entries are reconstructed from the decision log (`TEAM_TASKS.md` §11) and the
commit history. Add any further meetings with their real dates.

| Date | Members present | Completed work | Decisions/problems | Next actions |
|---|---|---|---|---|
| 2026-10-28 | All four | Lab built (Juice Shop 20.3.0 in Docker on `127.0.0.1:3000`); baseline health and isolation checks; Nmap recon (EV-001); ZAP quick scan (EV-002); manual verification of WA-001 to WA-004 | Target and scope approved; findings WA-001 to WA-004 selected. Problem: Nmap misidentified the service as `ppp?` — resolved by reading the raw HTTP fingerprint | Risk scoring; choose a finding to remediate |
| 2026-10-30 | All four | Risk register and CVSS v3.1 reasoning; WA-001 remediated with a loopback nginx CSP proxy and retested (before/after `.txt` and `.png`); Q&A sheet drafted | Contributions agreed at 25/25/25/25; WA-001 chosen for remediation because it is safe and reversible at the web tier | Video script, demo rehearsal, Word report draft |
