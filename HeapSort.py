from numbers import Number
from typing import List

sample = [1, 4, 1, 6, 9, 0, 2]


def heapify(root: List[Number], parent_node=0):
    def left(index):
        return index * 2 if index != 0 else 1

    def right(index):
        return left(index) + 1

    left_node = left(parent_node)
    right_node = right(parent_node)

    nodes = [node for node in (parent_node, left_node, right_node) if node < len(root)]
    max_node = max(nodes, key=lambda node: root[node])

    if max_node != parent_node:
        root[parent_node], root[max_node] = root[max_node], root[parent_node]
        heapify(root, max_node)


def build(root: List[Number]):
    for i in reversed(range(len(root) // 2)):
        heapify(root, i)


def heap_sort(root: List[Number]) -> List[Number]:
    result = []
    build(root)

    while root:
        heapify(root)
        result.insert(0, root.pop(0))

    return result


print(heap_sort(sample))

sample = [1, 4, 1, 6, 9, 0, 2]
build(sample)


def get_max(priority_q: List[Number]):
    return priority_q[0]


print(get_max(sample))


def pop_max(priority_q: List[Number]):
    result = priority_q.pop(0)
    heapify(priority_q)
    return result


print(pop_max(sample))


def set_value(priority_q: List[Number], current_node: int, value: Number):
    def parent(node):
        return node - (2 - (node % 2))

    original_value = priority_q[current_node]
    priority_q[current_node] = value

    if original_value < value:
        while current_node != 0:

            parent_node = parent(current_node)
            if priority_q[parent_node] < priority_q[current_node]:
                priority_q[parent_node], priority_q[current_node] = priority_q[current_node], priority_q[parent_node]
                current_node = parent_node
            else:
                break

    elif original_value > value:
        heapify(priority_q, current_node)

print(sample)
set_value(sample, 2, 10)
print(sample)


def insert(priority_q: List[Number], value: Number):
    priority_q.append(float('-inf'))
    set_value(priority_q, len(priority_q) - 1, value)


insert(sample, 14)
print(sample)
