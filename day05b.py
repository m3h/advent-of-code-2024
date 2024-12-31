#!/usr/bin/env python3
import re

from aocd import data
from collections import defaultdict

rules = defaultdict(list)
d = []
data = data.splitlines()

i = 0
while i < len(data):
    line = data[i]
    if line == "":
        break
    a,b = line.split("|")
    rules[int(a)].append(int(b))

    i += 1

i += 1
updates = list()
while i < len(data):
    line = data[i]

    update_s = [int(x) for x in line.split(",")]

    updates.append(update_s)
    i += 1

def check_update(update):
    for i in range(len(update)):
        for j in range(i+1, len(update)):
            a, b= update[i], update[j]

            if b not in rules[a]:
                return False
    return True


# start_point = None
# for values in rules.values():
#     for value in values:
#         if value not in rules:
#             assert start_point is None
#             start_point = value

order = []

def reorder(update):
    for i in range(len(update)):
        for j in range(i+1, len(update)):
            a, b= update[i], update[j]

            if b not in rules[a]:
                update[i] = b
                update[j] = a
                return reorder(update)
    return True

    
ssum = 0
for update in updates:
    if check_update(update):
        pass
    else:
        reorder(update)
        ssum += update[len(update)//2]
print(ssum)

# print(ans)
# print(ans)
# submit(ans)
