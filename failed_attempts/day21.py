from enum import Enum, auto

direction_keypad = [[f'{1+i+3*j}' for i in range(3)] for j in range(3)][::-1] + [[None, '0', 'A']]

directional_keypad = [
    [None, -1, 'A'],
    [-1j, 1, 1j],
]

def sequence_to_moves(sequence, start_key, )
print(direction_keypad)