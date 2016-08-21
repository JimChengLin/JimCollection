from random import uniform, shuffle, randint, random


def select(obj_l: iter, key: callable, num: int, clone_func: callable = None) -> list:
    result = []
    for obj in obj_l:
        setattr(obj, 'temp_fitness__', key(obj))

    total_fitness = sum(obj.temp_fitness__ for obj in obj_l)
    offset = 1 / num

    i = 0
    supply = 0
    demand = uniform(0, offset)
    while len(result) < num:
        obj = obj_l[i]

        supply += (obj.temp_fitness__ / total_fitness)
        while demand <= supply:
            result.append(obj)
            demand += offset
        i += 1

    if clone_func:
        result[:] = map(clone_func, result)
    return result


def crossover(code_l: iter, rate: float):
    shuffle(code_l)

    for i in range(0, len(code_l), 2):
        if rate < random():
            continue

        next_ab = []
        a = code_l[i]
        b = code_l[i + 1]

        point = randint(1, len(a) - 1)
        for head, tail in ((a, b), (b, a)):
            next_ab.append(head[:point] + tail[point:])
        a[:], b[:] = next_ab


def mutate(code_l: iter, func: callable, rate: float):
    for code in code_l:
        if rate < random():
            continue
        index = randint(0, len(code) - 1)
        code[index] = func(index)
