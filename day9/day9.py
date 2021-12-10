import sys

filename = sys.argv[1]
heightmap = []

with open(filename) as f:
    data = [row.strip() for row in f.readlines()]


for row in data:
    heightmap.append([int(x) for x in list(row)])


MAX_WIDTH = len(heightmap[0])
MAX_HEIGHT = len(heightmap)


def get_neighbours(row, col, width=MAX_WIDTH, height=MAX_HEIGHT):
    right = col + 1
    left = col - 1
    top = row - 1
    bottom = row + 1

    if left < 0 and top < 0:
        # [right, bottom]
        return [(row, right, heightmap[row][right]), (bottom, col, heightmap[bottom][col])]
    if right >= width and top < 0:
        # [left, bottom]
        return [(row, left, heightmap[row][left]), (bottom, col, heightmap[bottom][col])]
    if left < 0 and bottom >= height:
        # [right, top]
        return [(top, col, heightmap[top][col]), (row, right, heightmap[row][right])]
    if right >= width and bottom >= height:
        # [left, top]
        return [(row, left, heightmap[row][left]), (top, col, heightmap[top][col])]

    if left < 0:
        # [right, top, bottom]
        return [(top, col, heightmap[top][col]), (bottom, col, heightmap[bottom][col]), (row, right, heightmap[row][right])]
    if right >= width:
        # [left, top, bottom]
        return [(top, col, heightmap[top][col]), (row, left, heightmap[row][left]), (bottom, col, heightmap[bottom][col])]

    if top < 0:
        # [right, left, bottom]
        return [(row, left, heightmap[row][left]), (row, right, heightmap[row][right]), (bottom, col, heightmap[bottom][col])]
    if bottom >= height:
        # [right, left, top]
        return [(top, col, heightmap[top][col]), (row, left, heightmap[row][left]), (row, right, heightmap[row][right])]

    return [(row, left, heightmap[row][left]), (row, right, heightmap[row][right]), (top, col, heightmap[top][col]), (bottom, col, heightmap[bottom][col])]


def adj(s):
    return get_neighbours(s[0], s[1])


def bfs(s):
    # s is a pair of (row, col)
    frontiers = [[s]]
    level = {s: 0}
    i = 1
    frontier = [s]
    while frontier:
        next = []
        for u in frontier:
            for v in adj(u):
                if v not in level:
                    level[v] = i
                    if v[2] != 9:
                        next.append(v)
        frontier = next
        frontiers.append(frontier)
        i += 1
    return frontiers


lows = []
for i in range(len(heightmap)):
    row = heightmap[i]
    for j in range(len(row)):
        neighbours = get_neighbours(i, j, len(row), len(heightmap))
        if all([row[j] < n[2] for n in neighbours]):
            lows.append((i, j, row[j]))


print(lows)
print(sum([x[2] + 1 for x in lows]))

basin_sizes = []
for low in lows:
    basin = bfs(low)
    basin_sizes.append(sum([len(f) for f in basin if f is not None]))

result = 1
for s in sorted(basin_sizes, reverse=True)[:3]:
    result = result * s

print(result)