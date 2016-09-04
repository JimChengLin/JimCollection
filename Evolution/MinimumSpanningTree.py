from bisect import insort
from random import uniform, randint, shuffle, random, choice


class Vertex:
    all_m = {}

    @staticmethod
    def find(id: str):
        return Vertex.all_m[id]

    @staticmethod
    def all_vertex():
        return list(Vertex.all_m.values())

    def __init__(self, id: str):
        self.id = id
        self.adjacency_l = []
        Vertex.all_m[id] = self

    def __repr__(self):
        return self.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id

    def connect(self, *others):
        for i in others:
            insort(self.adjacency_l, i)


class Map:
    line_m = {}

    @staticmethod
    def set_line(name: str, distance: int):
        Map.line_m[name] = distance
        Map.line_m[name[::-1]] = distance

    @staticmethod
    def get_line(name: str) -> int:
        return Map.line_m[name]

    @staticmethod
    def path(begin: Vertex, end: Vertex) -> list:
        explore_s = set()
        que = [(begin, begin.id)]
        while que:
            cursor, path = que.pop(0)
            if cursor in explore_s:
                continue
            else:
                explore_s.add(cursor)

            for sub in cursor.adjacency_l:
                if sub is end:
                    path += sub.id
                    que.clear()
                    break
                else:
                    que.append((sub, path + sub.id))

        result = []
        for i in range(1, len(path)):
            result.append((Vertex.find(path[i - 1]), Vertex.find(path[i])))
        return result


def prufer_de(code: list) -> list:
    result = []
    code = code[:]
    leaf_l = sorted(i for i in Vertex.all_vertex() if i not in code)
    while code:
        leaf = leaf_l.pop(0)
        pt = code.pop(0)

        if leaf in pt.adjacency_l and pt in leaf.adjacency_l:
            result.append((leaf, pt))
        else:
            result.extend(Map.path(leaf, pt))
        if pt not in code:
            insort(leaf_l, pt)

    a, b = leaf_l
    if a in b.adjacency_l and b in a.adjacency_l:
        result.append((a, b))
    else:
        result.extend(Map.path(a, b))
    return result


class Solution:
    all_fitness = None

    def __init__(self, code: list):
        self.code = code
        self.fitness = None

    def calc_fitness(self):
        line_s = set(prufer_de(self.code))
        self.fitness = sum(Map.get_line(a.id + b.id) / 2 if (b, a) in line_s else Map.get_line(a.id + b.id)
                           for a, b in line_s)

    def __repr__(self):
        return ''.join(str(i) for i in self.code)

    def __lt__(self, other):
        return self.fitness < other.fitness

    @property
    def possibility(self):
        return self.fitness / Solution.all_fitness

    def clone(self) -> 'Solution':
        another = Solution(self.code)
        another.fitness = self.fitness
        return another


class EA:
    CROSS_RATE = 0.1
    MUTATE_RATE = 0.05

    @staticmethod
    def mark(solution_l: list):
        for solution in solution_l:
            solution.calc_fitness()
        solution_l.sort()

        Solution.all_fitness = sum(i.fitness for i in solution_l)
        mid = len(solution_l) // 2
        for head, tail in zip(solution_l[:mid], reversed(solution_l[mid:])):
            head.fitness, tail.fitness = tail.fitness, head.fitness

    @staticmethod
    def select(solution_l: list):
        offset = 1 / len(solution_l)
        next_solution_l = []

        i = 0
        supply = 0
        demand = uniform(0, offset)
        while len(next_solution_l) < len(solution_l):
            solution = solution_l[i]

            supply += solution.possibility
            while demand <= supply:
                next_solution_l.append(solution.clone())
                demand += offset
            i += 1
        solution_l[:] = next_solution_l

    @staticmethod
    def crossover(solution_l: list):
        shuffle(solution_l)

        for i in range(len(solution_l) // 2):
            if random() > EA.CROSS_RATE:
                continue
            a = solution_l[i * 2]
            b = solution_l[i * 2 + 1]

            for i in range(len(a.code) // 2):
                exchange_pt = randint(0, len(a.code) - 1)
                a.code[exchange_pt], b.code[exchange_pt] = b.code[exchange_pt], a.code[exchange_pt]

    @staticmethod
    def mutate(solution_l: list):
        for solution in solution_l:
            if random() < EA.MUTATE_RATE:
                index = randint(0, len(solution.code) - 1)
                solution.code[index] = choice(Vertex.all_vertex())


def rand_solution() -> Solution:
    return Solution([choice(Vertex.all_vertex()) for _ in range(len(Vertex.all_m) - 2)])


def inspect(solution_l: list):
    print(len(solution_l), sum(i.fitness for i in solution_l))


if __name__ == '__main__':
    def main():
        v1 = Vertex('1')
        v2 = Vertex('2')
        v3 = Vertex('3')
        v4 = Vertex('4')
        v5 = Vertex('5')
        v6 = Vertex('6')

        v1.connect(v2, v5)
        v2.connect(v1, v5, v6, v3)
        v3.connect(v2, v5, v6, v4)
        v4.connect(v3, v6)
        v5.connect(v1, v2, v3, v6)
        v6.connect(v5, v2, v3, v4)

        Map.set_line('12', 1)
        Map.set_line('23', 2)
        Map.set_line('34', 3)
        Map.set_line('25', 4)
        Map.set_line('26', 5)
        Map.set_line('35', 6)
        Map.set_line('36', 7)
        Map.set_line('15', 8)
        Map.set_line('56', 9)
        Map.set_line('46', 10)

        solution_l = [rand_solution() for _ in range(100)]
        for i in range(100):
            for call in (EA.mark,
                         EA.select,
                         EA.crossover,
                         EA.mutate,
                         EA.mark,
                         inspect):
                call(solution_l)


    main()
