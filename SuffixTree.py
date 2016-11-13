def print_tree(node, fn_sub, fn_str, level=0):
    '''
    图形化打印
    '''
    if level == 0:
        prefix = ''
    elif level == 1:
        prefix = '-- '
    else:
        prefix = '  ' * (level - 1) + '-- '
    print(prefix + fn_str(node))

    for child in fn_sub(node):
        print_tree(child, fn_sub, fn_str, level + 1)


target = 'xyzxyaxyz$'


class Node:
    '''
    后缀树节点
    '''

    def __init__(self):
        self.sub_d = {}

        # None 表示 root
        self.op = None
        self.ed = None

        # 可升级成 internal node
        self.suffix_link_to = None

    def __repr__(self):
        if self.op is None:
            return ':root'

        if self.ed == 'END':
            ed = end
        else:
            ed = self.ed
        return target[self.op:ed] + ' {} {}'.format(self.op, ed)

    def __lt__(self, other):
        return str(self) < str(other)


root = Node()

remaining = 0
active_node = root
active_direction = -1
active_len = 0
end = 0


def insert(char: str):
    global remaining, active_node, active_direction, active_len, end

    # 任何情况 remaining 都要+1
    remaining += 1

    # 可以直接从 sub_d 比较
    if active_len == 0:
        # 最简单的, 不重复, 新添加一个 Node 的情况
        if char not in active_node.sub_d:
            new_node = Node()
            new_node.op = end
            new_node.ed = 'END'
            active_node.sub_d[char] = new_node
            remaining -= 1

        # 可以陷入坍缩
        else:
            collapse_node = active_node.sub_d[char]
            active_direction = collapse_node.op
            active_len += 1

    # 已经陷入坍缩, 进入坍缩点匹配
    else:
        collapse_node = active_node.sub_d[target[active_direction]]

        # 是否坍缩能扩大? 可以
        if char == str(collapse_node)[active_len]:
            active_len += 1

        # 无法坍缩, 把已有的后缀炸开
        else:
            # while remaining >= 0:
            # 没有 suffix link 的爆炸, 需要手动计算偏移量
            if collapse_node.suffix_link_to is None:
                while True:
                    # 原坍缩点退化成共有部分
                    collapse_node.ed = collapse_node.op + active_len

                    # 新建一个继承原有的点
                    inherit_node = Node()
                    inherit_node.op = collapse_node.ed
                    inherit_node.ed = 'END'
                    collapse_node.sub_d[target[inherit_node.op]] = inherit_node

                    # 再新建一个点用于当前的 char
                    new_char_node = Node()
                    new_char_node.op = end
                    new_char_node.ed = 'END'
                    collapse_node.sub_d[target[new_char_node.op]] = new_char_node
                    remaining -= 1

                    # 状态转移
                    active_len -= 1
                    if active_len > 0:
                        active_direction += 1
                        collapse_node = active_node.sub_d[target[active_direction]]

                    # active_len == 0 表明需要直接检测 sub_d
                    else:
                        assert active_node is root
                        if char in root.sub_d:
                            pass
                        else:
                            new_char_node = Node()
                            new_char_node.op = end
                            new_char_node.ed = 'END'
                            root.sub_d[char] = new_char_node
                            remaining -= 1
                        break

    # 任何情况 end 都会 +1
    end += 1


if __name__ == '__main__':
    insert('x')
    insert('y')
    insert('z')
    insert('x')
    insert('y')
    insert('a')

    print_tree(root, lambda node: sorted(node.sub_d.values()), str)
    print()
    print('remaining -', remaining)
    print('active_node -', active_node)
    print('active_direction -', active_direction)
    print('active_len -', active_len)
    print('end -', end)
