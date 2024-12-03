#!/usr/bin/env python3
import re

from aocd import data

state = True
ans = 0

while True:
    next_do = data.find('do()')
    next_dont = data.find('don\'t()')

    if next_do == -1:
        next_do = float('inf')

    if next_dont == -1:
        next_dont = float('inf')
    next_mul_m = [match for match in re.finditer(r'mul\(\d+,\d+\)', data)]
    if len(next_mul_m) == 0:
        next_mul = float('inf')
    else:
        next_mul = next_mul_m[0].start()

    next_pos = min(next_do, next_dont, next_mul)

    if next_do == next_pos:
        state = True
    elif next_dont == next_pos:
        state = False
    elif next_mul == next_pos:
        if state:
            m = next_mul_m[0].group()
            cp = m.find(',')
            n1 = int(m[4:cp])
            n2 = int(m[cp+1:-1])

            ans += n1*n2

    if next_pos > len(data):
        break
    data = data[next_pos+1:]
for m in re.findall(r'mul\(\d+,\d+\)', data):
    cp = m.find(',')
    n1 = int(m[4:cp])
    n2 = int(m[cp+1:-1])

    ans += n1*n2
print(ans)
# print(ans)
# submit(ans)
