from bisect import bisect, insort
from functools import total_ordering
from typing import List


@total_ordering
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.key < other.key
        else:
            return self.key < other

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.key == other.key
        else:
            return self.key == other

    def __repr__(self):
        return str(self.key)


class BTreeNode:
    def __init__(self, is_leaf: bool):
        self.is_leaf = is_leaf
        self.nodes = []  # type: List[Node]
        if not is_leaf:
            self.children = []  # type: List[BTreeNode]

    def __repr__(self):
        return '|' + ', '.join(str(i) for i in self.nodes) + '|'


class BTree:
    def __init__(self, min_degree: int):
        self.min_degree = min_degree
        self.root = BTreeNode(is_leaf=True)

    def insert(self, key, value):
        def split_child(parent: BTreeNode, child_index: int):
            child = parent.children[child_index]
            median_next_index = (len(child.nodes) - 1) // 2 + 1

            sibling = BTreeNode(is_leaf=child.is_leaf)
            sibling.nodes = child.nodes[median_next_index:]
            del child.nodes[median_next_index:]
            if not sibling.is_leaf:
                sibling.children = child.children[median_next_index:]
                del child.children[median_next_index:]

            parent.nodes.insert(child_index, child.nodes.pop())
            parent.children.insert(child_index + 1, sibling)

        insert_node = Node(key, value)
        cursor = self.root
        if len(cursor.nodes) == 2 * self.min_degree - 1:
            root = BTreeNode(is_leaf=False)
            root.children.append(self.root)
            split_child(root, 0)
            cursor = self.root = root

        while not cursor.is_leaf:
            child_index = bisect(cursor.nodes, insert_node)
            child = cursor.children[child_index]
            if len(child.nodes) == 2 * self.min_degree - 1:
                split_child(cursor, child_index)
                if cursor.nodes[child_index] < insert_node:
                    child = cursor.children[child_index + 1]
            cursor = child
        insort(cursor.nodes, insert_node)

    def search(self, key):
        def travel(init_node: BTreeNode):
            index = bisect(init_node.nodes, key)
            if init_node.nodes[index - 1] == key:
                return init_node.nodes[index - 1]
            elif not init_node.is_leaf:
                return travel(init_node.children[index])

        return travel(self.root)

    def delete(self, key):
        def travel(init_node: BTreeNode, key):
            key_index = bisect(init_node.nodes, key) - 1

            if key_index >= 0 and init_node.nodes[key_index].key == key:
                if init_node.is_leaf:
                    del init_node.nodes[key_index]

                else:
                    left_child = init_node.children[key_index]
                    right_child = init_node.children[key_index + 1]

                    if len(left_child.nodes) >= self.min_degree:
                        last_node = left_child.nodes.pop()
                        ori_node = init_node.nodes[key_index]
                        init_node.nodes[key_index] = last_node
                        right_child.nodes.insert(0, ori_node)
                        if not left_child.is_leaf:
                            last_child = left_child.children.pop()
                            right_child.children.insert(0, last_child)
                        return travel(right_child, key)

                    elif len(right_child.nodes) >= self.min_degree:
                        first_node = right_child.nodes.pop(0)
                        ori_node = init_node.nodes[key_index]
                        init_node.nodes[key_index] = first_node
                        left_child.nodes.append(ori_node)
                        if not right_child.is_leaf:
                            first_child = right_child.children.pop(0)
                            left_child.children.append(first_child)
                        return travel(left_child, key)

                    else:
                        del_node = init_node.nodes[key_index]
                        del init_node.nodes[key_index]
                        del init_node.children[key_index + 1]

                        left_child.nodes.append(del_node)
                        left_child.nodes += right_child.nodes
                        if not left_child.is_leaf:
                            left_child.children += right_child.children
                        return travel(left_child, del_node.key)

            elif not init_node.is_leaf:
                key_index += 1
                left_sibling, cursor, right_sibling = (init_node.children[key_index + i]
                                                       if 0 <= key_index + i < len(init_node.children) else None
                                                       for i in (-1, 0, 1))

                if len(cursor.nodes) < self.min_degree:
                    if left_sibling and len(left_sibling.nodes) >= self.min_degree:
                        cursor.nodes.insert(0, init_node.nodes.pop(key_index - 1))
                        init_node.nodes.insert(key_index - 1, left_sibling.nodes.pop())
                        if not cursor.is_leaf:
                            cursor.children.insert(0, left_sibling.children.pop())

                    elif right_sibling and len(right_sibling.nodes) >= self.min_degree:
                        cursor.nodes.append(init_node.nodes.pop(key_index))
                        init_node.nodes.insert(key_index, right_sibling.nodes.pop(0))
                        if not cursor.is_leaf:
                            cursor.children.append(right_sibling.children.pop(0))

                    else:
                        if left_sibling:
                            del_node = init_node.nodes[key_index - 1]
                            del init_node.nodes[key_index - 1]
                            del init_node.children[key_index - 1]

                            cursor.nodes = [*left_sibling.nodes, del_node, *cursor.nodes]
                            if not cursor.is_leaf:
                                cursor.children = [*left_sibling.children, *cursor.children]

                        elif right_sibling:
                            del_node = init_node.nodes[key_index]
                            del init_node.nodes[key_index]
                            del init_node.children[key_index + 1]

                            cursor.nodes = [*cursor.nodes, del_node, *right_sibling.nodes]
                            if not cursor.is_leaf:
                                cursor.children = [*cursor.children, *right_sibling.children]

                        if init_node is self.root and len(self.root.nodes) == 0:
                            self.root = cursor

                return travel(cursor, key)

        travel(self.root, key)

    def __iter__(self):
        def travel(init_node: BTreeNode):
            if init_node.is_leaf:
                for node in init_node.nodes:
                    yield node
            else:
                for index, node in enumerate(init_node.nodes):
                    for sub_node in travel(init_node.children[index]):
                        yield sub_node
                    yield node
                for sub_node in travel(init_node.children[index + 1]):
                    yield sub_node

        return travel(self.root)


if __name__ == '__main__':
    from random import randint, choice

    STD = 5000


    def main():
        tree = BTree(min_degree=3)

        expected = set()
        for i in range(STD):
            expected.add(randint(0, STD))
        expected = list(expected)
        expected.sort()

        def test():
            output = [i for i in tree]
            if output == expected:
                return True
            else:
                return False

        for i in expected:
            tree.insert(i, i)

        for i in range(STD // 10):
            if randint(0, 1):
                i = choice(expected)
                print('del {}'.format(i))
                tree.delete(i)
                expected.remove(i)

            if not test():
                assert False

        for i in expected:
            assert i == tree.search(i)


    main()
