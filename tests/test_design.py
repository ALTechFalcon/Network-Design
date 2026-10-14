import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import rulecheck  # noqa: E402
import subnetcheck  # noqa: E402

RULES = rulecheck.load_rules(ROOT / "firewall-rules.csv")


def test_subnets_ok():
    _, problems = subnetcheck.check()
    assert problems == []


def test_overlap_is_detected():
    _, problems = subnetcheck.check({"A": "10.10.10.0/24", "B": "10.10.10.128/25"})
    assert problems


def test_all_expectations_hold():
    assert rulecheck.main(["x", ROOT / "firewall-rules.csv", ROOT / "tests" / "expected.csv"]) == 0


def test_last_rule_is_default_deny():
    last = RULES[-1]
    assert (last["From"], last["To"], last["Action"]) == ("any", "any", "deny")


def test_lab_never_reaches_internet_or_users():
    for proto, port in [("tcp", 80), ("tcp", 443), ("udp", 53), ("icmp", 0), ("tcp", 22)]:
        for dst in ("Internet", "Users"):
            assert rulecheck.verdict(RULES, "Lab", dst, proto, port)[0] == "deny"


def test_every_rule_has_a_reason():
    assert all(r["Reason"].strip() for r in RULES)


def test_checker_catches_a_bad_rule(tmp_path):
    """Mutation test: a rule that lets Lab reach the Internet must make the checker fail."""
    bad = tmp_path / "bad.csv"
    rows = [dict(r) for r in RULES]
    rows[4]["Action"] = "allow"  # rule 5 flipped
    with open(bad, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    assert rulecheck.main(["x", bad, ROOT / "tests" / "expected.csv"]) == 1
