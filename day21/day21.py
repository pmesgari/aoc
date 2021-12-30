from enum import Enum


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


class Player(Enum):
    White = 'white'
    Black = 'black'


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


board = Board()
# board.take_turn()
# print(board.scores, board.pos)
while not board.is_win:
    board.take_turn()

# for _ in range(400):
#     board.take_turn()

# dice = Dice()
# for _ in range(350):
#     dice.throw()
