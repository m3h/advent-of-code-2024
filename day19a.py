#!/usr/bin/env python3
from aocd import data
import sys
import functools
sys.setrecursionlimit(100000)

available_patterns, designs = data.split('\n\n')

available_patterns = [pattern for pattern in available_patterns.split(', ')]

designs = designs.splitlines()

available_patterns = set(available_patterns)

@functools.cache
def try_design(remaining_design: str):

    if remaining_design == '':
        return True

    # work backwards for better caching, or somin
    for i in range(len(remaining_design)):
        front, back = remaining_design[:-i-1], remaining_design[-1-i:]
        if back in available_patterns:
            if try_design(front):
                return True
    return False


ans = 0
for design in designs:
    if try_design(design):
        ans += 1
print(ans)

