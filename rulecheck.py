#!/usr/bin/env python3
"""Evaluate firewall-rules.csv (first match wins) against tests/expected.csv.

Usage: python3 rulecheck.py [rules.csv] [expected.csv]
Exit code 0 if every expectation holds, 1 otherwise.
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).parent


def load_rules(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def _match_field(rule_value, value):
    return rule_value.lower() == "any" or rule_value.lower() == value.lower()


def _match_ports(rule_ports, port):
    if rule_ports.lower() == "any":
        return True
    return str(port) in [p.strip() for p in rule_ports.split(",")]


def verdict(rules, src, dst, proto, port):
    """Return (action, rule_no) of the first matching rule; default deny."""
    for r in rules:
        if (_match_field(r["From"], src) and _match_field(r["To"], dst)
                and _match_field(r["Protocol"], proto)
                and _match_ports(r["Ports"], port)):
            return r["Action"].lower(), r["No"]
    return "deny", "implicit"


def main(argv):
    rules = load_rules(argv[1] if len(argv) > 1 else HERE / "firewall-rules.csv")
    exp_path = argv[2] if len(argv) > 2 else HERE / "tests" / "expected.csv"
    failed = 0
    with open(exp_path, newline="") as fh:
        for t in csv.DictReader(fh):
            got, rule = verdict(rules, t["From"], t["To"], t["Protocol"], t["Port"])
            ok = got == t["Expected"].lower()
            failed += not ok
            print(f"{'PASS' if ok else 'FAIL'}  {t['From']:>8} -> {t['To']:<9} "
                  f"{t['Protocol']}/{t['Port']:<4} expected {t['Expected']:<5} "
                  f"got {got:<5} (rule {rule})  {t['Why']}")
    print(f"\n{failed} failed" if failed else "\nAll expectations hold")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
