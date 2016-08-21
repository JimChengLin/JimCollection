from math import exp
from random import randint, random

ITER_NUM_PER = 100
START_T = 1000000
STOP_T = 10


def calc_poss(diff: float, temperature: float) -> float:
    return exp(-diff / temperature)


def de(temperature: float) -> float:
    return temperature * 0.999


def swap(target: list) -> tuple:
    a = randint(0, len(target) - 1)
    b = randint(0, len(target) - 1)
    target[a], target[b] = target[b], target[a]
    return a, b


def obj_func(target: list) -> int:
    diff = 0
    for i in range(1, len(target)):
        diff += abs(target[i] - target[i - 1])
    return diff


def sa_fab(target: list, iter_num: int, temperature: float, temp=[]) -> callable:
    curr_mark = obj_func(target)
    a, b = swap(target)
    next_mark = obj_func(target)

    if not (next_mark < curr_mark or calc_poss(next_mark - curr_mark, temperature) > random()):
        target[a], target[b] = target[b], target[a]

    iter_num += 1
    if iter_num >= ITER_NUM_PER:
        temperature = de(temperature)

    if temperature > STOP_T:
        print(curr_mark, next_mark)
        if not temp:
            temp.append(min(curr_mark, next_mark))
        else:
            temp.append(min(min(curr_mark, next_mark), temp.pop()))
        return lambda: sa_fab(target, iter_num, temperature)
    else:
        print(temp.pop())


if __name__ == '__main__':
    RAND_LIST = [randint(1, 100) for _ in range(100)]
    seed = sa_fab(RAND_LIST, 10, START_T)
    while seed:
        seed = seed()
