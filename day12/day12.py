import sys


filename = 'input.txt'
with open(filename) as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

print(lines)

graph = {}
for line in lines:
    u, v = line.split('-')
    graph[u] = graph.get(u, []) + [v]
    if u != 'start':
        graph[v] = graph.get(v, []) + [u]

# print(graph)

visited = set()


def dfs(s, visited):
    total = 0
    if s == 'end':
        return 1
    for n in graph[s]:
        if n.lower() == n and n in visited:
            continue
        # this is the same as saying parent[n] = s in the usual DFS algorithm
        visited = visited.union({s})
        total += dfs(n, visited)
    return total


path = []


def dfs_with_double(s,  path, doubled=False):
    total = 0
    if s == 'end':
        return 1
    # for all vertices we can reach from s
    for n in graph[s]:
        # if we have visited this vertex and already doubled, can't explore it anymore, so skip
        if doubled and n in path:
            continue
        # if we have visited this neighbour
        if n in path:
            # and our current cave is a small one
            if s.lower() == s:
                # if current cave is not in our path, meaning this is the first time we enter it
                if s not in path:
                    # add current cave to our path
                    path = path + [s]
                # then explore the neighbour from this path and allow a double visit to the current cave
                total += dfs_with_double(n, path, True)
            else:
                # otherwise we have been to the current cave already, so continue exploration from this path
                total += dfs_with_double(n, path, True)
        # otherwise this is the first time we visit this neighbour
        else:
            # if current cave is small
            if s.lower() == s:
                # and we haven't been to it before
                if s not in path:
                    # add current cave to our path
                    path = path + [s]
                # then explore this neighbour from this path
                total += dfs_with_double(n, path, doubled)
            else:
                total += dfs_with_double(n, path, doubled)
    return total


print(dfs_with_double('start', path))


# paths = []
# Q = [(['start'], graph.get('start'), None)]
# while Q:
#     path, to_explore, doubled = Q.pop()

#     for e in to_explore:
#         if e == 'end':
#             paths.append(path + [e])
#             continue

#         if e.lower() == e and e in path:
#             continue

#         new_path = path + [e]
#         new_to_explore = []
#         for edge in graph[e]:
#             new_to_explore.append(edge)
#         Q.append((new_path, new_to_explore, doubled))

# for p in paths:
#     print(p)
# print(len(paths))
