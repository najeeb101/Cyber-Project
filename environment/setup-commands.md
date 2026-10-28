# Setup Commands

All commands are scoped to the authorized local lab only. Run them in
PowerShell on the project computer. After running each block, save the real
output as evidence (for example `evidence/environment/baseline-health.txt`).
Do **not** change the `127.0.0.1` binding — it is what keeps the target off the
network.

## Setup

```powershell
# Confirm the container tooling is available
docker --version
docker compose version

# Pull the intentionally vulnerable target.
# Pin a specific tag when possible instead of :latest, then record the tag
# and digest in environment-inventory.md.
docker pull bkimminich/juice-shop

# Run the target bound to loopback only (not 0.0.0.0)
docker run --name juice-shop -d -p 127.0.0.1:3000:3000 bkimminich/juice-shop

# Confirm the container is running and inspect startup logs
docker ps
docker logs --tail 50 juice-shop
```

## Health check

```powershell
# The app should return HTTP 200 on loopback
curl.exe -I http://127.0.0.1:3000
```

Then open `http://127.0.0.1:3000` in the browser and confirm the Juice Shop
home page loads. Record the browser + version in the inventory.

## Isolation check

```powershell
# Must show: 3000/tcp -> 127.0.0.1:3000  (NOT 0.0.0.0)
docker port juice-shop

# From another device on the LAN (or using this host's LAN IP), a request to
# http://<LAN-IP>:3000 should FAIL. Record that it failed as proof of isolation.
```

## Reset (return to a clean state between tests)

```powershell
# Fast reset: restart the same container
docker restart juice-shop

# Full reset: remove and recreate for a guaranteed clean state
docker stop juice-shop
docker rm juice-shop
docker run --name juice-shop -d -p 127.0.0.1:3000:3000 bkimminich/juice-shop
```

## Cleanup (end of project)

```powershell
# Only act on the named project container
docker stop juice-shop
docker rm juice-shop

# Optional: remove the image as well
# docker rmi bkimminich/juice-shop
```

> Do not use broad deletion commands such as `docker system prune -a` or
> `docker rm $(docker ps -aq)` — they would affect unrelated Docker resources.
