#!/usr/bin/env python3
from collections import defaultdict
import math
import sys
sys.setrecursionlimit(100000)
from aocd import data

def read_map(data: str) -> tuple[complex, complex, list[list[str]]]:
    mmap = [[c for c in line] for line in data.splitlines()]

    start = None
    end = None
    for i in range(len(mmap)):
        for j in range(len(mmap[i])):
            if mmap[i][j] == 'S':
                mmap[i][j] = '.'
                start = i + 1j * j
            elif mmap[i][j] == 'E':
                mmap[i][j] = '.'
                end = i + 1j * j
    
    assert start is not None
    assert end is not None
    return start, end, mmap

def sget(mmap: list[list[str]], n: complex) -> str:
    if n.real < 0 or n.imag < 0 or n.real >= len(mmap) or n.imag >= len(mmap[int(n.real)]):
        return None
    return mmap[int(n.real)][int(n.imag)]

def dist(a: complex, b: complex) -> float:
    return abs(a.real - b.real) + abs(a.imag - b.imag)

def get_all_neighbours(mmap: list[list[str]], n: complex):
    return filter(lambda node_value: node_value[1], map(lambda node: (node, sget(mmap, node)), (n + (1j ** i) for i in range(4))))

def get_cheat_neighbours(mmap: list[list[str]], cheat_start: complex, cheat_length: int) -> set[complex]:
    queue = {cheat_start}

    visited = set()
    while queue:
        n = queue.pop()
        visited.add(n)

        for adjacent_node, adjacent_value in get_all_neighbours(mmap, n):
            if dist(cheat_start, adjacent_node) >= cheat_length:
                continue
            elif adjacent_value == '.':
                yield adjacent_node
            elif adjacent_node not in visited:
                queue.add(adjacent_node)


def get_neighbours(mmap: list[list[str]], n: complex, allow_cheats: bool, cheat_length: int) -> set[tuple[complex, complex]]:
    for potential_neighbour, potential_neighbour_value in get_all_neighbours(mmap, n):

        if potential_neighbour_value == '.':
            yield potential_neighbour, None
        elif allow_cheats and potential_neighbour_value == '#':
            for cheat_end in get_cheat_neighbours(mmap, potential_neighbour, cheat_length):
                if cheat_end == n:
                    continue
                yield cheat_end, potential_neighbour

def add_cheat(cheats, cheat_loc, cost, max_picoseconds):
    if cost <= max_picoseconds and cost < cheats[cheat_loc]:
        cheats[cheat_loc] = cost

dfs_cache = dict()
def dfs_shortest_path(mmap: list[list[str]], start: complex, end: complex, allow_cheats: bool, cheat_length: int, max_picoseconds: float, visited: set[complex]):
    cache_key = start, allow_cheats
    if cache_key in dfs_cache:
        return dfs_cache[cache_key]

    if start == end:
        return 0, {}
    
    if start in visited:
        return float('inf'), {}
    
    visited = visited | {start}

    cheats = defaultdict(lambda: math.inf) 
    min_cost = float('inf')

    for neighbour, cheat_start in get_neighbours(mmap=mmap, n=start, allow_cheats=allow_cheats, cheat_length=cheat_length):
        new_cheat = None
        if cheat_start:
            new_cheat = (start, neighbour)
        if new_cheat in cheats:
            # we've already counted this cheat, no need to check again
            continue
        neighbour_cost = dist(start, neighbour)
        sub_cost, sub_cheats = dfs_shortest_path(
            mmap=mmap,
            start=neighbour,
            end=end,
            allow_cheats=allow_cheats and cheat_start is None,
            cheat_length=cheat_length,
            max_picoseconds=max_picoseconds,
            visited=visited,
        )

        new_cost = sub_cost + neighbour_cost

        min_possible_goal_cost = new_cost + dist(neighbour, end) - 2
        if min_possible_goal_cost > max_picoseconds:
            continue
        if new_cost > max_picoseconds:
            continue
        min_cost = min(new_cost, min_cost)

        for sub_cheat_locs, sub_cheat_cost in sub_cheats.items():
            new_cheat_cost = sub_cheat_cost + neighbour_cost
            add_cheat(cheats, sub_cheat_locs, new_cheat_cost, max_picoseconds)
        if cheat_start:
            new_cheat = (start, neighbour)
            add_cheat(cheats, new_cheat, new_cost, max_picoseconds)
    
    dfs_cache[cache_key] = min_cost, cheats
    return min_cost, cheats

def main(data: str, cheat_length: int, cheat_reduction: int):
    start, end, mmap = read_map(data)

    min_cost_no_cheats, _= dfs_shortest_path(
        mmap=mmap,
        start=start,
        end=end,
        allow_cheats=False,
        cheat_length=cheat_length,
        max_picoseconds=math.inf,
        visited=set(),
    )

    cheat_max_picoseconds = min_cost_no_cheats - cheat_reduction
    _, cheats = dfs_shortest_path(
        mmap=mmap,
        start=start,
        end=end,
        allow_cheats=True,
        cheat_length=cheat_length,
        max_picoseconds=cheat_max_picoseconds,
        visited=set(),
    )

    return len(cheats)

if __name__ == "__main__":
    # print('example p1', main(data=data_example, cheat_length=2, cheat_reduction=12))
    # print('example p2', main(data=data_example, cheat_length=20, cheat_reduction=76))

    print('real p1', main(data=data, cheat_length=20, cheat_reduction=100))

