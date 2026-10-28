# Final Report Outline

The final submission must be an MS Word document. Keep the main report body at
or below **3,500 words**, excluding the Appendix. Word budgets below are a guide
(they sum to roughly 3,000–3,350, leaving headroom). Recommended formatting:
Times New Roman or Arial, 11 pt, single column, 1.0 spacing.

## Main report (counts toward the 3,500-word limit)

1. **Cover page** *(excluded from word count)* — title; course/semester;
   Group ID (G02); all member names + QUIDs; contribution % totaling 100%;
   main-report word count; submission date.
2. **Introduction and motivation** *(≈250–350 words)* — web-application risk,
   why layered assessment matters, the problem statement, the controlled-lab
   ethical context. Cite sources.
3. **Objectives and research question** *(≈150–250 words)* — main objective,
   measurable sub-objectives, the research question, success criteria.
4. **Application, use cases, and threat model** *(≈400–500 words)* — why Juice
   Shop; synthetic roles/assets; architecture and trust boundaries; the selected
   scenarios (S1–S4/S5); scope and authorization summary.
5. **Methodology** *(part of the ≈500–650 environment+method budget)* — recon →
   automated scan → manual verification → CVSS-informed prioritization →
   remediation/retest; evidence and safety controls.
6. **Lab environment and tools** *(remainder of the ≈500–650 budget)* — OS,
   Docker/Compose, target version, tools + why each was chosen and its limits;
   isolation controls.
7. **Verified findings and proof of concepts** *(≈850–1,000 words)* — findings
   table, then 3+ verified findings (WA-001…) with sanitized evidence
   references. Keep long console output in the Appendix.
8. **Risk analysis and CVSS reasoning** *(fold into findings budget)* — per
   finding: affected asset, exploitability in the lab, CVSS rationale, technical
   severity vs business risk.
9. **Remediation and retesting** *(≈200 words + evidence)* — the fix applied,
   before/after result, residual risk.
10. **Impact, learning outcomes, and limitations** *(≈450–550 words)* — impact
    on security practice, benefit to developers/testers/users, possible misuse +
    safeguards, what others can learn, novelty, and honest limitations.
11. **Conclusion** *(≈150–200 words)* — answer the research question; strongest
    evidence; what the team would do next in a real authorized engagement.
12. **References** — numbered list matching in-text `[n]` citations.

## Appendix (no word limit)

13. **Appendix A: Individual reflections** — one distinct section per member
    (name, QUID, role, tasks, problems, how solved, learning, honest %).
14. **Appendix B: User manual** — prerequisites, install, isolation/authorization
    warning, start, health check, test-account setup, Nmap, ZAP, per-use-case
    manual steps, evidence capture, reset/stop, troubleshooting, cleanup.
15. **Appendix C: Commands and environment setup** — sanitized commands and
    selected outputs (pull from [../environment/](../environment/)).
16. **Appendix D: Source code and attribution** — the custom script
    (`../source/custom-script/`), compose/run command, and attribution for any
    external code.
17. **Appendix E: Screenshots, logs, and evidence index** — the completed
    [evidence index](../evidence/findings-index.md).
18. **Appendix F: Similarity and attribution log** — source, date accessed, what
    was reused, where cited, what was rewritten.

> Traceability: every row of the rubric matrix in [kickoff.md](../kickoff.md)
> §16 must map to a section above before submission.
