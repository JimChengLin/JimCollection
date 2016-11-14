g_target = ''


class Node:
    def __init__(self):
        self.sub = {}

        self.op = self.ed = None
        self.ptr_to = None

    @property
    def is_root(self):
        return self.op is None and self.ed is None

    @property
    def is_leaf(self):
        return not self.is_root and self.ptr_to is None

    @property
    def is_inter(self):
        return not self.is_root and self.ptr_to is not None

    def __repr__(self):
        if self.is_root:
            return '<root>'
        else:
            op, ed = self.op, self.ed
            if ed == ':ed':
                ed = len(g_target)
            return g_target[op:ed] + ' {}:{}'.format(op, ed)

    def __lt__(self, other: 'Node'):
        return str(self) < str(other)


class SuffixTree:
    def __init__(self):
        self.root = Node()

        self.remainder = 0
        self.cursor = 0

        self.ac_node = self.root
        self.ac_direction = 0
        self.ac_offset = 0

    def repr(self):
        def print_tree(node: 'Node', level=0):
            if level == 0:
                prefix = ''
            elif level == 1:
                prefix = '-- '
            else:
                prefix = '  ' * (level - 1) + '-- '
            print(prefix + str(node))

            for child in reversed(sorted(node.sub.values())):
                print_tree(child, level + 1)

        print_tree(self.root)
        print(self.__dict__)

    def insert(self, char: str):
        global g_target
        g_target += char

        self.remainder += 1

        # 1. ac_node 是 root
        if self.ac_node.is_root and self.ac_offset == 0:

            # 1.1. 无法坍缩, 建立新的叶节点
            if char not in self.ac_node.sub:
                leaf_node = Node()
                leaf_node.op = self.cursor
                leaf_node.ed = ':ed'
                self.ac_node.sub[char] = leaf_node
                self.remainder -= 1

            # 1.2. 开始坍缩
            else:
                collapse_node = self.ac_node.sub[char]
                self.ac_direction = collapse_node.op
                self.ac_offset += 1

        # 2. 已经坍缩
        else:
            collapse_node = self.ac_node.sub[g_target[self.ac_direction]]

            # 2.1. 能否扩大坍缩? 可以
            if char == g_target[collapse_node.op + self.ac_offset]:
                self.ac_offset += 1

                # 2.1.1.如果是 inner_node, 坍缩是否达到极限? 是
                if collapse_node.is_inter \
                        and collapse_node.op + self.ac_offset == collapse_node.ed:
                    # todo: implement
                    pass

            # 2.2. 无法继续坍缩, 炸开累积的后缀
            else:
                while self.remainder > 0:

                    # 2.2.1. 没有 suffix link 用于状态转移
                    if collapse_node.ptr_to is None:
                        # todo: implement
                        pass

        self.cursor += 1


if __name__ == '__main__':
    t = SuffixTree()
    t.insert('x')
    t.insert('y')
    t.insert('z')
    t.insert('x')
    t.insert('y')
    t.repr()
