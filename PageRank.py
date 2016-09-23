from collections import OrderedDict
from math import isclose

import numpy as np

JUMP = 0.15


class Vertex:
    total_weight = 0
    dangling_s = set()
    matrix = OrderedDict()

    def __init__(self, name: str):
        self.name = name
        if self.name not in Vertex.matrix:
            Vertex.matrix[self.name] = {'$i': len(Vertex.matrix)}

    def connect(self, weight: int, *vertex_l):
        Vertex.total_weight += weight
        Vertex.matrix[self.name]['$weight'] = weight

        if vertex_l:
            val = 1 / len(vertex_l)
            for vertex in vertex_l:
                Vertex.matrix[vertex.name][self.name] = val
        else:
            Vertex.dangling_s.add(self.name)


class PageRank:
    def __init__(self):
        a_num = len(Vertex.matrix) + 1
        total = len(Vertex.matrix) + Vertex.total_weight
        self.average = 1 / total
        self.reserve = 1 - JUMP
        self.spread = JUMP / total

        self.pr_a = np.empty(a_num)
        self.pr_a.fill(self.average)
        self.temp_pr_a = np.zeros(a_num)

        self.counter = 0
        Vertex.matrix['_'] = {}

    def calc(self):
        for r_name, r_map in Vertex.matrix.items():
            if '$done' in r_map:
                continue
            pr = 0
            cum = 0
            r_i = r_map.get('$i', -1)
            weight = r_map.get('$weight', 0)

            for c_name, c_val in r_map.items():
                if c_name not in ('$i', '$weight'):
                    c_i = Vertex.matrix[c_name]['$i']
                    pr += self.pr_a[c_i] * self.trans(c_val)
                    cum += self.pr_a[c_i]

            for c_name in Vertex.dangling_s:
                c_i = Vertex.matrix[c_name]['$i']
                pr += self.pr_a[c_i] * self.average
                cum += self.pr_a[c_i]

            vpr = self.pr_a[-1]
            pr += self.trans(1) * vpr * weight + self.trans(0) * vpr * (Vertex.total_weight - weight)
            pr += (1 - cum - Vertex.total_weight * vpr) * self.spread
            self.temp_pr_a[r_i] = pr

            if isclose(pr, self.pr_a[r_i]):
                Vertex.matrix[r_name]['$done'] = True
                self.counter += 1
        self.pr_a, self.temp_pr_a = self.temp_pr_a, self.pr_a
        if self.counter == len(Vertex.matrix):
            return True

    def trans(self, val: float) -> float:
        return val * self.reserve + self.spread


if __name__ == '__main__':
    # 预期结果: [ 0.12583295  0.21330472  0.23940615  0.20935905  0.03534952]
    v_0 = Vertex('v_0')
    v_1 = Vertex('v_1')
    v_2 = Vertex('v_2')
    v_3 = Vertex('v_3')
    v_0.connect(0, v_1, v_2, v_3)
    v_1.connect(1, v_2, v_3)
    v_2.connect(2, v_0)
    v_3.connect(3)
    pagerank = PageRank()
    while not pagerank.calc():
        print(pagerank.pr_a)
        continue
    print(pagerank.pr_a)
