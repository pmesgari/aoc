import sys


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as f:
        data = [int(x) for x in f.read().split(',')]
    # data = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    positions = sorted(data)
    median = positions[len(positions) // 2]
    # median = 10
    print('Median is ' + str(median))

    cost = 0
    for x in positions:
        cost = cost + abs((int(x) - int(median)))

    print('Total cost is ' + str(cost))

    def fuel(distance):
        return distance * (distance + 1) / 2

    best = 1e9
    for med in range(2000):
        cost = 0
        for x in positions:
            d = abs(x - med)
            cost += fuel(d)
        if cost < best:
            best = cost

    print('Total cost with variable fuel is: ' + str(best))