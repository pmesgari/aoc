import sys
from termcolor import colored


filename = sys.argv[1]
boards = []
with open(filename) as f:
    numbers = [int(x) for x in f.readline().split(',')]
    rest = [line.split() for line in f.read().splitlines() if line != '']
    start = 0
    stop = 5
    count = 0
    board = []
    while stop < len(rest) + 1:
        for i in range(start, stop):
            board.append([(int(x), False) for x in rest[i]])
            count += 1
            if count == 5:
                boards.append(board)
                start = stop
                stop += 5
                count = 0
                board = []


def place(b, n):
    for r in range(len(b)):
        for c in range(len(b[r])):
            if b[r][c][0] == n:
                b[r][c] = (n, True)


def print_board(b):
    for r in range(len(b)):
        row = []
        for c in range(len(b[r])):
            if b[r][c][1]:
                row.append(f"*{str(b[r][c][0])}*")
            else:
                row.append(str(b[r][c][0]))
        print(' '.join(row))


def is_win(b):
    for r in range(len(b)):
        if all([x[1] for x in b[r]]):
            return True
    b_transpose = [list(x) for x in list(zip(*b))]
    for r in range(len(b_transpose)):
        if all([x[1] for x in b_transpose[r]]):
            return True
    return False


def score(b, n):
    s = 0
    for r in range(len(b)):
        for c in range(len(b[r])):
            if not b[r][c][1]:
                s += b[r][c][0]
    return s * n


def part1():
    win = False
    for n in numbers:
        if win:
            break
        for b in boards:
            place(b, n)
            if is_win(b):
                print(score(b, n))
                win = True


def part2():
    wins = []
    for n in numbers:
        for i in range(len(boards)):
            if is_win(boards[i]):
                continue
            place(boards[i], n)
            if is_win(boards[i]):
                wins.append((i, n))

    unique_wins = []
    l = []
    for w in wins:
        if w[0] not in l:
            l.append(w[0])
            unique_wins.append((w[0], w[1]))

    return score(boards[unique_wins[-1][0]], unique_wins[-1][1])
# part1()
print(part2())
print('done')

