g_target = ''
repeat_l = []


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
        return not self.is_root and not self.sub

    @property
    def is_inner(self):
        return not self.is_root and self.sub

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
        repr_str = ''

        def print_tree(node: 'Node', level=0):
            nonlocal repr_str
            if level == 0:
                prefix = ''
            elif level == 1:
                prefix = '-- '
            else:
                prefix = '  ' * (level - 1) + '-- '
            repr_str += prefix + str(node) + '\n'

            for child in sorted(node.sub.values()):
                print_tree(child, level + 1)

        print_tree(self.root)
        repr_str += ', '.join(sorted('{}: {}'.format(k, v) for k, v in self.__dict__.items() if k != 'root'))
        print(repr_str)
        return repr_str

    def insert(self, char: str):
        global g_target
        g_target += char
        self.remainder += 1

        # offset 超过边长时的修正
        def overflow_fix():
            curr_collapse_node = self.ac_node.sub[g_target[self.ac_direction]]
            if not curr_collapse_node.is_leaf and self.ac_offset > curr_collapse_node.ed - curr_collapse_node.op:
                self.ac_node = curr_collapse_node
                self.ac_direction += 1
                self.ac_offset -= (curr_collapse_node.ed - curr_collapse_node.op)
                return overflow_fix()

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
                repeat_l.append((len(g_target) - 1, collapse_node.op))
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
                repeat_l.append((len(g_target) - 1, collapse_node.op + self.ac_offset))
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
                def split_grow():
                    if collapse_node.is_leaf or collapse_node.ed - collapse_node.op > 1:
                        # 新节点继承 :ed, sub
                        inherit_node = Node()
                        inherit_node.op = collapse_node.op + self.ac_offset
                        inherit_node.ed = collapse_node.ed
                        inherit_node.sub = collapse_node.sub

                        # 原坍缩点成为 inner_node
                        collapse_node.ed = inherit_node.op
                        collapse_node.sub = {g_target[inherit_node.op]: inherit_node}

                    # 新节点记录 char
                    leaf_node = Node()
                    leaf_node.op = self.cursor
                    leaf_node.ed = ':ed'
                    collapse_node.sub[g_target[leaf_node.op]] = leaf_node
                    self.remainder -= 1

                while self.remainder > 0:
                    # 2.2.1. 没有 suffix link
                    if not self.ac_node.is_inner:
                        split_grow()

                        # 状态转移
                        self.ac_offset -= 1
                        self.ac_direction += 1

                        if self.ac_offset > 0:
                            overflow_fix()

                            next_collapse_node = self.ac_node.sub[g_target[self.ac_direction]]
                            collapse_node.link_to = next_collapse_node
                            collapse_node = next_collapse_node

                        # 累积后缀已炸完
                        else:
                            # 进入 case 1.
                            collapse_node.link_to = self.root
                            case_1()
                            break

                    # 2.2.2. 需要运用 suffix link
                    else:
                        split_grow()
                        # 状态转移
                        self.ac_node = self.ac_node.link_to
                        overflow_fix()

                        next_collapse_node = self.ac_node.sub[g_target[self.ac_direction]]
                        collapse_node.link_to = next_collapse_node
                        collapse_node = next_collapse_node
                        # suffix link 消耗完之后. 自动进入 case 2.2.1.
        self.cursor += 1


class SuffixTreeDB(SuffixTree):
    def __setitem__(self, k, v):
        self.insert('[')
        for char in k:
            self.insert(char)
        self.insert(']')
        for char in v:
            self.insert(char)

    def __getitem__(self, k):
        result = ''

        try:
            cursor = self.root.sub[k[0]]
            offset = 0
            for require_char in k:
                if cursor.op + offset == cursor.ed:
                    cursor = cursor.sub[require_char]
                    offset = 0

                exist_char = g_target[cursor.op + offset]
                if exist_char != require_char:
                    return
                else:
                    offset += 1

            result += g_target[cursor.op + offset:cursor.ed if cursor.ed != ':ed' else None]
            while cursor.sub:
                cursor = cursor.sub.popitem()
                result += g_target[cursor.op:cursor.ed]
            return result
        except KeyError:
            return

    def __delitem__(self, k):
        pass


if __name__ == '__main__':
    def test_0():
        t = SuffixTree()
        for char in 'xyzxyaxyz$':
            t.insert(char)
        expect = '''
<root>
-- $ 9:10
-- axyz$ 5:10
-- xy 0:2
  -- axyz$ 5:10
  -- z 2:3
    -- $ 9:10
    -- xyaxyz$ 3:10
-- y 1:2
  -- axyz$ 5:10
  -- z 2:3
    -- $ 9:10
    -- xyaxyz$ 3:10
-- z 2:3
  -- $ 9:10
  -- xyaxyz$ 3:10
ac_direction: 3, ac_node: <root>, ac_offset: 0, cursor: 10, remainder: 0
'''
        assert t.repr() == expect.strip()
        repeat_l.clear()


    def test_1():
        global g_target
        g_target = ''

        t = SuffixTree()
        for char in 'mississi$':
            t.insert(char)
        expect = '''
<root>
-- $ 8:9
-- i 1:2
  -- $ 8:9
  -- ssi 2:5
    -- $ 8:9
    -- ssi$ 5:9
-- mississi$ 0:9
-- s 2:3
  -- i 4:5
    -- $ 8:9
    -- ssi$ 5:9
  -- si 3:5
    -- $ 8:9
    -- ssi$ 5:9
ac_direction: 5, ac_node: <root>, ac_offset: 0, cursor: 9, remainder: 0
'''
        assert t.repr() == expect.strip()
        repeat_l.clear()


    def test_2():
        global g_target
        g_target = ''

        t = SuffixTree()
        for char in 'abcabxabcd':
            t.insert(char)
        expect = '''
<root>
-- ab 0:2
  -- c 2:3
    -- abxabcd 3:10
    -- d 9:10
  -- xabcd 5:10
-- b 1:2
  -- c 2:3
    -- abxabcd 3:10
    -- d 9:10
  -- xabcd 5:10
-- c 2:3
  -- abxabcd 3:10
  -- d 9:10
-- d 9:10
-- xabcd 5:10
ac_direction: 3, ac_node: <root>, ac_offset: 0, cursor: 10, remainder: 0
'''
        assert t.repr() == expect.strip()
        repeat_l.clear()


    def test_3():
        global g_target
        g_target = ''

        db = SuffixTree()
        for char in '[abc]abcabxabcd':
            db.insert(char)
            db.repr()
            print(char)
            print()
            # db['abc'] = 'abcabxabcd'
            # print('val', db['[abc]'])


    # test_0()
    # test_1()
    # test_2()
    test_3()
