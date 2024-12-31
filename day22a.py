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
    for _ in range(iterations):
        s = next_secret(s)
    return s

next_iterations(123, 10)

ans = 0
for secret_number in data.splitlines():
    secret_number = int(secret_number)
    ans += next_iterations(secret_number, 2000)
print(ans)



