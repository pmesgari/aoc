import sys
import heapq


filename = sys.argv[1]
with open(filename) as f:
    grid = [list(map(int, list(i))) for i in [x.rstrip('\n') for x in f.readlines()]]


def adj(v, grid):
    row, col = v
    neighbours = []

    right = (row, col + 1)
    left = (row, col - 1)
    top = (row - 1, col)
    bottom = (row + 1, col)

    for row, col in [right, bottom, left, top]:
        if 0 <= row < len(grid) and 0 <= col < len(grid[row]):
            neighbours.append((row, col))

    return neighbours


# part 1: 613
def dijkstra(grid, s):
    D = {}
    PI = {}
    Q = []
    S = set()

    def init():
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                D[(row, col)] = float('inf')
                PI[(row, col)] = None
        D[s] = 0

    init()

    heapq.heappush(Q, (0, s))

    while Q:
        w, u = heapq.heappop(Q)
        S.add(u)

        for v in adj(u, grid):
            row, col = v
            if D[v] > D[u] + grid[row][col]:
                D[v] = D[u] + grid[row][col]
                PI[v] = u
                heapq.heappush(Q, (D[v], v))

    return D


def part1():
    source = (0, 0)
    target = (len(grid) - 1, len(grid[0]) - 1)
    shortest_paths = dijkstra(grid, source)
    print(shortest_paths[target])


def part2():
    """
    expand the tile in x and y directions
        i=0     i=1     i=2     i=3     i=4
        ----    ----    ----    ----    ----
    j=0 |
    j=1 |
    j=2 |
    j=3 |
    j=4 |
    
    the values in the tile (0, 0) must stay as they are.
    at tile i=1 and j=0 each value will be:
        value at tile i=0,j=0 + 1
    taking the example
        value at tile i=0,j=0 of 8 expanded in x will become 9, 1, 2, 3
    since we are told to wrap back around to 1 as soon as we increase a value of 9, to keep track how far
    we are from 9 at each value we take the mod of the value with 9
    
    at tile 0, 0 if we want to generate the value 8 we can simply do 8 % 9 to get an 8
    but, what happens if we have a value of 9 at tile 0,0 we are not allowed to increase and if we
    do 9 % 9 we get a zero. To get a value of 9 at tile 0,0 we can do value - 1 % 9 + 1
    so, we get (9 - 1) % 9 + 1 = 8 using this formula every other value in tile 0,0 can be generated intact
    that is we get back the same value e.g with value 5 the formula gives (5 - 1) % 9 + 1 = 5
    the way to read this is to say: take a step back and measure how far you are from 9 then add a step
    
    at tile 1,0 the value 8 now must become a 9. we can apply the same formula but with a shift in x, so
        ((value - 1) + shift_x) % 9 + 1
    so a value 8 becomes (8 - 1) + 1 % 9 + 1 = 9
    and a value 9 becomes (9 - 1) + 1 % 9 + 1 = 1
    
    the shift_x takes care of the expansion in x direction
    
    once we reach tile 4, 0 we need to expand in y and come back to x=0
    our original value at tile 0,0 is still 8 and we are told to increase the risk level by 1 everytime we repeat a tile
    so our 8 at tile 0,1 should become a 9, we can apply the same principles
        value - 1 % 9 + 1
    so for an 8 we have 8 - 1 % 9 + 1 = 8 but we need a 9 so we are short by 1, however we can use the shift in y to
    compensate for that so our formula becomes
        value - 1 + shift_y % 9 + 1
    and for an 8
        8 - 1 + 1 % 9 + 1 = 9
    and for a 9
        9 - 1 + 1 % 9 + 1 = 1
    
    it is good to mention that our expansion is limited to 5 in each direction so it is impossible to wrap around 9
    twice in a direction
    
    now we need to implement this in code!
    
    we expand by first performing an expansion of x then incrementing y going back to x = 0 and expand again in x
    """

    total_grid = []
    for y in range(5):
        for row in grid:
            expanded_row = []
            for x in range(5):
                for value in row:
                    expanded_row.append((value - 1 + x + y) % 9 + 1)
            total_grid.append(expanded_row)

    print(len(total_grid))

    source = (0, 0)
    target = (len(total_grid) - 1, len(total_grid[0]) - 1)
    shortest_paths = dijkstra(total_grid, source)
    print(shortest_paths[target])

part2()




