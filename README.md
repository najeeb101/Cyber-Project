# Web Application Security Assessment

## CMPS 380 Cybersecurity Fundamentals - Fall 2026

This project studies how penetration-testing tools and manual security testing can identify weaknesses in a deliberately vulnerable web application.

The team will build a safe local lab, assess the application, document verified findings, explain their impact, recommend fixes, and retest at least one fix.

> **Safety rule:** Test only the deliberately vulnerable application running in your own isolated lab. Do not scan or attack public websites, university systems, cloud services, other people's devices, or any system without written authorization.

---

## Project objective

The objective is to demonstrate a complete, ethical web-application security assessment:

1. Discover the application's exposed services and attack surface.
2. Use automated tools to identify possible weaknesses.
3. Manually verify selected findings.
4. Explain the security impact of each verified finding.
5. Prioritize findings using CVSS-informed reasoning.
6. Recommend a defensive remediation.
7. Retest at least one finding after remediation.
8. Present the results clearly in a report and demonstration.

## Recommended project setup

Use:

- **Target:** OWASP Juice Shop running locally.
- **Environment:** Docker or an isolated virtual machine.
- **Reconnaissance:** Nmap.
- **Automated web testing:** OWASP ZAP.
- **Manual testing:** Burp Suite Community or browser developer tools.
- **Optional configuration checks:** Nikto.
- **Risk analysis:** CVSS and OWASP guidance.
- **Creativity feature:** A small Python script that organizes evidence or compares scanner results.

Start with one target. Add another application only if the first lab is stable and the team has enough time.

## Recommended scope

Aim for **three to five verified findings**, not a large number of unverified alerts. Select different categories where possible, such as:

- Broken access control or IDOR
- Cross-site scripting or input-validation weakness
- Authentication or session weakness
- Security misconfiguration or information disclosure
- Injection-related weakness, only when it can be demonstrated safely

Only report findings that the team actually reproduces in its own lab.

## What is not allowed

Do not:

- Test real or public systems.
- Use real credentials or personal data.
- Perform denial-of-service or destructive attacks.
- Steal credentials or access real accounts.
- Create malware, persistence, or ransomware.
- Dump or publish sensitive data.
- Claim that a scanner result is a confirmed vulnerability without manual review.
- Copy another group's report or use uncited external material.

## Project deliverables

### 1. Project report

Submit one **MS Word document**, not PDF. The main report must be no more than **3,500 words excluding the Appendix**.

The report should include:

1. Introduction and motivation
2. Project objectives
3. Application, use cases, and threat model
4. Lab environment and tools
5. Methodology
6. Verified findings and proof of concepts
7. Risk analysis and CVSS reasoning
8. Remediation and retesting
9. Impact, learning outcomes, and limitations
10. Conclusion
11. Numbered references

The cover page must include:

- Group ID
- Names and QUIDs of all members
- Main-report word count excluding the Appendix
- Contribution percentage for each member
- Percentages adding up to 100%

### 2. Appendix

Include:

- Individual reflection from every member
- Each member's specific tasks and contribution
- Problems faced and lessons learned
- Complete user manual
- Environment setup instructions
- Safe commands
- Source code and attribution
- Screenshots and tool logs
- Evidence index

### 3. Video

The video must be **less than 12 minutes** and must include continuous narration.

The opening frame must show:

- Group ID
- Every member's name
- Every member's QUID

Show the lab, tools, selected findings, evidence, impact, remediation, and retest.

### 4. Live demonstration

The live session is approximately:

- 12 minutes for demonstration
- 8 minutes for questions and answers

Do not use PowerPoint slides. Demonstrate the working proof of concept and explain why each tool was selected.

## Simple workflow

### Step 1: Organize the team

- Confirm the Group ID.
- Record every member's name, QUID, and email.
- Assign responsibilities.
- Agree on contribution percentages.
- Select one submission owner.

### Step 2: Build the safe lab

- Install Docker or a virtual machine.
- Run OWASP Juice Shop locally.
- Keep the application on localhost or a host-only network.
- Use synthetic accounts and data only.
- Record operating-system, application, and tool versions.

### Step 3: Map the target

- Confirm the application is reachable.
- Run safe local service discovery with Nmap.
- Browse the application normally.
- Record the application routes, roles, and important assets.

### Step 4: Scan and test

- Run OWASP ZAP against the local target.
- Review scanner alerts.
- Select realistic findings from different categories.
- Manually verify every selected finding.
- Save sanitized screenshots and logs.

### Step 5: Analyze risk

For every finding, record:

- Finding ID and title
- Affected URL or component
- Preconditions
- Discovery method
- Reproduction steps
- Expected behavior
- Observed behavior
- Evidence
- Security impact
- CVSS-informed severity
- Remediation
- Retest result
- Limitations and confidence

### Step 6: Remediate and retest

- Choose at least one finding.
- Apply or demonstrate a defensive fix locally.
- Repeat the same test.
- Capture before-and-after evidence.
- Explain remaining risk.

### Step 7: Write and rehearse

- Write from the team's evidence, not assumptions.
- Keep the main report under 3,500 words.
- Complete the Appendix and user manual.
- Add numbered references and cite external sources.
- Record the narrated video.
- Rehearse the live demonstration within 12 minutes.

## Suggested folder structure

```text
project/
  README.md
  kickoff.md
  report/
  source/
  evidence/
    environment/
    reconnaissance/
    automated-scans/
    manual-tests/
    remediation-retest/
    screenshots/
  video/
  references/
```

## Evidence rule

Every important claim needs evidence. Use clear filenames such as:

```text
WA-001-original-response.png
WA-001-remediation-retest.png
EV-001-nmap-local-baseline.txt
EV-002-zap-scan-sanitized.html
```

Remove passwords, tokens, cookies, personal data, and other secrets before placing evidence in the report or video.

## Immediate next actions

1. Read [kickoff.md](./kickoff.md).
2. Confirm the group members and contribution percentages.
3. Select OWASP Juice Shop as the target unless the instructor approves another target.
4. Install and isolate the lab.
5. Create the evidence folders.
6. Record all tool and application versions.
7. Complete the baseline and reconnaissance checks.
8. Select three to five findings that can be safely verified.
9. Create one finding record for each selected finding.
10. Complete one remediation and retest.
11. Draft the report using the rubric checklist in [kickoff.md](./kickoff.md).
12. Record and rehearse the video and live demonstration.

## Definition of success

The project is ready when:

- The lab can be rebuilt from the user manual.
- Testing stayed inside the authorized local environment.
- Three or more findings were manually verified.
- Every finding has evidence, impact, severity, remediation, and limitations.
- At least one finding was retested after remediation.
- The report, Appendix, video, and live demonstration satisfy the course rubric.
- All external sources and code are properly acknowledged.

## Deadline

The report and video are due on Blackboard by **midnight, 14 November 2026**.

