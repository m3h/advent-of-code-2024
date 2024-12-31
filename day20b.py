#!/usr/bin/env python3
from aocd import data
import sys
from collections import defaultdict
import copy
import functools
import tqdm
import math
sys.setrecursionlimit(100000)


start = None
end = None

mmap = []
for i, line in enumerate(data.splitlines()):
    mmap.append(list())
    for j, c in enumerate(line):
        if c == 'S':
            c = '.'
            start = i + 1j * j
        elif c == 'E':
            c = '.'
            end = i + 1j * j
        mmap[-1].append(c)

def sget(n: complex):
    if n.real < 0 or n.imag < 0 or n.real >= len(mmap) or n.imag >= len(mmap[0]):
        return None
    else:
        return mmap[int(n.real)][int(n.imag)]

def neighbours(n, include_walls):
    direction = 1
    for _ in range(4):
        direction *= 1j
        neighbour = n + direction
        neigbour_value = sget(neighbour)
        if neigbour_value == '.':
            yield neighbour
        elif neigbour_value == '#' and include_walls:
            yield neighbour

def cheat_neighbours(mmap: list[list[str]], n: complex, allow_cheats: bool, cheat_length: int) -> set[tuple[complex, complex]]:
    for potential_neighbour, potential_neighbour_value in neighbours(n, include_walls=True):

        if potential_neighbour_value == '.':
            continue
        elif allow_cheats and potential_neighbour_value == '#':
            for cheat_end in get_cheat_neighbours(mmap, potential_neighbour, cheat_length):
                if cheat_end == n:
                    continue
                yield cheat_end, potential_neighbour

def dist(a: complex, b: complex) -> float:
    return abs(a.real - b.real) + abs(a.imag - b.imag)
def get_all_neighbours(mmap: list[list[str]], n: complex):
    return filter(lambda node_value: node_value[1], map(lambda node: (node, sget(node)), (n + (1j ** i) for i in range(4))))
def get_cheat_neighbours(mmap: list[list[str]], cheat_start: complex, cheat_length: int) -> set[complex]:
    queue = {cheat_start}

    visited = set()
    while queue:
        n = queue.pop()
        visited.add(n)

        for adjacent_node, adjacent_value in get_all_neighbours(mmap, n):
            if dist(cheat_start, adjacent_node) > cheat_length:
                continue

            if adjacent_value == '.':
                yield adjacent_node

            if adjacent_node not in visited:
                queue.add(adjacent_node)

minimum_time = defaultdict(lambda: float('inf'))
def dfs_no_cheats(n, visited, end):
    cache_key = n, end
    if cache_key in minimum_time:
        return minimum_time[cache_key]

    if n in visited:
        return float('inf')
    
    visited = visited | {n}

    if n == end:
        return 0
    min_picoseconds = float('inf')
    for neighbour in sorted(neighbours(n, include_walls=False), key=lambda n: dist(n, end), reverse=True):
        min_picoseconds = min(min_picoseconds, 1+dfs_no_cheats(neighbour, visited, end))

    if min_picoseconds != math.inf:
        minimum_time[cache_key] = min(minimum_time[cache_key], min_picoseconds)
    return min_picoseconds

min_time = dfs_no_cheats(start, set(), end=end)

def find_good_cheats(mmap, cheat_length, max_time):
    cheat_locations = set()
    for i in tqdm.tqdm(range(len(mmap))):
        for j in range(len(mmap[i])):
            if mmap[i][j] != '.':
                continue

            cheat_start = i + 1j * j     
            for cheat_end in get_cheat_neighbours(mmap=mmap, cheat_start=cheat_start, cheat_length=cheat_length):
                dist_cheat_end_to_end = dfs_no_cheats(cheat_end, set(), end)
                if dist_cheat_end_to_end > max_time:
                    continue
                dist_cheat_start_to_cheat_end = dist(cheat_start, cheat_end)
                if dist_cheat_end_to_end + dist_cheat_start_to_cheat_end > max_time:
                    continue
                dist_start_to_cheat_start = dfs_no_cheats(cheat_start, set(), start)

                dist_total = dist_start_to_cheat_start + dist_cheat_start_to_cheat_end + dist_cheat_end_to_end

                if dist_total <= max_time:
                    cheat_locations.add((cheat_start, cheat_end))
    return cheat_locations

cheat_length=20; reduction=100

good_cheats = find_good_cheats(mmap=mmap, cheat_length=cheat_length, max_time = min_time - reduction)        
print(len(good_cheats))
