import sys


filename = sys.argv[1]
with open(filename) as f:
    data = [(x.rstrip('\n')) for x in f.readlines()]

readings = [list(x) for x in list(zip(*data))]


def most_common_bits(data):
    readings = list(map(list, zip(*data)))
    m_bits = []
    for r in readings:
        m_bits.append(max(r, key=r.count))
    return m_bits


def least_common_bits(data):
    readings = list(map(list, zip(*data)))
    l_bits = []
    for r in readings:
        l_bits.append(min(r, key=r.count))
    return l_bits


gamma_rate = int(''.join(most_common_bits(readings)), 2)
epsilon_rate = int(''.join(least_common_bits(readings)), 2)


def f(data, rating_bits, last, criteria):
    readings = data
    r_bits = rating_bits
    for i in range(len(r_bits)):
        next = []
        if len(readings) == 1:
            return readings[0]
        if len(readings) == 2:
            if readings[0][i] != readings[1][i]:
                return list(filter(lambda x: x[i] == last, readings))[0]
        for r in readings:
            if r[i] == r_bits[i]:
                next.append(r)
        readings = next
        r_bits = criteria(readings)


o_rating = f(data, most_common_bits(readings), '1', most_common_bits)
co2_rating = f(data, least_common_bits(readings), '0', least_common_bits)
print(int(o_rating, 2) * int(co2_rating, 2))