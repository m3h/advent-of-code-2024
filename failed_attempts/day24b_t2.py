#!/usr/bin/env python3
from aocd import data
import operator
import itertools
import tqdm
import networkx

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

def test_gate(values, gates, z_num, max_z):


    for x, y, c_in in itertools.product((1,0), repeat=3):
        for k in values:
            if k[0] in {'x', 'y'}:
                values[k] = 0
            else:
                values[k] = None

        if z_num == 0:
            c_in = 0
        elif z_num == max_z:
            x = 0
            y = 0

        values[f"x{z_num-1:02}"] = c_in
        values[f"x{z_num:02}"] = x
        values[f"y{z_num:02}"] = y

        try:
            if resolve_value(values, gates, f'z{z_num:02}') != x ^ y ^ c_in:
                return False
        except InfiniteLoopies:
            return False
    return True

def all_pairs(items):
    items = list(items)
    for a_idx, a in enumerate(items):
        for b in items[a_idx+1:]:
            yield a, b

def count_faulty_gates(values, gates, max_z):
    gates_working = [test_gate(values, gates, z, max_z) for z in range(max_z+1)]
    return sum(not gate for gate in gates_working)

def main():
    max_z = max([int(v.removeprefix('z')) for v in values if v.startswith('z')])

    num_faulty_gates = count_faulty_gates(values, gates, max_z)

    all_pairs_l = list(all_pairs(gates))

    good_looking_pair = set()

    all_pairs_l = []
    for p1, p2 in tqdm.tqdm(all_pairs_l):
        gates[p1], gates[p2] = gates[p2], gates[p1]

        new_num_faulty_gates = count_faulty_gates(values, gates, max_z)

        if new_num_faulty_gates < num_faulty_gates:
            good_looking_pair.add((p1, p2))

        gates[p1], gates[p2] = gates[p2], gates[p1]

    print(good_looking_pair)

    good_looking_pair = {('z05', 'pnn'), ('z05', 'ttr'), ('z05', 'ntm'), ('pnn', 'chf'), ('ddt', 'rqv'), ('ddt', 'z16'), ('ttr', 'chf'), ('z06', 'nff'), ('z06', 'qjc'), ('z06', 'cph'), ('sqn', 'z14'), ('sqn', 'fsg'), ('z09', 'dvh'), ('z09', 'sdg'), ('z09', 'trv'), ('vvg', 'tfq'), ('vvg', 'sjr'), ('vvg', 'jrk'), ('mwb', 'dvh'), ('mwb', 'sdg'), ('mwb', 'trv'), ('scf', 'z19'), ('scf', 'ntj'), ('gqt', 'rqv'), ('gqt', 'z16'), ('dqf', 'z41'), ('dqf', 'wjd'), ('fpb', 'fqd'), ('fpb', 'pnh'), ('fpb', 'nkq'), ('thj', 'ngq'), ('thj', 'hqj'), ('thj', 'qgg'), ('qhc', 'bmw'), ('qhc', 'z12'), ('tfq', 'z42'), ('ngq', 'z11'), ('tqd', 'z30'), ('tqd', 'kbg'), ('dgg', 'gqk'), ('dgg', 'dvs'), ('dgg', 'dct'), ('rgb', 'z02'), ('rgb', 'srh'), ('chh', 'fmd'), ('chh', 'z15'), ('jvk', 'bhc'), ('jvk', 'z35'), ('kdv', 'hrm'), ('kdv', 'z18'), ('pht', 'fmd'), ('pht', 'z15'), ('kbm', 'hhg'), ('kbm', 'z44'), ('nff', 'kvq'), ('z28', 'qhb'), ('z28', 'tsf'), ('z28', 'kjs'), ('qjc', 'kvq'), ('kfg', 'z30'), ('kfg', 'kbg'), ('jwp', 'bmw'), ('jwp', 'z12'), ('hqj', 'z11'), ('z30', 'ccb'), ('mvv', 'z24'), ('mvv', 'pww'), ('qgg', 'z11'), ('cpq', 'jww'), ('cpq', 'z23'), ('qhb', 'bdw'), ('ggg', 'z04'), ('ggg', 'wfj'), ('z02', 'gkk'), ('z02', 'kkk'), ('gvv', 'qtr'), ('gvv', 'z43'), ('gkk', 'srh'), ('smj', 'bhc'), ('smj', 'z35'), ('z24', 'dcj'), ('z24', 'chn'), ('ccb', 'kbg'), ('vcp', 'z19'), ('vcp', 'ntj'), ('ngs', 'pvt'), ('ngs', 'z03'), ('tjr', 'z29'), ('tjr', 'kpk'), ('hsk', 'hrm'), ('hsk', 'z18'), ('hhg', 'spc'), ('hhg', 'z45'), ('wjp', 'bdf'), ('wjp', 'fgd'), ('wjp', 'kkg'), ('cph', 'kvq'), ('bhc', 'drq'), ('pvj', 'z41'), ('pvj', 'wjd'), ('dvc', 'bmw'), ('dvc', 'z12'), ('z14', 'ftk'), ('z14', 'kjf'), ('pww', 'dcj'), ('pww', 'chn'), ('mqf', 'fmd'), ('mqf', 'z15'), ('drq', 'z35'), ('bdf', 'z10'), ('ddk', 'tww'), ('ddk', 'z36'), ('kwq', 'hrm'), ('kwq', 'z18'), ('kff', 'jww'), ('kff', 'z23'), ('pwn', 'pvt'), ('pwn', 'z03'), ('z44', 'spc'), ('z44', 'z45'), ('z19', 'wtw'), ('jww', 'pvw'), ('ftk', 'fsg'), ('vcn', 'ndb'), ('vcn', 'gbh'), ('vcn', 'pqk'), ('ghw', 'z29'), ('ghw', 'kpk'), ('z08', 'sbr'), ('z08', 'vdk'), ('z08', 'cdm'), ('pvw', 'z23'), ('vft', 'nhg'), ('vft', 'z17'), ('z01', 'ndb'), ('z01', 'gbh'), ('z01', 'pqk'), ('wsw', 'z41'), ('wsw', 'wjd'), ('fsg', 'kjf'), ('rgp', 'kdm'), ('rgp', 'z13'), ('fdh', 'kdm'), ('fdh', 'z13'), ('kkk', 'srh'), ('pvt', 'vfk'), ('gqk', 'z07'), ('dvs', 'z07'), ('ckb', 'hkv'), ('ckb', 'z31'), ('hkv', 'dwf'), ('hkv', 'sqr'), ('fjk', 'nhg'), ('fjk', 'z17'), ('ntj', 'wtw'), ('z37', 'fqd'), ('z37', 'pnh'), ('z37', 'nkq'), ('rqv', 'nqp'), ('nhg', 'jhc'), ('mvq', 'z04'), ('mvq', 'wfj'), ('z16', 'nqp'), ('sbn', 'tww'), ('sbn', 'z36'), ('hhp', 'qtr'), ('hhp', 'z43'), ('tww', 'dds'), ('dwf', 'z31'), ('z04', 'pdr'), ('tsf', 'bdw'), ('kdm', 'crm'), ('qtr', 'bns'), ('dct', 'z07'), ('fgd', 'z10'), ('wfj', 'pdr'), ('z17', 'jhc'), ('z13', 'crm'), ('sqr', 'z31'), ('sjr', 'z42'), ('bns', 'z43'), ('kjs', 'bdw'), ('kkg', 'z10'), ('z36', 'dds'), ('chf', 'ntm'), ('sbr', 'hsg'), ('vdk', 'hsg'), ('z42', 'jrk'), ('z29', 'tcv'), ('kpk', 'tcv'), ('vfk', 'z03'), ('cdm', 'hsg')}

    good_looking_pair = list(good_looking_pair)
    good_looking_pair = [('z05', 'pnn'), ('z05', 'ttr'), ('z05', 'ntm'), ('pnn', 'chf'), ('ddt', 'rqv'), ('ddt', 'z16'), ('ttr', 'chf'), ('z06', 'nff'), ('z06', 'qjc'), ('z06', 'cph'), ('sqn', 'z14'), ('sqn', 'fsg'), ('z09', 'dvh'), ('z09', 'sdg'), ('z09', 'trv'), ('vvg', 'tfq'), ('vvg', 'sjr'), ('vvg', 'jrk'), ('mwb', 'dvh'), ('mwb', 'sdg'), ('mwb', 'trv'), ('scf', 'z19'), ('scf', 'ntj'), ('gqt', 'rqv'), ('gqt', 'z16'), ('dqf', 'z41'), ('dqf', 'wjd'), ('fpb', 'fqd'), ('fpb', 'pnh'), ('fpb', 'nkq'), ('thj', 'ngq'), ('thj', 'hqj'), ('thj', 'qgg'), ('qhc', 'bmw'), ('qhc', 'z12'), ('tfq', 'z42'), ('ngq', 'z11'), ('tqd', 'z30'), ('tqd', 'kbg'), ('dgg', 'gqk'), ('dgg', 'dvs'), ('dgg', 'dct'), ('rgb', 'z02'), ('rgb', 'srh'), ('chh', 'fmd'), ('chh', 'z15'), ('jvk', 'bhc'), ('jvk', 'z35'), ('kdv', 'hrm'), ('kdv', 'z18'), ('pht', 'fmd'), ('pht', 'z15'), ('kbm', 'hhg'), ('kbm', 'z44'), ('nff', 'kvq'), ('z28', 'qhb'), ('z28', 'tsf'), ('z28', 'kjs'), ('qjc', 'kvq'), ('kfg', 'z30'), ('kfg', 'kbg'), ('jwp', 'bmw'), ('jwp', 'z12'), ('hqj', 'z11'), ('z30', 'ccb'), ('mvv', 'z24'), ('mvv', 'pww'), ('qgg', 'z11'), ('cpq', 'jww'), ('cpq', 'z23'), ('qhb', 'bdw'), ('ggg', 'z04'), ('ggg', 'wfj'), ('z02', 'gkk'), ('z02', 'kkk'), ('gvv', 'qtr'), ('gvv', 'z43'), ('gkk', 'srh'), ('smj', 'bhc'), ('smj', 'z35'), ('z24', 'dcj'), ('z24', 'chn'), ('ccb', 'kbg'), ('vcp', 'z19'), ('vcp', 'ntj'), ('ngs', 'pvt'), ('ngs', 'z03'), ('tjr', 'z29'), ('tjr', 'kpk'), ('hsk', 'hrm'), ('hsk', 'z18'), ('hhg', 'spc'), ('hhg', 'z45'), ('wjp', 'bdf'), ('wjp', 'fgd'), ('wjp', 'kkg'), ('cph', 'kvq'), ('bhc', 'drq'), ('pvj', 'z41'), ('pvj', 'wjd'), ('dvc', 'bmw'), ('dvc', 'z12'), ('z14', 'ftk'), ('z14', 'kjf'), ('pww', 'dcj'), ('pww', 'chn'), ('mqf', 'fmd'), ('mqf', 'z15'), ('drq', 'z35'), ('bdf', 'z10'), ('ddk', 'tww'), ('ddk', 'z36'), ('kwq', 'hrm'), ('kwq', 'z18'), ('kff', 'jww'), ('kff', 'z23'), ('pwn', 'pvt'), ('pwn', 'z03'), ('z44', 'spc'), ('z44', 'z45'), ('z19', 'wtw'), ('jww', 'pvw'), ('ftk', 'fsg'), ('vcn', 'ndb'), ('vcn', 'gbh'), ('vcn', 'pqk'), ('ghw', 'z29'), ('ghw', 'kpk'), ('z08', 'sbr'), ('z08', 'vdk'), ('z08', 'cdm'), ('pvw', 'z23'), ('vft', 'nhg'), ('vft', 'z17'), ('z01', 'ndb'), ('z01', 'gbh'), ('z01', 'pqk'), ('wsw', 'z41'), ('wsw', 'wjd'), ('fsg', 'kjf'), ('rgp', 'kdm'), ('rgp', 'z13'), ('fdh', 'kdm'), ('fdh', 'z13'), ('kkk', 'srh'), ('pvt', 'vfk'), ('gqk', 'z07'), ('dvs', 'z07'), ('ckb', 'hkv'), ('ckb', 'z31'), ('hkv', 'dwf'), ('hkv', 'sqr'), ('fjk', 'nhg'), ('fjk', 'z17'), ('ntj', 'wtw'), ('z37', 'fqd'), ('z37', 'pnh'), ('z37', 'nkq'), ('rqv', 'nqp'), ('nhg', 'jhc'), ('mvq', 'z04'), ('mvq', 'wfj'), ('z16', 'nqp'), ('sbn', 'tww'), ('sbn', 'z36'), ('hhp', 'qtr'), ('hhp', 'z43'), ('tww', 'dds'), ('dwf', 'z31'), ('z04', 'pdr'), ('tsf', 'bdw'), ('kdm', 'crm'), ('qtr', 'bns'), ('dct', 'z07'), ('fgd', 'z10'), ('wfj', 'pdr'), ('z17', 'jhc'), ('z13', 'crm'), ('sqr', 'z31'), ('sjr', 'z42'), ('bns', 'z43'), ('kjs', 'bdw'), ('kkg', 'z10'), ('z36', 'dds'), ('chf', 'ntm'), ('sbr', 'hsg'), ('vdk', 'hsg'), ('z42', 'jrk'), ('z29', 'tcv'), ('kpk', 'tcv'), ('vfk', 'z03'), ('cdm', 'hsg')]
    for i in tqdm.tqdm(range(len(good_looking_pair))):
        p11, p12 = good_looking_pair[i]
        for j in tqdm.tqdm(range(i+1, len(good_looking_pair))):
            p21, p22 = good_looking_pair[j]
            if len({p11, p12, p21, p22}) != 4:
                continue
            for k in tqdm.tqdm(range(j+1, len(good_looking_pair))):
                p31, p32 = good_looking_pair[k]
                if len({p11, p12, p21, p22, p31, p32}) != 6:
                    continue
                for l in range(k+1, len(good_looking_pair)):
                    p41, p42 = good_looking_pair[l]
                    if len({p11, p12, p21, p22, p31, p32, p41, p42}) != 8:
                        continue
                    
                    pairs = ((p11, p12), (p21, p22), (p31, p32), (p41, p42))

                    for p1, p2 in pairs:
                        gates[p1], gates[p2] = gates[p2], gates[p1]
                    
                    if count_faulty_gates(values, gates, max_z) == 0:
                        return pairs

                    for p1, p2 in pairs:
                        gates[p1], gates[p2] = gates[p2], gates[p1]

    for pairs in tqdm.tqdm(itertools.combinations(good_looking_pair, r=4)):
        if len({p1 for p1, p2 in pairs} | {p2 for p1, p2 in pairs}) != 8:
            continue
        for p1, p2 in pairs:
            gates[p1], gates[p2] = gates[p2], gates[p1]
        
        if count_faulty_gates(values, gates, max_z) == 0:
            return pairs

        for p1, p2 in pairs:
            gates[p1], gates[p2] = gates[p2], gates[p1]


main()