#!/usr/bin/env python3
from collections import defaultdict
from aocd import data

edges: defaultdict[str, set[str]] = defaultdict(set)

for line in data.splitlines():
    n1, n2 = line.split('-')

    edges[n1].add(n2)
    edges[n2].add(n1)

well_connected_sets = set()
for n1 in set(edges):

    well_connected_set = {n1}

    for n2 in set(edges):
        if all(n2 in edges[n] for n in well_connected_set):
            well_connected_set.add(n2)

    well_connected_sets.add(tuple(sorted(well_connected_set)))

largest_set = max(well_connected_sets, key=len)
print(','.join(largest_set))