# Scope and Authorization

## Authorized target

- **Application:** OWASP Juice Shop
- **Host/URL:** `http://127.0.0.1:3000`
- **Testing period:** 28 October 2026 - 10 November 2026
- **Environment:** Docker Desktop running locally on the project computer
- **Data:** Synthetic accounts and test data only
- **Authorized testers:** The four project members listed below

If the team uses a virtual machine instead of Docker Desktop, update the host/URL and environment with the actual private lab address before testing. Do not use an address that is not confirmed to belong to the isolated lab.

## Project purpose

The purpose of this assessment is to evaluate an intentionally vulnerable training web application using safe penetration-testing and vulnerability-analysis techniques for the CMPS 380 Cybersecurity Fundamentals project.

## In-scope activities

The team may perform the following activities against the authorized local target only:

- Confirm that the local application is running.
- Perform local service and version discovery.
- Browse the application normally.
- Run controlled OWASP ZAP scans.
- Use Burp Suite Community or browser developer tools for manual verification.
- Use Nmap against the local lab address.
- Test selected vulnerabilities using non-destructive proof-of-concept steps.
- Capture sanitized screenshots, logs, requests, and responses.
- Recommend remediation.
- Retest selected findings after remediation.

## Out-of-scope activities

The team must not:

- Scan or test public websites.
- Scan or test university systems, campus networks, or cloud services.
- Test any system that the team does not own or have written permission to test.
- Use real credentials, personal data, or real payment information.
- Perform denial-of-service, stress, flooding, or destructive testing.
- Perform credential theft, password spraying, phishing, or social engineering.
- Create malware, persistence, ransomware, or backdoors.
- Exfiltrate, publish, or retain sensitive data.
- Attempt to escape the Docker container or virtual machine.
- Continue testing if traffic could reach a system outside the authorized lab.

## Isolation and safety controls

- The application will be bound to localhost or an isolated host-only network.
- The application will not be exposed to the public internet.
- Only synthetic users and test data will be used.
- The team will keep a clean container or VM snapshot for recovery.
- Cookies, passwords, tokens, and other secrets will be removed from screenshots and logs.
- Testing will stop immediately if the application becomes unstable or unintended traffic is observed.

## Team authorization statement

The team authorizes testing only against the locally controlled OWASP Juice Shop instance and the isolated lab network created for this project. Testing is non-destructive, uses synthetic accounts and data, and will stop if activity could affect systems outside the lab.

## Team approval

| Member | Name | QUID | Approval/date |
|---|---|---|---|
| Member 1 | Najeeb Abdi | 202307172 | Approved 2026-10-28 |
| Member 2 | Mohanad Elhabash | 202314448 | Approved 2026-10-28 |
| Member 3 | Moaaz Mohamed | 202207862 | Approved 2026-10-28 |
| Member 4 | Ahmed Hari | 202203669 | Approved 2026-10-28 |

**Date approved:** 2026-10-28 (recorded in the decision log, `TEAM_TASKS.md` §11: target and scope agreed by all four members)

## Change-control rule

Any change to the target, network, testing period, tools, or testing activities must be discussed and approved by all members before testing continues. If the change significantly affects the project scope, ask the instructor for approval.
