from math import inf
from typing import List

from ElementaryGraph import Vertex
from FibonacciHeap import FibHeap, FibNode

W = [[0, 3, 8, inf, -4],
     [inf, 0, inf, 1, 7],
     [inf, 4, 0, inf, inf],
     [2, inf, -5, 0, inf],
     [inf, inf, inf, 6, 0]]


class Node:
    def __init__(self, weight: int):
        self.weight = weight
        self.parent = -1

    def __repr__(self):
        return '{:2}'.format(self.weight)


class Matrix:
    def __init__(self, weight_matrix: List[List[int]]):
        self.matrix = [[Node(weight) for weight in row] for row in weight_matrix]

    def __repr__(self):
        return '\n'.join((str(i) for i in self.matrix))

    def extend_shortest_paths(self) -> bool:
        is_modified = False
        matrix_len = len(self.matrix)

        for pos_from in range(matrix_len):
            for pos_to in range(matrix_len):
                for pos_mid in range(matrix_len):
                    curr_weight = self.matrix[pos_from][pos_mid].weight + self.matrix[pos_mid][pos_to].weight
                    if curr_weight < self.matrix[pos_from][pos_to].weight:
                        self.matrix[pos_from][pos_to].weight = curr_weight
                        self.matrix[pos_from][pos_to].parent = pos_mid
                        is_modified = True
        return is_modified

    def floyd_shortest_paths(self):
        matrix_len = len(self.matrix)

        for pos_mid in range(matrix_len):
            for pos_from in range(matrix_len):
                for pos_to in range(matrix_len):

                    curr_weight = self.matrix[pos_from][pos_mid].weight + self.matrix[pos_mid][pos_to].weight
                    path_from_to = self.matrix[pos_from][pos_to]

                    if curr_weight < path_from_to.weight:
                        path_from_to.weight = curr_weight
                        path_from_to.parent = pos_mid

                    elif path_from_to.parent == -1 and pos_from != pos_to and path_from_to.weight < inf:
                        path_from_to.parent = pos_from

    def print_paths(self):
        print('\n'.join(','.join('{:2}'.format(node.parent) for node in row) for row in self.matrix))

    def print_path_from_to(self, pos_from, pos_to):
        print(pos_from)
        if self.matrix[pos_from][pos_to].parent != -1:
            return self.print_path_from_to(self.matrix[pos_from][pos_to].parent, pos_to)

    def transitive_closure(self):
        matrix_len = len(self.matrix)

        for pos_mid in range(matrix_len):
            for pos_from in range(matrix_len):
                for pos_to in range(matrix_len):
                    self.matrix[pos_from][pos_to].weight = self.matrix[pos_from][pos_to].weight or (
                        self.matrix[pos_from][pos_mid].weight and self.matrix[pos_mid][pos_to].weight)


def slow_matrix():
    matrix = Matrix(W)
    while matrix.extend_shortest_paths():
        matrix.extend_shortest_paths()
    print(matrix)


def floyd_matrix():
    matrix = Matrix(W)
    matrix.floyd_shortest_paths()
    print(matrix)
    print('---------------')
    matrix.print_paths()


def transitive_closure():
    g = [[1, 0, 0, 0],
         [0, 1, 1, 1],
         [0, 1, 1, 0],
         [1, 0, 1, 1]]

    matrix = Matrix(g)
    matrix.transitive_closure()
    print(matrix)


# -----------------------------------------Johnson's algorithm

class VertexBellmanFordPlus(Vertex):
    def __init__(self, identifier: str):
        super().__init__(identifier)
        self.distance = inf  # type: int
        self.fee = 0

    def relax(self, edge_map: dict):
        next_level_vertexes = []
        for adjacency in self.adjacency_list:
            distance = self.distance + edge_map[self.identifier + adjacency.identifier]
            if distance < adjacency.distance:
                adjacency.distance = distance
                adjacency.fee = self.fee + 1
                next_level_vertexes.append(adjacency)
        return next_level_vertexes

    @staticmethod
    def calculate(vertexes: List['VertexBellmanFordPlus'], edge_map: dict) -> bool:
        s = vertexes[0]
        s.distance = 0
        mod_q = [s]

        for i in range(len(vertexes) - 1):
            if not mod_q:
                break

            temp = []
            for cursor in mod_q:
                if cursor.fee != i:
                    continue
                temp.extend(cursor.relax(edge_map))
            mod_q = temp

        for vertex in vertexes:
            for adjacency in vertex.adjacency_list:
                if adjacency.distance > vertex.distance + edge_map[vertex.identifier + adjacency.identifier]:
                    return False
        return True

    @staticmethod
    def re_weight(vertexes: List['VertexBellmanFordPlus'], edge_map: dict):
        for vertex in vertexes:
            for adjacency in vertex.adjacency_list:
                edge_map[vertex.identifier + adjacency.identifier] += (vertex.distance - adjacency.distance)


class VertexDijkstraPlus(Vertex):
    heap = FibHeap()

    def __init__(self, identifier: str):
        super().__init__(identifier)
        self.distance = inf - 1
        self.parent = VertexDijkstraPlus
        self.reference = VertexDijkstraPlus.heap.push(self.distance, self)

    def decrease(self, distance: int):
        self.distance = distance
        VertexDijkstraPlus.heap.decrease(self.reference, distance)

    def relax(self, edge_map: dict):
        for adjacency in self.adjacency_list:
            distance = self.distance + edge_map[self.identifier + adjacency.identifier]
            if distance < adjacency.distance:
                adjacency.distance = distance
                adjacency.parent = self
                adjacency.decrease(distance)

    def restore(self):
        self.distance = inf - 1
        self.parent = VertexDijkstraPlus
        self.reference = VertexDijkstraPlus.heap.push(self.distance, self)

    @staticmethod
    def calculate(start_vertex: 'VertexDijkstraPlus', edge_map):
        start_vertex.decrease(0)
        while VertexDijkstraPlus.heap.min_node is not FibNode:
            cursor = VertexDijkstraPlus.heap.pop().value
            cursor.relax(edge_map)

    @staticmethod
    def output(start_vertex: 'VertexDijkstraPlus', vertexes: List['VertexDijkstraPlus'], matrix: List[List]):
        for vertex in vertexes:
            if vertex is not start_vertex:
                matrix[int(start_vertex.identifier) - 1][int(vertex.identifier) - 1] = vertex.parent
            vertex.restore()


def johnson_algorithm_main():
    s = VertexBellmanFordPlus('s')
    v_1 = VertexBellmanFordPlus('1')
    v_2 = VertexBellmanFordPlus('2')
    v_3 = VertexBellmanFordPlus('3')
    v_4 = VertexBellmanFordPlus('4')
    v_5 = VertexBellmanFordPlus('5')

    s.connect(v_1, v_2, v_3, v_4, v_5)
    v_1.connect(v_2, v_3, v_5)
    v_2.connect(v_5, v_4)
    v_3.connect(v_2)
    v_4.connect(v_3, v_1)
    v_5.connect(v_4)
    vertexes = [s, v_1, v_2, v_3, v_4, v_5]

    edge_map = {
        's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0,
        '12': 3, '13': 8, '15': -4,
        '25': 7, '24': 1,
        '32': 4,
        '43': -5, '41': 2,
        '54': 6
    }

    VertexBellmanFordPlus.calculate(vertexes, edge_map)
    VertexBellmanFordPlus.re_weight(vertexes, edge_map)

    v_1 = VertexDijkstraPlus('1')
    v_2 = VertexDijkstraPlus('2')
    v_3 = VertexDijkstraPlus('3')
    v_4 = VertexDijkstraPlus('4')
    v_5 = VertexDijkstraPlus('5')

    v_1.connect(v_2, v_3, v_5)
    v_2.connect(v_5, v_4)
    v_3.connect(v_2)
    v_4.connect(v_3, v_1)
    v_5.connect(v_4)

    vertexes = [v_1, v_2, v_3, v_4, v_5]
    matrix = [[VertexDijkstraPlus for _ in range(len(vertexes))] for _ in range(len(vertexes))]

    for start_vertex in vertexes:
        VertexDijkstraPlus.calculate(start_vertex, edge_map)
        VertexDijkstraPlus.output(start_vertex, vertexes, matrix)
        print()


johnson_algorithm_main()
