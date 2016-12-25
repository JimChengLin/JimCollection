class CBInternal:
    def __init__(self):
        self.diff_at = None
        self.mask = None
        self.crit_is_0 = None
        self.crit_is_1 = None

    def print(self, lv=0):
        intent = '  '
        print(intent * lv, 'diff_at: {}, mask: {}'.format(self.diff_at, bin(self.mask)))

        lv += 1
        for sub in (self.crit_is_0, self.crit_is_1):
            if isinstance(sub, CBInternal):
                sub.print(lv)
            else:
                print(intent * lv, sub)


class CBTree:
    def __init__(self):
        self.root = None

    def insert(self, new_bytes: bytes):
        if self.root is None:
            self.root = new_bytes
        else:
            grand, pa, old_bytes = self.find_best_match(new_bytes)
            # 查找哪个字节不同
            # 我在这里认为各个字符串一定会以 $ 结尾, 所以不考虑子串判断的问题
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

            # 0b0111_1111 => 0b1011_1111
            # 过程:
            # ~(diff_byte >> 1) = 0b1100_0000
            # diff_byte & 0b1100_0000 = 0b0111_1111 & 0b1100_0000 = 0b0100_0000
            mask = (diff_byte & ~(diff_byte >> 1)) ^ 255

            direct = (1 + (mask | new_bytes[diff_at])) >> 8
            # 生成一个新节点
            new_node = CBInternal()
            new_node.diff_at = diff_at
            new_node.mask = mask
            if direct == 0:
                new_node.crit_is_0 = new_bytes
            else:
                new_node.crit_is_1 = new_bytes

            # 插入节点


    def find_best_match(self, src: bytes):
        q = [None] * 3

        q[-1] = cursor = self.root
        while isinstance(cursor, CBInternal):
            # 计算方向
            check_byte = src[cursor.diff_at] if len(src) > cursor.diff_at else 0
            direct = (1 + (cursor.mask | check_byte)) >> 8

            if direct == 0:
                cursor = cursor.crit_is_0
            else:
                cursor = cursor.crit_is_1

            del q[0]
            q.append(cursor)
        return q  # grand, pa, des

    def print(self):
        if self.root is None:
            print('empty')
        elif isinstance(self.root, CBInternal):
            self.root.print()
        else:
            print(self.root)
