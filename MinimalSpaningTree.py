from DisjointSet import SetPathCompressed as DisjointSet
from ElementaryGraph import Vertex
from FibonacciHeap import FibHeap


class VertexPrim(Vertex):
    def __init__(self, identifier):
        super().__init__(identifier)
        self.parent = VertexPrim
        self.is_in_tree = False


a = VertexPrim('a')
b = VertexPrim('b')
c = VertexPrim('c')
d = VertexPrim('d')
e = VertexPrim('e')
f = VertexPrim('f')
g = VertexPrim('g')
h = VertexPrim('h')
i = VertexPrim('i')

a.connect(b, h)
b.connect(a, h, c)
c.connect(b, i, f, d)
d.connect(c, f, e)
e.connect(d, f)
f.connect(g, c, e)
g.connect(h, i, f)
i.connect(c, h, g)
h.connect(a, i, g)

e_map = {'ab': 4, 'bc': 8,
         'cd': 7, 'de': 9,
         'bh': 11, 'hi': 7,
         'ic': 2, 'ig': 6,
         'cf': 4, 'df': 14,
         'ah': 8, 'hg': 1,
         'gf': 2, 'fe': 10}

vertexes = [a, b, c, d, e, f, g, h, i]
v_map = {i.identifier: DisjointSet(i.identifier) for i in vertexes}


def kl_mst():
    edges = list(i for i in e_map.items())
    edges.sort(key=lambda x: x[1])
    total = 0

    for edge in edges:
        key = edge[0]
        first_s, second_s = key
        first = v_map[first_s]
        second = v_map[second_s]

        if first.find().identifier != second.find().identifier:
            print(edge)
            total += edge[1]
            first.find().union(second.find())

    print(total)


def prim_mst():
    def get_weight(a, b):
        return e_map.get(a + b) or e_map.get(b + a)

    possible_moves = FibHeap()
    vertex = vertexes[0]
    vertex.is_in_tree = True

    for adjacency in vertex.adjacency_list:
        possible_moves.push(get_weight(vertex.identifier, adjacency.identifier), (vertex, adjacency))

    count = 1
    while count != len(vertexes):
        best_move = possible_moves.pop().value
        first, second = best_move

        if first.is_in_tree ^ second.is_in_tree:
            count += 1

            if first.is_in_tree:
                cursor = second
            else:
                cursor = first
            cursor.is_in_tree = True

            for adjacency in cursor.adjacency_list:
                possible_moves.push(get_weight(cursor.identifier, adjacency.identifier), (cursor, adjacency))

            print(best_move)
            print('---')


prim_mst()
