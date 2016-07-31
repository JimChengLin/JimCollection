from math import ceil


def find_mid_snake(a: str, b: str) -> tuple:
    # 通过delta可以判断是在正方向扩张还是反方向扩张的时候overlap
    delta = len(a) - len(b)
    is_even = (delta % 2 == 0)
    # 分治法
    half_supply = ceil((len(a) + len(b)) / 2)
    # pool用于检测扩张时是否overlap反方向的path
    # 没有检测到overlap时, 要覆写pool
    overlap_pool = set()
    counter = [0, 0]

    # 正方向扩张
    def forward():  # generator
        max_x_nth_k = {1: 0}
        for supply in range(half_supply + 1):
            extend_l = []
            counter[0] = supply
            for nth_k in range(-supply, supply + 1, 2):
                # snake: [..., point: (x, y)]
                snake = []
                common = []
                if nth_k == -supply or \
                        (nth_k != supply and max_x_nth_k[nth_k - 1] < max_x_nth_k[nth_k + 1]):
                    x = max_x_nth_k[nth_k + 1]
                    # snake起始点, x不变, y-1
                    snake.append((x, x - (nth_k + 1)))
                else:
                    # snake起始点, y不变, x-1
                    snake.append((max_x_nth_k[nth_k - 1], max_x_nth_k[nth_k - 1] - (nth_k - 1)))
                    x = max_x_nth_k[nth_k - 1] + 1
                y = x - nth_k
                # snake中间点
                snake.append((x, y))

                if not is_even and (x, y) in overlap_pool:
                    yield snake, common

                while x < len(a) and y < len(b) and a[x] == b[y]:
                    common.append(a[x])
                    x += 1
                    y += 1
                    # snake对角点
                    snake.append((x, y))

                    if not is_even and (x, y) in overlap_pool:
                        yield snake, common
                max_x_nth_k[nth_k] = x
                extend_l.extend(snake)

            # 切换到反方向的generator, 覆写pool
            overlap_pool.clear()
            overlap_pool.update(extend_l)
            yield False

    # 反方向扩张
    def reverse():
        # 输入reverse就相当于反方向扩张, 输出时再变换恢复
        reverse_a = a[::-1]
        reverse_b = b[::-1]

        def r_a(i: int) -> int:
            return i + round((len(reverse_a) / 2 - i) * 2)

        def r_b(i: int) -> int:
            return i + round((len(reverse_b) / 2 - i) * 2)

        def r_ab(point: tuple) -> tuple:
            return r_a(point[0]), r_b(point[1])

        max_x_nth_k = {1: 0}
        for supply in range(half_supply + 1):
            extend_l = []
            counter[1] = supply
            for nth_k in range(-supply, supply + 1, 2):

                snake = []
                common = []
                if nth_k == -supply or \
                        (nth_k != supply and max_x_nth_k[nth_k - 1] < max_x_nth_k[nth_k + 1]):
                    x = max_x_nth_k[nth_k + 1]
                    snake.append((x, x - (nth_k + 1)))
                else:
                    snake.append((max_x_nth_k[nth_k - 1], max_x_nth_k[nth_k - 1] - (nth_k - 1)))
                    x = max_x_nth_k[nth_k - 1] + 1
                y = x - nth_k
                snake.append((x, y))

                if is_even and (r_a(x), r_b(y)) in overlap_pool:
                    yield [r_ab(point) for point in reversed(snake)], common

                while x < len(reverse_a) and y < len(reverse_b) and reverse_a[x] == reverse_b[y]:
                    common.append(reverse_a[x])
                    x += 1
                    y += 1
                    snake.append((x, y))

                    if is_even and (r_a(x), r_a(y)) in overlap_pool:
                        yield [r_ab(point) for point in reversed(snake)], common
                max_x_nth_k[nth_k] = x
                extend_l.extend(snake)

            overlap_pool.clear()
            for point in extend_l:
                overlap_pool.add(r_ab(point))
            yield False

    # 主体调用部分
    forward_gen = forward()
    reverse_gen = reverse()
    for _ in range(half_supply + 1):

        result = next(forward_gen)
        if result:
            snake, common = result
            return snake, common, sum(counter)

        result = next(reverse_gen)
        if result:
            snake, common = result
            return snake, common, sum(counter)


def diff(a: str, b: str, output_l: list):
    if len(a) > 0 and len(b) > 0:
        snake, common, supply = find_mid_snake(a, b)

        # snake: [(x, y), ..., (u, v)]
        x, y = snake[0]
        u, v = snake[-1]

        if supply > 1:
            diff(a[:x], b[:y], output_l)
            output_l.extend(common)
            diff(a[u:], b[v:], output_l)
        elif len(b) > len(a):
            output_l.extend(list(a))
        else:
            output_l.extend(list(b))


if __name__ == '__main__':
    A = 'ABCABBA'
    B = 'CBABAC'


    def main():
        output_l = []
        diff(A, B, output_l)
        print(output_l)


    main()
