#!/usr/bin/env python3
import re

from aocd import data

# wide, tall
space_size = 101, 103

iters = 0

max_safety = 0
max_diagonal_length = -1
seen = set()
while True:
    q1, q2, q3, q4 = 0,0,0,0
    positions = set()

    mmap = [[' ' for _ in range(space_size[1])] for _ in range(space_size[0])]

    for line in data.splitlines():
        px, py, vx, vy = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line).groups()
        px, py, vx, vy = int(px), int(py), int(vx), int(vy)

        px = px + vx * iters
        py = py + vy * iters

        px %= space_size[0]
        py %= space_size[1]

        px %= space_size[0]
        py %= space_size[1]


        positions.add((px, py))

        x_mid = space_size[0] // 2
        y_mid = space_size[1] // 2

        if px < x_mid and py < y_mid:
            q1 += 1
        elif px < x_mid and py > y_mid:
            q2 += 1
        elif px > x_mid and py < y_mid:
            q3 += 1
        elif px > x_mid and py > y_mid:
            q4 += 1

        mmap[px][py] = '#'

    
    local_max_diag = 0
    local_diag = 0
    for i in range(len(mmap)):
        for j in range(len(mmap[i])):
            if mmap[i][j] != '#':
                local_max_diag = max(local_max_diag, local_diag)
                local_diag = 0
            else:
                local_diag += 1

    positions = tuple(sorted(positions))
    if positions in seen:
        exit()
    else:
        seen.add(positions)
    safety = q1 * q2 * q3 * q4
    if local_max_diag >= max_diagonal_length:
        max_diagonal_length = local_max_diag
        max_safety = safety
        print("&&&&&&&&&&&&&&&&&&&&")
        print(iters)

        for j in range(len(mmap[0])):
            for i in range(len(mmap)):
                print(mmap[i][j], end='')
            print()
    iters += 1
