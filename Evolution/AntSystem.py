from math import sqrt, inf
from random import uniform, choice


# 不考虑回到原点的TSP
# p: float = 信息素
class City:
    all = []
    p_m = {}  # {..., name: p}

    def __init__(self, name: str, pos_x: int, pos_y: int):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        City.all.append(self)

    def distance_to(self, other: 'City') -> float:
        return sqrt((self.pos_x - other.pos_x) ** 2 + (self.pos_y - other.pos_y) ** 2)

    @staticmethod
    def set_p(a: 'City', b: 'City', p_num: float):
        name_ab = a.name + b.name
        if name_ab in City.p_m:
            City.p_m[name_ab] = p_num
        else:
            City.p_m[b.name + a.name] = p_num

    @staticmethod
    def get_p(a: 'City', b: 'City') -> float:
        return City.p_m.get(a.name + b.name) or City.p_m.get(b.name + a.name) or 0

    @staticmethod
    def dec_all_p():
        for key in City.p_m.keys():
            City.p_m[key] *= 0.9

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


def select(obj_l: iter, func: callable, num: int) -> list:
    result = []
    fitness_l = [func(i) for i in obj_l]

    total_fitness = sum(fitness_l)
    offset = 1 / num

    i = 0
    supply = 0
    demand = uniform(0, offset)
    while len(result) < num:
        obj = obj_l[i]
        fitness = fitness_l[i]

        supply += (fitness / total_fitness)
        while demand <= supply:
            result.append(obj)
            demand += offset
        i += 1
    return result


Q = 10


class Ant:
    def __init__(self, curr_pos: 'City'):
        self.curr_pos = curr_pos
        self.tab_l = []

    def move_next(self):
        move_l = []
        for move in (c for c in City.all if c not in self.tab_l and c is not self.curr_pos):
            p = City.get_p(self.curr_pos, move)
            d = self.curr_pos.distance_to(move)
            v = p ** 2 + (1 / d) ** 2
            move_l.append((move, v))

        next_pos = select(move_l, func=lambda x: x[1], num=1).pop()[0]
        self.tab_l.append(next_pos)
        self.curr_pos = next_pos

    def update_p(self) -> int:
        assert len(self.tab_l) == len(City.all) - 1

        total_distance = 0
        for i in range(1, len(self.tab_l)):
            a = self.tab_l[i - 1]
            b = self.tab_l[i]
            total_distance += a.distance_to(b)

        for i in range(1, len(self.tab_l)):
            a = self.tab_l[i - 1]
            b = self.tab_l[i]
            curr_p = City.get_p(a, b)
            City.set_p(a, b, curr_p + Q / total_distance)
        return total_distance


if __name__ == '__main__':
    def main():
        City('a', 1, 2)
        City('b', 1, 3)
        City('c', 2, 5)
        City('d', 2, 3)
        City('e', 3, 4)
        City('f', 3, 2)
        City('g', 4, 5)
        City('h', 5, 6)

        City('ar', 2, 1)
        City('br', 3, 1)
        City('cr', 5, 2)
        City('er', 4, 3)
        City('gr', 5, 4)
        City('hr', 6, 5)

        min_distance = inf
        min_path = None
        # 循环100次
        # 每次4只蚂蚁
        for _ in range(100):
            ant_l = [Ant(choice(City.all)) for _ in range(4)]
            for _ in range(len(City.all) - 1):
                for ant in ant_l:
                    ant.move_next()
            City.dec_all_p()
            for ant in ant_l:
                distance = ant.update_p()
                if distance < min_distance:
                    min_distance = distance
                    min_path = ant.tab_l[:]
            print(min_distance, min_path)


    main()
