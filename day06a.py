#!/usr/bin/env python3
import re

from aocd import data
from collections import defaultdict

pos = None
mmap = []
for i, line in enumerate(data.splitlines()):
    mmap.append(list())
    for j, value in enumerate(line):
        if value == '^':
            pos = i, j, 'UP'
            mmap[-1].append('.')
        else:
            mmap[-1].append(value)
assert pos

def forward(pos):
    if pos[2] == 'UP':
        return pos[0]-1,pos[1],'UP'
    elif pos[2] == 'RIGHT':
        return pos[0], pos[1]+1, 'RIGHT'
    elif pos[2] == 'DOWN':
        return pos[0]+1,pos[1],'DOWN'
    elif pos[2] == 'LEFT':
        return pos[0], pos[1]-1,'LEFT'

def turn(pos):
    return pos[0], pos[1], {
        'UP': 'RIGHT',
        'RIGHT': 'DOWN',
        'DOWN': 'LEFT',
        'LEFT': 'UP'
    }[pos[2]]

visited = {(pos[0], pos[1])}

while True:
    forward_pos = forward(pos)

    if forward_pos[0] < 0 or forward_pos[1] < 0 or forward_pos[0] >= len(mmap) or forward_pos[1] >= len(mmap[0]):
        break

    if mmap[forward_pos[0]][forward_pos[1]] == '#':
        pos = turn(pos)
    else:
        pos = forward_pos
        visited.add((pos[0], pos[1]))

print(len(visited))
