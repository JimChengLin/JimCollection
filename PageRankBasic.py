import numpy as np


# 将Vertex转化为行列式
class Vertex:
    all = []

    def __init__(self, identifier: str = None):
        self.id = identifier
        self.connect_to_l = []
        self.num = len(Vertex.all)
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
    d = np.array([v.to_l() for v in Vertex.all])
    d = d.transpose()
    average = (1 / len(Vertex.all),)
    v = np.array([average for _ in range(len(Vertex.all))])
    print(d)
    print(v)
    print(d @ v)


def clear():
    Vertex.all.clear()


if __name__ == '__main__':
    def main():
        v_1 = Vertex()
        v_2 = Vertex()
        v_3 = Vertex()
        v_4 = Vertex()

        v_1.connect_to(v_2, v_3, v_4)
        v_2.connect_to(v_3, v_4)
        v_3.connect_to(v_1)
        v_4.connect_to(v_1, v_3)

        page_rank()


    main()
