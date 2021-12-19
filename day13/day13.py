import sys


filename = sys.argv[1]

with open(filename) as f:
    def to_tuple(x):
        i, j = x.split(',')
        return int(i), int(j)
    data, instructions = f.read().split('\n\n')
    data = list(map(to_tuple, data.split('\n')))
    instructions = [i[2] for i in [i.split(' ') for i in instructions.split('\n')]]


def print_grid(grid):
    for i in range(len(grid)):
        print(''.join(grid[i]))
    print('\n')


def fold(dots, direction, line):
    folded_dots = []
    if direction == 'x':
        for x, y in dots:
            if x < line:
                folded_dots.append((x, y))
            else:
                if (line - (x - line), y) not in folded_dots:
                    folded_dots.append((line - (x - line), y))
    if direction == 'y':
        for x, y in dots:
            if y < line:
                folded_dots.append((x, y))
            else:
                if (x, line - (y - line)) not in folded_dots:
                    folded_dots.append((x, line - (y - line)))
    return folded_dots


dots = []
for d in data:
    x, y = d
    dots.append((x, y))

for i in instructions:
    direction, line = i.split('=')
    dots = fold(dots, direction, int(line))

print(len(dots))


width = max([d[0] for d in dots]) + 1
height = max([d[1] for d in dots]) + 1

grid = []
for i in range(height):
    row = []
    for j in range(width):
        row.append('.')
    grid.append(row)

for i in dots:
    x, y = i
    grid[y][x] = '#'

print_grid(grid)
