M = ((0, 0, 1, 1 / 2),
     (1 / 3, 0, 0, 0),
     (1 / 3, 1 / 2, 0, 1 / 2),
     (1 / 3, 1 / 2, 0, 0))

V = (1 / 4,
     1 / 4,
     1 / 4,
     1 / 4)

FACTOR = 0.15


def calc_without_random() -> list:
    result = []
    for row in M:
        result.append(sum(a * b for a, b in zip(row, V)))
    return result


def trans(val: float) -> float:
    return val * (1 - FACTOR) + FACTOR * (1 / 4)


def calc_with_random() -> list:
    result = []
    for row in M:
        result.append(sum(trans(a) * b for a, b in zip(row, V)))
    return result


M_DICT = {0: {2: 1, 3: 1 / 2},
          1: {0: 1 / 3},
          2: {0: 1 / 3, 1: 1 / 2, 3: 1 / 2},
          3: {0: 1 / 3, 1: 1 / 2}}


def calc_dict_without_random():
    result = []
    for i_col in range(4):
        total = 0
        for i_row in range(4):
            total += M_DICT[i_col].get(i_row, 0) * V[i_row]
        result.append(total)
    return result


def calc_dict_with_random():
    result = []
    for i_col in range(4):
        total = 0
        for i_row in range(4):
            total += trans(M_DICT[i_col].get(i_row, 0)) * V[i_row]
        result.append(total)
    return result


# 以下全部默认添加阻尼系数
# -1表示权重
M_DICT_WEIGHT = {0: {2: 1, 3: 1 / 2, -1: 1},
                 1: {0: 1 / 3, -1: 2},
                 2: {0: 1 / 3, 1: 1 / 2, 3: 1 / 2, -1: 3},
                 3: {0: 1 / 3, 1: 1 / 2, -1: 4}}


def calc_dict_with_weight():
    result = []
    for i_col in range(4):
        total = 0
        for i_row in range(4):
            total += trans(M_DICT[i_col].get(i_row, 0)) * V[i_row]
        total += M_DICT_WEIGHT[i_col][-1] * (1 / 4)
        result.append(total)
    return result


if __name__ == '__main__':
    print(calc_without_random())
    print(calc_dict_without_random())
    print(calc_with_random())
    print(calc_dict_with_random())
    print(calc_dict_with_weight())
