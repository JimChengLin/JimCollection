from numbers import Number
from typing import List

sample = [-1, -5, 7, 19, -10, 7, 15, 19, -16, 20, -5, 19]


def max_list(root: List[Number]) -> (Number, List[Number]):
    root_len = len(root)
    if root_len == 1:
        return root[0], root

    root_mid = root_len // 2
    return max(max_list(root[:root_mid]), max_list(root[root_mid:]), mid_max_list(root))


def mid_max_list(root: List[Number]) -> (Number, List[Number]):
    root_len = len(root)
    root_mid = root_len // 2

    left_index = right_index = None
    left_sum = right_sum = float('-inf')

    total = 0
    for left_cursor in reversed(range(root_mid)):
        total += root[left_cursor]

        if total > left_sum:
            left_sum = total
            left_index = left_cursor

    total = 0
    for right_cursor in range(root_mid, root_len):
        total += root[right_cursor]

        if total > right_sum:
            right_sum = total
            right_index = right_cursor

    return left_sum + right_sum, root[left_index:right_index + 1]


print(max_list(sample))
