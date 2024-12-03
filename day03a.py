#!/usr/bin/env python3
import re

from aocd import data

ans = 0
for m in re.findall(r'mul\(\d+,\d+\)', data):
    cp = m.find(',')
    n1 = int(m[4:cp])
    n2 = int(m[cp+1:-1])

    ans += n1*n2
print(ans)
# print(ans)
# submit(ans)
