#!/usr/bin/env python3
from collections import defaultdict
from aocd import data

edges: defaultdict[str, set[str]] = defaultdict(set)

for line in data.splitlines():
    n1, n2 = line.split('-')

    edges[n1].add(n2)
    edges[n2].add(n1)

sets_of_three_with_t = set()
for n1 in set(edges):
    if n1[0] != 't':
        continue
    connected_to_n = set(edges[n1])

    for n2 in connected_to_n:
        for n3 in connected_to_n:
            if n3 in edges[n2]:
                s = tuple(sorted({n1, n2, n3}))
                sets_of_three_with_t.add(s)

print(len(sets_of_three_with_t))
