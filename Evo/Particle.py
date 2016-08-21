from math import inf
from random import random, uniform

MIN = -30
MAX = 30


def obj_func(pos_l: list) -> float:
    assert len(pos_l) == 5
    total = 0
    for i in range(len(pos_l) - 1):
        a = pos_l[i]
        b = pos_l[i + 1]
        assert MIN <= a <= MAX and MIN <= b <= MAX

        value = 100 * (b - a ** 2) ** 2 + (a - i) ** 2
        total += value
    return total


class Particle:
    all = []
    best_mark = inf
    best_pos_l = None

    def __init__(self, pos_l: list, speed_l: list):
        self.pos_l = pos_l
        self.speed_l = speed_l
        self.best_mark = inf
        self.best_pos_l = None
        Particle.all.append(self)
        self.calc()

    def calc(self):
        curr_mark = obj_func(self.pos_l)
        if curr_mark < self.best_mark:
            self.best_mark = curr_mark
            self.best_pos_l = self.pos_l[:]

            if self.best_mark < Particle.best_mark:
                Particle.best_mark = self.best_mark
                Particle.best_pos_l = self.best_pos_l[:]

    def move_next(self):
        next_speed_l = []
        for i in range(len(self.speed_l)):
            speed = self.speed_l[i]
            pos = self.pos_l[i]
            best_pos = self.best_pos_l[i]
            glo_best_pos = Particle.best_pos_l[i]

            next_speed = 0.5 * speed + 2 * random() * (best_pos - pos) + 2 * random() * (glo_best_pos - pos)
            next_speed = min(max(next_speed, MIN - MAX), MAX - MIN)
            next_speed_l.append(next_speed)
        self.speed_l[:] = next_speed_l

        for i in range(len(self.pos_l)):
            self.pos_l[i] = min(max(self.pos_l[i] + self.speed_l[i], MIN), MAX)
        self.calc()


if __name__ == '__main__':
    def main():
        particle_l = [Particle([uniform(MIN, MAX) for _ in range(5)],
                               [uniform(MIN / 2, MAX / 2) for _ in range(5)]) for _ in range(5)]
        for _ in range(100):
            for p in particle_l:
                p.move_next()
            print(Particle.best_mark, Particle.best_pos_l)


    main()
