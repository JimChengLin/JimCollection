from math import log
from typing import Generic, TypeVar, List, Tuple, Optional

T = TypeVar('T')


def log2(x):
    return log(x, 3)


class Node(Generic[T]):
    def __init__(self, val: T = None):
        assert isinstance(val, int)
        self.val = val

        self.small: Node = None
        self.big: Node = None

    def print(self, lv=0):
        intent = '    '
        print(intent * lv, 'val: {}'.format(self.val))
        if self.small is self.big and self.big is None:
            return

        lv += 1
        for sub in (self.small, self.big):
            if sub is None:
                print(intent * lv, '-')
            else:
                sub.print(lv)

    def __repr__(self):
        return str(self.val)


class ScapegoatTree(Generic[T]):
    def __init__(self):
        self.size = 0
        self.root: Node = None

    def insert(self, val: T):
        if self.root is None:
            self.root = Node(val)

        height = 0
        path: List[Node] = []  # record parents

        # insert like BST
        cursor: Node = self.root
        while True:
            if cursor.val == val:
                # already exist
                return

            height += 1
            # go down
            path.append(cursor)
            if val < cursor.val:
                cursor = cursor.small

                if cursor is None:
                    self.size += 1
                    cursor = path[-1].small = Node(val)
                    break
            else:
                cursor = cursor.big

                if cursor is None:
                    self.size += 1
                    cursor = path[-1].big = Node(val)
                    break

        # check if need rebuild
        if height > log(self.size, 1 / 0.75):
            self.print()
            self.rebuild(*self.find_scapegoat(path, cursor))

    def rebuild(self, scapegoat: Node, scapegoat_parent: Node):
        ordered_nodes: List[Node] = []

        def add(node: Node):
            if node.small:
                add(node.small)
            ordered_nodes.append(node)
            if node.big:
                add(node.big)

        add(scapegoat)

        def pick_mid(op: int, ed: int) -> int:
            return (op + ed) // 2

        def build_node(op: int, ed: int) -> Optional[Node]:
            if op > ed:
                return None
            if op == ed:
                return Node(ordered_nodes[op].val)

            mid_point = pick_mid(op, ed)
            val = ordered_nodes[mid_point].val

            ret_node = Node(val)
            ret_node.small = build_node(op, mid_point - 1)
            ret_node.big = build_node(mid_point + 1, ed)
            return ret_node

        re_node = build_node(0, len(ordered_nodes) - 1)
        if scapegoat_parent is None:
            self.root = re_node
        elif scapegoat_parent.small is scapegoat:
            scapegoat_parent.small = re_node
        else:
            scapegoat_parent.big = re_node

    @staticmethod
    def find_scapegoat(path: List[Node], cursor: Node) -> Tuple[Node, Node]:
        size = 1
        height = 0

        scapegoat_parent = None
        while path:
            parent = path.pop()
            if parent.small is cursor:
                sibling = parent.big
            else:
                sibling = parent.small

            height += 1
            size += ScapegoatTree.get_size(sibling) + 1
            # if parent is balanced
            if height > log(size, 1 / 0.75):  # unbalanced
                scapegoat_parent = parent
                break
            cursor = parent
        return cursor, scapegoat_parent

    @staticmethod
    def get_size(node: Node) -> int:
        if node is None:
            return 0
        size_of_small = ScapegoatTree.get_size(node.small) if node.small is not None else 0
        size_of_big = ScapegoatTree.get_size(node.big) if node.big is not None else 0
        return size_of_small + size_of_big + 1

    def print(self):
        if self.root is None:
            print('empty')
        else:
            self.root.print()


if __name__ == '__main__':
    # n7 = Node(7)
    # n5 = Node(5)
    # n3 = Node(3)
    # n6 = Node(6)
    # n8 = Node(8)
    # n9 = Node(9)
    #
    # n7.small = n5
    # n7.big = n8
    #
    # n5.small = n3
    # n5.big = n6
    #
    # n8.big = n9
    #
    # tree = ScapegoatTree()
    # tree.size = 6
    # tree.root = n7
    # tree.print()
    #
    # tree.insert(10)
    # tree.print()
    n5 = Node(5)
    n2 = Node(2)
    n8 = Node(8)
    n3 = Node(3)
    n9 = Node(9)
    n12 = Node(12)

    n5.small = n2
    n5.big = n8
    n2.big = n3
    n8.big = n9

    tree = ScapegoatTree()
    tree.root = n5
    tree.size = 5
    tree.print()

    tree.insert(12)
    for i in range(100):
        tree.insert(i)
    print('---\n')
    tree.print()
