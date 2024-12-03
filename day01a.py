#!/usr/bin/env python3

from aocd import data, submit

data1 = """3   4
4   3
2   5
1   3
3   9
3   3"""

print(data)


l1 = list()
l2 = list()
for line in data.splitlines():
  a,b=line.split()
  l1.append(int(a.strip()))
  l2.append(int(b.strip()))

print(l1)
print(l2)
ssum = 0
while len(l1):
  a = min(l1)
  b = min(l2)

  l1.remove(a)
  l2.remove(b)

  v = abs(b-a)
  ssum += v
  print(a, b, v, ssum)
ans = ssum
print(ans)
# submit(ans)
