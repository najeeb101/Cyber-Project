# WA-001 Remediation - Reverse Proxy with CSP (step by step)

Safe, reversible, loopback-only. Adds a `Content-Security-Policy` header to every response
by running an nginx reverse proxy in front of Juice Shop. Juice Shop itself is unchanged.

## Why a reverse proxy

The Juice Shop container is a prebuilt image; editing its source for a class demo is
fragile. In real deployments, security headers are added at the web tier (reverse proxy,
WAF, or app middleware). The proxy approach is realistic, non-destructive, and easy to
show as a clean before/after.

## Topology

```
Browser / curl
   |
   |  127.0.0.1:3000  (BEFORE - direct, no CSP)
   |  127.0.0.1:8080  (AFTER  - via proxy, CSP injected)
   v
[ nginx proxy :8080 ] --> [ juice-shop :3000 ]
```

Both ports stay on `127.0.0.1`. Nothing is exposed to the network.

## Prerequisites

Juice Shop already running and bound to loopback:

```powershell
docker ps --filter "name=juice-shop"
docker port juice-shop        # expect 3000/tcp -> 127.0.0.1:3000
```

## Step 1 - nginx config

`csp-proxy.conf` is in this folder. It proxies to the host's port 3000 and adds the CSP
header. (On Docker Desktop for Windows, `host.docker.internal` resolves to the host.)

## Step 2 - capture BEFORE

```powershell
curl.exe -s -D - -o NUL http://127.0.0.1:3000/ | Out-File -Encoding utf8 WA-001-before.txt
# Also take a browser screenshot of DevTools > Network > document > Response Headers -> WA-001-before.png
```

## Step 3 - start the proxy

```powershell
docker run --name csp-proxy -d `
  -p 127.0.0.1:8080:80 `
  -v "${PWD}/csp-proxy.conf:/etc/nginx/conf.d/default.conf:ro" `
  nginx:1.27-alpine

docker ps --filter "name=csp-proxy"
```

## Step 4 - capture AFTER

```powershell
curl.exe -s -D - -o NUL http://127.0.0.1:8080/ | Out-File -Encoding utf8 WA-001-after.txt
curl.exe -s -D - -o NUL http://127.0.0.1:8080/ | Select-String "Content-Security-Policy"
# Browser: load http://127.0.0.1:8080/ , confirm the app loads, screenshot headers -> WA-001-after.png
```

Expected AFTER header:

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'self'; object-src 'none'
```

## Step 5 - record result

Fill the retest table in `retest-record.md`.

## Cleanup (reset lab)

```powershell
docker stop csp-proxy
docker rm csp-proxy
```

Removing the proxy returns the lab to its original state. Juice Shop was never modified.

## Limitation to note in the report

CSP is enforced only for traffic through the proxy (`:8080`). The direct port (`:3000`)
still lacks it. In production the app would not be reachable except through the proxy;
in the lab both ports remain open for clear before/after comparison. State this explicitly
so the fix is not overclaimed.
