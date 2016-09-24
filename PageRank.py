from array import array
from collections import OrderedDict
from math import isclose

JUMP = 0.15


class Vertex:
    dgl_l = []
    total_weight = 0
    matrix = OrderedDict()

    @staticmethod
    def reset():
        Vertex.dgl_l.clear()
        Vertex.total_weight = 0
        Vertex.matrix.clear()

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
            Vertex.dgl_l.append(self.name)


class PageRank:
    def __init__(self):
        total = len(Vertex.matrix) + Vertex.total_weight
        self.average = 1 / total
        self.reserve = 1 - JUMP
        self.spread = JUMP / total

        a_len = len(Vertex.matrix) + 1
        self.pr_a = array('d', [self.average]) * a_len
        self.temp_pr_a = array('d', [0]) * a_len

        self.nth_calc = 0
        self.done_num = 0
        Vertex.matrix['_'] = {'$i': a_len - 1, '$weight': 0}

    def calc(self):
        self.nth_calc += 1
        dgl_pr = 0
        dgl_cum = 0
        for name in Vertex.dgl_l:
            i = Vertex.matrix[name]['$i']
            dgl_pr += self.pr_a[i] * self.average
            dgl_cum += self.pr_a[i]

        done_l = []
        for r_name, r_map in Vertex.matrix.items():
            if '$done' in r_map:
                break
            pr = dgl_pr
            cum = dgl_cum
            r_i = r_map['$i']
            weight = r_map['$weight']

            for c_name, c_val in r_map.items():
                if c_name not in ('$i', '$weight'):
                    c_i = Vertex.matrix[c_name]['$i']
                    pr += self.pr_a[c_i] * self.trans(c_val)
                    cum += self.pr_a[c_i]

            vpr = self.pr_a[-1]
            pr += self.trans(1) * vpr * weight + self.trans(0) * vpr * (Vertex.total_weight - weight)
            pr += (1 - cum - Vertex.total_weight * vpr) * self.spread
            self.temp_pr_a[r_i] = pr

            if self.nth_calc >= 3 and isclose(pr, self.pr_a[r_i], rel_tol=1e-3):
                self.done_num += 1
                done_l.append(r_name)
                Vertex.matrix[r_name]['$done'] = True

        for name in done_l:
            Vertex.matrix.move_to_end(name)
        self.pr_a, self.temp_pr_a = self.temp_pr_a, self.pr_a
        if self.done_num == len(self.pr_a):
            return True
        if self.nth_calc >= 3:
            self.nth_calc = 0

    def trans(self, val: float) -> float:
        return val * self.reserve + self.spread


if __name__ == '__main__':
    # [ 0.19613095  0.13916915  0.17757937  0.21598958  0.04518849]
    v_0 = Vertex('v_0')
    v_1 = Vertex('v_1')
    v_2 = Vertex('v_2')
    v_3 = Vertex('v_3')
    v_0.connect(0, v_1, v_2, v_3)
    v_1.connect(1)
    v_2.connect(2, v_0)
    v_3.connect(3)
    pagerank = PageRank()
    while not pagerank.calc():
        print(pagerank.pr_a)
        continue
    print(pagerank.pr_a)
