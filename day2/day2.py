import sys


filename = sys.argv[1]
with open(filename) as f:
    data = [(x.rstrip('\n')) for x in f.readlines()]

# print(data)

x = 0
y = 0
a = 0
for course in data:
    direction, value = course.split()
    if direction == 'forward':
        x += int(value)
        y += int(value) * a
    elif direction == 'down':
        a += int(value)
    else:
        a -= int(value)

print(x, y)
print(x * y)