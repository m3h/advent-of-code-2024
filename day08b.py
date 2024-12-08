#!/usr/bin/env python3
from aocd import data
from collections import defaultdict

frequencies = defaultdict(set)
antinodes = defaultdict(set)

anitnodes_no_overlap = set()

mmap = list()
for i, line in enumerate(data.splitlines()):
    mmap.append(list())
    for j, char in enumerate(line):
        mmap[-1].append(char)
        if char != '.':
            frequencies[char].add((i, j))

def check_bounds(n):
    return n[0] >= 0 and n[1] >= 0 and n[0] < len(mmap) and n[1] < len(mmap[0])

for frequency, locations in frequencies.items():
    for a in locations:
        # if len(locations) > 1:
            # anitnodes_no_overlap.add(a)
        for b in locations:
            if b == a:
                continue

            # 3, 4
            # 5, 5

            # 1, 3
            # 7, 6

            d = 0
            while True:
                na = a[0] - d*(b[0] - a[0]), a[1] - d*(b[1] - a[1])
                nb = b[0] - d*(a[0] - b[0]), b[1] - d*(a[1] - b[1])

                end = True
                if check_bounds(na):
                    antinodes[frequency].add(na)
                    anitnodes_no_overlap.add(na)
                    end = False
                if check_bounds(nb):
                    antinodes[frequency].add(nb)
                    anitnodes_no_overlap.add(nb)
                    end = False
                if end:
                    break
                else:
                    d += 1

            d = 0
            while True:
                na = a[0] - d*(b[0] - a[0]), a[1] - d*(b[1] - a[1])
                nb = b[0] - d*(a[0] - b[0]), b[1] - d*(a[1] - b[1])

                end = True
                if check_bounds(na):
                    antinodes[frequency].add(na)
                    anitnodes_no_overlap.add(na)
                    end = False
                if check_bounds(nb):
                    antinodes[frequency].add(nb)
                    anitnodes_no_overlap.add(nb)
                    end = False
                if end:
                    break
                else:
                    d -= 1

ans = 0
for f in antinodes:
    for n in antinodes[f]:
        ans += 1
print(len(anitnodes_no_overlap))