import sys


class Stack:
    def __init__(self):
        self.items = []

    def top(self):
        return self.items[-1]

    def push(self, item):
        self.items.append(item)

    def pop(self):
        self.items = self.items[:-1]

    def size(self):
        return len(self.items)


mapping = {
    '(': ')',
    '<': '>',
    '[': ']',
    '{': '}'
}

penalties = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

LOG = False


def matches(a, b):
    if a == '(' and b == ')':
        return True
    if a == '[' and b == ']':
        return True
    if a == '{' and b == '}':
        return True
    if a == '<' and b == '>':
        return True
    return False


def corrupt_score(chunk, log=LOG):
    illegals = {}
    s = Stack()
    s.push(chunk[0])
    corrupt = False
    for i in range(1, len(chunk)):
        if corrupt:
            break
        if chunk[i] in ['{', '[', '<', '(']:
            s.push(chunk[i])
            continue
        if chunk[i] in ['}', ']', '>', ')']:
            if matches(s.top(), chunk[i]):
                s.pop()
            else:
                illegals.update({chunk[i]: illegals.get(chunk[i], 0) + 1})
                if log:
                    print(f'Expected {mapping[s.top()]}, but found {chunk[i]}')
                corrupt = True
    return sum([penalties[key] * value for key, value in illegals.items()])


def _complete(chunk):
    s = Stack()
    s.push(chunk[0])
    for i in range(1, len(chunk)):
        if chunk[i] in ['{', '[', '<', '(']:
            s.push(chunk[i])
            continue
        if chunk[i] in ['}', ']', '>', ')']:
            if matches(s.top(), chunk[i]):
                s.pop()
    s.items.reverse()
    missing = [mapping[c] for c in s.items]
    return ''.join(missing)


def complete_score(chunk):
    s = Stack()
    s.push(chunk[0])
    for i in range(1, len(chunk)):
        if chunk[i] in ['{', '[', '<', '(']:
            s.push(chunk[i])
            continue
        if chunk[i] in ['}', ']', '>', ')']:
            if matches(s.top(), chunk[i]):
                s.pop()
    s.items.reverse()
    missing = [mapping[c] for c in s.items]

    score = 0
    for c in missing:
        score = (score * 5) + scores[c]
    return score
    # def reduce(arr, func, initial=0):
    #     result = initial
    #     for x in arr:
    #         result += func(x, result)
    #     return result
    #
    # return reduce(missing, lambda x, acc: (acc * 5) + scores[x])


filename = sys.argv[1]
with open(filename) as f:
    data = [line.rstrip() for line in f.readlines()]

corrupts = []
for row in data:
    score = corrupt_score(row)
    if score != 0:
        corrupts.append(score)

print(sum(corrupts))


auto_complete_scores = []
incomplete_rows = []
for row in data:
    if corrupt_score(row) == 0:
        auto_complete_scores.append(complete_score(row))

final_score = sorted(auto_complete_scores)
print(final_score)
print(final_score[len(final_score) // 2])