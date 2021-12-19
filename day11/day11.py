import sys

filename = sys.argv[1]

with open(filename) as f:
    data = [line.rstrip() for line in f.readlines()]

os = []
for row in data:
    os.append([int(o) for o in row])

print(os)


def get_neighbours(s):
    # s is a pair of (row, col)
    r = s[0]
    c = s[1]

    right = (r, c + 1)
    left = (r, c - 1)
    top = (r - 1, c)
    bottom = (r + 1, c)

    # north west
    nw = (r - 1, c - 1)
    # south west
    sw = (r + 1, c - 1)
    # north east
    ne = (r - 1, c + 1)
    # south east
    se = (r + 1, c + 1)

    return [
        right, left, top, bottom,
        nw, sw, ne, se
    ]


count = 0


def _flash(p):
    global count
    count += 1
    p_n = get_neighbours(p)
    for i, j in p_n:
        if 0 <= i < len(os) and 0 <= j < len(os[i]):
            os[i][j] += 1
            if os[i][j] == 10:
                flash((i, j))


def flash(p):
    c = 0
    p_n = get_neighbours(p)
    frontier = p_n
    while frontier:
        next = []
        for i in range(len(frontier)):
            r = frontier[i][0]
            c = frontier[i][1]
            if 0 <= r < len(os) and 0 <= c < len(os[i]):
                os[r][c] += 1
                if os[r][c] == 10:
                    c += 1
                    next.insert(i, (r, c))
            next = next[1:]
        frontier = next


def step():
    for r in range(len(os)):
        for c in range(len(os[r])):
            os[r][c] += 1
            if os[r][c] == 10:
                flash((r, c))
                os[r][c] += 1
    for r in range(len(os)):
        for c in range(len(os[r])):
            if os[r][c] > 9:
                os[r][c] = 0


for s in range(10):
    step()
    # o_count = 0
    # for r in os:
    #     if r.count(0) == len(r):
    #         o_count += 1
    # if o_count == len(os):
    #     print('all 0s at ', s + 1)
    #     break

# print(step(100))
print(count)