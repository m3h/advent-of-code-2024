#!/usr/bin/env python3
from aocd import data
import sys
from collections import defaultdict
import copy
import functools
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

minimum_time = defaultdict(lambda: float('inf'))
def dfs_no_cheats(n, visited):
    if n in minimum_time:
        return minimum_time[n]

    if n in visited:
        return float('inf')

    visited = visited | {n}

    if n == end:
        return 0
    min_picoseconds = float('inf')
    for neighbour in neighbours(n, include_walls=False):
        min_picoseconds = min(min_picoseconds, 1+dfs_no_cheats(neighbour, visited))

    minimum_time[n] = min(minimum_time[n], min_picoseconds)
    return min_picoseconds

def cheat(n):
    undo_list = set()
    for neighbour in neighbours(n, include_walls=True):
        if sget(neighbour) == '#':
            undo_list.add(neighbour)
            mmap[int(neighbour.real)][int(neighbour.imag)] = '.'
    return undo_list

def undo_cheat(undo_list):
    for n in undo_list:
        mmap[int(n.real)][int(n.imag)] = '#'

def dfs_with_cheats(n, picoseconds, max_picoseconds, visited):
    if n in visited:
        return set()

    if picoseconds > max_picoseconds:
        return set()

    visited = visited | {n}

    if n == end:
        return set()

    cheat_locations = set()
    for neighbour in neighbours(n, include_walls=True):
        if sget(neighbour) == '#':
            # mmap[int(neighbour.real)][int(neighbour.imag)] = '.'
            for neighbours_neighbour in neighbours(neighbour, include_walls=True):
                if sget(neighbours_neighbour) == '#':
                    continue
                # mmap[int(neighbours_neighbour.real)][int(neighbours_neighbour.imag)] = '.'

                new_pico = picoseconds + 2 + dfs_no_cheats(neighbours_neighbour, visited | {neighbour})
                if new_pico <= max_picoseconds:
                    cheat_locations.add((neighbour, neighbours_neighbour))

                    # mmap[int(neighbours_neighbour.real)][int(neighbours_neighbour.imag)] = '#'
            # mmap[int(neighbour.real)][int(neighbour.imag)] = '#'
        else:
            cheat_locations |= dfs_with_cheats(neighbour, picoseconds+1, max_picoseconds, visited)

    return cheat_locations

original_mmap = copy.deepcopy(mmap)

min_time = dfs_no_cheats(start, set())

cheat_locations = dfs_with_cheats(start, 0, min_time - 100, set())
print(len(cheat_locations))
