class BinaryNode:
    def __init__(self):
        self.val = None
        self.parent = None

        self._small = None
        self._big = None

        self.inverse = False

    def toggle(self):
        self.inverse = not self.inverse

    @property
    def small(self):
        return self._small if not self.inverse else self._big

    @small.setter
    def small(self, val):
        if not self.inverse:
            self._small = val
        else:
            self._big = val
        val.parent = self

    @property
    def big(self):
        return self._big if not self.inverse else self._small

    @big.setter
    def big(self, val):
        if not self.inverse:
            self._big = val
        else:
            self._small = val
        val.parent = self

    def print(self, lv=0):
        intent = '    '
        print(intent * lv, 'val: {}'.format(self.val))

        if self._small is None and self._small is self._big:
            return

        lv += 1
        for sub in (self._small, self._big):
            if sub:
                sub.print(lv)
            else:
                print(intent * lv, 'nil')

    def what_direct(self, child):
        if self.small is child:
            return 'small'
        elif self.big is child:
            return 'big'
        else:
            raise Exception

    def __repr__(self):
        return str(self.val)


class SplayTree:  # 懒得写完所有操作
    def __init__(self):
        self.root = BinaryNode()

    def insert(self, val):
        if self.root.val is None:
            self.root.val = val
            return

        cursor = self.root
        while True:
            if val == cursor.val:
                break

            if val < cursor.val:
                if cursor.small is not None:
                    cursor = cursor.small
                else:
                    new_node = BinaryNode()
                    new_node.val = val
                    new_node.parent = cursor

                    cursor.small = new_node
                    cursor = new_node
                    break
            else:
                if cursor.big is not None:
                    cursor = cursor.big
                else:
                    new_node = BinaryNode()
                    new_node.val = val
                    new_node.parent = cursor

                    cursor.big = new_node
                    cursor = new_node
                    break
        self.move_top(cursor)

    def move_top(self, node: BinaryNode):
        # 因为, insert 导致的高度加一
        # 都会被 zig zig(直线型) 和 zig zag(之字形) 在一的时间内, 还原到 log(n) 高度
        # 两者副作用导致的高度增加也遵循 log(n)
        # 所以, splay tree 不断趋近于平衡树
        # 均摊分析可以理解为不断借债还老债, 但总资产是正数, 只不过在不断借债而已

        def toggle(*node_i):
            for i in node_i:
                i.toggle()

        def small_up(s):
            p = s.parent

            if p and p.parent:
                if p.parent.small is p:
                    p.parent.small = s
                elif p.parent.big is p:
                    p.parent.big = s
                else:
                    raise Exception
                s.parent = p.parent

            p.small = s.big
            s.big.parent = p

            s.big = p
            p.parent = s

            self.print()
            print()

        def big_up(b):
            p = b.parent

            toggle(p, b)
            small_up(b)
            toggle(p, b)

        parent = grand = None  # type: BinaryNode

        # <--- parent 是 root
        def zig():
            # node 处于 root.small 的情况
            self.root = node
            small_up(node)
            self.root.parent = None

        def zig_():
            toggle(node, parent)
            zig()
            toggle(node, parent)

        # --->

        # <--- 之字形
        def zig_zag():
            # small.big
            big_up(node)
            small_up(node)

        def zig_zag_():
            toggle(grand, parent, node)
            zig_zag()
            toggle(grand, parent, node)

        # --->

        # <--- 一字型
        def zig_zig():
            # small.small
            small_up(parent)
            small_up(node)

        def zig_zig_():
            toggle(grand, parent, node)
            zig_zig()
            toggle(grand, parent, node)

        # --->

        while True:
            parent = node.parent
            grand = parent.parent

            node_2_parent = parent.what_direct(node)
            if grand is None:
                if node_2_parent == 'small':
                    zig()
                else:
                    zig_()
                break

            parent_2_grand = grand.what_direct(parent)
            if node_2_parent == parent_2_grand:
                if node_2_parent == 'small':
                    zig_zig()
                else:
                    zig_zig_()
            else:
                if parent_2_grand == 'small':
                    zig_zag()
                else:
                    zig_zag_()

            if grand.parent is None:
                self.root = node
                self.root.parent = None

            print('------\n')
            self.print()
            print()

    def print(self):
        if self.root is not None:
            self.root.print()
        else:
            print('empty')


if __name__ == '__main__':
    def build_node(val):
        node = BinaryNode()
        node.val = val
        return node


    def t_0():
        n_11 = build_node(11)
        n_1 = build_node(1)
        n_12 = build_node(12)
        n_0 = build_node(0)
        n_9 = build_node(9)
        n_3 = build_node(3)
        n_10 = build_node(10)
        n_2 = build_node(2)
        n_5 = build_node(5)
        n_4 = build_node(4)
        n_7 = build_node(7)
        n_6 = build_node(6)
        n_8 = build_node(8)

        n_11.small = n_1
        n_11.big = n_12

        n_1.small = n_0
        n_1.big = n_9

        n_9.small = n_3
        n_9.big = n_10

        n_3.small = n_2
        n_3.big = n_5

        n_5.small = n_4
        n_5.big = n_7

        n_7.small = n_6
        n_7.big = n_8

        t = SplayTree()
        t.root = n_11

        t.print()
        t.move_top(n_7)


    t_0()
