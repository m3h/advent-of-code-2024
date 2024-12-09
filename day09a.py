#!/usr/bin/env python3
from aocd import data

blocks = []
for i, c in enumerate(data):
    if i%2 == 0:
        blocks += [f'{int(i)//2}'] * int(c)
    else:
        blocks += ['.'] * int(c)

while True:
    for i in range(len(blocks)-1, -1, -1):
        if blocks[i] != '.':
            break
    if i == -1:
        break

    for j in range(len(blocks)):
        if blocks[j] == '.':
            break
    if j > i:
        break
    blocks[i], blocks[j] = blocks[j], blocks[i]

ans = 0
for i in range(len(blocks)):
    if blocks[i] != '.':
        ans += i * int(blocks[i])
print(ans)