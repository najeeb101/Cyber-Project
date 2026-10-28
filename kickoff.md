# Kickoff Specification

## Web Application Security Assessment Using Penetration Testing and Vulnerability Analysis Techniques

**Course:** CMPS 380 Cybersecurity Fundamentals, Fall 2026  
**Project deliverables:** Project Report (MS Word, including Appendix) and narrated Video  
**Blackboard deadline:** 14 November 2026, midnight  
**Live presentation:** 20 minutes total during Weeks 12-13: 12 minutes demonstration and 8 minutes Q&A  
**Working project name:** Controlled Web Application Security Assessment Lab  
**Document purpose:** This file is the authoritative project brief for the team and for any AI assistant helping the team. It defines the objective, scope, safety rules, technical plan, evidence requirements, report structure, video plan, grading alignment, acceptance checks, and exclusions.

> **Important:** This document is a project execution specification, not the final report. It may be used to create the report, appendix, source code, screenshots, evidence package, and demonstration. The final report must be written in the team's own words and must cite all external material.

---

## 1. Executive project definition

### 1.1 Project idea

The team will build a small, isolated web application security assessment laboratory and use it to assess an intentionally vulnerable training web application. The assessment will combine:

1. **Reconnaissance and attack-surface discovery** using Nmap.
2. **Automated web vulnerability discovery** using OWASP ZAP and, where appropriate, Nikto.
3. **Manual verification** of selected findings against the application.
4. **Risk analysis** using CVSS concepts and business impact.
5. **Evidence-based reporting** with reproducible steps, screenshots, request/response evidence, affected components, and remediation advice.
6. **Remediation validation** by retesting after a mitigation or configuration change.

The preferred target is **OWASP Juice Shop** running locally in Docker or another isolated local environment. A deliberately vulnerable local application such as DVWA may be used instead if the team documents the choice and ensures that the selected use cases are suitable for a web-application assessment.

The project is not intended to attack a real organization, public website, university service, cloud tenant, classmate's device, or any system without written authorization. Every test must remain inside the team's local lab or an explicitly authorized educational platform.

### 1.2 Central research question

> How effectively can a layered penetration-testing workflow identify, verify, prioritize, and communicate web-application security weaknesses in a controlled training application, and how does retesting demonstrate the value of remediation?

### 1.3 Main thesis

A repeatable assessment that combines network discovery, automated scanning, manual verification, risk scoring, and remediation retesting produces more useful security results than relying on a single scanner. The project will demonstrate both the capabilities and the limitations of common penetration-testing tools.

### 1.4 Expected final result

At the end of the project, a reviewer should be able to:

- Start the lab from the user manual.
- Understand the application's attack surface and trust boundaries.
- Reproduce at least three documented, authorized findings.
- See which tool or method discovered each finding.
- Distinguish scanner observations from manually verified vulnerabilities.
- Follow the risk rationale and remediation recommendations.
- Observe at least one retest showing that a mitigation changed the result.
- Understand the limitations, ethical boundaries, and societal impact of the work.

---

## 2. Assignment requirements extracted from the course brief

These are mandatory requirements from the supplied course handout. The team must treat them as acceptance criteria.

### 2.1 Submission requirements

- Submit **one MS Word report**, not PDF.
- Include the main report and Appendix in the same Word file.
- Submit **one video** in the separate Blackboard Video folder.
- Only one group member uploads one copy of each deliverable.
- Deadline for the report and video: **14-11-2026 at midnight**.
- The video must be less than 12 minutes and must include continuous background narrative.
- The live session is 20 minutes: approximately 12 minutes of demonstration and 8 minutes of questions.
- All group members must attend the presentations delivered by other groups.

### 2.2 Cover-page requirements

The report cover page must include:

- Group ID.
- Every student's name.
- Every student's QUID.
- Total word count of the main report, excluding the Appendix.
- Contribution percentage for each member.
- Contribution percentages that add up to exactly 100%.
- Agreement by all members on the effort distribution.

The video opening frame must include:

- Group ID.
- Every student's name.
- Every student's QUID.

The video must be readable, high quality, logically sequenced, and narrated.

### 2.3 Main-report requirements

The main report must not exceed **3,500 words excluding the Appendix**. It must include:

- Project objective.
- Application use case.
- What was done and how it was done.
- Environment setup commands.
- Implementation, application, or prototype details.
- Proof-of-concept details.
- Technologies and tools used.
- Limitations.
- Impact on society and computer security.
- What other people can learn from the project.
- References, with numbered citations in the body.

The recommended formatting is:

- Times New Roman or Arial.
- 11-point font.
- Single-column format.
- 1.0 line spacing.
- Clear sections and subsections.
- Tables and diagrams where they improve clarity.

### 2.4 Appendix requirements

The Appendix has no word limit and must include:

- Individual reflection for every group member.
- Specific tasks and contributions of every group member.
- Problems faced and how they were addressed.
- What each member learned.
- User manual for the implementation/prototype/demo.
- Source code created by the team.
- Source code or material used from other resources, with appropriate attribution.
- Commands for the functions/use cases of the demonstration.
- Technology and environment setup information.

### 2.5 Grading distribution

| Area | Weight | What must be demonstrated |
|---|---:|---|
| Overall report structure, clarity, margins, fonts, documentation quality | 2% | Professional, readable, logically organized report |
| Requirement 1: Project description | 2% | Introduction, objectives, key applications/use cases/scenarios, references |
| Requirement 2: Implementation explanation | 2% | Working PoC, environment, tools, technologies, learning outcomes, novelty, quality |
| Requirement 3: Impact and limitations | 2% | Usefulness, harm/risk, impact on security and society, learning value, limitations |
| Appendix: Requirement 4 reflection | 1% | Individual contributions, difficulties, and learning |
| Appendix: Requirement 5 manual/code | 1% | Setup, commands, technologies, environment, source code, user instructions |
| Video | 4% | Quality, narration, group information, sequence, tool explanations, clarity |
| Live demonstration | 6% | No PowerPoint slides; working PoC, clear explanation, tool rationale, Q&A, confidence |
| Project complexity | 5% | Creativity, effort, multiple appropriate tools, realistic scenarios, depth |
| **Total** | **25%** | All deliverables and presentation |

### 2.6 Academic-integrity requirements

- Do not copy another group's work or an old student report.
- Do not copy text without citation.
- Cite external tools, documentation, vulnerability descriptions, standards, images, code, and datasets.
- Keep similarity below the course's stated 20% threshold.
- Use original screenshots and original lab results.
- Keep a research log recording the source and purpose of every borrowed idea or code fragment.
- Never claim that a tool found or verified a weakness unless the team has evidence from its own lab.

---

## 3. Scope and boundaries

### 3.1 In scope

- A local, intentionally vulnerable training web application.
- The application's HTTP/HTTPS interface and its locally exposed supporting service ports.
- Authentication and session behavior in the training application using only team-created test accounts.
- Input validation and output encoding checks in non-destructive lab scenarios.
- Access-control checks using accounts and roles supplied by the lab.
- Common OWASP-style categories such as injection, broken access control, authentication/session weaknesses, security misconfiguration, and sensitive-data exposure.
- Network and service discovery of the team's own lab host.
- Automated and manual assessment results.
- CVSS-informed prioritization.
- Remediation recommendations and at least one retest.
- Tool limitations, false positives, false negatives, and ethical implications.

### 3.2 Explicitly out of scope

- Scanning or testing public websites, university infrastructure, cloud subscriptions, third-party systems, or networks without written authorization.
- Testing real users, real credentials, real personal data, or real payment information.
- Credential theft, password spraying, phishing, social engineering, or bypassing another person's account.
- Denial-of-service, stress testing, resource exhaustion, destructive payloads, ransomware, persistence, malware, or data exfiltration.
- Exploiting systems beyond what is necessary to demonstrate the selected local training use case.
- Evading endpoint detection, bypassing access controls on non-lab systems, or publishing weaponized exploit code.
- Claiming production security or compliance from a toy application.
- Collecting or displaying secrets in the report or video.
- Using a payload that can escape the local container/VM or affect the host.

### 3.3 Safety rule

If a test could affect a system, person, account, or data outside the isolated lab, stop and obtain explicit written authorization or remove that test from the project. When uncertain, choose the safer non-destructive demonstration.

### 3.4 Authorization record

The Appendix must contain a short authorization statement signed or approved by the group:

> The team authorizes testing only against the locally controlled training application and lab network created for this project. The team will not test third-party or public systems. Testing is non-destructive, uses synthetic accounts/data, and stops if the activity could affect systems outside the lab.

If the instructor requires a different authorization format, replace this statement with the instructor-approved version.

---

## 4. Proposed lab architecture

### 4.1 Recommended architecture

```text
                         Isolated local lab

  Analyst workstation
  (browser, ZAP, Nmap, Nikto)
           |
           | localhost or private host-only network
           v
  Docker host / Linux VM
  +---------------------------+
  | OWASP Juice Shop          |
  | intentionally vulnerable  |
  | synthetic data only       |
  +---------------------------+
           |
           v
  Optional local database/container
  (never populated with real data)
```

### 4.2 Environment options

Preferred:

- Windows host with Docker Desktop, or
- Linux VM such as Ubuntu, Kali, or Parrot in VirtualBox/VMware.

The team may use any operating environment permitted by the assignment. Record:

- Operating system and version.
- VM or container platform and version.
- CPU, RAM, and disk allocation if a VM is used.
- Docker and image versions if Docker is used.
- Browser and version.
- Tool versions.
- Local IP address or localhost binding.
- Date and time of every important test.

### 4.3 Isolation controls

- Bind the vulnerable application to `127.0.0.1` where practical.
- If a VM is required, use host-only or an explicitly isolated private network.
- Do not use bridged networking unless there is a documented reason and a firewall rule preventing unintended access.
- Do not expose the vulnerable application to the public internet.
- Use synthetic usernames, passwords, products, and orders.
- Disable or remove unnecessary port forwarding.
- Take a clean snapshot before testing.
- Keep a restore procedure in the Appendix.

---

## 5. Technical work plan

### Phase 0: Team and approval

**Goal:** Confirm the team, topic, scope, and responsibilities.

Checklist:

- [ ] Group ID recorded.
- [ ] Names, QUIDs, and contact details collected.
- [ ] Contribution percentages agreed and total exactly 100%.
- [ ] Project topic sent to the instructor by the required course date, if still applicable.
- [ ] Scope and authorization statement approved by all members.
- [ ] One member designated as submission owner.
- [ ] One backup member designated for the demo.

### Phase 1: Research and design

**Goal:** Establish a defensible assessment methodology before running tools.

Tasks:

1. Read the OWASP Web Security Testing Guide and relevant OWASP Top 10 material.
2. Read the OWASP Juice Shop documentation and safe-use guidance.
3. Read official documentation for Nmap, OWASP ZAP, Nikto, and CVSS.
4. Define the selected use cases and expected evidence before testing.
5. Create a threat model:
   - Assets: user account, session, order/profile data, application integrity.
   - Actors: unauthenticated visitor, normal user, administrator-like lab user.
   - Trust boundaries: browser-to-application, user-to-user data access, application-to-database.
   - Security objectives: confidentiality, integrity, availability, authentication, authorization, accountability.
6. Define success measures:
   - At least three findings reproducibly verified.
   - At least two different assessment approaches used.
   - Every finding has evidence, impact, severity rationale, and remediation.
   - At least one finding is retested after mitigation.
   - The lab can be rebuilt using the user manual.

Deliverables:

- Scope and authorization record.
- Architecture diagram.
- Threat model.
- Test-case matrix.
- Source and evidence log.

### Phase 2: Build and baseline the lab

**Goal:** Produce a reproducible, isolated environment.

Example setup commands (adapt to the chosen platform and record actual output):

```powershell
# Verify Docker is available
docker --version
docker compose version

# Pull and run the intentionally vulnerable training application locally
docker pull bkimminich/juice-shop
docker run --name juice-shop -d -p 127.0.0.1:3000:3000 bkimminich/juice-shop

# Confirm the container is running
docker ps
docker logs --tail 50 juice-shop

# Confirm the application responds locally
curl.exe -I http://127.0.0.1:3000
```

If the team uses a compose file, include the exact file in the Appendix and use a pinned image version when possible. Do not copy commands blindly: verify image names and versions from official documentation.

Baseline checks:

- [ ] The application opens in a browser at the documented local URL.
- [ ] The target is reachable only from the intended workstation/lab network.
- [ ] No real data is present.
- [ ] A clean snapshot or container recreation procedure exists.
- [ ] The application version and hash/tag are recorded.
- [ ] The team has a test account created solely for the lab.
- [ ] The baseline has no unexplained errors.

### Phase 3: Reconnaissance and attack-surface mapping

**Goal:** Identify the lab's exposed services without disruption.

Example commands against the local target only:

```powershell
# Replace the target with the documented local lab address.
nmap -sV -Pn -p 3000 127.0.0.1 -oN evidence\nmap-baseline.txt

# If the lab uses a private VM address, use that address only.
nmap -sV --top-ports 100 <LAB_PRIVATE_IP> -oN evidence\nmap-services.txt
```

Record:

- Target address and why it is authorized.
- Scan date/time.
- Port, protocol, service, and version.
- What the result means for the attack surface.
- Any discrepancy between expected and observed services.

Do not run broad internet scans or scan an address that is not proven to belong to the isolated lab.

### Phase 4: Automated web assessment

**Goal:** Generate candidate findings, not blindly declare vulnerabilities.

Use OWASP ZAP:

1. Configure the target URL manually.
2. Start with passive browsing/spidering.
3. Use an authenticated context only with the synthetic lab account.
4. Run active scanning only against the local target.
5. Export the report.
6. Record the scanner version, policy, scope, duration, and exclusions.

Optional Nikto example, only against the local target:

```powershell
nikto -h http://127.0.0.1:3000 -output evidence\nikto-baseline.txt
```

Scanner rules:

- Treat scanner alerts as hypotheses until manually verified.
- Record false positives and duplicate alerts.
- Do not include an alert solely because it appears in a report.
- Do not use a high-impact scan profile if a lower-impact profile answers the question.
- Stop if the application becomes unstable.

### Phase 5: Manual verification and proof of concept

**Goal:** Confirm selected findings safely and explain them clearly.

Select at least three findings covering different security concepts. A strong set may include:

- One access-control or authorization issue.
- One injection or input-validation issue in a harmless training endpoint.
- One authentication/session/security-configuration issue.
- One information-disclosure or security-header issue.

The exact findings must be based on the current lab version and actual evidence. Never invent results.

For each finding, create a test record:

| Field | Required content |
|---|---|
| Finding ID | Stable ID such as `WA-001` |
| Title | Clear vulnerability name |
| Affected URL/component | Local target only |
| Preconditions | Account, role, or state needed |
| Discovery method | Tool, manual observation, or both |
| Safe reproduction | Minimal steps and sanitized request/response |
| Expected behavior | What a secure application should do |
| Observed behavior | What the lab actually did |
| Evidence | Screenshot, log, request/response, timestamp |
| Impact | Confidentiality, integrity, availability, and affected actor |
| Severity | CVSS-informed rationale |
| Remediation | Specific defensive change |
| Retest | Result after mitigation, or reason retest is not possible |
| Confidence | High, medium, or low with justification |

Proof-of-concept rules:

- Use the smallest non-destructive action that proves the issue.
- Use synthetic accounts and data.
- Mask tokens, cookies, passwords, and secrets in screenshots.
- Do not publish a reusable attack against real software.
- Explain the security concept rather than maximizing offensive effect.
- Restore the lab after every test that changes state.

### Phase 6: Risk analysis

**Goal:** Prioritize findings in a transparent and reproducible way.

For each verified finding:

1. Identify the affected asset and security property.
2. Explain exploitability in the lab.
3. Explain whether authentication or user interaction is required.
4. Explain potential confidentiality, integrity, and availability impact.
5. Use CVSS terminology and cite the official CVSS source.
6. Record the vector or scoring rationale when the team can justify it.
7. Distinguish technical severity from business risk.
8. State limitations: a toy lab does not prove production exploitability.

Recommended risk table:

| ID | Finding | Affected asset | Severity | Confidence | Why it matters | Priority |
|---|---|---|---|---|---|---|
| WA-001 | ... | ... | High/Medium/Low | High/Medium/Low | ... | P1/P2/P3 |

Do not inflate severity merely to make the project appear complex. A well-supported medium finding with honest limitations is better than an unsupported critical claim.

### Phase 7: Remediation and retesting

**Goal:** Demonstrate that assessment leads to measurable improvement.

For at least one finding:

1. Capture the original result.
2. Identify a defensive remediation.
3. Apply the remediation locally, or implement a safe demonstrator fix in a wrapper/test application.
4. Restart or reset the lab as needed.
5. Repeat the same test.
6. Capture the changed result.
7. Explain residual risk and what the fix does not address.

Possible remediation categories:

- Server-side authorization checks on every object access.
- Input validation and parameterized queries.
- Output encoding and context-aware escaping.
- Secure cookie flags and session invalidation.
- Security headers and removal of unnecessary disclosure.
- Least privilege and safer error handling.
- Dependency and image updates.

The project must clearly distinguish a real fix to the selected application from a conceptual recommendation. Do not claim that a vulnerable third-party image was modified unless the team actually modified and tested it.

### Phase 8: Package evidence and write deliverables

**Goal:** Make every claim traceable.

Evidence package structure:

```text
evidence/
  00-scope-authorization/
  01-environment/
  02-reconnaissance/
  03-zap/
  04-manual-tests/
  05-remediation-retest/
  06-screenshots/
  07-tool-versions/
  findings-index.md
  evidence-log.csv
```

Every artifact should have:

- A meaningful filename.
- Date/time.
- Test ID or finding ID.
- Target scope.
- Sanitized content.
- A short description in the evidence log.

---

## 6. Proposed assessment use cases

The team should choose three to five use cases and keep the final set coherent. The following are recommended candidates; they are not claims that the target contains every issue.

### Use case A: Unauthenticated attack-surface discovery

**Question:** What services and web entry points are exposed by the local lab?  
**Method:** Nmap service discovery, browser navigation, ZAP passive crawl.  
**Evidence:** Nmap output, discovered routes, architecture map.  
**Learning point:** Enumeration is necessary but does not itself prove a vulnerability.  
**Safety:** Local target only; no aggressive or broad scanning.

### Use case B: Access-control verification

**Question:** Can a normal synthetic user access another user's object or privileged function?  
**Method:** Use two team-created accounts with distinct data; compare authorized and unauthorized requests.  
**Evidence:** Sanitized request/response, account-role table, screenshots, expected/observed behavior.  
**Learning point:** Authentication proves identity; authorization decides permitted actions.  
**Safety:** Synthetic data only; do not access another real person's data.

### Use case C: Input-validation or injection verification

**Question:** Does a selected input reach a security-sensitive operation without adequate server-side validation?  
**Method:** Use a minimal, non-destructive training payload and observe only a controlled response.  
**Evidence:** Input location, sanitized request, response, log, and safe expected result.  
**Learning point:** Client-side validation is not a security boundary.  
**Safety:** Never alter or delete data; stop if the behavior could become destructive.

### Use case D: Authentication and session review

**Question:** Are login, logout, session expiration, cookie attributes, or password-reset behaviors configured safely?  
**Method:** Browser developer tools and ZAP passive inspection using synthetic accounts.  
**Evidence:** Sanitized cookie/header view, session-state timeline, configuration observation.  
**Learning point:** Session security spans transport, token lifecycle, storage, and invalidation.  
**Safety:** No credential guessing, password spraying, or use of real credentials.

### Use case E: Security-configuration and information-disclosure review

**Question:** Does the application reveal unnecessary version, stack, directory, or diagnostic information?  
**Method:** ZAP/Nikto observations and manual confirmation.  
**Evidence:** Sanitized response headers/body and tool result.  
**Learning point:** Low-severity disclosures can make higher-impact attacks easier.  
**Safety:** Do not use disclosed information to attack anything outside the lab.

---

## 7. Tool selection and justification

| Tool | Purpose | Why it is included | Limitation to explain |
|---|---|---|---|
| Docker or VM | Isolated target environment | Reproducible, resettable lab | Container isolation is not a complete security boundary |
| OWASP Juice Shop or DVWA | Intentionally vulnerable target | Safe educational PoC target | Findings do not represent every production application |
| Nmap | Service and version discovery | Establishes attack surface | Port visibility does not prove application vulnerability |
| OWASP ZAP | Web proxy, crawling, passive and active scanning | Combines observation and automated assessment | Can miss logic flaws and produce false positives |
| Nikto, optional | Web-server configuration checks | Adds a second automated perspective | Signature-based checks can be noisy or outdated |
| Browser developer tools | Manual request, cookie, and header inspection | Makes behavior understandable | Manual observation depends on tester coverage |
| CVSS calculator/specification | Severity communication | Consistent risk vocabulary | CVSS is not the same as business impact |
| PowerShell/Linux shell | Reproducible setup and commands | User manual and repeatability | Commands depend on platform and versions |

The report must explain why each selected tool was used and why another tool was not sufficient by itself.

---

## 8. Data, privacy, and evidence handling

- Use only synthetic names, accounts, products, orders, and tokens.
- Do not include passwords, API keys, session cookies, authorization headers, or personal data in the report.
- Redact secrets before adding screenshots to evidence.
- Store evidence in the project folder, not in a public repository.
- Do not upload vulnerable application data or exploit output to public services.
- Keep original evidence and a sanitized copy separate.
- If a screenshot contains a secret, delete the exposed secret from the lab and recapture the screenshot.
- Use a consistent finding ID in filenames and the report.

---

## 9. Report blueprint, limited to 3,500 main-text words

The following allocation is a guide, not a requirement to hit every number exactly.

### Cover page (excluded from main word count)

- Project title.
- Course and semester.
- Group ID.
- Names and QUIDs.
- Contribution percentages totaling 100%.
- Main-report word count excluding Appendix.
- Submission date.

### 1. Introduction and motivation (250-350 words)

- Web-application risk in general terms.
- Why layered assessment matters.
- Project problem statement.
- Ethical and controlled-lab context.
- References.

### 2. Objectives and research question (150-250 words)

- Main objective.
- Measurable sub-objectives.
- Research question.
- Success criteria.

### 3. Application, use cases, and threat model (400-500 words)

- Target application and why it was chosen.
- Intended user roles and synthetic assets.
- Architecture and trust boundaries.
- Selected use cases and scenarios.
- Scope and authorization.

### 4. Environment, tools, and methodology (500-650 words)

- OS, VM/container, target version, and tools.
- Isolation controls.
- Reconnaissance workflow.
- Automated scanning workflow.
- Manual verification workflow.
- CVSS-informed prioritization.
- Evidence and safety controls.

### 5. Implementation and proof-of-concept results (850-1,000 words)

- Setup summary.
- Findings table.
- Three or more verified findings.
- Evidence references.
- Tool rationale.
- At least one remediation and retest.

Do not paste every console line into the main report. Put long output in the Appendix.

### 6. Impact, learning outcomes, novelty, and limitations (450-550 words)

- Impact on computer security practice.
- Potential benefit to developers, testers, and users.
- Possible harmful use and safeguards.
- What the public can learn.
- Novelty: the integrated, evidence-based, retested workflow.
- Limitations of the target, tools, sample size, and lab.

### 7. Conclusion (150-200 words)

- Answer the research question.
- Summarize the strongest evidence.
- State what the team would do next in a real authorized engagement.

### References

- Numbered list.
- Every external claim has a matching in-text reference such as `[1]`.
- Use official sources where possible.

### Recommended reference categories

- OWASP Web Security Testing Guide.
- OWASP Top 10.
- OWASP Juice Shop documentation.
- Nmap official reference guide.
- OWASP ZAP documentation.
- Nikto documentation if used.
- FIRST CVSS specification/calculator.
- Docker or VM documentation.
- Relevant peer-reviewed or textbook sources.

Do not fabricate references. Record access dates for web resources if required by the chosen citation style.

---

## 10. Appendix blueprint

### Appendix A: Individual reflections

Each member writes a distinct section containing:

- Name and QUID.
- Assigned role.
- Specific tasks completed.
- Evidence or files produced.
- Problems encountered.
- How the problems were solved.
- Technical and professional learning.
- What the member would improve.
- Honest contribution percentage.

Do not use identical paragraphs for every person.

### Appendix B: User manual

Include:

1. Prerequisites.
2. Installation steps.
3. Lab isolation and authorization warning.
4. Start commands.
5. Health checks.
6. Browser URL.
7. Test-account setup.
8. Nmap procedure.
9. ZAP procedure.
10. Manual test procedure for each selected use case.
11. Evidence capture procedure.
12. Reset/stop commands.
13. Troubleshooting.
14. Cleanup instructions.

Example cleanup commands:

```powershell
docker stop juice-shop
docker rm juice-shop
```

Only run cleanup against the named project container. Do not use broad deletion commands against unrelated Docker resources.

### Appendix C: Source code and configuration

Include or link to:

- Compose file or exact container command.
- Any scripts written by the team.
- Configuration files.
- Remediation code if created.
- A short license/attribution note for every external code fragment.

### Appendix D: Complete commands and outputs

Include sanitized commands and selected outputs. Explain what each command does and why it is safe in this lab.

### Appendix E: Evidence index

| Evidence ID | Filename | Finding/use case | What it proves | Sanitized? |
|---|---|---|---|---|
| EV-001 | ... | Baseline | Target was local and available | Yes |
| EV-002 | ... | WA-001 | Original behavior | Yes |
| EV-003 | ... | WA-001 retest | Behavior after remediation | Yes |

### Appendix F: Similarity and attribution log

Track:

- Source URL/title.
- Date accessed.
- What was learned or reused.
- Where it is cited.
- Whether any code or image was reused.
- What was rewritten in the team's own words.

---

## 11. Video plan: less than 12 minutes

The opening frame must show the group ID, every member's name, and every QUID. Keep the text readable for several seconds.

Recommended timeline:

| Time | Content |
|---|---|
| 0:00-0:20 | Opening frame and scope/authorization statement |
| 0:20-1:00 | Problem, objective, and research question |
| 1:00-1:45 | Lab architecture and safety isolation |
| 1:45-2:30 | Tool selection and why each tool is used |
| 2:30-3:15 | Application startup and baseline health check |
| 3:15-4:15 | Nmap attack-surface discovery |
| 4:15-6:45 | ZAP workflow and first selected finding |
| 6:45-8:30 | Manual verification of additional findings |
| 8:30-9:40 | Risk prioritization and evidence |
| 9:40-10:45 | Remediation and retest |
| 10:45-11:30 | Limitations, impact, and learning |
| 11:30-11:50 | Conclusion and credits/references |

Video quality checklist:

- [ ] Duration is below 12 minutes.
- [ ] Continuous background narration is present.
- [ ] Audio is understandable.
- [ ] Text and terminal output are readable.
- [ ] Cursor movement is intentional.
- [ ] No secrets or personal data appear.
- [ ] The demonstration follows a logical sequence.
- [ ] Each tool is explained, not merely shown.
- [ ] The video uses original lab evidence.
- [ ] The final file plays from beginning to end on another computer.

If a voice must be anonymous, the course brief permits voice distortion, but narration must remain understandable.

---

## 12. Live demonstration and Q&A plan

The live session has no PowerPoint slides. Use the working lab and a concise verbal structure.

### 12-minute demonstration

1. State the problem, scope, and safety boundary.
2. Show the architecture and target startup.
3. Show one reconnaissance result.
4. Show the selected findings with direct evidence.
5. Demonstrate one manual verification.
6. Show remediation and retest.
7. State limitations and the main conclusion.

### Eight-minute Q&A preparation

Prepare short, honest answers to:

- Why was this target selected?
- Why were these tools selected?
- What did the automated scanner miss?
- How did you distinguish a false positive?
- Why is the finding rated at that severity?
- What would change in a production engagement?
- How did you prevent harm?
- What is novel or complex about the project?
- What was the hardest technical problem?
- What would you improve with more time?
- Why does the remediation reduce risk?
- What evidence proves the result?

If the live lab fails:

- Have a clean snapshot/container recreation procedure.
- Keep a short local recording of the expected flow.
- Use the saved evidence to explain the result.
- Do not improvise tests against a public target.
- Explain the failure honestly rather than hiding it.

---

## 13. Complexity and originality strategy

The topic should be complex enough for the project-complexity marks without becoming unsafe or unmanageable. The team will demonstrate complexity through depth, not through dangerous payloads.

Complexity indicators:

- Multiple complementary tools.
- Multiple user roles and trust boundaries.
- Both automated and manual assessment.
- Findings from different vulnerability categories.
- Evidence normalization and false-positive analysis.
- CVSS-informed prioritization.
- Remediation and retesting.
- Reproducible environment.
- Clear limitations and societal analysis.
- A realistic workflow from discovery to risk communication.

Originality indicators:

- Team-created architecture and threat model.
- Team-created test-case matrix.
- Original screenshots and measurements.
- A comparison of scanner output versus manual verification.
- A before/after retest.
- A transparent explanation of tool limitations.
- A small, safe script or report-normalization helper written by the team, if useful.

Do not manufacture complexity by adding unrelated tools or unsafe tests. Every tool must answer a project question.

---

## 14. Team roles and contribution tracking

For a three- or four-person group, assign roles as follows. Roles may overlap, but contributions must remain individually identifiable.

### Member 1: Project lead and methodology owner

- Scope, authorization, schedule, threat model.
- Coordinates evidence IDs and report integration.
- Checks rubric coverage.

### Member 2: Lab and tooling owner

- Builds the VM/container lab.
- Records versions and setup commands.
- Maintains reset and troubleshooting procedure.

### Member 3: Assessment and evidence owner

- Runs Nmap/ZAP/Nikto as appropriate.
- Conducts manual verification.
- Captures sanitized evidence and findings records.

### Member 4: Risk, remediation, and media owner

- CVSS-informed prioritization.
- Remediation and retest.
- Video editing, narration, and presentation rehearsal.

Every member must perform technical work and understand the whole demo. The contribution percentages must reflect actual work, not assumed equal shares.

Maintain a contribution log:

| Date | Member | Task | Evidence/file | Time/effort | Verified by |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

---

## 15. Schedule and gates

Use the following relative schedule and adjust it to the team's actual start date.

### Gate 1: Scope approved

- [ ] Topic and research question finalized.
- [ ] Lab target selected.
- [ ] Authorization and safety boundaries agreed.
- [ ] Roles assigned.

### Gate 2: Lab reproducible

- [ ] A second member can rebuild the lab from the manual.
- [ ] Target is isolated and synthetic.
- [ ] Version/tool inventory complete.

### Gate 3: Assessment complete

- [ ] Reconnaissance complete.
- [ ] Automated scan complete.
- [ ] Manual verification complete.
- [ ] False positives reviewed.
- [ ] At least three findings have evidence.

### Gate 4: Remediation demonstrated

- [ ] At least one remediation implemented or clearly demonstrated.
- [ ] Same test repeated.
- [ ] Before/after evidence captured.
- [ ] Residual risk documented.

### Gate 5: Report-ready

- [ ] Main text is at or below 3,500 words.
- [ ] All rubric requirements map to a section/evidence item.
- [ ] Appendix is complete.
- [ ] References and in-text citations match.
- [ ] Similarity/attribution review complete.

### Gate 6: Video-ready

- [ ] Under 12 minutes.
- [ ] Opening group information included.
- [ ] Narration understandable.
- [ ] No secrets or unauthorized targets shown.
- [ ] Video tested on a second device.

### Gate 7: Presentation-ready

- [ ] Live flow rehearsed within 12 minutes.
- [ ] Q&A answers prepared.
- [ ] Backup demo path available.
- [ ] All members can explain the findings.

### Final submission gate

- [ ] Report is an MS Word file, not PDF.
- [ ] Report and video are in the correct Blackboard folders.
- [ ] Only one member uploads each deliverable.
- [ ] Deadline verified: 14 November 2026, midnight.
- [ ] Other-group presentation attendance plan recorded.

---

## 16. Rubric-to-evidence traceability matrix

This matrix must be completed before submission. The evidence column must contain actual section/page/appendix references after the Word report is finalized.

| Rubric requirement | Planned report location | Required evidence/check |
|---|---|---|
| Overall structure, clarity, margins, fonts, documentation quality | Entire report | Arial or Times New Roman, 11 pt, one column, 1.0 spacing, proofreading |
| Requirement 1: introduction | Section 1 | Problem context and cited sources |
| Requirement 1: objectives | Section 2 | Measurable objectives and research question |
| Requirement 1: applications/use cases/scenarios | Section 3 | Use-case table and threat model |
| Requirement 1: references | References and in-text citations | Every external claim traceable |
| Requirement 2: implementation/PoC | Section 5 and Appendix D | Working lab, screenshots, sanitized outputs |
| Requirement 2: environment | Section 4 and Appendix B | OS, versions, commands, isolation |
| Requirement 2: tools/technology | Section 4 | Tool-selection rationale and limitations |
| Requirement 2: learning outcomes | Section 6 and reflections | Specific technical learning |
| Requirement 2: novelty/quality | Sections 5-6 | Layered workflow and retest |
| Requirement 3: usefulness | Section 6 | Developer/tester/user value |
| Requirement 3: harmful potential | Section 6 | Misuse discussion and safety controls |
| Requirement 3: public/societal impact | Section 6 | Balanced impact analysis |
| Requirement 3: learning for others | Section 6 and manual | Reproducible educational workflow |
| Requirement 3: limitations | Section 6 | Target/tool/sample/validity limitations |
| Requirement 4: individual reflection | Appendix A | Distinct member reflections |
| Requirement 5: user manual | Appendix B | Rebuild/start/test/reset instructions |
| Requirement 5: code/commands | Appendix C-D | Source, attribution, exact safe commands |
| Video quality | Video | Readable, narrated, logical, under 12 minutes |
| Live demonstration | Demo | No slides; working PoC; Q&A readiness |
| Project complexity | Entire package | Multiple tools, roles, findings, retest, originality |
| Cover page requirements | Cover page | Group ID, names, QUIDs, word count, percentages |
| Video opening requirements | Opening frame | Group ID, names, QUIDs |
| Academic integrity | Entire package | Original work, citations, similarity review |

---

## 17. Final pre-submission checklists

### Technical correctness

- [ ] Every reported finding was observed in the team's lab.
- [ ] Every finding has a stable ID.
- [ ] Every claim has evidence.
- [ ] Scanner alerts were manually reviewed.
- [ ] False positives are marked.
- [ ] Severity rationale is honest and cited.
- [ ] At least one finding has a before/after retest.
- [ ] No test affected an unauthorized system.
- [ ] No secrets appear in evidence.
- [ ] The lab can be reset.

### Report correctness

- [ ] The main text is <= 3,500 words excluding Appendix.
- [ ] The cover page contains every required field.
- [ ] Contribution percentages total 100%.
- [ ] The report is an MS Word file.
- [ ] Formatting follows the brief.
- [ ] Sections match the rubric.
- [ ] Tables and diagrams are labeled.
- [ ] References are numbered and cited in the body.
- [ ] Appendix contains reflections, manual, code, commands, and evidence index.
- [ ] Grammar, spelling, captions, and page numbers are checked.

### Video and presentation correctness

- [ ] Video is under 12 minutes.
- [ ] Video includes continuous narration.
- [ ] Opening frame includes group details.
- [ ] Recording is readable and audible.
- [ ] Video demonstrates the PoC, not only slides.
- [ ] Live demonstration uses no PowerPoint slides.
- [ ] The demo fits 12 minutes.
- [ ] All members can answer technical and ethical questions.
- [ ] Backup plan is ready.

### Ethical and academic correctness

- [ ] Written scope/authorization record is included.
- [ ] Only synthetic data and accounts were used.
- [ ] No public target was scanned.
- [ ] No destructive activity occurred.
- [ ] External sources and code are attributed.
- [ ] Similarity was reviewed and remains below the course threshold.
- [ ] The team can explain what it did without overstating results.

---

## 18. Definition of done

The project is complete only when all of the following are true:

1. The local lab can be rebuilt by a team member who did not originally create it.
2. The target is isolated, synthetic, and explicitly authorized.
3. The assessment uses at least two complementary tools and manual verification.
4. At least three findings are verified and documented with reproducible evidence.
5. Each finding includes impact, severity rationale, remediation, and limitations.
6. At least one finding is retested after a mitigation.
7. The report satisfies every row of the traceability matrix.
8. The Appendix is complete and contains a useful user manual.
9. The video is narrated, readable, under 12 minutes, and includes the required opening information.
10. The live demonstration works without PowerPoint slides and fits the time limit.
11. The work is original, cited, safe, and does not test unauthorized systems.
12. The final report and video are submitted correctly before the course deadline.

---

## 19. Instructions to any AI assistant helping with this project

An AI assistant may help the team organize, explain, proofread, or implement safe project artifacts, but it must follow these constraints:

- Treat this document and the course handout as the source of truth.
- Ask for clarification when a choice would change the scope, target, or safety posture.
- Prefer the local intentionally vulnerable lab.
- Never recommend scanning a real target without written authorization.
- Never use real credentials, personal data, or secrets.
- Never create destructive payloads, persistence, malware, denial-of-service actions, or credential theft workflows.
- Do not invent scan results, CVEs, references, screenshots, or remediation outcomes.
- Clearly label assumptions and unverified examples.
- Keep commands scoped to the named local lab.
- Preserve the report's 3,500-word main-text limit.
- Use original writing and cite external sources.
- Keep a clear distinction between:
  - a tool alert,
  - a manually verified vulnerability,
  - a risk hypothesis,
  - a confirmed remediation result.
- When editing project files, avoid unrelated changes and preserve existing team work.
- Validate setup commands and outputs before describing them as successful.
- Redact secrets from all generated evidence.
- If an action could affect a system outside the lab, stop and request authorization or choose a safer alternative.

---

## 20. Immediate next actions

1. Replace the cover-page placeholders with the actual Group ID, names, QUIDs, and contribution plan.
2. Confirm whether the instructor accepts OWASP Juice Shop as the selected target.
3. Select three to five use cases from Section 6.
4. Assign roles and create the contribution log.
5. Build the isolated lab and record exact versions.
6. Create the evidence folder structure.
7. Run the baseline health and scope checks.
8. Complete reconnaissance before active testing.
9. Log every finding using the test-record fields.
10. Complete one remediation/retest cycle.
11. Write the report from evidence, not from assumptions.
12. Rehearse the narrated video and live demonstration against the rubric matrix.

