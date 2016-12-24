class CBInternal:
    def __init__(self):
        self.diff_at = None
        self.mask = None
        self.crit_is_0 = None
        self.crit_is_1 = None

    def print(self, lv=0):
        print('  ' * lv, 'diff_at: {}, mask: {}'.format(self.diff_at, bin(self.mask)))
        lv += 1

        for sub in (self.crit_is_0, self.crit_is_1):
            if isinstance(sub, CBInternal):
                sub.print(lv)
            else:
                print('  ' * lv, sub)


class CBTree:
    def __init__(self):
        self.root = None

    def insert(self, src: str):
        pass

    def find_best_match(self, src: str):
        grand = pa = des = self.root

        while isinstance(pa, CBInternal):

            direct = 0
            # 计算方向
            grand = pa
            if direct == 0:
                pa = pa.crit_is_0
            else:
                pa = pa.crit_is_1
        return grand, pa, des

    def print(self):
        if self.root is None:
            print('empty')
        elif isinstance(self.root, CBInternal):
            self.root.print()
        else:
            print(self.root)
