from numbers import Number
from typing import List

sample = [-1, -5, 7, 19, -10, 7, 15, 19, -16, 20, -5, 19]


def partition(root: List[Number], index_from=0, index_to=None):
    if index_to is None:
        index_to = len(root) - 1
    if index_from >= index_to:
        return

    pivot = root[index_to]
    small_cursor = None
    for current_cursor in range(index_from, index_to):

        if root[current_cursor] < pivot:
            if small_cursor is None:
                small_cursor = index_from
            else:
                small_cursor += 1

            if small_cursor != current_cursor:
                root[small_cursor], root[current_cursor] = root[current_cursor], root[small_cursor]

    if small_cursor is None:
        small_cursor = index_from
    else:
        small_cursor += 1
    root[index_to], root[small_cursor] = root[small_cursor], root[index_to]

    if small_cursor < index_to:
        partition(root, index_from, small_cursor - 1)
        partition(root, small_cursor + 1, index_to)


partition(sample)
print(sample)
