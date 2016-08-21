from asyncio import wait, get_event_loop, ensure_future
from random import choice

from lib import select, crossover, mutate

END = 20
FINE = 1
INTEREST_RATE = 0.01


class Project:
    all = []

    def __init__(self, name: str):
        self.name = name
        self.depend_l = []
        self.enable_l = []
        self.candidate_d = {}
        self.num = len(Project.all)
        Project.all.append(self)

        self.curr_candidate = None
        self.curr_fut = None
        self.curr_start = self.curr_end = None
        self.curr_float = None

    def depend_on(self, *others):
        self.depend_l.extend(others)
        for other in others:
            other.enable_l.append(self)

    def add_candidate(self, c: 'Candidate', price: int, time: int):
        for pair in self.candidate_d.values():
            price_exist, time_exist = pair
            do_return = False
            if not do_return:
                do_return = (price_exist <= price and time_exist <= time)
            if not do_return:
                do_return = (price_exist == price and time_exist < time) or (time_exist == time and price_exist < price)
            if do_return:
                return
        self.candidate_d[c] = (price, time)

    def candidate_time(self, time_from, time_to) -> 'Candidate':
        result = []
        for candidate in self.candidate_d.keys():
            if time_from <= self.candidate_d[candidate][1] <= time_to:
                result.append(candidate)
        return choice(result)

    # 与curr_candidate有关部分
    def set_candidate(self, c: 'Candidate'):
        self.curr_candidate = c
        self.curr_fut = ensure_future(self.coro())

    @property
    def curr_price(self) -> int:
        return self.candidate_d[self.curr_candidate][0]

    @property
    def curr_time(self) -> int:
        return self.candidate_d[self.curr_candidate][1]

    async def coro(self):
        prev_time = 0
        for depend in self.depend_l:
            prev_time = max(prev_time, await depend.curr_fut)
        self.curr_start = prev_time
        self.curr_end = self.curr_start + self.curr_time
        return self.curr_end

    def __repr__(self):
        return self.name


class Candidate:
    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class Solution:
    def __init__(self, candidate_l: list):
        self.candidate_l = candidate_l
        self.price = None
        self.time = None

    def stimulate(self):
        for project, candidate in zip(Project.all, self.candidate_l):
            project.set_candidate(candidate)
        loop.run_until_complete(wait([project.curr_fut for project in Project.all]))

        last = Project.all[-1]
        self.time = last.curr_end
        seg_tree = SegmentTree(0, self.time)

        self.price = 0
        for project in Project.all:
            seg_tree.insert(project.curr_start, project.curr_end, project)
            self.price += (project.curr_price + (self.time - project.curr_start) * project.curr_price * INTEREST_RATE)
        if self.time > END:
            self.price += ((END - self.time) * FINE)

        for project in Project.all:
            float = 0
            for cursor in reversed(range(0, project.curr_end)):
                if len(seg_tree.search(cursor, project.curr_end)) == 1:
                    float -= 1
                else:
                    break
            if float == 0:
                closest_enable = min(project.enable_l, key=lambda x: x.curr_start)
                float = closest_enable.curr_start - project.curr_end
            project.curr_float = float

    def improve(self):
        float_i = list(map(lambda x: x.curr_float, Project.all))
        min_float = min(float_i)
        max_float = max(float_i)
        if self.time < END:
            p = select(Project.all, key=lambda x: x.curr_float - min_float + 1, num=1).pop()
            self.candidate_l[p.num] = p.candidate_time(p.curr_time, p.curr_time + (END - self.time))
        elif self.time > END:
            p = select(Project.all, key=lambda x: max_float - x.curr_float + 1, num=1).pop()
            self.candidate_l[p.num] = p.candidate_time(p.curr_time - (self.time - END), p.curr_time)

    def clone(self) -> 'Solution':
        return Solution(self.candidate_l[:])


class SegmentTree:
    def __init__(self, seg_from: int, seg_to: int):
        self.root = SegmentTreeNode(seg_from, seg_to)

    def insert(self, seg_from: int, seg_to: int, value):
        self.root.insert(seg_from, seg_to, value)

    def search(self, seg_from, seg_to) -> list:
        result = set()
        self.root.search(seg_from, seg_to, lambda x: result.update(x))
        return list(filter(lambda x: x.curr_end != seg_from and x.curr_start != seg_to, result))


class SegmentTreeNode:
    def __init__(self, seg_from: int, seg_to: int):
        self.seg_from = int(seg_from)
        self.seg_to = int(seg_to)

        self._values = None
        self._left = self._right = None

    @property
    def left(self) -> 'SegmentTreeNode':
        if not self._left:
            self._left = SegmentTreeNode(self.seg_from, (self.seg_from + self.seg_to) // 2)
        return self._left

    @property
    def right(self) -> 'SegmentTreeNode':
        if not self._right:
            self._right = SegmentTreeNode((self.seg_from + self.seg_to) // 2 + 1, self.seg_to)
        return self._right

    @property
    def values(self) -> list:
        if not self._values:
            self._values = []
        return self._values

    def insert(self, seg_from: int, seg_to: int, value):
        seg_from = int(seg_from)
        seg_to = int(seg_to)

        if seg_from == self.seg_from and seg_to == self.seg_to:
            return self.values.append(value)

        mid = (self.seg_from + self.seg_to) // 2
        if seg_from <= mid:
            self.left.insert(seg_from, min(seg_to, mid), value)
        if seg_to >= mid + 1:
            self.right.insert(max(seg_from, mid + 1), seg_to, value)

    def search(self, seg_from: int, seg_to: int, output_call: callable):
        seg_from = int(seg_from)
        seg_to = int(seg_to)

        def include(node: 'SegmentTreeNode'):
            if node._values:
                output_call(node._values)
            if node._left:
                include(node._left)
            if node._right:
                include(node._right)

        if seg_from == self.seg_from and seg_to == self.seg_to:
            return include(self)
        if self._values:
            output_call(self._values)

        mid = (self.seg_from + self.seg_to) // 2
        if seg_from <= mid:
            self.left.search(seg_from, min(seg_to, mid), output_call)
        if seg_to >= mid + 1:
            self.right.search(max(seg_from, mid + 1), seg_to, output_call)

    def __repr__(self):
        return '{}:{}'.format(self.seg_from, self.seg_to)


if __name__ == '__main__':
    loop = get_event_loop()


    def test():
        c_foo = Candidate('foo')
        c_bar = Candidate('bar')
        c_lol = Candidate('lol')

        p_se = Project('se')
        p_s1 = Project('s1')
        p_12 = Project('12')
        p_e3 = Project('e3')
        p_23 = Project('23')
        p_24 = Project('24')
        p_2e = Project('2e')
        p_34 = Project('34')
        p_45 = Project('45')
        p_e5 = Project('e5')
        p_ee = Project('ee')
        p_56 = Project('56')
        p_e6 = Project('e6')
        p_e7 = Project('e7')
        p_67 = Project('67')
        p_7e = Project('7e')

        p_e3.depend_on(p_se)
        p_12.depend_on(p_s1)
        p_23.depend_on(p_12)
        p_34.depend_on(p_e3, p_23)
        p_24.depend_on(p_12)
        p_2e.depend_on(p_12)
        p_e5.depend_on(p_2e)
        p_ee.depend_on(p_2e)
        p_45.depend_on(p_34, p_24)
        p_56.depend_on(p_45, p_e5)
        p_e6.depend_on(p_ee)
        p_e7.depend_on(p_ee)
        p_67.depend_on(p_56, p_e6)
        p_7e.depend_on(p_67, p_e7)

        p_se.add_candidate(c_foo, 2, 2)
        p_se.add_candidate(c_bar, 1, 3)
        p_se.add_candidate(c_lol, 3, 1)

        p_s1.add_candidate(c_foo, 1, 1)

        p_12.add_candidate(c_foo, 3, 3)
        p_12.add_candidate(c_bar, 4, 2)
        p_12.add_candidate(c_lol, 2, 4)

        p_e3.add_candidate(c_foo, 1, 1)

        p_23.add_candidate(c_foo, 2, 2)
        p_23.add_candidate(c_bar, 1, 3)
        p_23.add_candidate(c_lol, 3, 1)

        p_24.add_candidate(c_foo, 1, 1)

        p_2e.add_candidate(c_foo, 3, 3)
        p_2e.add_candidate(c_bar, 4, 2)
        p_2e.add_candidate(c_lol, 2, 4)

        p_34.add_candidate(c_foo, 2, 2)
        p_34.add_candidate(c_bar, 3, 1)

        p_45.add_candidate(c_foo, 3, 3)
        p_45.add_candidate(c_bar, 4, 2)
        p_45.add_candidate(c_lol, 2, 4)

        p_e5.add_candidate(c_foo, 3, 3)
        p_e5.add_candidate(c_bar, 4, 2)
        p_e5.add_candidate(c_lol, 2, 4)

        p_ee.add_candidate(c_foo, 2, 2)
        p_ee.add_candidate(c_bar, 3, 1)

        p_56.add_candidate(c_foo, 3, 3)

        p_e6.add_candidate(c_foo, 3, 3)
        p_e6.add_candidate(c_bar, 4, 2)
        p_e6.add_candidate(c_lol, 2, 4)

        p_e7.add_candidate(c_foo, 4, 4)
        p_e7.add_candidate(c_bar, 5, 3)
        p_e7.add_candidate(c_lol, 3, 5)

        p_67.add_candidate(c_foo, 1, 1)
        p_7e.add_candidate(c_bar, 1, 1)

        def rand_solution():
            return Solution([choice(list(project.candidate_d.keys())) for project in Project.all])

        solution_l = [rand_solution() for _ in range(100)]
        for i in range(100):
            max_price = 0
            for solution in solution_l:
                solution.stimulate()
                solution.improve()
                solution.stimulate()
                max_price = max(max_price, solution.price)

            solution_l = select(solution_l, key=lambda x: max_price - x.price + 1,
                                num=len(solution_l), clone_func=lambda x: x.clone())
            crossover([s.candidate_l for s in solution_l], rate=0.2)
            mutate((s.candidate_l for s in solution_l),
                   func=lambda i: choice(list(Project.all[i].candidate_d)), rate=0.05)

            for solution in solution_l:
                solution.stimulate()
            print(sum(solution.price for solution in solution_l))


    test()
