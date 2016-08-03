from math import ceil


def find_mid_snake(a: str, b: str) -> list:
    # 通过delta的奇偶性可以判断是在正方向扩张还是反方向扩张的时候overlap
    is_even = ((len(a) - len(b)) % 2 == 0)
    is_odd = not is_even
    # 分治法
    half_supply = ceil((len(a) + len(b)) / 2)
    # set用于检测扩张时是否overlap
    f_extend_s = set()
    r_extend_s = set()
    # 当前supply
    counter = [0, 0]

    # 正向扩张
    def forward():
        max_x_nth_k = {1: 0}
        for supply in range(half_supply + 1):
            counter[0] = supply

            for nth_k in range(-supply, supply + 1, 2):
                # snake: [..., point: (x, y)]
                snake = []
                is_overlap = False

                if nth_k == -supply or \
                        (nth_k != supply and max_x_nth_k[nth_k - 1] < max_x_nth_k[nth_k + 1]):
                    x = max_x_nth_k[nth_k + 1]
                    # snake起始点, x不变, y少1
                    snake.append((x, x - (nth_k + 1)))
                else:
                    # y不变, x少1
                    snake.append((max_x_nth_k[nth_k - 1], max_x_nth_k[nth_k - 1] - (nth_k - 1)))
                    x = max_x_nth_k[nth_k - 1] + 1
                y = x - nth_k
                # snake中间点
                snake.append((x, y))

                if is_odd and (x, y) in r_extend_s:
                    is_overlap = True
                while x < len(a) and y < len(b) and a[x] == b[y]:
                    x += 1
                    y += 1
                    if is_overlap and (x, y) not in r_extend_s:
                        break
                    # snake尾巴点
                    snake.append((x, y))

                    if not is_overlap and is_odd and (x, y) in r_extend_s:
                        is_overlap = True
                if is_overlap:
                    yield snake
                max_x_nth_k[nth_k] = x
                f_extend_s.update(snake)
            # 切换到反方向的generator
            yield False

    # 反向扩张
    def reverse():
        # reverse就相当于反向扩张, 输出时再变换恢复
        reverse_a = a[::-1]
        reverse_b = b[::-1]

        def r_a(i: int) -> int:
            return i + round(((len(reverse_a) - 1) / 2 - i) * 2)

        def r_b(i: int) -> int:
            return i + round(((len(reverse_b) - 1) / 2 - i) * 2)

        def r_ab(point: tuple) -> tuple:
            a, b = point
            return r_a(a), r_b(b)

        max_x_nth_k = {1: 0}
        for supply in range(half_supply + 1):
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

                if is_even and r_ab((x, y)) in f_extend_s:
                    is_overlap = True
                while x < len(reverse_a) and y < len(reverse_b) and reverse_a[x] == reverse_b[y]:
                    x += 1
                    y += 1
                    if is_overlap and r_ab((x, y)) not in f_extend_s:
                        break
                    snake.append((x, y))

                    if not is_overlap and is_even and r_ab((x, y)) in f_extend_s:
                        is_overlap = True
                if is_overlap:
                    yield [r_ab(point) for point in snake]
                max_x_nth_k[nth_k] = x
                r_extend_s.update(r_ab(point) for point in snake)
            yield False

    # 主体调用部分
    forward_g = forward()
    reverse_g = reverse()
    for _ in range(half_supply + 1):

        snake = next(forward_g)
        if snake is not False:
            return snake, sum(counter)

        snake = next(reverse_g)
        if snake is not False:
            return snake, sum(counter)

###
def diff(a: str, b: str, output_l: list):
    if len(a) > 0 and len(b) > 0:
        # 小规模问题加速组件
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
        print(snake)
        # snake: [(x, y), ..., (u, v)]
        sorted_snake = sorted(snake)
        x, y = sorted_snake[0]
        u, v = sorted_snake[-1]

        if supply > 1:
            diff(a[:x], b[:y], output_l)
            output_l.extend(snake)

            # 必须跳跃的两种情况
            if (u - 1 == 0 and v - 1 == 0) or (u - 1 < len(a) and v - 1 < len(b) and a[u - 1] == b[v - 1]):
                diff(a[u:], b[v:], output_l)
            else:
                diff(a[max(u - 1, 0):], b[max(v - 1, 0):], output_l)
        elif len(b) > len(a):
            output_l.extend(list(a))
        else:
            output_l.extend(list(b))


if __name__ == '__main__':
    from random import randint, choice


    def longest_common_string(string_a: str, string_b: str):
        def get_longest_string_length(a_index: int, b_index: int):
            if a_index == -1 or b_index == -1:
                return 0
            if string_a[a_index] == string_b[b_index]:
                return get_longest_string_length(a_index - 1, b_index - 1) + 1
            else:
                longest_common_string_len_except_a = get_longest_string_length(a_index - 1, b_index)
                longest_common_string_len_except_b = get_longest_string_length(a_index, b_index - 1)
                if longest_common_string_len_except_a >= longest_common_string_len_except_b:
                    return longest_common_string_len_except_a
                else:
                    return longest_common_string_len_except_b

        return get_longest_string_length(len(string_a) - 1, len(string_b) - 1)


    CHAR_L = 'QWERTYUIOP'


    def main():
        for _ in range(100):
            print('--------')
            rand_a = ''.join(choice(CHAR_L) for _ in range(randint(3, 5)))
            rand_b = ''.join(choice(CHAR_L) for _ in range(randint(3, 5)))
            print('a:', rand_a)
            print('b:', rand_b)

            length = longest_common_string(rand_a, rand_b)
            print('len:', length)

            output_l = []
            diff(rand_a, rand_b, output_l)
            if len(output_l) != length:
                return print('!', output_l)


    def main_2():
        a = 'IRIYW'
        b = 'UR'
        # length = longest_common_string(a, b)
        # print('len:', length)
        #
        # output_l = []
        # diff(a, b, output_l)
        # print(output_l)
        snake, supply = find_mid_snake(a, b)
        print(snake, supply)


    main_2()
