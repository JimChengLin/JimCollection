output_pool = []


class CBInternal:
    def __init__(self):
        self.diff_at = None
        self.mask = None
        self.crit_0 = None
        self.crit_1 = None

    def print(self, lv=0):
        intent = '    '
        print(intent * lv, 'diff_at: {}, mask: {}'.format(self.diff_at, self.mask))

        lv += 1
        for sub in (self.crit_0, self.crit_1):
            if isinstance(sub, CBInternal):
                sub.print(lv)
            else:
                output_pool.append(sub)
                print(intent * lv, sub)


class CBTree:
    def __init__(self):
        self.root = None
        self.break_point = None
        self.find_q = []

    def insert(self, new_bytes: bytes):
        if self.root is None:
            self.root = new_bytes
        else:
            grand, pa, old_bytes = self.find_best_match(new_bytes)
            # 查找哪个字节不同
            # 我在这里认为各个字符串一定会以 $ 结尾, 所以不考虑子串的问题
            for i in range(min(len(new_bytes), len(old_bytes))):
                if new_bytes[i] != old_bytes[i]:
                    diff_at = i
                    diff_byte = new_bytes[i] ^ old_bytes[i]
                    break
            else:
                return 'ALREADY_IN'

            # 查找哪个 bit 不同
            # 0b0100_1000 => 0b0111_1111
            diff_byte |= diff_byte >> 1
            diff_byte |= diff_byte >> 2
            diff_byte |= diff_byte >> 4

            # 结果: 0b0111_1111 => 0b1011_1111
            # 过程:
            # ~(diff_byte >> 1) = 0b1100_0000
            # diff_byte & 0b1100_0000 = 0b0111_1111 & 0b1100_0000 = 0b0100_0000
            mask = (diff_byte & ~(diff_byte >> 1)) ^ 255

            direct = (1 + (mask | new_bytes[diff_at])) >> 8
            # 生成一个新节点
            node = CBInternal()
            node.diff_at = diff_at
            node.mask = mask
            if direct == 0:
                node.crit_0 = new_bytes
            else:
                node.crit_1 = new_bytes

            # 插入节点:
            # 因为分歧点是按顺序发现的, 无论这次的分歧点在于路径上的前面还是后面
            # 都可以直接插入而保持性质不变
            # 即, 分歧顺序按照 1st 2nd 3rd 4th 排列
            # 比如, 当前在 3rd 处分歧. 那么, 剩余所有已存在的串 3rd 必然没有分歧
            parent = None
            insert_point = self.root  # 用 new_node 替换的节点
            while True:

                if isinstance(insert_point, bytes):
                    break
                else:
                    if insert_point.diff_at > diff_at:
                        break
                    elif insert_point.diff_at == diff_at and insert_point.mask > node.mask:
                        # 同 byte 位置, 分歧 bit 越靠后, 数值越小
                        break

                check_byte = new_bytes[insert_point.diff_at] if len(new_bytes) > insert_point.diff_at else 0
                direct = (1 + (insert_point.mask | check_byte)) >> 8

                parent = insert_point
                if direct == 0:
                    insert_point = insert_point.crit_0
                else:
                    insert_point = insert_point.crit_1

            if parent is None:
                self.root = node
            else:
                if direct == 0:
                    parent.crit_0 = node
                else:
                    parent.crit_1 = node

            if node.crit_0 is None:
                node.crit_0 = insert_point
            else:
                node.crit_1 = insert_point

    def delete(self, target: bytes):
        if self.root is None:
            return 'NOT_FOUND'

        grand, pa, des = self.find_best_match(target)
        if des != target:
            return 'NOT_FOUND'

        if pa is None:
            self.root = None
        elif grand is None:
            self.root = pa.crit_0 if des is pa.crit_1 else pa.crit_1
        else:
            if grand.crit_0 is pa:
                grand.crit_0 = pa.crit_0 if des is pa.crit_1 else pa.crit_1
            else:
                grand.crit_1 = pa.crit_0 if des is pa.crit_1 else pa.crit_1

    def find_best_match(self, src: bytes):
        q = [None] * 3

        q[-1] = cursor = self.root
        while isinstance(cursor, CBInternal):
            # 计算方向
            check_byte = src[cursor.diff_at] if len(src) > cursor.diff_at else 0
            if cursor.diff_at < len(src):
                self.break_point = cursor

            direct = (1 + (cursor.mask | check_byte)) >> 8

            if direct == 0:
                cursor = cursor.crit_0
            else:
                cursor = cursor.crit_1

            del q[0]
            q.append(cursor)
        return q  # grand, pa, des

    def iter(self, from_node=None):
        if self.root is None:
            return
        if isinstance(self.root, bytes):
            yield self.root
            return

        def iter_node(node: CBInternal):
            for sub_node in (node.crit_0, node.crit_1):
                if isinstance(sub_node, bytes):
                    yield sub_node
                else:
                    yield from iter_node(sub_node)

        if from_node is None:
            from_node = self.root
        yield from iter_node(from_node)

    def prefix_iter(self, prefix: bytes):
        _, _, des = self.find_best_match(prefix)
        start_node = self.break_point
        des: bytes
        if not des.startswith(prefix):
            return

        prefix = prefix[:-1] + bytes(chr(prefix[-1] + 1), encoding='ascii')
        _, _, end_bytes = self.find_best_match(prefix)

        yield_mode = False
        for i in self.iter(start_node):
            if i is des:
                yield_mode = True
            if i is end_bytes:
                break
            if yield_mode:
                yield i

    def prefix_iter_plus(self, prefix: bytes):
        can_start = False

        def yield_search(cursor, on: bool):
            nonlocal can_start

            if isinstance(cursor, bytes):
                if can_start:
                    yield cursor
                else:
                    if cursor.startswith(prefix):
                        can_start = True
                        yield cursor
                return

            check_byte = prefix[cursor.diff_at] if len(prefix) > cursor.diff_at else 0
            direct = (1 + (cursor.mask | check_byte)) >> 8

            if not on and cursor.diff_at >= len(prefix):
                on = True

            if not on:
                if direct == 0:
                    yield from yield_search(cursor.crit_0, False)
                else:
                    yield from yield_search(cursor.crit_1, False)
            else:
                yield from yield_search(cursor.crit_0, True)
                yield from yield_search(cursor.crit_1, True)

        yield from yield_search(self.root, False)

    def print(self):
        if self.root is None:
            print('empty')
        elif isinstance(self.root, CBInternal):
            self.root.print()
        else:
            print(self.root)


if __name__ == '__main__':
    from random import seed, choice

    seed(19950207)

    cbt = CBTree()

    alphabet = (b'a', b'b', b'c', b'd', b'e', b'f', b'g')
    samples = []
    for _ in range(1):
        sample = b''
        for _ in range(_ % 10 + 1):
            sample += choice(alphabet)
        sample += b'$'

        samples.append(sample)
        cbt.insert(sample)

        a = list(sorted(filter(lambda x: x.startswith(b'd'), set(samples))))
        b = list(cbt.prefix_iter(b'd'))
        c = list(cbt.prefix_iter_plus(b'd'))
        assert a == c
        assert b == c

        # samples = [b'a$', b'b$', b'c$']
        # for sample in samples:
        #     cbt.insert(sample)
        #
        # cbt.print()
        # print(list(cbt.prefix_iter_plus(b'b')))
