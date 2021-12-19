import sys


filename = sys.argv[1]
with open(filename) as f:
    template_string, rules = f.read().split('\n\n')
    rules = {key: val for key, val in [r.split(' -> ') for r in rules.split('\n')]}

print(template_string)
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


def _solve(t):
    def decompose(pair, ins_value):
        first, second = pair
        return [(first, ins_value), (ins_value, second)]

    new_template = {}
    for key, value in t.items():
        if not value:
            if key[1] in rules:
                new_template[key] = (decompose(key[1], rules[key[1]]))


    return new_template


def print_template(template):
    shift = 0
    ans = None
    for key, value in template.items():

        def combine(value):
            first, second = value
            return f"{first[0]}{first[1]}{second[1]}"
        s = combine(value)
        if ans is None:
            ans = list(s)
        if shift != 0:
            ans.pop()
            ans = ans + list(s)
        shift += 1

    print(''.join(ans))
    return ans


template = {}
initial_template_pairs = pairs(template_string)
for i in range(len(initial_template_pairs)):
    template[(i, initial_template_pairs[i])] = []

last_template = {}
for _ in range(40):
    print(f"solving step: {_ + 1}")
    template = solve(template)
    template_string = print_template(template)
    template_pairs = pairs(''.join(template_string))
    last_template = template
    template = {}
    for i in range(len(template_pairs)):
        template[(i, template_pairs[i])] = []

print('done')
mce = max(list(template_string), key=template_string.count)
lce = min(list(template_string), key=template_string.count)

print(template_string.count(mce), template_string.count(lce))
print(template_string.count(mce) - template_string.count(lce))
