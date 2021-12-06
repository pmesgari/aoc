import sys


def line_to_point(start, end):
    x1, y1 = start
    x2, y2 = end
    u = 1
    v = 1

    if x1 > x2:
        u = -1
    if y1 > y2:
        v = -1

    if x1 == x2:
        return [(x1, y1 + (v * dy))for dy in range(abs(y2 - y1) + 1)]
    elif y1 == y2:
        return [(x1 + (u * dx), y1) for dx in range(abs(x2 - x1) + 1)]
    elif abs((x2 - x1) / (y2 - y1)) == 1:
        return [(x1 + (u * dx), (v * dx) + y1) for dx in range(abs(x2 - x1) + 1)]


class Board:
    def __init__(self):
        self.grid = []
        for x in range(0, 1000):
            self.grid.append([])
            for y in range(0, 1000):
                self.grid[x].append(0)

    def mark(self, x, y):
        self.grid[x][y] += 1

    def get_score(self, x, y):
        return self.grid[x][y]

    def overlap_count(self):
        count = 0
        for x in range(0, 1000):
            for y in range(0, 1000):
                if self.grid[x][y] > 1:
                    count += 1
        return count


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as f:
        rows = f.readlines()
    lines = []
    for row in rows:
        line = row.rstrip('\n').split(' -> ')

        def make_coordinate(coordinate):
            x, y = coordinate.split(',')
            return int(x), int(y)
        lines.append([make_coordinate(c) for c in line])

    board = Board()
    for line in lines:
        points = line_to_point(line[0], line[1])
        for point in points:
            board.mark(point[0], point[1])

    overlap_count = board.overlap_count()
    print('number of overlapping lines is: ' + str(overlap_count))
