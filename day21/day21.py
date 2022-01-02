from enum import Enum
from dataclasses import dataclass


class Dice:
    def __init__(self):
        self.count = 0
        self.current = 0
        self.values = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= 100:
            self.current = 0
        self.current += 1
        self.count += 1
        self.values.append(self.current)

    def throw(self):
        for _ in range(3):
            next(self)
        total = sum(self.values)
        print(','.join([str(v) for v in self.values]), self.count, total)
        self.values = []
        return total


q_dice_permutations = {}
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            q_dice_permutations.update({i +j + k: q_dice_permutations.get(i +j + k, 0) + 1})

print(q_dice_permutations)



class Player(Enum):
    White = 'white'
    Black = 'black'


@dataclass(frozen=True)
class GameState:
    player: Player
    score: int
    pos: int

import functools

@functools.lru_cache(maxsize=None)
def quantum_play(white_state, black_state):
    # we assume black just played
    if black_state.score >= 21:
        return [0, 1]
    else:
        white_wins = 0
        black_wins = 0
        for key, value in q_dice_permutations.items():
            mod = (key + white_state.pos) % 10
            if mod > 0:
                next_pos = mod
            else:
                next_pos = 10
            next_score = white_state.score + next_pos
            black_win, white_win = quantum_play(black_state, GameState(player=white_state.player, score=next_score, pos=next_pos)) 
            black_wins += black_win * value
            white_wins += white_win * value
    return (white_wins, black_wins)


white = GameState(player=Player.White, score=0, pos=2)
black = GameState(player=Player.Black, score=0, pos=7)

win1, win2 = quantum_play(white, black)
print(win1, win2)
print(max(win1, win2))


class Board:
    def __init__(self):
        self.player = Player.White
        self.dice = Dice()
        self.scores = {
            Player.White: 0,
            Player.Black: 0
        }
        self.pos = {
            Player.White: 4,
            Player.Black: 8
        }
        self.is_win = False

    def take_turn(self):
        rolled = self.dice.throw()
        mod = (rolled + self.pos[self.player]) % 10

        if mod > 0:
            self.pos[self.player] = mod
        else:
            self.pos[self.player] = 10

        self.scores[self.player] += self.pos[self.player]
        if self.scores[self.player] >= 1000:
            ans = self.dice.count * self.scores[self.other(self.player)]
            print(ans)
            self.is_win = True
        print(self.pos, 'last player ' + self.player.name)
        self.player = self.other(self.player)

    @staticmethod
    def other(player):
        return Player.Black if player == Player.White else Player.White


# board = Board()
# board.take_turn()
# print(board.scores, board.pos)
# while not board.is_win:
#     board.take_turn()

# for _ in range(400):
#     board.take_turn()

# dice = Dice()
# for _ in range(350):
#     dice.throw()
