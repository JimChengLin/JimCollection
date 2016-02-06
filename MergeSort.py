from numbers import Number
from typing import List

sample = [1, 4, 6, 9, 0, 2, 6, 9, 1, 2, 6]


def divide(root: List[Number]) -> List[Number]:
    if len(root) > 1:
        mid = len(root) // 2
        return merge(divide(root[:mid]), divide(root[mid:]))
    else:
        return root


def merge(left: List[Number], right: List[Number]) -> List[Number]:
    result = []

    def make_generator(gen_obj):
        for i in (*gen_obj, StopIteration):
            yield i

    left_generator = make_generator(left)
    right_generator = make_generator(right)

    left_value = next(left_generator)
    right_value = next(right_generator)

    while True:

        if left_value < right_value:
            result.append(left_value)
            left_value = next(left_generator)
        else:
            result.append(right_value)
            right_value = next(right_generator)

        if left_value == StopIteration:
            result.extend([right_value, *(i for i in right_generator if i != StopIteration)])
            break
        elif right_value == StopIteration:
            result.extend([left_value, *(i for i in left_generator if i != StopIteration)])
            break

    return result


print(divide(sample))
