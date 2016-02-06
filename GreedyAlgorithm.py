from typing import List
from math import inf


def get_value(x):
    return x[1]


def heapify(root: List, node_index=0):
    def get_left_index(index):
        return index * 2 if index != 0 else 1

    def get_right_index(index):
        return get_left_index(index) + 1

    left_index = get_left_index(node_index)
    right_index = get_right_index(node_index)

    node_index_list = [index for index in (node_index, left_index, right_index) if index < len(root)]
    if not node_index_list:
        return
    min_node_index = min(node_index_list, key=lambda index: get_value(root[index]))

    if min_node_index != node_index:
        root[node_index], root[min_node_index] = root[min_node_index], root[node_index]
        heapify(root, min_node_index)


def build(root: List):
    for i in reversed(range(round(len(root) / 2))):
        heapify(root, i)


def set_value(small_first_q: List, node_index: int, node):
    def get_parent_index(node_index):
        return node_index - (2 - (node_index % 2))

    original_value = get_value(small_first_q[node_index])
    small_first_q[node_index] = node
    node = get_value(node)

    if original_value < node:
        heapify(small_first_q, node_index)

    elif original_value > node:
        while node_index != 0:
            parent_index = get_parent_index(node_index)
            if get_value(small_first_q[parent_index]) > get_value(small_first_q[node_index]):
                small_first_q[parent_index], small_first_q[node_index] = small_first_q[node_index], small_first_q[
                    parent_index]
                node_index = parent_index
            else:
                break


def insert(small_first_q: List, node):
    small_first_q.append((None, inf))
    set_value(small_first_q, len(small_first_q) - 1, node)


def get_min(small_first_q: List):
    return small_first_q[0]


def pop_min(small_first_q: List):
    result = small_first_q.pop(0)
    heapify(small_first_q)
    return result


def heap_sort(root: List) -> List:
    result = []
    build(root)
    while root:
        heapify(root)
        result.append(pop_min(root))
    return result


codes = [('a', 45), ('b', 13), ('c', 12), ('d', 16), ('e', 9), ('f', 5)]


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key

    def __getitem__(self, *_):
        return self.key


def huffman_tree(codes):
    build(codes)
    while len(codes) != 1:
        min_a = pop_min(codes)
        min_b = pop_min(codes)
        node = Node(min_a[1] + min_b[1])
        node.left = min_a
        node.right = min_b
        insert(codes, node)
    print()


huffman_tree(codes)
