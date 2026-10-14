# Secure Network Design

Design verified by rule simulation. Live firewall tests are yours to run (see `build-guide.md`).

## What is in this folder
| File | Purpose |
| --- | --- |
| segments.md | Four segments, subnets, trust levels |
| firewall-rules.csv | The 7 rules, default deny, a reason on each |
| rulecheck.py | Simulates the rules (first match wins) against `tests/expected.csv` |
| subnetcheck.py | Confirms subnets are private and do not overlap |
| tests/expected.csv | 16 expected allow/deny cases, one per rule plus negatives |
| tests/test_design.py | 7 automated tests, including one that proves the checker catches a bad rule |
| tests/results-*.txt | Saved run of the simulation |
| threat-note.md | One page: entry path and stopping rule per segment, residual risks |
| build-guide.md | How to build it in VirtualBox/VMware and record live test results |
| diagram/network.svg | The network diagram (open in a browser or import into draw.io) |

## Run it
```
python3 subnetcheck.py
python3 rulecheck.py
python3 -m pytest -q tests
```

## Safety
Internal virtual networks only. No NAT or bridged adapter on any lab VM. Nothing here touches a real network.

## Limits
One firewall, no redundancy. Simulation shows the rules are consistent, not that your firewall enforces them.

## Related
`linux-baseline` and `web-vuln-lab` run on the Lab segment machines defined here.
