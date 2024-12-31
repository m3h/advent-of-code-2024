#!/usr/bin/env python3
from aocd import data
import operator
import itertools
import tqdm
import pydot

initialisation_values_data, gates_data = data.split('\n\n')

values = dict()
gates = dict()

for line in gates_data.splitlines():
    lhs, op, rhs, _, out = line.split()
    gates[out] = lhs, op, rhs

    for wire in (lhs, rhs, out):
        values[wire] = None
for line in initialisation_values_data.splitlines():
    wire, value = line.split(': ')
    values[wire] = int(value)
for k in values:
    values[k] = 0

class InfiniteLoopies(Exception):
    ...

def resolve_value(values, gates, gate, visited: set = set()):
    if gate in visited:
        raise InfiniteLoopies()
    
    visited = visited | {gate}

    if values[gate] is None:
        lhs, op, rhs = gates[gate]
        values[gate] = {
            'AND': operator.and_,
            'OR': operator.or_,
            'XOR': operator.xor,
        }[op](resolve_value(values, gates, lhs, visited), resolve_value(values, gates, rhs, visited))
    return values[gate]


def add_edges(nx, values, gates, gate, visited: set = set()):
    if gate in visited:
        raise InfiniteLoopies()
    
    visited = visited | {gate}

    if values[gate] is None:
        lhs, op, rhs = gates[gate]
        values[gate] = {
            'AND': operator.and_,
            'OR': operator.or_,
            'XOR': operator.xor,
        }[op](resolve_value(values, gates, lhs, visited), resolve_value(values, gates, rhs, visited))
    return values[gate]

def plot_graph(filename):
    graph = pydot.Dot('my_graph', graph_type='graph')

    G = nx.Graph()
    for (out, (lhs, op, rhs)) in gates.items():

        op_symbol = {
            'AND': '&',
            'OR': '+',
            'XOR': '^'
        }[op]

        op_node = f'{out}{op_symbol}'
        # G.add_edge(out, op_node)
        G.add_edge(out, lhs)
        G.add_edge(out, rhs)

        graph.add_edge(pydot.Edge(out, op_node))

        graph.add_edge(pydot.Edge(op_node, lhs))
        graph.add_edge(pydot.Edge(op_node, rhs))

    # o = nx.planar_layout(G)
    # import matplotlib.pyplot as plt
    # nx.draw(G, pos=nx.spring_layout(G), with_labels=True)

    graph.write_svg(filename)
    # plt.show()


plot_graph('pre-swaps.svg')

pairs = [
    # ('z33', 'smj'),
    # ('z40', 'cpp')
    ('pfw', 'z39'),
    ('dqr', 'z33'),
    ('dtk', 'vgs'),
    ('z21', 'shh'),
]

for p1, p2 in pairs:
    gates[p1], gates[p2] = gates[p2], gates[p1]

plot_graph('post-swaps.svg')

print(','.join(sorted([p[0] for p in pairs] + [p[1] for p in pairs])))
