#!/usr/bin/env python3
"""Check that segment subnets are valid, private, and do not overlap."""
import ipaddress
import itertools
import sys

SEGMENTS = {
    "Users": "10.10.10.0/24",
    "Servers": "10.10.20.0/24",
    "Lab": "10.10.30.0/24",
    "Mgmt": "10.10.40.0/24",
}


def check(segments=SEGMENTS):
    nets = {n: ipaddress.ip_network(c) for n, c in segments.items()}
    problems = [f"{n} {net} is not a private range" for n, net in nets.items() if not net.is_private]
    for (a, na), (b, nb) in itertools.combinations(nets.items(), 2):
        if na.overlaps(nb):
            problems.append(f"{a} {na} overlaps {b} {nb}")
    return nets, problems


if __name__ == "__main__":
    nets, problems = check()
    for n, net in nets.items():
        print(f"{n:<8} {net}  usable hosts: {net.num_addresses - 2}")
    print("\n" + ("\n".join(problems) if problems else "OK: no overlaps, all private"))
    sys.exit(1 if problems else 0)
