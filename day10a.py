#!/usr/bin/env python3
from aocd import data

mmap = []
for line in data.splitlines():
    mmap.append(list())
    for ch in line:
        if ch == ".":
            mmap[-1].append(-1)
        else:
            mmap[-1].append(int(ch))


def sget(i, j):
    if i < 0 or j < 0 or i >= len(mmap) or j >= len(mmap[i]):
        return -1
    else:
        return mmap[i][j]


nines = set()


def score(i, j):
    global nines
    if sget(i, j) == 9:
        nines |= {(i, j)}

    if sget(i - 1, j) == mmap[i][j] + 1:
        score(i - 1, j)
    if sget(i + 1, j) == mmap[i][j] + 1:
        score(i + 1, j)
    if sget(i, j - 1) == mmap[i][j] + 1:
        score(i, j - 1)
    if sget(i, j + 1) == mmap[i][j] + 1:
        score(i, j + 1)


ans = 0
for i in range(len(mmap)):
    for j in range(len(mmap[i])):
        if mmap[i][j] == 0:
            nines = set()
            score(i, j)
            ans += len(nines)
print(ans)
