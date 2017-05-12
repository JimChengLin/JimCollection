from math import log2

DEBUG = True

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~'

init_table = {}
update_table = {}


class BitPack:
    def __init__(self, length, val):
        self.length = length
        self.val = val

    def __repr__(self):
        return f'0b{self.val:0{self.length}b}'

    def __add__(self, other):
        self.length += other.length
        self.val <<= other.length
        self.val |= other.val
        return self


# 初始化翻译表
# m = 2^e + r
e = int(log2(len(ALPHABET)))
r = len(ALPHABET) - 2 ** e
k = 2 * r

cnt = r
i = None
for i in range(len(ALPHABET) - k):
    init_table[ALPHABET[i]] = BitPack(e, cnt)
    cnt += 1

cnt = 0
for j in range(i + 1, i + 1 + k):
    init_table[ALPHABET[j]] = BitPack(e + 1, cnt)
    cnt += 1

if DEBUG:
    for k, v in init_table.items():
        print(k, v)
    print()


class Node:
    def __init__(self):
        self.parent = None
        self.left = None
        self.right = None

        self.weight = 0

    def __repr__(self):
        for k, v in update_table.items():
            if v is self:
                return k + ' ' + str(self.weight)
        return 'INNER ' + str(self.weight)


class Tree:
    def __init__(self):
        self.root = Node()
        self.NYT = self.root
        update_table['NYT'] = self.NYT

    def encode(self, char: str) -> BitPack:
        # 不存在, 新建节点
        if char not in update_table:
            cnt = 0
            code = 0
            cursor = self.NYT
            while cursor.parent is not None:
                cnt += 1

                if cursor is cursor.parent.left:
                    code <<= 1
                else:
                    assert cursor is cursor.parent.right
                    code <<= 1
                    code |= 1
                cursor = cursor.parent
            res = BitPack(cnt, code) + init_table[char]

            nyt_parent = Node()
            nyt_parent.weight += 1
            new_char_node = Node()
            new_char_node.weight += 1

            nyt_parent.left = self.NYT
            self.NYT.parent, nyt_parent.parent = nyt_parent, self.NYT.parent
            nyt_parent.right = new_char_node
            new_char_node.parent = nyt_parent

            if self.NYT is self.root:
                self.root = nyt_parent
                self.root.parent = None
            else:
                nyt_parent.parent.left = nyt_parent
            update_table[char] = new_char_node

            char_node = new_char_node

            def swap_node(a, b):
                a_s = str(a)
                b_s = str(b)
                if 'INNER' not in a_s:
                    update_table[str(a)[0]] = b
                if 'INNER' not in b_s:
                    update_table[str(b)[0]] = a
                a.__dict__, b.__dict__ = b.__dict__, a.__dict__
                # if a.parent:
                #     if a.parent.left is a:
                #         a.parent.left = b
                #     else:
                #         a.parent.right = b
                # if b.parent:
                #     if b.parent.left is b:
                #         b.parent.left = a
                #     else:
                #         b.parent.right = a
                # a.parent, b.parent = b.parent, a.parent
                #
                # if b is self.root:
                #     self.root = a

            def go_up_node(priority_target):
                nonlocal char_node
                if priority_target is self.root and priority_target.right.weight >= char_node.weight:
                    priority_target.weight = 0
                    if priority_target.left:
                        priority_target.weight += priority_target.left.weight
                    if priority_target.right:
                        priority_target.weight += priority_target.right.weight
                    return

                # 优先向上跑, 其次向右跑
                if priority_target.weight < char_node.weight:
                    # 能不能继续跑?
                    if priority_target.parent \
                            and priority_target.parent.weight < char_node.weight:
                        return go_up_node(priority_target.parent)

                    swap_node(char_node, priority_target)
                elif priority_target.right.weight < char_node.weight:
                    swap_node(char_node, priority_target.right)

                # 更新parent的weight
                if char_node.parent:
                    char_node.parent.weight = 0
                    if char_node.parent.left:
                        char_node.parent.weight += char_node.parent.left.weight
                    if char_node.parent.right:
                        char_node.parent.weight += char_node.parent.right.weight

                    if char_node.parent.parent:
                        char_node = char_node.parent
                        go_up_node(char_node.parent)

            if new_char_node.parent:
                go_up_node(new_char_node.parent)

        # 存在, 返回值并更新
        else:
            cnt = 0
            code = 0
            char_node = update_table[char]
            cursor = char_node
            while cursor.parent is not None:
                cnt += 1

                if cursor is cursor.parent.left:
                    code <<= 1
                else:
                    assert cursor is cursor.parent.right
                    code <<= 1
                    code |= 1
                cursor = cursor.parent

            res = BitPack(cnt, code)

            # 更新 weight
            char_node.weight += 1

            def swap_node(a, b):
                if a.parent:
                    if a.parent.left is a:
                        a.parent.left = b
                    else:
                        a.parent.right = b
                if b.parent:
                    if b.parent.left is b:
                        b.parent.left = a
                    else:
                        b.parent.right = a
                a.parent, b.parent = b.parent, a.parent

                if b is self.root:
                    self.root = a

            def go_up_node(priority_target):
                nonlocal char_node
                if priority_target is self.root:
                    priority_target.weight = 0
                    if priority_target.left:
                        priority_target.weight += priority_target.left.weight
                    if priority_target.right:
                        priority_target.weight += priority_target.right.weight
                    return

                    # 优先向上跑, 其次向右跑
                if priority_target.weight < char_node.weight:
                    # 能不能继续跑?
                    if priority_target.parent \
                            and priority_target.parent.weight < char_node.weight:
                        return go_up_node(priority_target.parent)

                    swap_node(char_node, priority_target)
                elif priority_target.right.weight < char_node.weight:
                    swap_node(char_node, priority_target.right)

                # 更新parent的weight
                if char_node.parent:
                    char_node.parent.weight = 0
                    if char_node.parent.left:
                        char_node.parent.weight += char_node.parent.left.weight
                    if char_node.parent.right:
                        char_node.parent.weight += char_node.parent.right.weight

                    if char_node.parent.parent:
                        char_node = char_node.parent
                        go_up_node(char_node.parent)

            if char_node.parent:
                go_up_node(char_node.parent)
        return res

    def __repr__(self):
        res = ''

        def print_node(node, lv=0):
            nonlocal res

            if not node:
                return

            if lv == 0:
                prefix = ''
            else:
                prefix = '  ' * (lv - 1) + '  '

            res += prefix + str(node) + '\n'
            print_node(node.left, lv + 1)
            print_node(node.right, lv + 1)

        print_node(self.root)
        return res


if __name__ == '__main__':
    source = 'aardv'
    tree = Tree()
    for i in source:
        res = tree.encode(i)
        print('Out: ', i, res, 'orig', init_table[i])
        print(tree)
