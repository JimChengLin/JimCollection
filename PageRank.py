import numpy as np


# 将Vertex转化为行列式
class Vertex:
    all = []

    def __init__(self, val: int, identifier: str = None):
        self.val = val
        self.connect_to_l = []
        # 分配一个序号
        self.num = len(Vertex.all)
        self.id = identifier
        Vertex.all.append(self)

    def connect_to(self, *other_vertex_i):
        self.connect_to_l.extend(other_vertex_i)

    def to_l(self) -> list:
        output = list(0 for _ in range(len(Vertex.all)))
        importance = 1 / len(self.connect_to_l)
        for other_v in self.connect_to_l:
            output[other_v.num] = importance
        return output

    def __repr__(self):
        return self.id if self.id else 'No.' + str(self.num)


def page_rank():
    input_matrix = [v.to_l() for v in Vertex.all]
    matrix = np.array(input_matrix)
    matrix = matrix.transpose()

    vector = np.array([(v.val / len(Vertex.all),) for v in Vertex.all])
    print(matrix)
    print(vector)
    print(matrix @ vector)


def clear():
    Vertex.all.clear()


if __name__ == '__main__':
    def main():
        v_1 = Vertex(1)
        v_2 = Vertex(1)
        v_3 = Vertex(1)
        v_4 = Vertex(1)

        v_1.connect_to(v_2, v_3, v_4)
        v_2.connect_to(v_3, v_4)
        v_3.connect_to(v_1)
        v_4.connect_to(v_1, v_3)

        page_rank()


    main()
