#!/usr/bin/env python3
"""Evidence toolkit for the CMPS 380 web-application assessment project.

A small, dependency-free helper (Python standard library only) with two jobs:

  scan-summary   Normalize an OWASP ZAP JSON report into a de-duplicated,
                 risk-sorted summary (console table + optional CSV). Helps the
                 team triage raw scanner alerts into candidate findings, and
                 see at a glance how many instances each alert has. Optionally
                 lists Nikto findings alongside for comparison.

  evidence-index Build an index of the files under evidence/ by parsing the
                 project's WA-### / EV-### naming convention, flag files that do
                 not match it, and (optionally) scan text evidence for leftover
                 secrets so they can be sanitized before submission.

Safety: the tool is read-only against its inputs. It never deletes or modifies
evidence; it only reads files and, when asked, writes a summary/index file to a
path you specify. It makes no network connections.

Usage examples (run from the project root):

  python source/custom-script/evidence_toolkit.py scan-summary \\
      --zap evidence/automated-scans/zap-report.json --csv

  python source/custom-script/evidence_toolkit.py scan-summary \\
      --zap source/custom-script/samples/zap-sample.json

  python source/custom-script/evidence_toolkit.py evidence-index \\
      --dir evidence --check-secrets

Run `python evidence_toolkit.py <command> -h` for per-command options.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ZAP encodes risk as a numeric code; map it to a readable label and a sort key.
RISK_LABELS = {"0": "Informational", "1": "Low", "2": "Medium", "3": "High"}
CONFIDENCE_LABELS = {
    "0": "False Positive",
    "1": "Low",
    "2": "Medium",
    "3": "High",
    "4": "Confirmed",
}

# Filenames should start with a finding id (WA-001) or evidence id (EV-001).
ID_PATTERN = re.compile(r"^(?P<id>(?:WA|EV)-\d{3,})\b[-_]?(?P<rest>.*)$", re.IGNORECASE)

# Conservative patterns for things that must be redacted from evidence. These
# only flag candidates for human review; they are not a guarantee of safety.
SECRET_PATTERNS = {
    "authorization-header": re.compile(r"authorization\s*:\s*\S+", re.IGNORECASE),
    "bearer-token": re.compile(r"bearer\s+[A-Za-z0-9._\-]+", re.IGNORECASE),
    "set-cookie": re.compile(r"set-cookie\s*:", re.IGNORECASE),
    "password-field": re.compile(r"password\s*[=:]\s*\S+", re.IGNORECASE),
    "jwt-like": re.compile(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+"),
}

TEXT_EXTENSIONS = {".txt", ".log", ".md", ".csv", ".json", ".html", ".htm", ".xml"}


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


# --------------------------------------------------------------------------- #
# scan-summary
# --------------------------------------------------------------------------- #
def load_zap_alerts(zap_path: Path) -> list[dict]:
    """Return a normalized list of alert rows from a ZAP JSON report."""
    try:
        data = json.loads(zap_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: ZAP report not found: {zap_path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"error: {zap_path} is not valid JSON ({exc})")

    rows: list[dict] = []
    for site in data.get("site", []):
        site_name = site.get("@name", "")
        for alert in site.get("alerts", []):
            riskcode = str(alert.get("riskcode", "0"))
            instances = alert.get("instances", []) or []
            # ZAP provides a "count" field; fall back to the instance list.
            try:
                count = int(alert.get("count", len(instances)))
            except (TypeError, ValueError):
                count = len(instances)
            example_uri = instances[0].get("uri", "") if instances else ""
            rows.append(
                {
                    "risk": RISK_LABELS.get(riskcode, riskcode),
                    "risk_sort": int(riskcode) if riskcode.isdigit() else -1,
                    "alert": alert.get("alert") or alert.get("name", ""),
                    "pluginid": alert.get("pluginid", ""),
                    "cweid": alert.get("cweid", ""),
                    "confidence": CONFIDENCE_LABELS.get(
                        str(alert.get("confidence", "")), alert.get("confidence", "")
                    ),
                    "instances": count,
                    "site": site_name,
                    "example_uri": example_uri,
                }
            )
    # Highest risk first, then most instances.
    rows.sort(key=lambda r: (r["risk_sort"], r["instances"]), reverse=True)
    return rows


def load_nikto_findings(nikto_path: Path) -> list[str]:
    """Return Nikto '+' finding lines from a plain-text Nikto report."""
    try:
        text = nikto_path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        sys.exit(f"error: Nikto report not found: {nikto_path}")
    return [line.strip() for line in text.splitlines() if line.strip().startswith("+")]


def print_markdown_table(rows: list[dict]) -> None:
    headers = ["Risk", "Alert", "Instances", "Confidence", "Plugin", "CWE", "Example URI"]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        print(
            f"| {r['risk']} | {r['alert']} | {r['instances']} | {r['confidence']} "
            f"| {r['pluginid']} | {r['cweid']} | {r['example_uri']} |"
        )


def cmd_scan_summary(args: argparse.Namespace) -> int:
    rows = load_zap_alerts(Path(args.zap))

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["risk"]] = counts.get(r["risk"], 0) + 1

    print(f"# ZAP scan summary  (generated {_now()})")
    print(f"Source report: {args.zap}")
    print(f"Distinct alerts: {len(rows)}")
    order = ["High", "Medium", "Low", "Informational"]
    print("By risk: " + ", ".join(f"{k}={counts.get(k, 0)}" for k in order))
    print()
    print_markdown_table(rows)

    if args.nikto:
        nikto = load_nikto_findings(Path(args.nikto))
        print(f"\n## Nikto findings ({len(nikto)}) — review for overlap with the above")
        for line in nikto:
            print(f"- {line}")

    if args.csv:
        out = Path(args.out) if args.out else Path(args.zap).with_suffix(".summary.csv")
        with out.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=[
                    "risk", "alert", "instances", "confidence",
                    "pluginid", "cweid", "site", "example_uri",
                ],
            )
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r[k] for k in writer.fieldnames})
        print(f"\nCSV written: {out}")

    # A nudge, not a verdict: scanner alerts are hypotheses until verified.
    print("\nReminder: each alert is a candidate finding, not a confirmed "
          "vulnerability. Manually verify before reporting it.")
    return 0


# --------------------------------------------------------------------------- #
# evidence-index
# --------------------------------------------------------------------------- #
def scan_secrets(path: Path) -> list[str]:
    """Return names of secret patterns found in a text file (read-only)."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    hits = []
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            hits.append(name)
    return hits


def cmd_evidence_index(args: argparse.Namespace) -> int:
    root = Path(args.dir)
    if not root.is_dir():
        sys.exit(f"error: evidence directory not found: {root}")

    rows: list[dict] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        match = ID_PATTERN.match(path.name)
        row = {
            "id": match.group("id").upper() if match else "",
            "filename": path.name,
            "path": str(path.relative_to(root.parent)),
            "category": path.parent.name,
            "size_bytes": path.stat().st_size,
            "matches_convention": "Y" if match else "N",
            "possible_secrets": "",
        }
        if args.check_secrets and path.suffix.lower() in TEXT_EXTENSIONS:
            hits = scan_secrets(path)
            if hits:
                row["possible_secrets"] = ";".join(hits)
        rows.append(row)

    print(f"# Evidence index  (generated {_now()})")
    print(f"Scanned: {root}  —  {len(rows)} file(s)")
    nonconforming = [r for r in rows if r["matches_convention"] == "N"]
    flagged = [r for r in rows if r["possible_secrets"]]
    print(f"Not matching WA-/EV- naming: {len(nonconforming)}")
    if args.check_secrets:
        print(f"Files with possible unsanitized secrets: {len(flagged)}")
    print()

    headers = ["ID", "Filename", "Category", "Bytes", "Convention", "Possible secrets"]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        print(
            f"| {r['id']} | {r['filename']} | {r['category']} | {r['size_bytes']} "
            f"| {r['matches_convention']} | {r['possible_secrets']} |"
        )

    if flagged:
        print("\n## Review before submission — possible unsanitized secrets")
        for r in flagged:
            print(f"- {r['path']}: {r['possible_secrets']}")

    if args.csv:
        out = Path(args.out) if args.out else root / "evidence-index.csv"
        with out.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=[
                    "id", "filename", "path", "category",
                    "size_bytes", "matches_convention", "possible_secrets",
                ],
            )
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nCSV written: {out}")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evidence toolkit: summarize ZAP scans and index evidence.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan-summary", help="normalize a ZAP JSON report")
    p_scan.add_argument("--zap", required=True, help="path to a ZAP JSON report")
    p_scan.add_argument("--nikto", help="optional path to a Nikto text report")
    p_scan.add_argument("--csv", action="store_true", help="also write a CSV summary")
    p_scan.add_argument("--out", help="CSV output path (default: next to the report)")
    p_scan.set_defaults(func=cmd_scan_summary)

    p_idx = sub.add_parser("evidence-index", help="index files under evidence/")
    p_idx.add_argument("--dir", default="evidence", help="evidence directory (default: evidence)")
    p_idx.add_argument("--check-secrets", action="store_true",
                       help="scan text evidence for leftover secrets")
    p_idx.add_argument("--csv", action="store_true", help="also write evidence-index.csv")
    p_idx.add_argument("--out", help="CSV output path (default: <dir>/evidence-index.csv)")
    p_idx.set_defaults(func=cmd_evidence_index)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
