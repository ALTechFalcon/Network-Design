# Segments

Four segments joined by one firewall VM. Subnets do not overlap (checked with `subnetcheck.py`).

| Segment | Subnet | Machines | Trust | Purpose |
| --- | --- | --- | --- | --- |
| Users | 10.10.10.0/24 | analyst-ws | Medium | Where the analyst works and starts tests |
| Servers | 10.10.20.0/24 | log-collector, file-server | High value, tightly limited | Receives logs, stores evidence |
| Lab | 10.10.30.0/24 | linux-target (linux-baseline), web-target (web-vuln-lab) | Untrusted by design | Machines we test and may weaken on purpose |
| Mgmt | 10.10.40.0/24 | mgmt-host, firewall admin port | Highest | Only mgmt-host may administer the firewall |

Policy: default deny. Everything not listed in `firewall-rules.csv` is blocked and logged.
No route from Lab to the Internet exists at all (the virtual network has no NAT).
