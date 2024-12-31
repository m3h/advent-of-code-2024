#!/usr/bin/env python3
from aocd import data
import itertools
from typing import Iterable

keypad = """
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

numpad = """
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""

def visualisation_to_mapping(visualisation):
    return {
        c: (i, j) for (i, line) in enumerate(visualisation.splitlines()[2::2]) for (j, c) in enumerate(line[2::4]) if c != ' '
    }

keypad_buttons = visualisation_to_mapping(keypad)
numpad_buttons = visualisation_to_mapping(numpad)

def test_moves_are_valid(location: tuple[int, int], moves: list[str], buttons: dict[str, tuple[int, int]]) -> bool:
    x, y = location
    for move in moves[:-1]:
        if move == 'v':
            x += 1
        elif move == '^':
            x -= 1
        elif move == '<':
            y -= 1
        elif move == '>':
            y += 1
        else:
            raise Exception("Invalid move", move)

        if (x, y) not in buttons.values():
            return False

    assert moves[-1] == 'A'
    return True

def required_presses(required_sequence: Iterable[str], levels: int, level: int = 0):
    if level == 3:
        return required_sequence 

    if level == 0:
        buttons = keypad_buttons
    else:
        buttons = numpad_buttons

    current_location = buttons['A']

    combined_presses = []
    for required_button in required_sequence:
        target_x, target_y = buttons[required_button]

        x, y = current_location
        required_moves = []
        while x < target_x:
            required_moves.append('v')
            x += 1
        while x > target_x:
            required_moves.append('^')
            x -= 1
        while y < target_y:
            required_moves.append('>')
            y += 1
        while y > target_y:
            required_moves.append('<')
            y -= 1

        permutations_of_moves = frozenset(itertools.permutations(required_moves))
        permutations_of_moves = [moves + ('A',) for moves in permutations_of_moves]
        permutations_of_moves = [moves for moves in permutations_of_moves if test_moves_are_valid(current_location, moves, buttons)]

        permutations_of_moves = [(required_presses(moves, levels, level+1), moves) for moves in permutations_of_moves]
        permutations_of_moves.sort(key=lambda x: len(x[0]))

        optimal_moves = permutations_of_moves[0][0]

        combined_presses += optimal_moves

        current_location = x, y

    return combined_presses

def main():
    ans = 0
    for code in data.splitlines():
        numeric_code = int(code[:-1])
        resolved_sequence = required_presses(code, levels=3)
        ans += len(resolved_sequence) * numeric_code

    print(ans)
if __name__ == '__main__':
    main()
