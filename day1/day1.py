import sys


filename = sys.argv[1]
with open(filename) as f:
    data = [int(x.rstrip('\n')) for x in f.readlines()]

print(data)

increases = []
print([(j, j+1) for j in range(len(data) - 1)])
for i, j in [(j, j+1) for j in range(len(data) - 1)]:
    if data[j] > data[i]:
        increases.append((i, j))

print([(j, j+1, j+2) for j in range(len(data) - 1)])
lumps = []
for i, j, k in [(j, j+1, j+2) for j in range(len(data) - 2)]:
    lumps.append(sum([data[m] for m in [i, j, k]]))

increasing_sequences = []
for i, j in [(j, j+1) for j in range(len(lumps) - 1)]:
    if lumps[j] > lumps[i]:
        increasing_sequences.append((i, j))

print(len(increases))
print(len(increasing_sequences))
#print(lumps)
