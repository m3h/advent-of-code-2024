#!/usr/bin/env python3
from collections import defaultdict
import math
import itertools
import sys
import tqdm
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

def all_nodes_path(mmap):
    for i in range(len(mmap)):
        for j in range(len(mmap[i])):
            if mmap[i][j] == '.':
                yield i + 1j * j

def floyd_warshall(mmap, cheat_length):

    dist_map = defaultdict(lambda: defaultdict(lambda: math.inf))
    for n1 in all_nodes_path(mmap):
        for end, start in get_neighbours(mmap=mmap, n=n1, allow_cheats=True, cheat_length=cheat_length):
            if start:
                # cheat
                dist_map[n1, False][end, True] = dist(n1, end)
            else:
                # legal
                dist_map[n1, False][end, False] = dist(n1, end)
                # The True/False indicates if we've ever cheated
                dist_map[n1, True][end, True] = dist(n1, end)
    for n1 in all_nodes_path(mmap):
        dist_map[n1, False][n1, False] = 0
        dist_map[n1, True][n1, True] = 0

    def all_paths_with_tf():
        return list(itertools.product(all_nodes_path(mmap), [True, False]))

    for k in all_paths_with_tf():
        for i in tqdm.tqdm(all_paths_with_tf()):
            for j in all_paths_with_tf():
                if dist_map[i][j] > dist_map[i][k] + dist_map[k][j]:
                    dist_map[i][j] = dist_map[i][k] + dist_map[k][j]
    return dist_map

def find_good_cheats(dist_map, max_picoseconds, start, end):

    start = start, False
    end = end, True
    good_cheats = set()
    for n1 in filter(lambda node: not node[1],dist_map):
        if n1[1]:
            continue

        for cheat_jump_node in filter(lambda node: node[1], dist_map[n1]):

            start_to_cheat_start = dist_map[start][n1]
            cheat_dist = dist_map[n1][cheat_jump_node]
            cheat_end_to_goal = dist_map[cheat_jump_node][end]

            cheat_id = n1[0], cheat_jump_node[0]

            total_dist = start_to_cheat_start + cheat_dist + cheat_end_to_goal

            if total_dist <= max_picoseconds:
                good_cheats.add(cheat_id)
    return good_cheats




    # coordinates = list(filter(lambda coord: mmap[coord[0]][coord[1]] == '.', itertools.combinations(range(len(mmap)), range(len(mmap[0])))))
    # dist = defaultdict(lambda: defaultdict: lambda)
def main(data: str, cheat_length: int, cheat_reduction: int):
    start, end, mmap = read_map(data)

    dist_map = floyd_warshall(mmap=mmap, cheat_length=cheat_length)

    no_cheat_min_dist = dist_map[start, False][end, False]
    print(f'{no_cheat_min_dist=}')

    good_cheats = find_good_cheats(dist_map=dist_map, max_picoseconds=no_cheat_min_dist-cheat_reduction, start=start, end=end)

    return len(good_cheats)

if __name__ == "__main__":
    # print('example p1', main(data=data_example, cheat_length=2, cheat_reduction=12))
    # print('example p2', main(data=data_example, cheat_length=20, cheat_reduction=76))

    print('real p1', main(data=data, cheat_length=20, cheat_reduction=100))

