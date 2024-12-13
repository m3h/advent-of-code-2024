#!/usr/bin/env python3
from aocd import data
import sys
sys.setrecursionlimit(100000)

mmap = []
for line in data.splitlines():
    # for _ in range(4):
    mmap.append(list())
    for c in line:
        mmap[-1].append(c)

mmap = []
for line in data.splitlines():
    for _ in range(4):
        mmap.append(list())
        for c in line:
            for _ in range(4):
                mmap[-1].append(c)

def sget(i, j):
    if i < 0 or j < 0 or i >= len(mmap) or j >= len(mmap[0]):
        return None
    return mmap[i][j]

perimeter = set()
def get_ap(i, j, c, visited=set()):
    global perimeter
    if ((i, j)) in visited:
        return visited

    visited.add((i, j))
    a = 1
    p = 0
    for id, jd in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ni, nj = i+id, j+jd
        n = sget(ni, nj)

        if n == c:
            visited = get_ap(ni, nj, c, visited)
        else:
            perimeter.add((i, j))
    return visited

def count_perimeter(visited):
    s = 0

    in_perimeter_count = 0

    for i in range(len(mmap)+1) :
        for j in range(len(mmap[0])+1):
            block_is_in = (i, j) in perimeter
            if block_is_in:
                in_perimeter_count += 1
            else:
                if in_perimeter_count >= 4:
                    s += 1
                in_perimeter_count = 0

    in_perimeter_count = 0
    for j in range(len(mmap[0])+1):
        for i in range(len(mmap)+1) :
            block_is_in = (i, j) in perimeter
            if block_is_in:
                in_perimeter_count += 1
            else:
                if in_perimeter_count >= 4:
                    s += 1
                in_perimeter_count = 0
    return s






def clear_plot(i, j, c, plot_points = None):
    if plot_points is None:
        plot_points = {(i, j)}
    for id, jd in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ni, nj = i+id, j+jd
        n = sget(ni, nj)

        if n == c and (ni, nj) not in plot_points:
            plot_points.add((ni, nj))
            clear_plot(ni, nj, c, plot_points)
    return plot_points

price = 0
for i in range(len(mmap)):
    for j in range(len(mmap[i])):

        if mmap[i][j]:
            perimeter.clear()
            visited = get_ap(i, j, mmap[i][j], set())
            s = count_perimeter(visited)
            a = len(visited) / 4 / 4
            price_plot = a * s
            price += price_plot

            minp = min(x[0] for x in perimeter), min(x[1] for x in perimeter)
            maxp = max(x[0] for x in perimeter), max(x[1] for x in perimeter)

            for ci, cj in visited:
                mmap[ci][cj] = None

print(price)