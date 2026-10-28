# Custom Script — Evidence Toolkit

`evidence_toolkit.py` is the team's small, safe creativity feature. It uses the
**Python standard library only** (no installs) and was tested on Python 3.14.0.
It has two jobs:

| Command | What it does |
|---|---|
| `scan-summary` | Reads an OWASP ZAP JSON report and prints a de-duplicated, risk-sorted summary (and optional CSV) so the team can triage raw alerts into candidate findings. Optionally lists Nikto findings alongside. |
| `evidence-index` | Walks the `evidence/` folder, indexes files by the `WA-###` / `EV-###` naming convention, flags files that don't match, and (with `--check-secrets`) scans text evidence for leftover secrets to sanitize. |

## Safety

- Read-only against its inputs. It never deletes or edits evidence.
- Only writes a summary/index file when you pass `--csv`, to a path you choose.
- Makes no network connections. Operates only on local project files.

## Usage

Run from the project root. On Windows use the `py` launcher (plain `python`
may not be on the PATH in some shells):

```powershell
# Summarize a ZAP report + write CSV next to it
py source\custom-script\evidence_toolkit.py scan-summary --zap evidence\automated-scans\zap-report.json --csv

# Include a Nikto report for comparison
py source\custom-script\evidence_toolkit.py scan-summary --zap evidence\automated-scans\zap-report.json --nikto evidence\automated-scans\nikto-report.txt

# Index evidence and flag possible unsanitized secrets
py source\custom-script\evidence_toolkit.py evidence-index --dir evidence --check-secrets --csv

# Per-command help
py source\custom-script\evidence_toolkit.py scan-summary -h
```

## How to get the ZAP JSON report

In OWASP ZAP: **Report ▸ Generate Report ▸ Traditional JSON** (or the automation
framework's JSON output). Save it under `evidence/automated-scans/`.

## Testing it

`samples/zap-sample.json` is a **synthetic, clearly-labelled** fixture (not real
scan data) so the script can be demonstrated before a real scan exists:

```powershell
py source\custom-script\evidence_toolkit.py scan-summary --zap source\custom-script\samples\zap-sample.json
```

Expected: 4 distinct alerts (1 High, 1 Medium, 1 Low, 1 Informational), sorted
with High first. This run is what to screenshot for Appendix D.

## Notes for the report (Appendix D)

- Document that the script is original team work, stdlib-only, and read-only.
- The `scan-summary` reminder line ("each alert is a candidate finding, not a
  confirmed vulnerability") reflects the project's rule that scanner output is a
  hypothesis until manually verified.
- `--check-secrets` uses conservative pattern matching (Authorization headers,
  bearer/JWT tokens, Set-Cookie, password fields). It flags candidates for human
  review; it is an aid to sanitization, not a guarantee.
