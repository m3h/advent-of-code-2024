#!/usr/bin/env python3
import re
from collections import defaultdict
from dataclasses import dataclass

from aocd import data

@dataclass(unsafe_hash=True)
class Node:
    x: int
    y: int
    tokens: int
    steps: int

def neighbours(n: Node) -> list[Node]:
    return [Node(
        x=n.x + a_x_move,
        y=n.y + a_y_move,
        tokens=n.tokens + 3,
        steps=n.steps+1,
    ) ,
    Node(
        x=n.x + b_x_move,
        y=n.y + b_y_move,
        tokens=n.tokens + 1,
        steps=n.steps+1,
    )]

def s_star(goal):
    def h(n):
        return ((goal.x - n.x) ** 2 + (goal.y - n.y) ** 2)**.5
    start = Node(0, 0, 0, 0)
    openSet = {start}

    gScore = defaultdict(lambda: float('inf'))
    gScore[start.x, start.y] = 0

    fScore = defaultdict(lambda: float('inf'))
    fScore[start.x, start.y] = h(start)

    while len(openSet):
        current_fscore = float('inf')
        current = None
        for n in openSet:
            if fScore[n.x, n.y] < current_fscore:
                current_fscore = fScore[n.x, n.y]
                current = n

        if current.x == goal.x and current.y == goal.y:
            return current.tokens

        openSet.remove(current)

        for neighbour in neighbours(current):
            if neighbour.steps > 200:
                continue
            tentative_gScore = neighbour.tokens
            if tentative_gScore < gScore[neighbour.x, neighbour.y]:
                gScore[neighbour.x, neighbour.y] = tentative_gScore
                fScore[neighbour.x, neighbour.y] = tentative_gScore + h(neighbour)
                if neighbour not in openSet:
                    openSet.add(neighbour)
    return None

total_tokens = 0
machinest = []
lines = data.splitlines()
for i in range(0, len(lines), 4):
    a_x_move, a_y_move = re.match(r'.*X\+(\d+), Y\+(\d+)', lines[i]).groups()
    b_x_move, b_y_move = re.match(r'.*X\+(\d+), Y\+(\d+)', lines[i+1]).groups()
    price_x, price_y= re.match(r'.*X=(\d+), Y=(\d+)', lines[i+2]).groups()

    a_x_move = int(a_x_move)
    a_y_move = int(a_y_move)
    b_x_move = int(b_x_move)
    b_y_move = int(b_y_move)
    price_x = int(price_x)
    price_y = int(price_y)

    tokens = s_star(Node(x=price_x, y=price_y, tokens=None, steps=None))

    if tokens is not None:
        total_tokens += tokens
print(total_tokens)