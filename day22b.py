#!/usr/bin/env python3
# from aocd import data
import sys
from collections import defaultdict
import copy
import functools
from aocd import data

def next_secret(s):
    s = ((s * 64) ^ s) % 16777216

    s = ((s // 32) ^ s) % 16777216

    s = ((s * 2048 ) ^ s) % 16777216

    return s

def next_iterations(s, iterations):
    secrets = [s]
    changes = []
    previous_digit = None

    seq_prices = {}
    for _ in range(iterations):
        s = next_secret(s)
        digit = s % 10

        if previous_digit is not None:
            delta = digit - previous_digit
            changes.append(delta)

        if len(changes) >= 4:
            seq = tuple(changes[-4:])
            if seq not in seq_prices:
                seq_prices[seq] = digit

        previous_digit = digit
    return seq_prices

seq_totals = defaultdict(int)
for secret_number in data.splitlines():
    secret_number = int(secret_number)
    for seq, bananas in next_iterations(secret_number, 2000).items():
        seq_totals[seq] += bananas

ans = max(seq_totals.values())
print(ans)



