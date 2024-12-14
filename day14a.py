#!/usr/bin/env python3
import re
from collections import defaultdict
from dataclasses import dataclass

from aocd import data

# wide, tall
space_size = 101, 103

iters = 100


q1, q2, q3, q4 = 0,0,0,0
for line in data.splitlines():
    px, py, vx, vy = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line).groups()
    px, py, vx, vy = int(px), int(py), int(vx), int(vy)

    px = px + vx * iters
    py = py + vy * iters

    px %= space_size[0]
    py %= space_size[1]


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

print(q1*q2*q3*q4)
