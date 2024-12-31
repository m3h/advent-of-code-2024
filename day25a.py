#!/usr/bin/env python3
import math
from aocd import data


keys = list()
locks = list()

for schematic in data.split('\n\n'):
    is_lock = schematic.startswith('#' * 5)
    is_key = not is_lock

    if is_key:
        keys.append([math.inf] * 5)
    elif is_lock:
        locks.append([-1] * 5)
    else:
        assert False

    for i, line in enumerate(schematic.split()):
        for j, c in enumerate(line):
            if c == '#':
                if is_key:
                    keys[-1][j] = min(keys[-1][j], i)
                elif is_lock:
                    locks[-1][j] = max(locks[-1][j], i)

def test_key(key, lock):
    for j in range(len(key)):
        if key[j] <= lock[j]:
            return 0
    return 1

ans = 0
for key in keys:
    for lock in locks:
        ans += test_key(key, lock)
print(ans)