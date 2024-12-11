#!/usr/bin/env python3
from aocd import data

stones = [int(x) for x in data.split()]

for _ in range(25):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone )) % 2 == 0:
            stone_s = str(stone)
            lhs, rhs = stone_s[:len(stone_s)//2], stone_s[len(stone_s)//2:]
            new_stones.append(int(lhs))
            new_stones.append(int(rhs))
        else:
            new_stones.append(stone * 2024)
    stones = new_stones 
print(len(stones))