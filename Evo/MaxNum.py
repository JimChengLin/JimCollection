from random import randint, random

BIT_NUM = 5
ACCEPT_RATE = 0.1


def rand_individual() -> int:
    individual = 0
    for i in range(BIT_NUM):
        individual <<= 1
        individual |= randint(0, 1)
    return individual


def obj_func(individual: int) -> int:
    return individual ** 2


def get_mask(n_1: int, n_0=0) -> int:
    mask = 0
    for i in range(n_1):
        mask <<= 1
        mask |= 1
    for i in range(n_0):
        mask <<= 1
    return mask


def select(population: list):
    total = 1
    group = []
    for i in population:
        fitness = obj_func(i)
        group.append(fitness)
        total += fitness

    next_population = []
    for index, fitness in enumerate(group):
        prob = round(fitness / total * len(population))
        for i in range(prob):
            next_population.append(population[index])

    while len(next_population) < len(population):
        next_population.append(next_population[0])
    while len(next_population) > len(population):
        del next_population[0]
    population[:] = next_population


def crossover(population: list):
    for i in range(len(population) // 2):
        a = population.pop(0)
        b = population.pop(0)

        head_len = randint(1, BIT_NUM - 1)
        tail_len = BIT_NUM - head_len
        head_mask = get_mask(head_len, tail_len)
        tail_mask = get_mask(tail_len)

        for head, tail in ((a, b), (b, a)):
            # 对齐
            child = head & (head_mask & get_mask(head.bit_length()))
            # 补全
            child <<= BIT_NUM - child.bit_length()
            child |= (tail & tail_mask)
            assert child.bit_length() <= BIT_NUM
            population.append(child)


def mutate(population: list):
    for i in range(len(population)):
        individual = population[i]
        mask = 2 ** randint(1, BIT_NUM - 1)

        if randint(0, 1):
            value = individual & mask
        else:
            value = individual ^ mask

        if value > individual or random() < ACCEPT_RATE:
            population[i] = value


if __name__ == '__main__':
    population = [rand_individual() for _ in range(10)]
    print('fitness:', sum(obj_func(i) for i in population))
    for i in range(100):
        select(population)
        crossover(population)
        mutate(population)
    print(*('{:5b}'.format(i) for i in population))
    print('fitness:', sum(obj_func(i) for i in population))
