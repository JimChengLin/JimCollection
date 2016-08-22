from AsyncDB import AsyncDB  # see my GitHub

db = AsyncDB('calc.db')


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
