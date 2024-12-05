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

def g(x,y):
    if x < 0 or y < 0 or x >= len(d) or y >= len(d[x]):
        return None
    return d[x][y]
def check_mas(x_s, y_s):
    if g(x_s, y_s) != 'A':
        return False

    c = 0
    if g(x_s-1, y_s-1) == 'M' and g(x_s+1, y_s+1) == 'S':
        c += 1
    if g(x_s-1, y_s-1) == 'S' and g(x_s+1, y_s+1) == 'M':
        c += 1
    if c != 1:
        return False

    c = 0
    if g(x_s-1, y_s+1) == 'M' and g(x_s+1, y_s-1) == 'S':
        c += 1
    if g(x_s-1, y_s+1) == 'S' and g(x_s+1, y_s-1) == 'M':
        c += 1
    if c != 1:
        return False

    return True


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
        if check_mas(i, j):
            count += 1

print(count)
# print(ans)
# print(ans)
# submit(ans)
