#!/usr/bin/env python3
import dataclasses
from aocd import data

import sys
sys.setrecursionlimit(100000)

grid_size = 70+1

fallen_memory = 1024

start = 0+0j
exit = grid_size-1 + 1j*(grid_size-1)

memory = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

for i, line in enumerate(data.splitlines()):
    if i == fallen_memory:
        break
    x, y = line.split(',')

    memory[int(y)][int(x)] = '#'

for line in memory:
    print(''.join(line))

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

def dfs(node, visited):

    if node == exit:
        return 0
    
    visited = set(visited)
    visited.add(node)
    
    min_cost = float('inf')

    for n in neighbours(node):
        if n not in visited:
            n_cost = 1 + dfs(n, visited)
            min_cost = min(min_cost, n_cost)
    return min_cost

ans = dfs(start, set())
print(ans)

