from math import inf
from random import randint

dist_matrix = [[0, 8, 5, 6, 7],
               [6, 0, 8, 5, 9],
               [7, 9, 0, 5, 6],
               [9, 7, 8, 0, 5],
               [5, 6, 7, 8, 0]]

HI = 4  # 广域搜索时的初始步长
LEAVE_TH = 2  # 突破等级2时还未重置限制, 限制等级直接变化为HI
LV_NUM = 5  # 限制等级
RE_PER_LV = 2  # 每个等级进行2次搜寻
RE_PER_SR = 2  # 每次搜寻进行2次变换


def exchange_2(obj: list) -> list:
    start = randint(0, len(obj) - 1)
    end = randint(start, len(obj))
    return [*obj[:start], *reversed(obj[start:end]), *obj[end:]]


def obj_func(obj: list) -> int:
    total = 0
    for i in range(len(obj) - 1):
        a = obj[i] - 1
        b = obj[i + 1] - 1
        total += dist_matrix[a][b]
    return total


class Predator:
    best_permutation = None
    best_mark = inf

    def __init__(self, obj: list):
        self.counter = 0
        self.limit_l = []
        self.lv = 0

        self.obj = obj
        self.calc_limit()

    def hunt(self):
        proposal_l = []
        for _ in range(RE_PER_SR):
            permutation = exchange_2(self.obj)
            mark = obj_func(permutation)
            proposal_l.append((mark, permutation))
        proposal = min(proposal_l)
        mark, permutation = proposal

        if mark < self.limit_l[self.lv]:
            self.obj = permutation
            if mark < Predator.best_mark:
                Predator.best_permutation = permutation
                Predator.best_mark = mark
                self.counter = 0
                self.lv = 0
                return self.calc_limit()

        self.counter += 1
        if self.counter > RE_PER_LV:
            self.counter = 0
            self.lv += 1
            if self.lv == LEAVE_TH:
                self.lv = HI

    def calc_limit(self):
        limit_l = []
        for _ in range(LV_NUM):
            permutation = exchange_2(self.obj)
            mark = obj_func(permutation)
            if mark < Predator.best_mark:
                Predator.best_permutation = permutation
                Predator.best_mark = mark
            limit_l.append(mark)
        self.limit_l[:] = [obj_func(self.obj), *sorted(limit_l)]


if __name__ == '__main__':
    def main():
        init_solution = [1, 2, 3, 4, 5]
        print(obj_func(init_solution))
        predator = Predator(init_solution)
        while predator.lv <= LV_NUM:
            predator.hunt()
            print(predator.best_mark)


    main()
