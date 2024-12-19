#!/usr/bin/env python3
import dataclasses
from collections import defaultdict
import math
import time
from aocd import data

import sys
sys.setrecursionlimit(100000)

grid_size = 70+1

start = 0+0j
end = grid_size-1 + 1j*(grid_size-1)

memory = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

falling_bytes = []

for i, line in enumerate(data.splitlines()):
    x, y = line.split(',')

    falling_bytes.append(int(y) + 1j * int(x))


def sget(n):
    if n.real < 0 or n.imag < 0 or n.real >= grid_size or n.imag >= grid_size:
        return '#'

    return memory[int(n.real)][int(n.imag)]

def neighbours(node):
    direction = 1
    for _ in range(4):
        direction *= 1j

        n = node + direction

        if sget(n) != '#':
            yield n

def dfs(node, goal, visited):
    if node == goal:
        return True

    visited.add(node)

    for n in neighbours(node):
        if n not in visited:
            if dfs(n, goal, visited):
                return True
    return False

for falling_byte in falling_bytes:
    memory[int(falling_byte.real)][int(falling_byte.imag)] = '#'


    visited = set()
    if not dfs(start, end, visited):
        print(f'{int(falling_byte.imag)},{int(falling_byte.real)}')
        exit()

print("NO ANSWER FOUND")
