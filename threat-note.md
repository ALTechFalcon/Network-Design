# Threat note: one page

Scope: the four-segment lab. Assets: analyst workstation, log collector (evidence), lab targets.

| Segment | One way an attacker could get in | Rule that stops or limits it |
| --- | --- | --- |
| Users | Analyst opens a malicious file from a lab target | Rule 4: Lab cannot open connections to Users; Lab can only answer on connections the analyst starts |
| Servers | A compromised lab target tries to reach the collector's admin or file services | Rule 3 lets Lab send only udp/514 to Servers; everything else falls to rule 7 |
| Lab | Analyst-side mistake exposes the vulnerable app to a real network | Rule 5 and the virtual network have no NAT, so the Lab has no path out; test #10 and #11 prove it |
| Mgmt | Someone on Users or Lab tries the firewall admin page | Rule 6 allows only MgmtHost; test #13 and #14 prove Users and Lab are denied |

## Residual risks (honest limits)
- One firewall VM, no redundancy: if it fails open, all rules vanish. Mitigation: check after every reboot with `rulecheck.py` and a ping test from Lab to Internet.
- Rule 2 trusts the analyst workstation completely.
- Syslog over UDP 514 is unauthenticated and can be forged by any lab machine; evidence from it is "reported by the sender", not proof.
- This design is for a lab. It is not a production design.
