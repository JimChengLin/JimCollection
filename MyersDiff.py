from math import ceil


def find_mid_snake(a: str, b: str) -> tuple:
    # 通过delta的奇偶性可以判断是在正方向扩张还是反方向扩张的时候overlap
    is_even = ((len(a) - len(b)) % 2 == 0)
    is_odd = not is_even
    # 分治法
    half_supply = ceil((len(a) + len(b)) / 2)
    # pool用于检测扩张时是否overlap反方向的path
    overlap_pool = set()
    counter = [0, 0]

    # 正方向扩张
    def forward():
        max_x_nth_k = {1: 0}
        for supply in range(half_supply + 1):
            extend_l = []
            counter[0] = supply

            for nth_k in range(-supply, supply + 1, 2):
                # snake: [..., point: (x, y)]
                snake = []
                is_overlap = False

                if nth_k == -supply or \
                        (nth_k != supply and max_x_nth_k[nth_k - 1] < max_x_nth_k[nth_k + 1]):
                    x = max_x_nth_k[nth_k + 1]
                    # snake起始点, x不变, y-1
                    snake.append((x, x - (nth_k + 1)))
                else:
                    # y不变, x-1
                    snake.append((max_x_nth_k[nth_k - 1], max_x_nth_k[nth_k - 1] - (nth_k - 1)))
                    x = max_x_nth_k[nth_k - 1] + 1
                y = x - nth_k
                # snake中间点
                snake.append((x, y))

                if is_odd and (x, y) in overlap_pool:
                    is_overlap = True
                while x < len(a) and y < len(b) and a[x] == b[y]:
                    x += 1
                    y += 1
                    if is_overlap and (x, y) not in overlap_pool:
                        break
                    # snake尾巴点
                    snake.append((x, y))

                    if not is_overlap and is_odd and (x, y) in overlap_pool:
                        is_overlap = True
                if is_overlap:
                    yield snake
                max_x_nth_k[nth_k] = x
                extend_l.extend(snake)

            # 切换到反方向的generator
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
            a, b = point
            return r_a(a), r_b(b)

        max_x_nth_k = {1: 0}
        for supply in range(half_supply + 1):
            extend_l = []
            counter[1] = supply

            for nth_k in range(-supply, supply + 1, 2):
                snake = []
                is_overlap = False

                if nth_k == -supply or \
                        (nth_k != supply and max_x_nth_k[nth_k - 1] < max_x_nth_k[nth_k + 1]):
                    x = max_x_nth_k[nth_k + 1]
                    snake.append((x, x - (nth_k + 1)))
                else:
                    snake.append((max_x_nth_k[nth_k - 1], max_x_nth_k[nth_k - 1] - (nth_k - 1)))
                    x = max_x_nth_k[nth_k - 1] + 1
                y = x - nth_k
                snake.append((x, y))

                if is_even and r_ab((x, y)) in overlap_pool:
                    is_overlap = True
                while x < len(reverse_a) and y < len(reverse_b) and reverse_a[x] == reverse_b[y]:
                    x += 1
                    y += 1
                    if is_overlap and r_ab((x, y)) not in overlap_pool:
                        break
                    snake.append((x, y))

                    if not is_overlap and is_even and r_ab((x, y)) in overlap_pool:
                        is_overlap = True
                if is_overlap:
                    yield [r_ab(point) for point in reversed(snake)]
                max_x_nth_k[nth_k] = x
                extend_l.extend(snake)

            overlap_pool.clear()
            overlap_pool.update(r_ab(point) for point in extend_l)
            yield False

    # 主体调用部分
    forward_g = forward()
    reverse_g = reverse()
    for _ in range(half_supply + 1):

        result = next(forward_g)
        if result:
            snake = result
            return snake, sum(counter)

        result = next(reverse_g)
        if result:
            snake = result
            return snake, sum(counter)


def diff(a: str, b: str, output_l: list):
    if len(a) > 0 and len(b) > 0:
        if len(a) <= 2 and len(b) <= 2:
            if a == b:
                output_l.extend(a)
            else:
                for char in a:
                    if char in b:
                        output_l.append(char)
                        break
            return

        snake, supply = find_mid_snake(a, b)
        # snake: [(x, y), ..., (u, v)]
        x, y = snake[0]
        u, v = snake[-1]

        if supply > 1:
            diff(a[:x], b[:y], output_l)
            output_l.extend(snake_to_str(snake, a))
            if a[u - 1] == b[v - 1]:
                del_zero = False
            diff(a[max(u - 1, 0):], b[max(v - 1, 0):], output_l)
        elif len(b) > len(a):
            output_l.extend(list(a))
        else:
            output_l.extend(list(b))


def snake_to_str(snake: list, a: str) -> str:
    result = ''
    for i in range(len(snake) - 1):
        head = snake[i]
        tail = snake[i + 1]
        if tail == (head[0] + 1, head[1] + 1):
            result += a[tail[0] - 1]
    return result


if __name__ == '__main__':
    A = 'MZJAWXU'
    B = 'XMJYAUZ'

    X = 'ABCBDAB'
    Y = 'BDCABA'

    U = 'ABCABBA'
    V = 'CBABAC'


    def main():
        output_l = []
        diff(Y, X, output_l)
        print(output_l)


    main()
