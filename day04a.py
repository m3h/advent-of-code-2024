#!/usr/bin/env python3
import re

from aocd import data


d = []
for line in data.splitlines():
    rd = []
    for row in line:
        rd.append(row)
    d.append(rd)
print(d)

w = list('XMAS')

def check_dir(x_s, y_s, x_dir, y_dir):
    x = 0
    y = 0
    for _ in range(len(w)):
        if x_s >= len(d) or y_s >= len(d[x_s]) or x_s <0 or y_s < 0:
            return 0

        if x_s >= len(d):
            x_s = 0
        if y_s >= len(d):
            y_s = 0
        if x_s < 0:
            x_s = len(d)-1
        if y_s < 0:
            y_s = len(d[0]) - 1
        
        if d[x_s][y_s] != w[_]:
            return 0
        
        x_s += x_dir
        y_s += y_dir
    return 1

count = 0
for i in range(len(d)):
    for j in range(len(d[i])):
        count += (
            check_dir(i, j, 0, 1)
             + check_dir(i, j, 1, 0)
             + check_dir(i, j, 0, -1)
             + check_dir(i, j, -1, 0)
             + check_dir(i, j, 1, 1)
             + check_dir(i, j, 1, -1)
             + check_dir(i, j, -1, 1)
             + check_dir(i, j, -1, -1)
        )

print(count)
# print(ans)
# print(ans)
# submit(ans)
