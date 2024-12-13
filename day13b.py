#!/usr/bin/env python3
import re

from aocd import data

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

    price_x += 10000000000000
    price_y += 10000000000000

    Px = price_x
    Py = price_y

    Ax = a_x_move
    Ay = a_y_move

    Bx = b_x_move
    By = b_y_move

    a = (Py * Bx - Px * By) // (Ay * Bx - Ax * By)
    b = (Px - Ax * a) // Bx

    if a < 0 or b < 0 or Px != (Ax*a + Bx*b) or Py != (Ay*a + By*b):
        continue

    cost = 3*int(a) + int(b)
    total_tokens += cost
print(total_tokens)