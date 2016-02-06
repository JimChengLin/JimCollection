from math import inf
from functools import lru_cache
from time import time

price_tuple = (1, 5, 8, 9, 10, 17, 17, 20, 24, 30)


def cut_rob(price_tuple: tuple, length: int):
    if length == 0:
        return 0

    revenue = -inf
    for i in range(1, min(len(price_tuple), length) + 1):
        revenue = max(revenue, price_tuple[i - 1] + cut_rob(price_tuple, length - i))
    return revenue


@lru_cache(100)
def cut_rob_cached(price_tuple: tuple, length: int):
    if length == 0:
        return 0

    revenue = -inf
    for i in range(1, min(len(price_tuple), length) + 1):
        revenue = max(revenue, price_tuple[i - 1] + cut_rob_cached(price_tuple, length - i))
    return revenue


def cut_rob_bottom_up(price_tuple: tuple, length: int):
    revenue_cache = [0]

    for n in range(1, length + 1):
        revenue = -inf
        for i in range(1, min(n, len(price_tuple)) + 1):
            revenue = max(revenue, price_tuple[i - 1] + revenue_cache[n - i])
        revenue_cache.append(revenue)
    return revenue


go_time = time()
for i in range(10000):
    result = cut_rob_cached(price_tuple, 8)
end_time = time()
print(result)
print(int(end_time - go_time))

go_time = time()
for i in range(10000):
    result = cut_rob_bottom_up(price_tuple, 8)
end_time = time()
print(result)
print(int(end_time - go_time))


def cut_rob_bottom_up_record(price_tuple: tuple, length: int):
    revenue_cache = [0]
    best_move_list = [0]

    for n in range(1, length + 1):
        revenue = -inf
        best_move_list.append(0)

        for i in range(1, min(n, len(price_tuple)) + 1):
            curr_revenue = price_tuple[i - 1] + revenue_cache[n - i]
            if curr_revenue > revenue:
                revenue = curr_revenue
                best_move_list[n] = i

        revenue_cache.append(revenue)
    return revenue, best_move_list


result, best_move_list = cut_rob_bottom_up_record(price_tuple, 11)
print(result)
print(best_move_list)


def longest_common_string_cached(string_a: str, string_b: str):
    best_move_dic = {}

    @lru_cache()
    def get_longest_string_length(a_index: int, b_index: int):
        if a_index == -1 or b_index == -1:
            return 0

        if string_a[a_index] == string_b[b_index]:
            best_move_dic[(a_index, b_index)] = (a_index - 1, b_index - 1)
            return get_longest_string_length(a_index - 1, b_index - 1) + 1

        else:
            longest_common_string_len_except_a = get_longest_string_length(a_index - 1, b_index)
            longest_common_string_len_except_b = get_longest_string_length(a_index, b_index - 1)

            if longest_common_string_len_except_a >= longest_common_string_len_except_b:
                best_move_dic[(a_index, b_index)] = (a_index - 1, b_index)
                return longest_common_string_len_except_a
            else:
                best_move_dic[(a_index, b_index)] = (a_index, b_index - 1)
                return longest_common_string_len_except_b

    return get_longest_string_length(len(string_a) - 1, len(string_b) - 1), best_move_dic


X = 'BDCABA'
Y = 'ABCBDAB'
length, best_move_dic = longest_common_string_cached(X, Y)

successful_key_probability = (None, 0.15, 0.1, 0.05, 0.1, 0.2)
failed_key_probability = (0.05, 0.1, 0.05, 0.05, 0.05, 0.1)


def optimal_binary_tree(successful_key_probability, failed_key_probability):
    best_root_dic = {}

    @lru_cache()
    def get_optimal_run_time(index_from, index_to):
        if index_to == index_from - 1:
            return failed_key_probability[index_to]

        run_time = inf
        for i in range(index_from, index_to + 1):
            aux_run_time = get_optimal_run_time(index_from, i - 1) + get_optimal_run_time(i + 1, index_to) + get_drift(
                index_from, index_to)
            if aux_run_time < run_time:
                best_root_dic[(index_from, index_to)] = i
                run_time = aux_run_time
        return run_time

    @lru_cache()
    def get_drift(index_from, index_to):
        if index_to == index_from - 1:
            return failed_key_probability[index_to]

        return get_drift(index_from, index_to - 1) + successful_key_probability[index_to] + failed_key_probability[
            index_to]

    return get_optimal_run_time(1, len(successful_key_probability) - 1), best_root_dic


run_time, best_root_dic = optimal_binary_tree(successful_key_probability, failed_key_probability)
print(run_time)
print()
