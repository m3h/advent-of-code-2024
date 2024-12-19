#!/usr/bin/env python3
import dataclasses
from aocd import data

@dataclasses.dataclass(order=True)
class Node:
    cost: int
    xy: int
    direction: int

    def without_cost(self):
        return dataclasses.replace(self, cost=-1)

    def neighbours(self):

        # clockwise and anticlockwise
        for turn in (1j, -1j):
            yield dataclasses.replace(self, direction=self.direction * turn, cost=self.cost + 1000)

        forward = dataclasses.replace(self, xy=self.xy+self.direction, cost=self.cost + 1)
        if get(forward) != '#':
            yield forward

data = data.splitlines()
mmap = list()
for i, line in enumerate(data):
    mmap.append(list())
    for j, c in enumerate(line):
        if c == 'S':
            c = '.'
            start = Node(cost=0, xy=i+j*1j, direction=1j)

        mmap[-1].append(c)




def get(node: Node):
    return mmap[int(node.xy.real)][int(node.xy.imag)]

def uniform_cost_search(start: Node):

    frontier: list[Node] = [start]
    expanded: list[Node] = list()

    while True:
        if not len(frontier):
            raise Exception("Path not found")

        node = min(frontier, key=lambda node: node.cost)
        frontier.remove(node)

        if get(node) == 'E':
            return node.cost

        expanded.append(node.without_cost())

        for neighbour in node.neighbours():
            try:
                neighbour_in_frontier = [n for n in frontier if n.direction == neighbour.direction and n.xy == neighbour.xy][0]
            except IndexError:
                neighbour_in_frontier = None

            if neighbour.without_cost() not in expanded and not neighbour_in_frontier:
                frontier.append(neighbour)
            elif neighbour_in_frontier and neighbour_in_frontier.cost > neighbour.cost:
                frontier.remove(neighbour_in_frontier)
                frontier.append(neighbour)

print(uniform_cost_search(start=start))
