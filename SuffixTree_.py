g_target = ''


class Node:
    def __init__(self):
        self.sub = {}

        self.op = self.ed = None
        self.link_to = None

    @property
    def is_root(self):
        return self.op is None and self.ed is None

    @property
    def is_leaf(self):
        return not self.is_root and self.link_to is None

    @property
    def is_inner(self):
        return not self.is_root and self.link_to is not None

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

            for child in sorted(node.sub.values()):
                print_tree(child, level + 1)

        print_tree(self.root)
        print(self.__dict__)

    def insert(self, char: str):
        global g_target
        g_target += char

        self.remainder += 1

        def case_1():
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

        # 1. ac_node 是 root 的初始状态
        if self.ac_node.is_root and self.ac_offset == 0:
            case_1()

        # 2. 已经坍缩
        else:
            collapse_node = self.ac_node.sub[g_target[self.ac_direction]]

            # 2.1. 能否扩大坍缩? 可以
            if char == g_target[collapse_node.op + self.ac_offset]:
                # 2.1.1. 如果是 inner_node, 坍缩是否达已经到极限? 是
                if collapse_node.is_inner \
                        and collapse_node.op + self.ac_offset == collapse_node.ed:
                    # 推移 ac_node
                    self.ac_node = collapse_node
                    self.ac_direction = collapse_node.op + self.ac_offset
                    self.ac_offset = 1
                # 2.1.2. 一般情况
                else:
                    self.ac_offset += 1

            # 2.2. 无法继续坍缩, 炸开累积的后缀
            else:
                while self.remainder > 0:

                    # 2.2.1. 没有 suffix link 用于状态转移
                    if self.ac_node.link_to is None:
                        # 原坍缩点成为 inner_node
                        collapse_node.ed = collapse_node.op + self.ac_offset

                        # 新节点继承 :ed
                        inherit_node = Node()
                        inherit_node.op = collapse_node.ed
                        inherit_node.ed = ':ed'
                        # 回连
                        collapse_node.sub[g_target[inherit_node.op]] = inherit_node

                        # 新节点记录 char
                        leaf_node = Node()
                        leaf_node.op = self.cursor
                        leaf_node.ed = ':ed'
                        collapse_node.sub[g_target[leaf_node.op]] = leaf_node
                        self.remainder -= 1

                        # 状态转移, 继续爆炸
                        self.ac_offset -= 1
                        self.ac_direction += 1

                        if self.ac_offset > 0:
                            next_collapse_node = self.ac_node.sub[g_target[self.ac_direction]]
                            collapse_node.link_to = next_collapse_node
                            collapse_node = next_collapse_node

                        # 累积后缀已炸完
                        else:
                            # 回到状态 1.
                            collapse_node.link_to = self.root
                            case_1()

                    # 2.2.2. 需要运用 suffix link
                    else:
                        print()
                        pass
        self.cursor += 1


if __name__ == '__main__':
    t = SuffixTree()
    t.insert('x')
    t.insert('y')
    t.insert('z')
    t.insert('x')
    t.insert('y')
    t.insert('a')
    t.insert('x')
    t.insert('y')
    t.insert('z')
    t.insert('$')
    t.repr()
