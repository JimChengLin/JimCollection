from collections import OrderedDict
from random import randint


def obj_func(target: list) -> int:
    diff = 0
    for i in range(1, len(target)):
        diff += abs(target[i] - target[i - 1])
    return diff


def swap_gen(target: list) -> iter:
    for cursor_self in range(len(target)):
        for cursor_other in range(cursor_self, len(target)):
            if cursor_other == cursor_self:
                continue
            target[cursor_self], target[cursor_other] = target[cursor_other], target[cursor_self]
            yield cursor_self, cursor_other
            target[cursor_self], target[cursor_other] = target[cursor_other], target[cursor_self]


class TabuTable:
    def __init__(self, max_len: int):
        self.max_len = max_len
        self.record = OrderedDict()

    def __getitem__(self, key):
        return self.record[key]

    def __setitem__(self, key, value):
        self.record[key] = value
        if len(self.record) > self.max_len:
            self.record.popitem(last=False)

    def __contains__(self, key):
        return key in self.record


class TabuSearch:
    def __init__(self, target: list):
        self.target = target
        self.tabu_table = TabuTable(max_len=3)

    def run(self):
        temp = []
        gen = swap_gen(self.target)
        for swap in gen:
            temp.append((obj_func(self.target), swap))

        temp.sort()
        for pair in temp:
            mark, swap = pair
            if swap not in self.tabu_table or mark < self.tabu_table[swap]:
                break
        else:
            return

        self.tabu_table[swap] = mark
        a, b = swap
        self.target[a], self.target[b] = self.target[b], self.target[a]
        print(mark)
        print(self.target)


if __name__ == '__main__':
    ITER_NUM = 10000
    RAND_LIST = [randint(1, 100) for _ in range(100)]


    def main():
        tab_search = TabuSearch(RAND_LIST)
        for i in range(ITER_NUM):
            tab_search.run()


    main()
