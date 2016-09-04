from random import random, uniform, shuffle, randint


class Item:
    all = []

    @staticmethod
    def all_cost() -> int:
        return sum(item.cost for item in Item.all)

    def __init__(self, cost: int, price: int):
        self.cost = cost
        self.price = price
        self.number = len(Item.all)
        Item.all.append(self)

    @property
    def price_cost(self):
        return self.price / self.cost


class Solution:
    all_fitness = None

    def __init__(self, code):
        self.code = list(code) if isinstance(code, str) else code
        self.fitness = None

    @property
    def cost(self) -> int:
        return sum(Item.all[i].cost for i, char in enumerate(self.code) if char == '1')

    @property
    def price(self) -> int:
        return sum(Item.all[i].price for i, char in enumerate(self.code) if char == '1')

    @property
    def possibility(self) -> float:
        return self.fitness / Solution.all_fitness

    def __repr__(self):
        return ''.join(self.code)

    def clone(self) -> 'Solution':
        another = Solution(self.code[:])
        another.fitness = self.fitness
        return another


class EA:
    MAX_COST = 100
    MUTATE_RATE = 0.05

    @staticmethod
    def mark_penalty(solution_l: list):
        penalty_basis = max(EA.MAX_COST, abs(Item.all_cost() - EA.MAX_COST))
        for solution in solution_l:
            solution.fitness = solution.price * (1 - abs(solution.cost - EA.MAX_COST) / penalty_basis)
            assert 0 <= (1 - abs(solution.cost - EA.MAX_COST) / penalty_basis) <= 1

    @staticmethod
    def mark_repair(solution_l: list):
        for solution in solution_l:
            if solution.cost <= EA.MAX_COST:
                solution.fitness = solution.price
                continue

            curr_cost = solution.cost
            for del_item in sorted(Item.all, key=lambda item: item.price_cost):
                if solution.code[del_item.number] == '1':
                    solution.code[del_item.number] = '0'
                    curr_cost -= del_item.cost
                    if curr_cost <= EA.MAX_COST:
                        solution.fitness = solution.price
                        break

    @staticmethod
    def mark_rand_code(solution_l: list):
        for solution in solution_l:
            if solution.cost <= EA.MAX_COST:
                solution.fitness = solution.price
                continue

            next_code = []
            curr_cost = 0
            for i, char in enumerate(solution.code):
                if char == '0':
                    next_code.append(char)
                else:
                    item = Item.all[i]
                    if curr_cost + item.cost <= EA.MAX_COST:
                        curr_cost += item.cost
                        next_code.append(char)
                    else:
                        next_code.extend(('0' for _ in range(len(solution.code) - len(next_code))))
                        break

            solution.code = next_code
            solution.fitness = solution.price

    @staticmethod
    def select_roulette(solution_l: list):
        Solution.all_fitness = sum(i.fitness for i in solution_l)
        next_solution_l = []
        while len(next_solution_l) < len(solution_l):
            location = random()
            distance = 0
            for solution in solution_l:
                distance += solution.possibility
                if distance >= location:
                    next_solution_l.append(solution.clone())
                    break
        solution_l[:] = next_solution_l

    # sus = stochastic universal sampling
    @staticmethod
    def select_sus(solution_l: list):
        Solution.all_fitness = sum(i.fitness for i in solution_l)
        offset = 1 / len(solution_l)
        next_solution_l = []

        i = 0
        supply = 0
        demand = uniform(0, offset)
        while len(next_solution_l) < len(solution_l):
            solution = solution_l[i]

            supply += solution.possibility
            while demand <= supply:
                next_solution_l.append(solution.clone())
                demand += offset
            i += 1
        solution_l[:] = next_solution_l

    @staticmethod
    def crossover(solution_l: list):
        shuffle(solution_l)
        next_solution_l = []

        # 默认可以被2整除
        for i in range(len(solution_l) // 2):
            a = solution_l.pop()
            b = solution_l.pop()

            point = randint(1, len(Item.all) - 1)
            for head, tail in ((a, b), (b, a)):
                next_solution_l.append(Solution(head.code[:point] + tail.code[point:]))
        solution_l[:] = next_solution_l

    @staticmethod
    def mutate(solution_l: list):
        for solution in solution_l:
            if random() < EA.MUTATE_RATE:
                index = randint(0, len(solution.code) - 1)
                solution.code[index] = '1' if solution.code[index] == '0' else '0'


def rand_solution() -> Solution:
    code = ''
    for i in range(len(Item.all)):
        code += '1' if randint(0, 1) else '0'
    return Solution(code)


def inspect(solution_l: list):
    print(len(solution_l), int(sum(i.fitness for i in solution_l)))


if __name__ == '__main__':
    def main():
        for cost, price in ((40, 40), (50, 60), (30, 10), (10, 10), (10, 3), (40, 20), (30, 60)):
            Item(cost, price)

        solution_l = [rand_solution() for _ in range(100)]
        for i in range(100):
            for call in (EA.mark_repair,
                         EA.select_sus,
                         EA.crossover,
                         EA.mutate,
                         EA.mark_repair,
                         inspect):
                call(solution_l)


    main()
