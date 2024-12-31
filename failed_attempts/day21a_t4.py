#!/usr/bin/env python3
from collections import Counter
import itertools
import copy
from typing import Self
from aocd import data

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
class Robot:
    def __init__(self, parent: Self | None, button_visualization: str):
        self.parent = parent
        self.buttons = dict()
        self.x = None
        self.y = None

        button_visualization = [line for line in button_visualization.splitlines()]
        for i in range(2, len(button_visualization), 2):
            for j in range(2, len(button_visualization[i]), 4):
                c = button_visualization[i][j]
                if c == ' ':
                    continue

                loc = (i - 2) // 2, (j - 2) // 4
                self.buttons[c] = loc

                if c == 'A':
                    self.x, self.y = loc
        assert self.x is not None
        assert self.y is not None

    def final_moves(self, moves):
        if self.parent is None:
            return moves
        else:
            parent_moves = copy.deepcopy(self.parent).moves_for_sequence(moves)
            return parent_moves

    def moves_cost(self, moves):
        return len(self.final_moves(moves))

    def find_optimal_order(self, moves: str) -> str:
        assert moves[-1] == 'A'

        move_permutations = [''.join(move_permutation) + 'A' for move_permutation in itertools.permutations(moves[:-1])]
        move_permutations = set(move_permutations)
        move_permutations = [x for x in move_permutations if self.moves_are_valid(x)]
        optimal_move = min(move_permutations, key=self.moves_cost)
        return optimal_move
    
    def moves_are_valid(self, moves):
        x, y = self.x, self.y
        for m in moves[:-1]:
            if m == 'v':
                x += 1
            elif m == '^':
                x -= 1
            elif m == '>':
                y += 1
            elif m == '<':
                y -= 1
            else:
                raise Exception()
            
            if (x, y) not in self.buttons.values():
                return False
        assert moves[-1] == 'A'
        return True

    def move_to(self, target_symbol: str) -> str:
        required_moves = ''

        target_x, target_y = self.buttons[target_symbol]

        x, y = self.x, self.y
        while x != target_x or y != target_y:
            if x < target_x and (x + 1, y) in self.buttons.values():
                required_moves += 'v'
                x += 1
            elif x > target_x and (x - 1, y) in self.buttons.values():
                required_moves += '^'
                x -= 1
            elif y < target_y and (x, y + 1) in self.buttons.values():
                required_moves += '>'
                y += 1
            elif y > target_y and (x, y - 1) in self.buttons.values():
                required_moves += '<'
                y -= 1
            else:
                assert False, 'no moves found'

        required_moves += 'A'
        optimal_moves = self.find_optimal_order(required_moves)
        self.x, self.y = x, y
        return optimal_moves
    
    def moves_for_sequence(self, target_sequence: str) -> str:
        return ''.join(self.move_to(symbol) for symbol in target_sequence)

def main(data: str):
    ans = 0
    robots: list[Robot] = []
    robots.insert(0, Robot(None, numpad))
    robots.insert(0, Robot(robots[0], numpad))
    robots.insert(0, Robot(robots[0], keypad))

    for code in data.splitlines():
        required_sequence = code
        for robot in robots:
            required_sequence = robot.moves_for_sequence(required_sequence)
        complexity = len(required_sequence) * int(code[:-1])
        print(len(required_sequence), int(code[:-1]))
        ans += complexity
    return ans

print(main(data))

