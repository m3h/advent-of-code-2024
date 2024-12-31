#!/usr/bin/env python3
from aocd import data
import operator
import itertools
import tqdm

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

class InfiniteLoopies(Exception):
    pass
def resolve_value(gate, gates, values, visited):
    if gate[0] not in {'x', 'y'}:
        visited = visited | {gate}
        touched_outputs = {gate}
        lhs, op, rhs = gates[gate]

        if lhs in visited or rhs in visited:
            raise InfiniteLoopies()

        lhs_value, lhs_touched_outputs = resolve_value(lhs, gates, values, visited)
        rhs_value, rhs_touched_outputs = resolve_value(rhs, gates, values, visited)

        touched_outputs |= lhs_touched_outputs
        touched_outputs |= rhs_touched_outputs

        return {
            'AND': operator.and_,
            'OR': operator.or_,
            'XOR': operator.xor,
        }[op](lhs_value, rhs_value), touched_outputs
    return values[gate], set()

def test_gate(z_gate_num, values, max_z_gate, gates):
    possibly_failing_outputs = set()


    z_gate_num_padded = f'{z_gate_num}'.zfill(2)
    z_gate_num_p1_padded = f'{z_gate_num+1}'.zfill(2)
    test_values = dict(values)


    for x, y in ((0,0), (0,1), (1,0), (1,1)):
        test_values[f'x{z_gate_num_padded}'] = x
        test_values[f'y{z_gate_num_padded}'] = y

        resolved_value, outputs = resolve_value(f'z{z_gate_num_padded}', gates, test_values, set())
        if resolved_value != x ^ y:
            possibly_failing_outputs |= outputs


        if z_gate_num == max_z_gate:
            continue
        else:
            resolved_value, outputs = resolve_value(f'z{z_gate_num_p1_padded}', gates, test_values, set())
            if resolved_value != x & y:
                possibly_failing_outputs |= outputs
    return possibly_failing_outputs

def find_possible_fix(z_gate_num, values, max_z_gate, gates):
    touched_outputs = test_gate(z_gate_num, values, max_z_gate, gates)

    if len(touched_outputs) == 0:
        return set()

    possible_fixes = list()
    for pair_count in range(1, 1+1): 
        for swaps in itertools.combinations(gates,r=pair_count*2):
            swapped_gates = dict(gates)
            pairs = set()
            for i in range(0, len(swaps), 2):
                p1, p2 = swaps[i], swaps[i+1]
                pairs.add(tuple(sorted((p1, p2))))
                swapped_gates[p1], swapped_gates[p2] = swapped_gates[p2], swapped_gates[p1]

            try: 
                is_adder = test_gate(z_gate_num, values, max_z_gate, swapped_gates)
                if len(is_adder) == 0:
                    possible_fixes.append(tuple(sorted((p1, p2))))
            except InfiniteLoopies:
                pass
    return possible_fixes


for k in values:
    values[k] = 0

max_z = max([int(v.removeprefix('z')) for v in values if v.startswith('z')])

for z in range(max_z+1):
    r = test_gate(z, set(), max_z, gates)
    print(r)

# swaps = set()
# for z in range(max_z+1):
#     o = find_possible_fix(z, values, max_z, gates)
#     for swap in o:
#         swaps.add(swap)
#     print(z, o)

swaps = {('sjk', 'z21'), ('ssw', 'z21'), ('z21', 'z22'), ('shh', 'z21'), ('vcj', 'z21'),
('shh', 'z21'),
('dtk', 'z26'), ('dtk', 'vgs'), ('qcr', 'z26'), ('z26', 'z27'),
('fdv', 'z34'), ('mtw', 'z34'), ('z33', 'z34'), ('fdv', 'vkp'), ('dqr', 'fdv'), ('fdv', 'pdf'), ('mtw', 'vkp'), ('vkp', 'z33'), ('dqr', 'mtw'), ('mtw', 'pdf'), ('dqr', 'z33'), ('pdf', 'z33'),
('mtw', 'z34'), ('z33', 'z34'), ('jqp', 'mtw'), ('dqr', 'mtw'), ('dqr', 'z33'),
('z39', 'z40'), ('sjq', 'z39'), ('pfw', 'z39'), ('nmt', 'z39'), ('jqk', 'z39'),
('z39', 'z40'), ('pfw', 'z39'), ('jqk', 'z39'), ('gqn', 'z39'),
}

maxl = 0
for i, swap_subset in enumerate(tqdm.tqdm(itertools.combinations(swaps, r=4))):

    l = len({s[0] for s in swap_subset} | {s[1] for s in swap_subset})
    if l > maxl:
        maxl = l
    if len({s[0] for s in swap_subset} | {s[1] for s in swap_subset}) != 8:
        continue
    swapped_gates = dict(gates)
    for swap in swap_subset:
        swapped_gates[swap[0]], swapped_gates[swap[1]] = swapped_gates[swap[1]], swapped_gates[swap[0]]

    try:
        print()
        print(swap_subset)
        fixed = True
        broken_things = 0
        for z in range(max_z+1):
            z_r = test_gate(z, values, max_z, swapped_gates)
            if z_r:
                broken_things += 1
                print(z)
                fixed = False
        if fixed:
            print("found solution")
        if not any(test_gate(z, values, max_z, swapped_gates) for z in range(max_z+1)):
            print("solution", swap_subset)
            break
    except InfiniteLoopies:
        print("infinite loops")
        pass

possibly_faulty_gates = list({s[0] for s in swaps} | {s[1] for s in swaps})

def get_pairs(items):
    for i in range(0, len(items)):
        for j in range(i+1, len(items)):
            for k in range(j+1, len(items)):
                for l in range(k+1, len(items)):
                    for m in range(l+1, len(items)):
                        for n in range(m+1, len(items)):
                            for o in range(n+1, len(items)):
                                for p in range(o+1, len(items)):
                                    yield ((items[i], items[j]), (items[k], items[l]), (items[m], items[n]), (items[o], items[p]))
#     for a_idx, a in enumerate(items):
#         for b in items[a_idx:]:
#             yield a, b

# possible_pairs = list(get_pairs(possibly_faulty_gates))

for pairs in get_pairs(possibly_faulty_gates):
    if len({pair[0] for pair in pairs} | {pair[1] for pair in pairs}) != 8:
        continue

    swapped_gates = dict(gates)
    for swap in pairs:
        swapped_gates[swap[0]], swapped_gates[swap[1]] = swapped_gates[swap[1]], swapped_gates[swap[0]]

    try:
        if not any(test_gate(z, values, max_z, swapped_gates) for z in range(max_z+1)):
            print("solution", pairs)
    except InfiniteLoopies:
        pass
