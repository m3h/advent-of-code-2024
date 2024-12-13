#!/usr/bin/env python3
from aocd import data

mmap = []
for line in data.splitlines():
    mmap.append(list())
    for c in line:
        mmap[-1].append(c)

def sget(i, j):
    if i < 0 or j < 0 or i >= len(mmap) or j >= len(mmap):
        return None
    return mmap[i][j]

def get_ap(i, j, c, visited=set()):
    if ((i, j)) in visited:
        return 0, 0

    visited.add((i, j))
    a = 1
    p = 0
    for id, jd in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ni, nj = i+id, j+jd
        n = sget(ni, nj)

        if n == c:
            na, np = get_ap(ni, nj, c, visited)
            a += na
            p += np
        else:
            p += 1
    return a, p

def clear_plot(i, j, c):
    plot_points = {(i, j)}
    for id, jd in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ni, nj = i+id, j+jd
        n = sget(ni, nj)

        if n == c and (ni, nj) not in plot_points:
            plot_points.add((ni, nj))
    return plot_points

price = 0
for i in range(len(mmap)):
    for j in range(len(mmap[i])):
        if mmap[i][j]:
            a, p = get_ap(i, j, mmap[i][j])
            price_plot = a * p
            price += price_plot

            area_to_clear = clear_plot(i, j, mmap[i][j])
            for ci, cj in area_to_clear:
                mmap[ci][cj] = None

print(price)