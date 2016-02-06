from collections import UserDict
from math import inf
from typing import Dict


class MapPivot(UserDict):
    def __getitem__(self, key):
        return self.data.setdefault(key, {})


def pivot(coeffs_eq: Dict[int, Dict[int, float]], consts_eq: Dict[int, float],
          coeffs_func: Dict[int, float], const_func: float,
          enter: int, leave: int):
    coeffs_eq_ret = MapPivot()  # type: Dict[int, Dict[int, float]]
    consts_eq_ret = MapPivot()  # type: Dict[int, float]
    coeffs_func_ret = MapPivot()  # type: Dict[int, float]

    # 交换enter与leave
    coeff = coeffs_eq[leave][enter]
    consts_eq_ret[enter] = consts_eq[leave] / coeff
    for x_index in coeffs_eq[leave]:
        if x_index == enter:
            continue
        coeffs_eq_ret[enter][x_index] = coeffs_eq[leave][x_index] / coeff
    coeffs_eq_ret[enter][leave] = 1 / coeff

    # 将等式代入原方程组
    const = consts_eq_ret[enter]
    for y_index in coeffs_eq:
        if y_index == leave:
            continue
        coeff = coeffs_eq[y_index][enter]

        consts_eq_ret[y_index] = consts_eq[y_index] + (- coeff * const)
        for x_index in coeffs_eq[y_index]:
            if x_index == enter:
                continue
            coeffs_eq_ret[y_index][x_index] = coeffs_eq[y_index][x_index] + (-coeff * coeffs_eq_ret[enter][x_index])
        coeffs_eq_ret[y_index][leave] = -coeff * coeffs_eq_ret[enter][leave]

    # 代入Objective Function
    coeff = coeffs_func[enter]
    const_func_ret = const_func + coeff * consts_eq_ret[enter]
    for x_index in coeffs_eq[leave]:
        if x_index == enter:
            continue
        coeffs_func_ret[x_index] = coeffs_func.setdefault(x_index, 0) - coeff * coeffs_eq_ret[enter][x_index]
    coeffs_func_ret[leave] = -coeff * coeffs_eq_ret[enter][leave]
    return coeffs_eq_ret, consts_eq_ret, coeffs_func_ret, const_func_ret


if __name__ == '__main__':
    def pivot_main():
        coeffs_eq = {1: {2: 1 / 16, 5: -1 / 8, 6: 5 / 16},
                     3: {2: 3 / 8, 5: 1 / 4, 6: -1 / 8},
                     4: {2: -3 / 16, 5: -5 / 8, 6: 1 / 16}}
        consts_eq = {1: 33 / 4,
                     3: 3 / 2,
                     4: 69 / 4}
        coeffs_func = {2: 1 / 16,
                       5: -1 / 8,
                       6: -11 / 16}
        const_func = 111 / 4
        result = pivot(coeffs_eq, consts_eq, coeffs_func, const_func, 2, 3)
        print(result)


# 输入格式与算导伪代码，略有不同
def init_simplex(coeffs_eq: Dict[int, Dict[int, float]], consts_eq: Dict[int, float], coeffs_func: Dict[int, float]):
    min_const_eq_index, min_const_eq = min(consts_eq.items(), key=lambda x: x[1])
    if min_const_eq >= 0:
        return coeffs_eq, consts_eq, coeffs_func, 0

    # 添加aux_x，下标0
    aux_coeffs_eq = {**coeffs_eq}
    for y_index in aux_coeffs_eq:
        aux_coeffs_eq[y_index][0] = -1
    aux_consts_eq = consts_eq
    aux_coeffs_func = {0: -1}
    aux_const_func = 0

    enter = 0
    leave = min_const_eq_index
    while True:
        aux_coeffs_eq, aux_consts_eq, aux_coeffs_func, aux_const_func = pivot(aux_coeffs_eq, aux_consts_eq,
                                                                              aux_coeffs_func, aux_const_func,
                                                                              enter, leave)
        for x_index in sorted(aux_coeffs_func.keys()):
            if aux_coeffs_func[x_index] > 0:
                enter = x_index

                leave = -1
                slack = inf
                for y_index in sorted(aux_coeffs_eq.keys()):
                    coeff = aux_coeffs_eq[y_index][enter]
                    if coeff > 0:
                        curr_slack = aux_consts_eq[y_index] / coeff
                        if curr_slack < slack:
                            slack = curr_slack
                            leave = y_index

                if leave == -1:
                    raise Exception
                else:
                    break

        # 没有正系数x在Objective Function
        else:
            break

    is_feasible = is_basic = False
    if 0 in aux_coeffs_func:
        is_feasible = True
    elif aux_consts_eq[0] == 0:
        is_feasible = is_basic = True

    if is_feasible:
        if is_basic:
            for x_index in aux_coeffs_eq[0]:
                if aux_coeffs_eq[0][x_index] != 0:
                    enter = x_index
                    break
            aux_coeffs_eq, aux_consts_eq, aux_coeffs_func, aux_const_func = pivot(aux_coeffs_eq, aux_consts_eq,
                                                                                  aux_coeffs_func, aux_const_func,
                                                                                  enter, 0)
        aux_const_func = 0
        for y_index in aux_coeffs_eq:
            del aux_coeffs_eq[y_index][0]
        del aux_coeffs_func[0]
        for i in aux_coeffs_func:
            aux_coeffs_func[i] = 0

        for ori_x_index in coeffs_func:
            if ori_x_index in aux_coeffs_eq:
                coeff = coeffs_func[ori_x_index]
                aux_y_index = ori_x_index

                aux_const_func += coeff * aux_consts_eq[aux_y_index]
                for aux_x_index in aux_coeffs_eq[aux_y_index]:
                    aux_coeffs_func[aux_x_index] += -coeff * aux_coeffs_eq[aux_y_index][aux_x_index]
            else:
                aux_coeffs_func[ori_x_index] += coeffs_func[ori_x_index]

        return aux_coeffs_eq, aux_consts_eq, aux_coeffs_func, aux_const_func
    else:
        raise Exception


if __name__ == '__main__':
    def init_main():
        coeffs_eq = {3: {1: 2, 2: -1},
                     4: {1: 1, 2: -5}}
        consts_eq = {3: 2,
                     4: -4}
        coeffs_func = {1: 2,
                       2: -1}
        result = init_simplex(coeffs_eq, consts_eq, coeffs_func)
        print(result)


    init_main()


def simplex(coeffs_eq: Dict[int, Dict[int, float]], consts_eq: Dict[int, float], coeffs_func: Dict[int, float]):
    coeffs_eq, consts_eq, coeffs_func, const_func = init_simplex(coeffs_eq, consts_eq, coeffs_func)

    while True:
        for x_index in sorted(coeffs_func.keys()):
            if coeffs_func[x_index] > 0:
                enter = x_index

                leave = -1
                slack = inf
                for y_index in sorted(coeffs_eq.keys()):
                    coeff = coeffs_eq[y_index][enter]
                    if coeff > 0:
                        curr_slack = consts_eq[y_index] / coeff
                        if curr_slack < slack:
                            slack = curr_slack
                            leave = y_index

                if leave == -1:
                    raise Exception
                else:
                    break
        else:
            break
        coeffs_eq, consts_eq, coeffs_func, const_func = pivot(coeffs_eq, consts_eq, coeffs_func, const_func,
                                                              enter, leave)
    
    for subscript, value in consts_eq.items():
        print('x_{}={}'.format(subscript, value))
    for subscript in coeffs_func:
        print('x_{}= 0'.format(subscript))


if __name__ == '__main__':
    def simplex_main():
        coeffs_eq = {4: {1: 1, 2: 1, 3: 3},
                     5: {1: 2, 2: 2, 3: 5},
                     6: {1: 4, 2: 1, 3: 2}}
        consts_eq = {4: 30,
                     5: 24,
                     6: 36}
        coeffs_func = {1: 3, 2: 1, 3: 2}
        simplex(coeffs_eq, consts_eq, coeffs_func)


    simplex_main()
