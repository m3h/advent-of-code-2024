#!/usr/bin/env python3
import re
from collections import defaultdict
from dataclasses import dataclass

from aocd import data

data = data.splitlines()

mmap = list()

grid_end = None
for i, line in enumerate(data):
    if line == '':
        grid_end = i
        break

    mmap.append(list())
    for j, c in enumerate(line):
        if c == '@':
            robot = i, j
        mmap[-1].append(c)

moves = list()
for line in data[grid_end:]:
    for c in line:
        moves.append(c)

def getm(block):
    return mmap[block[0]][block[1]]
def setm(block, value):
    mmap[block[0]][block[1]] = value

def try_move(block, direction):
    new_block = block[0]+direction[0], block[1]+direction[1]

    if getm(new_block) == '.':
        setm(new_block, getm(block))
        setm(block, '.')
        return new_block
    elif getm(new_block) == 'O':
        if try_move(new_block, direction):
            setm(new_block, getm(block))
            setm(block, '.')
            return new_block
        else:
            return None
    elif getm(new_block) == '#':
        return None

for move in moves:
    direction = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }[move]

    if new_block := try_move(robot, direction):
        robot = new_block
    
ans = 0
for i, line in enumerate(mmap):
    for j, c in enumerate(line):
        if c == 'O':
            ans += 100 *i + j
print(ans)
