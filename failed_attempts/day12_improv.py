#!/usr/bin/env python3
from aocd import data

data = [[c for c in line] for line in data.splitlines()]

def move(p, d):
    return p[0] + d[0], p[1] + d[1]

def sget(p):
    if p[0] < 0 or p[1] < 0 or p[0] >= len(data) or p[1] >= len(data[p[0]]):
        return None
    else:
        return data[p[0]][p[1]]

def neighbours(p):
    neighbours_ = set()
    for d in [(0,1), (0,-1), (1,0), (-1,0)]:
        n = move(p, d)
        if sget(n) == sget(p):
            neighbours_.add(n)
    return neighbours_

def count_area_and_corners(p, visited):
    if p in visited:
        return 0, 0, visited
    else:
        visited.add(p)

    n = neighbours(p)
    if len(n) == 0:
        #    X
        corners = 4
    elif len(n) == 3:
        #    x
        #   xXx
        corners = 0
    elif len(n) == 2:
        n1, n2 = n
        if n2[0] - n1[0] == 0 or n2[1] - n1[1] == 0:
            #   xXx
            corners = 0
        else:
            #   x
            #   Xx
            corners = 2
    elif len(n) == 1:
        #  Xx
        corners = 2
    elif len(n) == 4:
        #   x
        #  xXx
        #   x
        corners = 0

    area = 1

    for nx in n:
        new_corners, new_area, _ = count_area_and_corners(nx, visited)
        corners += new_corners
        area += new_area

    return area, corners, visited


total_cost = 0
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j]:
            area, corners, visited = count_area_and_corners((i,j), set())

            cost = area * corners
            total_cost += cost
            print(f'{data[i][j]=} {area=} {corners=} {cost=}')
            for n in visited:
                data[n[0]][n[1]] = None
print(total_cost)
