from math import log2
from typing import List

sample = [1, 5, 7, 19, 10, 7, 15, 19, 16]


class NamedList:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        if self.key:
            return '({}, {})'.format(self.key, self.value)
        else:
            return str(self.value)


def n_bit(integer: int) -> int:
    n = 0
    while integer:
        integer >>= 1
        n += 1
    return n


def bit_int(n: int) -> int:
    integer = 0
    for i in range(n):
        integer <<= 1
        integer |= 1
    return integer


def radix_sort(values: List[int]) -> List[int]:
    max_bit = max([n_bit(i) for i in values])
    radius = int(log2(max_bit))
    mask = bit_int(radius)

    bucket = []
    for i in range(mask + 1):
        bucket.append([])

    values = [NamedList(value, value) for value in values]

    counter = 0
    while counter < len(values):

        for value in values:
            if value.key:
                target = (value.key & mask)
                bucket[target].append(value)

                value.key >>= radius
                if not value.key:
                    counter += 1
            else:
                bucket[0].append(value)

        index = 0
        for group in bucket:
            for value in group:
                values[index] = value
                index += 1
            group.clear()
    return values


print(radix_sort(sample))
