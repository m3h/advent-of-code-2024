#!/usr/bin/env python3
import dataclasses
from aocd import data

"""
2,4
B = A & 0b111

1,2
B = (A & 0b111) ^ 0b010
B = A2.~A1.A0

7,5
C = A / 2 ** B
  = A >> A2.~A1.A0

1,3
B = A2.~A1.A0 ^ 0b011
  = A2.A1.~A0

4,3
B = A2.A1.~A0 ^ (A >> A2.~A1.A0)
`

5,5
OUTPUT A2.A1.~A0 ^ (A >> A2.~A1.A0)

0,3
A = A >> 3

3,0
GOTO 0 if A

"""

register_initialization, program = data.split("\n\n")

registers_init = [0,0,0]
for i, line in enumerate(register_initialization.splitlines()):
    value = int(line.split()[2])

    registers_init[i] = value

program = program.split()[-1]
machine_code = [int(x) for x in program.split(',')]

def get_combo(operand, registers):
    if 0 <= operand <= 3:
        return operand
    elif 4 <= operand <= 6:
        return registers[operand-4]
    elif operand >= 7:
        raise Exception("Invalid operand")

def run(a_init, machine_code, IP):

    registers = list(registers_init)
    registers[0] = a_init
    output = []
    while IP < len(machine_code) - 1:
        opcode, operand = machine_code[IP:IP+2]
        IP += 2

        if opcode == 0:
            # adv
            numerator = registers[0]
            denominator = 2** get_combo(operand, registers)
            registers[0] = int(numerator / denominator)
        elif opcode == 1:
            # bxl
            registers[1] ^= operand
        elif opcode == 2:
            # bst
            registers[1] = get_combo(operand, registers) % 8
        elif opcode == 3:
            # jnz
            if registers[0]:
                IP = operand
        elif opcode == 4:
            # bxc
            registers[1] ^= registers[2]
        elif opcode == 5:
            # out
            output.append(get_combo(operand, registers)%8)
        elif opcode == 6:
            # bdv
            numerator = registers[0]
            denominator = 2** get_combo(operand, registers)
            registers[1] = int(numerator / denominator)
        elif opcode == 7:
            # cdv
            numerator = registers[0]
            denominator = 2** get_combo(operand, registers)
            registers[2] = int(numerator / denominator)
    return output

a = 0

for machine_code_segment_len in range(1, len(machine_code)+1):
    machine_code_segment = machine_code[-machine_code_segment_len:]
    a = a << 3

    found = False
    an = a
    while True:

        run_result = run(an, machine_code, 0)
        if run_result == machine_code_segment:
            a = an
            break
        else:
            an += 1

print(a)
