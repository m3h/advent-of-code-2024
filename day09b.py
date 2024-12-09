#!/usr/bin/env python3
from aocd import data

blocks = []
for i, c in enumerate(data):
    if i%2 == 0:
        blocks += [f'{int(i)//2}'] * int(c)
        idx = blocks[-1]
    else:
        blocks += ['.'] * int(c)

def find_next_idx(idx):
    i = len(blocks)-1
    while blocks[i] != idx:
        i -= 1
    i2 = i
    while blocks[i2] == blocks[i]:
        i2 -= 1
    i2 += 1

    return  i2, i+1

def find_next_blank(s):
    for j in range(s, len(blocks)):
        if blocks[j] == '.':
            j2 = j
            while blocks[j2] == '.':
                j2 += 1
                if j2 >= len(blocks):
                    return -1, -1, -1
            return j, j2, j2-j

def find_first_big_blank(size):
    s = 0
    while True:
        j, j2, found_size = find_next_blank(s)
        if found_size == -1:
            raise ValueError
        if found_size >= size:
            return j, j2
        else:
            s = j2+1

i = len(blocks) - 1
while True:
    i, i2 = find_next_idx(idx)

    try:
        j, j2 = find_first_big_blank(i2-i)
    except ValueError:
        j = float('inf')

    idx = int(idx) - 1
    if idx < 0:
        break
    idx = f'{idx}'
    if j >= i:
        continue

    # if j-j2 < i - i2:
    #     continue

    for ix, jx in zip(range(i, i2), range(j, j2)):
        blocks[ix], blocks[jx] = blocks[jx], blocks[ix]
    
    # blocks[i], blocks[j] = blocks[j], blocks[i]

ans = 0
for i in range(len(blocks)):
    if blocks[i] != '.':
        ans += i * int(blocks[i])
print(ans)