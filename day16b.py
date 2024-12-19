#!/usr/bin/env python3
from collections import defaultdict
import dataclasses
from aocd import data

@dataclasses.dataclass(order=True, unsafe_hash=True)
class Node:
    xy: int
    direction: int

    def neighbours(self):

        # clockwise and anticlockwise
        for turn in (1j, -1j):
            yield 1000, dataclasses.replace(self, direction=self.direction * turn)

        forward = dataclasses.replace(self, xy=self.xy+self.direction)
        if get(forward) != '#':
            yield 1, forward

data = data.splitlines()
mmap = list()
for i, line in enumerate(data):
    mmap.append(list())
    for j, c in enumerate(line):
        if c == 'S':
            c = '.'
            start = Node(xy=i+j*1j, direction=1j)
        elif c == 'E':
            c = '.'
            end_xy = 1+j*1j

        mmap[-1].append(c)




def get(node: Node):
    return mmap[int(node.xy.real)][int(node.xy.imag)]

def djikstra(source: Node):

    dist: dict[Node, int] = dict()
    prev: dict[Node, set[Node]] = dict()
    for i in range(len(mmap)):
        for j in range(len(mmap)):
            if mmap[i][j] != '#':
                direction = 1
                for _ in range(4):
                    direction *= 1j
                    v=Node(xy=i+j*1j, direction=direction)
                    dist[v] = float('inf')
                    prev[v] = None

    Q: list[Node] = [source]
    dist[source] = 0

    while len(Q):
        u: Node = min(Q, key=dist.get)
        Q.remove(u)

        for edge, v in u.neighbours():
            alt = dist[u] + edge
            if alt == dist[v]:
                prev[v].add(u)
            elif alt < dist[v]:
                dist[v] = alt
                prev[v] = {u}

                Q.append(v)
    return dist, prev


dist, prev = djikstra(source=start)

ends = defaultdict(set)
possible_end = Node(xy=end_xy, direction=1)
for turn in range(4):
    possible_end.direction *= 1j

    total_cost = dist[possible_end]
    ends[total_cost].add(possible_end)

minimum_cost = min(ends)
ends = ends[min(ends)]

locs_in_paths = set()
nodes_to_add = ends

while nodes_to_add:
    n = nodes_to_add.pop()
    if n != start:
        for p in prev[n]:
            nodes_to_add.add(p)
    locs_in_paths.add(n.xy)

print(len(locs_in_paths))
