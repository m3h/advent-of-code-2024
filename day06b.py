#!/usr/bin/env python3
import re

from aocd import data
from collections import defaultdict

starting_pos = None
mmap = []
for i, line in enumerate(data.splitlines()):
    mmap.append(list())
    for j, value in enumerate(line):
        if value == '^':
            starting_pos = i, j, 'UP'
            mmap[-1].append('.')
        else:
            mmap[-1].append(value)
assert starting_pos

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


def print_map():
    for line in mmap:
        print(''.join(line))

ans = 0
for i in range(len(mmap)):
    for j in range(len(mmap[0])):
        # print('i', i)
        if mmap[i][j] == '#':
            continue
        mmap[i][j] = '#'

        pos = starting_pos
        visited = {pos}

        escape = False
        loop = False
        while True:
            # if pos in visited:
            #     loop = True
            #     break

            forward_pos = forward(pos)

            if forward_pos[0] < 0 or forward_pos[1] < 0 or forward_pos[0] >= len(mmap) or forward_pos[1] >= len(mmap[0]):
                escape = True
                break

            if mmap[forward_pos[0]][forward_pos[1]] == '#':
                pos = turn(pos)
                if pos in visited:
                    loop = True
                    break
                visited.add(pos)
            else:
                pos = forward_pos
                if pos in visited:
                    loop = True
                    break
                visited.add(pos)

        if loop:
            mmap[i][j] = 'O'
            ans += 1
        mmap[i][j] = '.'
print(ans)
