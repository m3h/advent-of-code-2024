#!/usr/bin/env python3
from aocd import data
import operator

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

def resolve_value(gate):
    if values[gate] is None:
        lhs, op, rhs = gates[gate]
        values[gate] = {
            'AND': operator.and_,
            'OR': operator.or_,
            'XOR': operator.xor,
        }[op](resolve_value(lhs), resolve_value(rhs))
    return values[gate]

bin_output = ''.join([f'{resolve_value(value)}' for value in sorted(values, reverse=True) if value.startswith('z')])
int_output = int(bin_output, base=2)
print(int_output)
