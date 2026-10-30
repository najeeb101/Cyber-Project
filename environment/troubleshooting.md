# Troubleshooting

| Problem | Cause | Solution | Verified by/date |
|---|---|---|---|
| Nmap reports port 3000 as `ppp?` instead of HTTP | Nmap's service fingerprint database has no match for Juice Shop's response pattern | Read the captured fingerprint in the output: it is `HTTP/1.1 200 OK` with Juice Shop HTML. Treat it as a fingerprint miss, not a different service | EV-001, 2026-10-28 |
| `py` / `python` "not recognized" in some terminals | Python 3.14 is installed under `%LOCALAPPDATA%\Programs\Python\Python314\` but is not on that shell's PATH | Use the full path: `& "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe" source\custom-script\evidence_toolkit.py ...`, or add the folder to PATH | 2026-10-30 |
| ZAP does not start from the command line | ZAP 2.17.0 needs a Java runtime | Install Temurin 17 JRE (installed with ZAP via winget) | 2026-10-28 |
| ZAP report shows an "Insights" memory warning (87% used) | ZAP's default JVM heap is `-Xmx512m` | Harmless for a single quick scan; for longer scans raise the heap in ZAP's JVM options | EV-002 / `zap-console.log`, 2026-10-28 |
| ZAP quick scan misses SPA routes (e.g. `/ftp`, basket API) | Juice Shop is an Angular single-page app; the traditional spider does not execute JavaScript (ZAP flags "Modern Web Application") | Use the AJAX spider and an authenticated context, and always complement with manual testing | 2026-10-28 |
| nginx CSP proxy on `:8080` returns 502 | The proxy forwards to `host.docker.internal:3000`; Juice Shop not running, or the host name does not resolve (Linux) | Check `docker ps` for `juice-shop`; on Linux add `--add-host=host.docker.internal:host-gateway` | `csp-proxy.conf`, 2026-10-30 |
| Registering a test account fails on re-run | The email is already registered in the running container | Use a new email, or `docker restart juice-shop` (Juice Shop resets its database on restart) | 2026-10-28 |
| `evidence-index --check-secrets` flags `WA-004-idor-basket.txt` | The file contains the text `Authorization: Bearer <B's JWT>` | False positive: the token is a redacted placeholder. No real JWT is stored | 2026-10-30 |
