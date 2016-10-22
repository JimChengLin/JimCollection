from functools import lru_cache, total_ordering
from math import inf
from typing import List


@lru_cache()
def heap_size(degree):
    if degree == 0:
        return 1
    elif degree == 1:
        return 2
    else:
        return 2 * heap_size(degree - 1)


def degree_test():
    for i in range(10):
        size = heap_size(i)
        total = sum(heap_size(i) for i in reversed(range(i + 1)))
        print('Degree: {}; Size: {}; Total: {}'.format(i, size, total))


# -------------------------------------
@total_ordering
class FibNode:
    key = inf

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.is_child_deleted = False

        self.parent = FibNode
        self.children = []  # type: List[FibNode]

    def __lt__(self, other: 'FibNode'):
        return self.key < other.key

    def __eq__(self, other: 'FibNode'):
        return self.key == other.key

    def __repr__(self):
        return str(self.key)

    def __iter__(self):
        yield self
        for node in self.children:
            yield from node


class FibHeap:
    def __init__(self):
        self.min_node = FibNode
        self.children = []  # type: List[FibNode]

    def union(self, other: 'FibHeap'):
        self.children.extend(other.children)
        self.min_node = min(self.min_node, other.min_node)

    def push(self, key, value):
        push_node = FibNode(key, value)
        self.children.append(push_node)
        self.min_node = min(self.min_node, push_node)
        return push_node

    def pop(self):
        for node in self.min_node.children:
            node.parent = FibNode
        self.children.extend(self.min_node.children)
        self.children.remove(self.min_node)
        pop_node = self.min_node

        def merge(a: FibNode, b: FibNode) -> FibNode:
            if a < b:
                small, big = a, b
            else:
                small, big = b, a

            big.parent = small
            big.is_child_deleted = False
            small.children.append(big)
            return small

        bucket = {}
        for node in self.children:
            degree = len(node.children)

            while degree in bucket:
                node = merge(node, bucket.pop(degree))
                degree += 1
            bucket[degree] = node

        self.children = list(bucket.values())
        self.min_node = min(self.children + [FibNode])
        return pop_node

    def decrease(self, decrease_node: FibNode, key):
        assert key < decrease_node.key
        decrease_node.key = key

        def dispatch(dispatch_node: FibNode, parent: FibNode):
            parent.children.remove(dispatch_node)

            dispatch_node.parent = FibNode
            dispatch_node.is_child_deleted = False
            self.children.append(dispatch_node)

            grandparent = parent.parent
            if grandparent is not FibNode:
                if parent.is_child_deleted:
                    dispatch(parent, grandparent)
                else:
                    parent.is_child_deleted = True

        parent = decrease_node.parent
        if parent is not FibNode and parent > decrease_node:
            dispatch(decrease_node, parent)
        self.min_node = min(self.min_node, decrease_node)

    def delete(self, delete_node: FibNode):
        self.decrease(delete_node, -inf)
        self.pop()

    def __iter__(self):
        for node in self.children:
            yield from node


def fib_heap_test():
    fib_heap = FibHeap()
    for i in range(10):
        fib_heap.push(i, i)
    for i in fib_heap:
        print(i)
        if i.key == 6:
            i.key = 1
        fib_heap.decrease(i, i.key - 1)

    for i in fib_heap:
        print(i)

    for i in range(10):
        print(fib_heap.pop())


if __name__ == '__main__':
    fib_heap_test()
