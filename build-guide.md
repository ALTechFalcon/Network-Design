# Build guide: making the design real in VirtualBox (VMware is similar)

Do this on your own laptop. Names below are suggestions.

1. Create four **Internal Networks** (VirtualBox: VM > Settings > Network > "Internal Network"): `seg-users`, `seg-servers`, `seg-lab`, `seg-mgmt`. Internal networks have no route to the Internet or your home network.
2. Create the **firewall VM** (any small Linux with nftables or iptables) with four adapters, one on each internal network, addresses 10.10.10.1, 10.10.20.1, 10.10.30.1, 10.10.40.1. Enable IP forwarding. Do not give it a NAT or bridged adapter.
3. Put each machine on exactly one internal network with a static address in its subnet and the firewall as gateway:
   analyst-ws 10.10.10.10 · log-collector 10.10.20.10 · linux-target 10.10.30.10 · web-target 10.10.30.20 · mgmt-host 10.10.40.10.
4. Translate `firewall-rules.csv` into firewall rules, default policy DROP, log drops. Keep the CSV as the source of truth.
5. Prove each rule: run each line of `tests/expected.csv` for real (for example `nc -zv` from the source machine) and write the real result next to the simulated one in `tests/live-results.md` (template below).
6. Take a snapshot of every VM named `clean-baseline`.

## live-results.md template
| Test | Command run | Expected | Actual | Date |
| --- | --- | --- | --- | --- |
| Lab -> Internet tcp/443 | `curl -m 5 https://example.com` from linux-target | fail | _fill in_ | |

Note: the simulated results in `tests/results-*.txt` prove the RULES are consistent. Only your live results prove the FIREWALL enforces them.
