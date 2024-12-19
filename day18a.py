#!/usr/bin/env python3
import dataclasses
from collections import defaultdict
import math
from aocd import data

import sys
sys.setrecursionlimit(100000)


grid_size = 70+1

fallen_memory = 1024

start = 0+0j
end = grid_size-1 + 1j*(grid_size-1)

memory = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

for i, line in enumerate(data.splitlines()):
    if i == fallen_memory:
        break
    x, y = line.split(',')

    memory[int(y)][int(x)] = '#'

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

def dfs(node, visited, min_cost, current_cost):

    if node == end:
        return current_cost
    current_cost += 1

    if current_cost >= min_cost:
        return math.inf

    visited = set(visited)
    visited.add(node)
    
    for n in neighbours(node):
        if n not in visited:
            n_cost = dfs(n, visited, min_cost, current_cost)

            min_cost = min(min_cost, n_cost)
    return min_cost

def dijkstra(start):
    dist = defaultdict(lambda: math.inf)
    prev = defaultdict(lambda: None)

    Q = set()
    for i in range(grid_size):
        for j in range(grid_size):
            Q.add(i+1j*j)
    
    dist[start] = 0
    while Q:
        u = min(Q, key=lambda u: dist[u])
        Q.remove(u)

        for v in neighbours(u):
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    return dist, prev


dist, prev = dijkstra(start)
ans = dist[end]

print(ans)
