from bisect import insort
from random import randint, random, shuffle

from lib import select


class Item:
    all = []
    sorted_all = []

    @staticmethod
    def all_cost() -> int:
        return sum(item.cost for item in Item.all)

    def __init__(self, cost: int, price: int):
        self.cost = cost
        self.price = price
        self.num = len(Item.all)

        Item.all.append(self)
        insort(Item.sorted_all, self)

    def __lt__(self, other: 'Item'):
        return self.price_cost < other.price_cost

    @property
    def price_cost(self) -> float:
        return self.price / self.cost


class Solution:
    def __init__(self, decision_l: list):
        self.decision_l = decision_l
        self.fitness = None

    def __lt__(self, other: 'Solution'):
        return self.fitness < other.fitness

    def __repr__(self):
        return ''.join(str(i) for i in self.decision_l)

    @property
    def cost(self) -> int:
        return sum(Item.all[i].cost for i, decision in enumerate(self.decision_l) if decision)

    @property
    def price(self) -> int:
        return sum(Item.all[i].price for i, decision in enumerate(self.decision_l) if decision)

    def clone(self) -> 'Solution':
        other = Solution(self.decision_l[:])
        other.fitness = self.fitness
        return other


# --- GA ---
MAX_COST = 100
CROSSOVER_RATE = 0.2
MUTATE_RATE = 0.05


def mark(solution_l: list):
    for solution in solution_l:
        if solution.cost <= MAX_COST:
            solution.fitness = solution.price
            continue

        curr_cost = solution.cost
        for inferior in Item.sorted_all:
            if solution.decision_l[inferior.num]:
                solution.decision_l[inferior.num] = 0

                curr_cost -= inferior.cost
                if curr_cost <= MAX_COST:
                    solution.fitness = solution.price
                    break


def crossover(solution_l: iter, rate: float):
    shuffle(solution_l)

    for i in range(0, len(solution_l), 2):
        if rate < random():
            continue

        next_ab = []
        a = solution_l[i].decision_l
        b = solution_l[i + 1].decision_l

        point = randint(1, len(a) - 1)
        for head, tail in ((a, b), (b, a)):
            next_ab.append(head[:point] + tail[point:])
        a[:], b[:] = next_ab


def mutate(solution_l: list):
    for solution in solution_l:
        if random() < MUTATE_RATE:
            index = randint(0, len(solution.decision_l) - 1)
            solution.decision_l[index] ^= 1


INIT_PERCENT = 0.1
INCREASE_TH = 0.1
INCREASE_RATE = 0.1

params = {'dual_num': None, 'effective_rate': None}


def dual(solution_l: list):
    prev_dual_num = params['dual_num']  # type: int
    prev_effective_rate = params['effective_rate']  # type: float

    if prev_dual_num is None:
        dual_num = round(len(solution_l) * INIT_PERCENT)
    else:
        if prev_effective_rate < INCREASE_TH:
            sign = 1
        elif prev_effective_rate == INCREASE_TH:
            sign = 0
        else:
            sign = -1
        dual_num = max(len(solution_l) // 20, min(len(solution_l), round(INCREASE_RATE ** sign * prev_dual_num)))

    solution_l.sort()
    effective_num = 0
    for i in range(dual_num):
        solution = solution_l[i].clone()
        solution.decision_l[:] = map(lambda decision: decision ^ 1, solution.decision_l)

        if solution > solution_l[i]:
            solution_l[i] = solution
            effective_num += 1
    params['dual_num'] = dual_num
    params['effective_rate'] = effective_num / dual_num


if __name__ == '__main__':
    def rand_solution() -> Solution:
        decision_l = []
        for i in range(len(Item.all)):
            decision_l.append(randint(0, 1))
        return Solution(decision_l)


    def inspect(solution_l: list):
        print(len(solution_l), round(sum(i.fitness for i in solution_l)))


    def main():
        for cost, price in ((40, 40), (50, 60), (30, 10), (10, 10), (10, 3), (40, 20), (30, 60)):
            Item(cost, price)

        def select_apply(solution_l: list):
            solution_l[:] = select(solution_l, lambda x: x.fitness, len(solution_l), lambda x: x.clone())

        def crossover_apply(solution_l: list):
            return crossover(solution_l, CROSSOVER_RATE)

        solution_l = [rand_solution() for _ in range(100)]
        for _ in range(10):
            for _ in range(100):
                for call in (mark,
                             select_apply,
                             crossover_apply,
                             mutate,
                             dual,
                             mark,
                             inspect):
                    call(solution_l)
            print('--- 动态变换 ---')
            for item in Item.all:
                item.price *= random() * 3
                item.cost *= random() * 3
            Item.sorted_all.sort()


    main()
