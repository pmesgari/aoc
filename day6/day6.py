import sys


class LanternFishSchool:
    def __init__(self, data=None):
        if data is None:
            self.data = []
        self.fishes = {}
        for fish in data:
            if fish in self.fishes:
                self.fishes[fish] += 1
            else:
                self.fishes[fish] = 1

    def next(self):
        for key, value in self.fishes.items():
            if key == 0:


    def total(self):
        return len(self.fishes)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as f:
        fishes = [int(day) for day in f.read().split(',')]
    # school = LanternFishSchool(fishes)
    school = LanternFishSchool([3, 4, 3, 1, 2])

    for i in range(18):
        school.next()
        print(f"After {i + 1} days: {school.total()}")

    print(f'Total number of fishes after {i + 1} days: {school.total()}')

