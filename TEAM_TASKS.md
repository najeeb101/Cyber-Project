# Four-Member Team Task Plan

## Web Application Security Assessment Project

This document divides the project between four members. Replace `Member 1` through `Member 4` with the actual names, QUIDs, and contact details.

> Every member must understand the complete project and be able to explain the final demonstration. Task ownership does not mean that only one person is responsible for understanding that part.

---

## 1. Team information

| Member | Name | QUID | Main role | Backup role |
|---|---|---|---|---|
| Member 1 | Najeeb Abdi | 202307172 | Project coordinator and methodology | Report editor |
| Member 2 | Mohanad Elhabash | 202314448 | Lab and environment engineer | Demonstration backup |
| Member 3 | Moaaz Mohamed | 202207862 | Security tester and evidence owner | Tool demonstrator |
| Member 4 | Ahmed Hari | 202203669 | Risk, remediation, report, and media | Presentation coordinator |

### Contribution percentages

The percentages must reflect actual work and must add up to exactly 100%.

| Member | Planned contribution | Final agreed contribution |
|---|---:|---:|
| Member 1 | 25% | 25% |
| Member 2 | 25% | 25% |
| Member 3 | 25% | 25% |
| Member 4 | 25% | 25% |
| **Total** | **100%** | **100%** |

---

## 2. Project boundaries for every member

All members must follow these rules:

- Test only the intentionally vulnerable application running in the team's isolated local lab.
- Do not scan public websites, university systems, cloud services, or another person's device.
- Use synthetic accounts and data only.
- Do not use real passwords, personal information, or secrets.
- Do not perform denial-of-service, destructive attacks, persistence, malware, or credential theft.
- Stop testing if traffic could leave the authorized lab.
- Record evidence for every finding.
- Do not report scanner alerts as confirmed vulnerabilities without manual verification.
- Sanitize cookies, tokens, passwords, and personal data from screenshots and logs.
- Cite external sources, commands, code, images, and documentation.

---

## 3. Role 1: Project coordinator and methodology owner

**Primary owner:** Member 1  
**Main purpose:** Keep the project aligned with the course rubric and ensure the work follows a recognized methodology.

### Responsibilities

- Confirm the Group ID, members, QUIDs, and contact details.
- Maintain the project schedule and meeting notes.
- Confirm the final scope and authorization statement.
- Create the project threat model.
- Define the selected use cases and acceptance criteria.
- Coordinate the OWASP WSTG/PTES-based methodology.
- Maintain the rubric-to-evidence checklist.
- Coordinate report structure and word count.
- Ensure all report sections are complete and logically connected.
- Collect each member's reflection and contribution information.
- Coordinate final submission by the designated uploader.

### Deliverables

- Final project scope.
- Authorization and safety statement.
- Threat model.
- Use-case and test-case matrix.
- Rubric-to-evidence checklist.
- Report outline.
- Meeting and decision log.
- Final submission checklist.

### Required evidence

- `evidence\00-scope-authorization\authorization-statement.md`
- `evidence\00-scope-authorization\threat-model.png`
- `evidence\00-scope-authorization\use-case-matrix.xlsx` or `.csv`
- `evidence\00-scope-authorization\meeting-log.md`

### Review partner

Member 4 reviews the report structure and rubric coverage. Member 1 reviews the technical accuracy of the final findings with Member 3.

---

## 4. Role 2: Lab and environment engineer

**Primary owner:** Member 2  
**Main purpose:** Build a reproducible, isolated, and resettable testing environment.

### Responsibilities

- Install or configure Docker or the selected virtual machine.
- Deploy OWASP Juice Shop locally unless the team approves another target.
- Configure localhost, host-only, or another isolated network.
- Verify that the vulnerable application is not exposed to the public internet.
- Record operating system, VM, Docker, browser, target, and tool versions.
- Create the clean baseline snapshot or container recreation procedure.
- Document startup, health-check, reset, and cleanup commands.
- Troubleshoot environment problems.
- Prepare the lab for the video and live demonstration.
- Keep a backup demonstration environment if practical.

### Deliverables

- Working isolated lab.
- Environment inventory.
- Setup instructions.
- Health-check procedure.
- Reset and cleanup procedure.
- Architecture diagram.
- Troubleshooting section.

### Required evidence

- `evidence\01-environment\environment-inventory.md`
- `evidence\01-environment\architecture-diagram.png`
- `evidence\01-environment\baseline-health.txt`
- `evidence\01-environment\isolation-check.txt`
- `evidence\01-environment\setup-commands.txt`
- `evidence\01-environment\reset-procedure.txt`

### Example safe setup record

Record the actual commands used. Do not copy a command without checking the target and binding:

```powershell
docker --version
docker compose version
docker pull bkimminich/juice-shop
docker run --name juice-shop -d -p 127.0.0.1:3000:3000 bkimminich/juice-shop
docker ps
docker logs --tail 50 juice-shop
curl.exe -I http://127.0.0.1:3000
```

### Review partner

Member 3 verifies that the target is reachable for testing. Member 1 verifies that the scope and isolation documentation are clear.

---

## 5. Role 3: Security tester and evidence owner

**Primary owner:** Member 3  
**Main purpose:** Perform safe reconnaissance, automated assessment, manual verification, and evidence collection.

### Responsibilities

- Confirm that every test target is inside the authorized lab.
- Perform safe local service discovery with Nmap.
- Configure OWASP ZAP for passive browsing and controlled scanning.
- Use Burp Suite Community or browser developer tools for manual verification.
- Use Nikto only if it contributes useful, non-duplicated evidence.
- Select three to five findings that can actually be reproduced.
- Create a finding record for every selected vulnerability.
- Capture sanitized screenshots, logs, requests, and responses.
- Identify false positives and duplicate scanner alerts.
- Avoid destructive payloads and excessive requests.
- Explain the expected secure behavior versus the observed behavior.

### Recommended finding categories

Choose only categories that are actually verified:

- Broken access control or IDOR.
- Cross-site scripting or input-validation weakness.
- Authentication or session weakness.
- Security misconfiguration or information disclosure.
- Injection-related weakness demonstrated safely.

### Deliverables

- Nmap reconnaissance output.
- ZAP scan output.
- Manual verification records.
- Three to five verified finding records.
- False-positive review.
- Sanitized screenshots and logs.
- Automated-versus-manual comparison data.

### Required evidence

- `evidence\02-reconnaissance\nmap-local-baseline.txt`
- `evidence\03-automated-scans\zap-report-sanitized.html`
- `evidence\03-automated-scans\nikto-report.txt` if used
- `evidence\04-manual-tests\WA-001-record.md`
- `evidence\04-manual-tests\WA-002-record.md`
- `evidence\04-manual-tests\WA-003-record.md`
- `evidence\06-screenshots\`

### Finding record

Every finding must contain:

- Finding ID.
- Title.
- Affected URL or component.
- Preconditions.
- Discovery method.
- Safe reproduction steps.
- Expected behavior.
- Observed behavior.
- Evidence filenames.
- OWASP category where applicable.
- Impact on confidentiality, integrity, and availability.
- CVSS-informed severity reasoning.
- Remediation recommendation.
- Retest status.
- Confidence and limitations.

### Review partner

Member 4 reviews the impact and severity evidence. Member 1 reviews whether the finding supports a rubric requirement.

---

## 6. Role 4: Risk, remediation, report, and media owner

**Primary owner:** Member 4  
**Main purpose:** Convert technical findings into risk analysis, remediation evidence, report content, and a clear demonstration.

### Responsibilities

- Review every finding for technical impact and business relevance.
- Prepare CVSS-informed severity reasoning.
- Map findings to the applicable OWASP category.
- Write remediation recommendations.
- Coordinate at least one remediation and retest.
- Maintain the evidence index.
- Build the report's impact, limitations, and learning-outcomes sections.
- Draft the narrated video script.
- Edit or assemble the video.
- Prepare the live demonstration sequence.
- Prepare likely Q&A answers.
- Check that no secrets appear in the report or video.

### Deliverables

- Risk register.
- CVSS reasoning table.
- Remediation plan.
- Before-and-after retest evidence.
- Impact and limitations content.
- Video script and final video.
- Live demo run sheet.
- Q&A preparation sheet.

### Required evidence

- `evidence\05-remediation-retest\WA-001-before.png`
- `evidence\05-remediation-retest\WA-001-after.png`
- `evidence\05-remediation-retest\retest-record.md`
- `evidence\findings-index.md`
- `video\script.md`
- `video\demo-run-sheet.md`
- `video\q-and-a.md`

### Review partner

Member 3 confirms that the remediation addresses the actual finding. Member 1 checks that risk and limitations are accurately described.

---

## 7. Shared responsibilities

No member should work only on their assigned section. Everyone must contribute to:

- Understanding the target application.
- Testing the demonstration flow.
- Reviewing the report.
- Practicing the video narration or live explanation.
- Answering questions about safety and methodology.
- Checking the final evidence.
- Attending required class presentations.

Each member must write an individual reflection. Reflections must be different and must describe real work.

---

## 8. Task dependency order

Tasks must be completed in this order:

1. Member 1 defines scope, roles, and use cases.
2. Member 2 builds and isolates the lab.
3. Member 3 verifies the lab and performs reconnaissance.
4. Member 3 performs scanning and manual testing.
5. Member 4 reviews findings and prioritizes risk.
6. Members 3 and 4 select and perform a safe remediation/retest.
7. Member 1 integrates the report structure and rubric evidence.
8. Member 4 produces the video and demo flow.
9. All members review, rehearse, and approve the final deliverables.
10. The submission owner uploads the final report and video.

Do not begin active testing before the lab scope and isolation are confirmed.

---

## 9. Two-week execution plan

The submission deadline is midnight on 14 November 2026. Adjust the dates if the team starts earlier or later, but do not delay the final review.

### Day 1: Team setup

- Member 1: Complete team information and scope.
- Member 2: Confirm Docker/VM availability.
- Member 3: Confirm testing tools.
- Member 4: Create evidence and media folders.

### Days 2-3: Lab construction

- Member 2 builds the isolated target.
- Member 1 approves the threat model and use cases.
- Members 3 and 4 independently verify that the application works.

### Days 4-5: Baseline and reconnaissance

- Member 3 runs Nmap and records the attack surface.
- Member 2 records environment and version information.
- Member 1 checks scope evidence.
- Member 4 prepares the initial risk-register format.

### Days 6-8: Scanning and manual verification

- Member 3 runs ZAP and optional Nikto.
- Member 3 manually verifies selected findings.
- Member 4 reviews severity and impact.
- Member 1 checks that findings support the rubric.

### Days 9-10: Remediation and retesting

- Member 4 proposes a defensive fix.
- Member 3 verifies the fix and repeats the test.
- Member 2 resets or rebuilds the lab when necessary.
- Member 1 records the result in the report structure.

### Days 11-13: Report and Appendix

- Member 1 coordinates the main report.
- Member 3 writes technical finding details.
- Member 4 writes risk, impact, limitations, and remediation sections.
- Member 2 writes setup, environment, commands, and troubleshooting.
- All members complete their reflections.

### Days 14-15: Video and rehearsal

- Member 4 produces the narrated video.
- Member 2 prepares the stable demo environment.
- Member 3 demonstrates the technical findings.
- Member 1 keeps the demo within 12 minutes and checks the rubric.

### Final review day

- All members read the complete report.
- Check the main word count.
- Check the cover page.
- Check the contribution percentages.
- Check references and citations.
- Check that the video is below 12 minutes and narrated.
- Test the final files on another computer if possible.
- The submission owner uploads only the final approved files.

---

## 10. Finding ownership matrix

Use this table when findings are selected. One member owns the technical record, but at least one other member must review it.

| Finding ID | Finding title | Technical owner | Risk reviewer | Evidence complete | Retested |
|---|---|---|---|---|---|
| WA-001 | `TODO` | Member 3 | Member 4 | `TODO` | `TODO` |
| WA-002 | `TODO` | Member 3 | Member 1 | `TODO` | `TODO` |
| WA-003 | `TODO` | Member 3 | Member 4 | `TODO` | `TODO` |
| WA-004 | `Optional` | Member 3 | Member 1 | `TODO` | `TODO` |
| WA-005 | `Optional` | Member 3 | Member 4 | `TODO` | `TODO` |

Do not fill this table with findings that were not reproduced.

---

## 11. Meeting and communication rules

Hold short team meetings at least twice per week. Each meeting should answer:

1. What was completed?
2. What evidence was created?
3. What is blocked?
4. What is the next task?
5. Is any safety or scope issue present?

Use a shared decision log:

| Date | Decision | Reason | Members agreeing |
|---|---|---|---|
| `TODO` | Selected target | `TODO` | `TODO` |
| `TODO` | Selected findings | `TODO` | `TODO` |
| `TODO` | Contribution percentages | `TODO` | `TODO` |

If members disagree about contribution percentages, record the disagreement and contact the instructor according to the course instructions.

---

## 12. Final individual checklists

### Member 1

- [ ] Team information is complete.
- [ ] Scope and authorization are documented.
- [ ] Threat model and use cases are complete.
- [ ] Rubric-to-evidence matrix is complete.
- [ ] Main report is logically organized.
- [ ] Word count is within the limit.
- [ ] Submission checklist is complete.

### Member 2

- [ ] Lab is isolated.
- [ ] Target starts reliably.
- [ ] Versions are recorded.
- [ ] Setup commands are tested.
- [ ] Reset and cleanup commands are tested.
- [ ] Architecture diagram is complete.
- [ ] Backup demo environment is available if possible.

### Member 3

- [ ] Reconnaissance is limited to the lab.
- [ ] Automated scans are saved.
- [ ] Selected findings are manually verified.
- [ ] Every finding has sanitized evidence.
- [ ] False positives are identified.
- [ ] No destructive activity occurred.
- [ ] Technical demo steps are rehearsed.

### Member 4

- [ ] Risk register is complete.
- [ ] CVSS reasoning is documented.
- [ ] Remediation is tested.
- [ ] Before-and-after evidence is saved.
- [ ] Impact and limitations are written.
- [ ] Video is narrated and under 12 minutes.
- [ ] Q&A and live demo are rehearsed.

---

## 13. Final team acceptance checklist

- [ ] Four members' names, QUIDs, and percentages are complete.
- [ ] Contribution percentages total exactly 100%.
- [ ] The target is authorized and isolated.
- [ ] Three to five findings are verified.
- [ ] At least two assessment approaches were used.
- [ ] Every finding has evidence and a reviewer.
- [ ] At least one finding was remediated and retested.
- [ ] The report body is no more than 3,500 words excluding the Appendix.
- [ ] The Appendix includes reflections, manual, commands, code, and logs.
- [ ] All external sources are cited.
- [ ] No secrets or personal data appear in the deliverables.
- [ ] The video is less than 12 minutes and has continuous narration.
- [ ] The video opening frame includes Group ID, names, and QUIDs.
- [ ] The live demonstration uses no PowerPoint slides.
- [ ] Every member can explain the complete project.
- [ ] The final report is an MS Word file, not PDF.
- [ ] Only one member uploads the final report and video.
- [ ] Submission is completed before midnight on 14 November 2026.

