# Environment Inventory

Verified facts recorded on 2026-10-28 on the project computer. Fields marked
`TODO` must be filled with the real value once that tool or component is
installed/confirmed. Do not guess version numbers — record what the machine
actually reports.

| Component | Version/details |
|---|---|
| Operating system | Windows 11 Pro, Version 10.0.26300.9711 |
| Docker Engine | Docker version 29.9.1, build dfc520d |
| Docker Compose | v5.6.0 |
| Python (for custom script) | 3.14.0 |
| Git | 2.52.0.windows.1 |
| Target application | OWASP Juice Shop (`bkimminich/juice-shop`) |
| Target image tag/digest Juice Shop 20.3.0, `bkimminich/juice-shop:latest`, digest `sha256:42843723a7bf4246aa5d63c324978b17ef296ac78434aeddd34c427bfb5853f4` (pulled 2026-10-28) |
| Browser | Google Chrome 156.0.8078.48 |
| Nmap | 7.993 (Npcap 1.90), installed 2026-10-28 |
| OWASP ZAP | 2.17.0 (winget `ZAP.ZAP`, with Temurin 17 JRE), installed 2026-10-28 |
| Burp Suite Community | Not used in the recorded assessment |
| Nikto, if used | Not used in the recorded assessment |
| Network mode | localhost — container bound to `127.0.0.1` only |
| Target URL | `http://127.0.0.1:3000` |

## Isolation verification

Planned verification method (record the actual output as evidence in
`evidence/environment/isolation-check.txt`):

1. Confirm the container publishes only to loopback:
   `docker port juice-shop` should show `3000/tcp -> 127.0.0.1:3000`
   (not `0.0.0.0:3000`).
2. Confirm the app answers on loopback: `curl.exe -I http://127.0.0.1:3000`.
3. Confirm the app is **not** reachable from the machine's LAN address:
   from another device (or using the host's LAN IP) the request to
   `http://<LAN-IP>:3000` should fail/time out.

**Confirmation status (2026-10-28):** all three checks passed. See
`evidence/environment/isolation-check.txt` and `baseline-health.txt`.

1. `docker port juice-shop` -> `3000/tcp -> 127.0.0.1:3000`
2. `curl.exe -I http://127.0.0.1:3000` -> `HTTP/1.1 200 OK`
3. Request to host LAN IP `192.168.199.1:3000` -> failed (HTTP code 000).
   A check from a second physical device is still recommended.

## Notes

- Nmap must be installed before Phase 3 reconnaissance (see
  [setup-commands.md](setup-commands.md)). On Windows, install from the official
  Nmap site; record the installed version here.
- OWASP ZAP and Burp Suite are GUI tools; their versions are read from each
  application's About dialog, not the command line.
