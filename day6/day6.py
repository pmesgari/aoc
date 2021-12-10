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
        timers = {}

        producer_count = self.fishes.get(0, 0)
        new_born_count = 0
        reset_count = 0

        for timer, value in self.fishes.items():
            new_timer = timer - 1
            if new_timer < 0:
                producer_count -= value
                new_born_count += value
                reset_count += value
            elif new_timer == 0:
                producer_count += value
            else:
                timers[new_timer] = value
        if producer_count > 0:
            timers[0] = producer_count
        if new_born_count > 0:
            timers[8] = timers.get(8, 0) + new_born_count
        if reset_count > 0:
            timers[6] = timers.get(6, 0) + reset_count
        self.fishes = timers
        return fishes



    def total(self):
        fishes = 0
        for key, value in self.fishes.items():
            fishes = fishes + value
        return fishes


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as f:
        fishes = [int(day) for day in f.read().split(',')]
    school = LanternFishSchool(fishes)
    #school = LanternFishSchool([3, 4, 3, 1, 2])

    for i in range(256):
        school.next()
        print(f"After {i + 1} days: {school.total()}")

    print(f'Total number of fishes after {i + 1} days: {school.total()}')

