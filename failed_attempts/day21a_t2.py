#!/usr/bin/env python3
from collections import Counter
import itertools
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

def combinations(move_segments: list[list[str]]) -> list[str]:
    if len(move_segments) == 0:
        return ['']

    combs = []
    for tail in combinations(move_segments[1:]):
        for segment in move_segments[0]:
            combs.append(segment + tail)
    return combs

class Robot:
    def __init__(self, button_visualization: str):
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

    def move_to(self, target_symbol: str) -> str:
        required_moves = ''

        target_x, target_y = self.buttons[target_symbol]

        while self.x != target_x or self.y != target_y:
            if self.x < target_x and (self.x + 1, self.y) in self.buttons.values():
                required_moves += 'v'
                self.x += 1
            elif self.x > target_x and (self.x - 1, self.y) in self.buttons.values():
                required_moves += '^'
                self.x -= 1
            elif self.y < target_y and (self.x, self.y + 1) in self.buttons.values():
                required_moves += '>'
                self.y += 1
            elif self.y > target_y and (self.x, self.y - 1) in self.buttons.values():
                required_moves += '<'
                self.y -= 1
            else:
                assert False, 'no moves found'

        ## sorting ensures that we don't have to move around as much 
        ## return ''.join(sorted(required_moves)) + 'A'
        required_moves += 'A'
        return required_moves

    def moves_for_sequence(self, target_sequence: str) -> str:
        move_segments = [self.move_to(symbol)[:-1] for symbol in target_sequence]
        move_segments = [
            {x + ("A",) for x in itertools.permutations(move_set)}
            for move_set in move_segments
        ]
        move_segments = [[''.join(char for char in word) for word in partition] for partition in move_segments]
        move_segments = combinations(move_segments)
        return move_segments
        move_segments = itertools.product(*move_segments)
        moves = ''.join(move_segments)
        return moves
        return ''.join(self.move_to(symbol) for symbol in target_sequence)

# r = Robot(numpad)
# required_ans= 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A'
# target = '<A^A>^^AvvvA'



# # required_ans = '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'
# # target = 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A'

# my_ans_all = r.moves_for_sequence(target)

# for i, s in enumerate(target):
#     expected = required_ans.split('A')[i] + 'A'

#     # my_ans = r.move_to(s)
#     my_ans = my_ans_all.split('A')[i] + 'A'

#     assert Counter(my_ans) == Counter(expected)


def main(data: str):
    ans = 0
    robots: list[Robot] = [Robot(keypad), Robot(numpad), Robot(numpad)]
    for code in data.splitlines():
        required_sequence = [code]
        for robot in robots:
            
            required_sequence = robot.moves_for_sequence(required_sequence)
        complexity = len(required_sequence) * int(code[:-1])
        print(len(required_sequence), int(code[:-1]))
        ans += complexity
    return ans

print(main(data))

