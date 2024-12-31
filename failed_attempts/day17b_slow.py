#!/usr/bin/env python3
import dataclasses
from aocd import data
from fractions import Fraction

register_initialization, program = data.split("\n\n")

register_init = [0,0,0]
for i, line in enumerate(register_initialization.splitlines()):
    value = int(line.split()[2])

    register_init[i] = value

program = program.split()[-1]
machine_code = [int(x) for x in program.split(',')]

def get_combo(operand, registers):
    if 0 <= operand <= 3:
        return operand
    elif 4 <= operand <= 6:
        return registers[operand-4]
    elif operand >= 7:
        raise Exception("Invalid operand")

def run(register_init):
    registers = list(register_init)
    IP = 0

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

i = 0
while True:
    print(i)
    register_init_i = list(register_init)
    register_init_i[0] = i
    output = run(register_init_i)
    if output == machine_code:
        print(i)
        exit()
    
    i += 1