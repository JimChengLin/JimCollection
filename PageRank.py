M = ((0, 0, 1, 1 / 2),
     (1 / 3, 0, 0, 0),
     (1 / 3, 1 / 2, 0, 1 / 2),
     (1 / 3, 1 / 2, 0, 0))

V = (1 / 4,
     1 / 4,
     1 / 4,
     1 / 4)

DAMPING_FACTOR = 0.15


def calc_without_random() -> list:
    result = []
    for row in M:
        result.append(a * b for a, b in zip(row, V))
    return result


def trans(val: float) -> float:
    return val * (1 - DAMPING_FACTOR) + DAMPING_FACTOR * (1 / 4)


def calc_with_random() -> list:
    result = []
    for row in M:
        result.append(sum(trans(a) * b for a, b in zip(row, V)))
    return result


if __name__ == '__main__':
    print(calc_with_random())
