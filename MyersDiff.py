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


def find_mid_snake(a: str, b: str):
    delta = len(a) - len(b)
    diff_gen = diff_len(a, b)
    diff_reverse_gen = diff_len_reverse(a, b)

    for supply in range(ceil((len(a) + len(b)) / 2)):
        try:
            print(diff_gen.send(None))
            print(diff_reverse_gen.send(None))
        except StopIteration:
            break
        print('------')


if __name__ == '__main__':
    # 测试用例
    A = 'ABCABBA'
    B = 'CBABAC'
    find_mid_snake(A, B)
