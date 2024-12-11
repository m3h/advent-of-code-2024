#!/usr/bin/env python3

from functools import cache
from aocd import data

stones = [int(x) for x in data.split()]

@cache
def count_stone(stone, iterations):
    if iterations == 0:
        return 1
    
    else:
        if stone == 0:
            return count_stone(1, iterations-1)
        elif len(str(stone )) % 2 == 0:
            stone_s = str(stone)
            lhs, rhs = stone_s[:len(stone_s)//2], stone_s[len(stone_s)//2:]
            lhs, rhs = int(lhs), int(rhs)

            return count_stone(lhs, iterations-1) + count_stone(rhs, iterations-1)
        else:
            return count_stone(stone * 2024, iterations-1)

ans = 0
for stone in stones:
    ans += count_stone(stone, iterations=75)
print(ans)