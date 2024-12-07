#!/usr/bin/env python3
from aocd import data


equations = []

for line in data.splitlines():
    lhs, rhs = line.split(":")

    lhs = int(lhs.strip())
    rhs = [int(x.strip()) for x in rhs.split()]

    assert lhs > 0
    assert all(r > 0 for r in rhs)

    equations.append((lhs, rhs))

def dfs(target, acc, rhs):
    if acc > target:
        return False
    elif len(rhs) == 0:
        return target == acc
    else:
        return dfs(target, acc + rhs[0], rhs[1:]) or dfs(target, acc * rhs[0], rhs[1:]) or dfs(target, int(f'{acc}{rhs[0]}'), rhs[1:])

ans = 0
for lhs, rhs in equations:
    assert len(rhs) > 1
    if dfs(lhs, rhs[0], rhs[1:]):
        ans += lhs
print(ans)
