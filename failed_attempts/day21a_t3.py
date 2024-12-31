#!/usr/bin/env python3
from collections import Counter
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
        required_moves_unoptimized = []
        moves = ''

        target_x, target_y = self.buttons[target_symbol]

        vmoves = abs(target_x - self.x)
        hmoves = abs(target_y - self.y)

        if target_x > self.x:
            required_moves_unoptimized += ['v'] * vmoves
        else:
            required_moves_unoptimized += ['^'] * vmoves
        
        if target_y > self.y:
            required_moves_unoptimized += ['>'] * hmoves
        else:
            required_moves_unoptimized += ['<'] * hmoves

        def sim_move(m):
            if m == '^':
                return self.x - 1, self.y
            elif m == 'v':
                return self.x + 1, self.y
            elif m == '>':
                return self.x, self.y + 1
            elif m == '<':
                return self.x, self.y - 1
            else:
                assert False

        def d(m):
            p = reference.buttons[m]
            dist = (p[0] - self.x) ** 2 + (p[1] - self.y) ** 2
            if sim_move(m) not in reference.buttons.values():
                dist += float('inf')
            return dist

        while self.x != target_x or self.y != target_y:
            next_move = min(required_moves_unoptimized, key=d)
            moves += next_move
            self.x, self.y = sim_move(next_move)
            required_moves_unoptimized.remove(next_move)

        # sorting ensures that we don't have to move around as much 
        return moves + 'A'
        # return ''.join() + 'A'
        # required_moves += 'A'
        # return required_moves

    def moves_for_sequence(self, target_sequence: str) -> str:
        return ''.join(self.move_to(symbol) for symbol in target_sequence)

reference = Robot(numpad)
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
        required_sequence = code
        for robot in robots:
            required_sequence = robot.moves_for_sequence(required_sequence)
        complexity = len(required_sequence) * int(code[:-1])
        print(len(required_sequence), int(code[:-1]))
        ans += complexity
    return ans

print(main(data))

