#!/usr/bin/env python3
import re
from collections import defaultdict
from dataclasses import dataclass

from aocd import data

data = data.splitlines()

walls = set()
left_boxes = set()
right_boxes = set()
robot = None

max_i, max_j = -1, -1

def print_map():
    for i in range(max_i+1):
        for j in range(max_j+1):
            b = i, j
            if b == robot:
                print('@', end='')
            elif b in walls:
                print('#', end='')
            elif b in left_boxes:
                print('[', end='')
            elif b in right_boxes:
                print(']', end='')
            else:
                print('.', end='')
        print()
    print('\n\n')

grid_end = None
for i, line in enumerate(data):
    if line == '':
        grid_end = i
        break

    max_i = max(i, max_i)
    for j, c in enumerate(line):
        max_j = max(2*j, max_j)
        if c == '@':
            robot = i, 2*j
        elif c == '#':
            walls.add((i, 2*j))
            walls.add((i, 2*j+1))
        elif c == 'O':
            left_boxes.add((i, 2*j))
            right_boxes.add((i, 2*j+1))
        elif c == '.':
            pass
        else:
            raise Exception()

moves = list()
for line in data[grid_end:]:
    for c in line:
        moves.append(c)

def can_move(block, direction):
    new_block = block[0] + direction[0], block[1] + direction[1]

    block_right = new_block[0], new_block[1]+1
    block_left = new_block[0], new_block[1]-1

    if abs(direction[0]):
        if new_block in walls:
            return False
        elif new_block in left_boxes:
            return can_move(new_block, direction) and can_move(block_right, direction)
        elif new_block in right_boxes:
            return can_move(new_block, direction) and can_move(block_left, direction)
        else:
            return True
    else:
        if new_block in walls:
            return False
        elif new_block in left_boxes or new_block in right_boxes:
            return can_move(new_block, direction)
        else:
            return True

def do_move(block, direction):
    global robot

    if block != robot and block not in left_boxes and block not in right_boxes:
        return
    new_block = block[0] + direction[0], block[1] + direction[1]

    block_right = new_block[0], new_block[1]+1
    block_left = new_block[0], new_block[1]-1

    if abs(direction[0]):
        if new_block in left_boxes:
            do_move(new_block, direction)
            do_move(block_right, direction)
        elif new_block in right_boxes:
            do_move(new_block, direction) 
            do_move(block_left, direction)
    else:
        do_move(new_block, direction)
    
    if block in left_boxes:
        left_boxes.remove(block)
        left_boxes.add(new_block)
    elif block in right_boxes:
        right_boxes.remove(block)
        right_boxes.add(new_block)
    elif block == robot:
        robot = new_block
    else:
        raise Exception()

# print_map()

for move in moves:
    direction = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }[move]

    if can_move(robot, direction):
        do_move(robot, direction)
        # print_map()


ans = 0

for i, j in left_boxes:
    ans += 100 * i + j
print(ans)
