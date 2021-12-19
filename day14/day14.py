import sys


filename = sys.argv[1]
with open(filename) as f:
    template, rules = f.read().split('\n\n')
    rules = {key: val for key, val in [r.split(' -> ') for r in rules.split('\n')]}

print(template)
print(rules)


def pairs(t):
    result = []
    i = 0
    j = 1
    while j < len(t):
        result.append(f"{t[i]}{t[j]}")
        i = j
        j += 1
    return result


def matches(t, p):
    n = len(t)
    m = len(p)
    result = []
    for s in range(n - m + 1):
        if p == t[s:s+m]:
            #print(f'pattern found with shift {s}')
            result.append(s)
    return result

# matches('NNCB', 'CB')


def solve(template, rules):
    pair_counter = {}
    letter_counter = {}
    ps = pairs(''.join(template))

    for p in ps:
        pair_counter[p] = pair_counter.get(p, 0) + 1

    for _ in range(41):
        next = {}
        letter_counter = {}
        for key, val in pair_counter.items():
            letter_counter[key[0]] = letter_counter.get(key[0], 0) + pair_counter[key]
        letter_counter[template[-1]] = letter_counter.get(template[-1], 0) + 1
        for key, val in pair_counter.items():
            ins_value = rules[key]
            first, second = key
            next[first + ins_value] = next.get(first + ins_value, 0) + pair_counter[key]
            next[ins_value + second] = next.get(ins_value + second, 0) + pair_counter[key]

        pair_counter = next

    letters = [(key, value) for key, value in letter_counter.items()]
    
    mce, mce_count = max(letters, key=lambda item: item[1])
    lce, lce_count = min(letters, key=lambda item: item[1])

    ans = mce_count - lce_count
    print(ans)


solve(template, rules)

