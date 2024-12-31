#!/usr/bin/env python3
import re
from collections import defaultdict

from aocd import data

mmap = []
for line in data.splitlines():
    mmap.append(list())
    for ch in line:
        if ch == '.':
            mmap[-1].append(-1)
        else:
            mmap[-1].append(int(ch))

print(mmap)


ans = 0

def sget(i, j):
    if i < 0 or j < 0 or i >= len(mmap) or j >= len(mmap[i]):
        return -1
    else:
        return mmap[i][j]

def score(i, j):
    if sget(i, j) == 9:
        print(i, j)
        return 1
    s = 0
    if sget(i-1, j) == mmap[i][j]+1:
        s += score(i-1, j)
    if sget(i+1, j) == mmap[i][j]+1:
        s += score(i+1, j)
    if sget(i, j-1) == mmap[i][j]+1:
        s += score(i, j-1)
    if sget(i, j+1) == mmap[i][j]+1:
        s += score(i, j+1)
    
    return s

for i in range(len(mmap)):
    for j in range(len(mmap[i])):
        if mmap[i][j] == 0:
            ans += score(i, j)
print(ans)