#!/usr/bin/env python3
from aocd import data
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


def plot_graph(filename):
    graph = pydot.Dot('my_graph', graph_type='graph')

    for (out, (lhs, op, rhs)) in gates.items():

        op_symbol = {
            'AND': '&',
            'OR': '+',
            'XOR': '^'
        }[op]

        op_node = f'{out}{op_symbol}'

        graph.add_edge(pydot.Edge(out, op_node))
        graph.add_edge(pydot.Edge(op_node, lhs))
        graph.add_edge(pydot.Edge(op_node, rhs))

    graph.write_svg(filename)


plot_graph('pre-swaps.svg')

# created by manual inspection of 'pre-swaps.svg'
pairs = [
    ('pfw', 'z39'),
    ('dqr', 'z33'),
    ('dtk', 'vgs'),
    ('z21', 'shh'),
]

for p1, p2 in pairs:
    gates[p1], gates[p2] = gates[p2], gates[p1]

# just to verify the chosen pairs
plot_graph('post-swaps.svg')

print(','.join(sorted([p[0] for p in pairs] + [p[1] for p in pairs])))
