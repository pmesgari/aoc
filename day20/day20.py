import sys


filename = 'input.txt' #sys.argv[1]
with open(filename) as f:
    rules, inp = f.read().split('\n\n')

image = [list(row) for row in inp.split('\n')]
rules = rules.replace('\n', '')

grid = {}
for row in range(len(image)):
    for col in range(len(image[row])):
        val = '1'
        if image[row][col] == '.':
            val = '0'

        grid.update({(row, col): val})

def adj(v):
    row, col = v
    n = []
    for r in [row - 1, row, row + 1]:
        for c in [col - 1, col, col + 1]:
            n.append((r, c))

    return n


def is_outside(v, max_row, max_col):
    row, col = v
    if row < 0 or row > max_row:
        return True
    if col < 0 or col > max_col:
        return True

def grid_to_image(grid):
    image = []

    min_row = min([r for r, _ in grid.keys()])
    max_row = max([r for r, _ in grid.keys()])
    min_col = min([c for _, c in grid.keys()])
    max_col = max([c for _, c in grid.keys()])

    for r in range(min_row, max_row + 1):
        row = []
        for c in range(min_col, max_col + 1):
            row.append('')
        image.append(row)

    for key, value in grid.items():
        row, col = key
        if value == '0':
            image[row][col] = '.'
        else:
            image[row][col] = '#'
    
    result = []
    for line in image:
        result.append(''.join(line))
    return '\n'.join(result)

# print(grid_to_image(grid))
# print('\n')
# print('---------------')
# print('\n')

def codify(v, grid, default, max_row, max_col):
    ns = adj(v)
    code = []
    for n in ns:
        r, c = n
        if is_outside(n, max_row, max_col):
            code.append(default)
        else:
            code.append(grid[(r, c)])

    return ''.join(code)

# code = codify((3, 0), grid)
# idx = int(code, 2)
# print(code)
# print(idx)
# print(rules[idx])

def enhance(steps, grid):
    toggle = False

    for _ in range(1, steps + 1):
        if toggle:
            default = '1'
        else:
            default = '0'
        new_grid = {}

        min_row = min([r for r, _ in grid.keys()])
        max_row = max([r for r, _ in grid.keys()])
        min_col = min([c for _, c in grid.keys()])
        max_col = max([c for _, c in grid.keys()])

        for row in range(min_row - 1, max_row + 2):
            for col in range(min_col - 1, max_col + 2):
                code = codify((row, col), grid, default, max_row, max_col)
                idx = int(code, 2)
                if rules[idx] == '.':
                    new_grid[(row + 1, col + 1)] = '0'
                else:
                    new_grid[(row + 1, col + 1)] = '1'
        grid = new_grid
        toggle = not toggle

    return grid

def lights(grid):
    count = 0
    for _, value in grid.items():
        if value == '1':
            count += 1
    return count

part1 = enhance(50, grid)
# print(grid_to_image(part1))
print(lights(part1))
