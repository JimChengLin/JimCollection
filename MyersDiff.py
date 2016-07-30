from math import ceil


def diff_len(a: str, b: str):
    max_supply = len(a) + len(b)
    best_x_nth_k_line = {1: 0}

    for supply in range(max_supply + 1):
        snake_s = set()
        for nth_k in range(-supply, supply + 1, 2):

            if nth_k == -supply or (nth_k != supply and best_x_nth_k_line[nth_k - 1] < best_x_nth_k_line[nth_k + 1]):
                x = best_x_nth_k_line[nth_k + 1]
            else:
                x = best_x_nth_k_line[nth_k - 1] + 1
            y = x - nth_k

            while x < len(a) and y < len(b) and a[x] == b[y]:
                snake_s.add((x, y))
                x += 1
                y += 1
            best_x_nth_k_line[nth_k] = x

            if x >= len(a) and y >= len(b):
                yield snake_s
                return
        yield snake_s


def diff_len_reverse(a: str, b: str):
    a = a[::-1]
    b = b[::-1]
    x_reverse_table = [0, *reversed(range(1, len(a) + 1))]
    y_reverse_table = [0, *reversed(range(1, len(b) + 1))]

    max_supply = len(a) + len(b)
    best_x_nth_k_line = {1: 0}

    for supply in range(max_supply + 1):
        snake_s = set()
        for nth_k in range(-supply, supply + 1, 2):

            if nth_k == -supply or (nth_k != supply and best_x_nth_k_line[nth_k - 1] < best_x_nth_k_line[nth_k + 1]):
                x = best_x_nth_k_line[nth_k + 1]
            else:
                x = best_x_nth_k_line[nth_k - 1] + 1
            y = x - nth_k

            while x < len(a) and y < len(b) and a[x] == b[y]:
                snake_s.add((x_reverse_table[x + 1] - 1, y_reverse_table[y + 1] - 1))
                x += 1
                y += 1
            best_x_nth_k_line[nth_k] = x

            if x >= len(a) and y >= len(b):
                yield snake_s
                return
        yield snake_s


def overlap(a_snake_s: set, b_snake_s: set) -> set:
    return a_snake_s & b_snake_s


def find_mid_snake(a: str, b: str) -> set:
    delta = len(a) - len(b)
    is_even = (delta % 2 == 0)

    diff_gen = diff_len(a, b)
    diff_reverse_gen = diff_len_reverse(a, b)

    result = set()
    reverse = set()
    for supply in range(ceil((len(a) + len(b)) / 2)):
        try:
            forward = next(diff_gen)
            if not is_even:
                result.update(overlap(forward, reverse))
            reverse = next(diff_reverse_gen)
            if is_even:
                result.update(overlap(forward, reverse))
        except StopIteration:
            break
    print(result)
    return result


_result = set()


def diff(a: str, b: str):
    if len(a) > 0 and len(b) > 0:
        _a = find_mid_snake(a, b)
        _a = _a.pop()
        _result.add(_a)
        u, v = _a
        x, y = u - 1, v - 1
        diff(a[:x + 1], b[:y + 1])
        diff(a[u:], b[v:])


if __name__ == '__main__':
    # 测试用例
    A = 'ABCABBA'
    B = 'CBABAC'
    diff(A, B)
    print(_result)
