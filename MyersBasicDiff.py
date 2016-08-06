def diff(a: str, b: str, output_l: list) -> int:
    # 一对字符串之间的差异, 表现在图中, 就是竖线与横线
    # 考虑最差的情况, 即A与B完全不相等, 将会有a+b最大总长度的竖线与横线
    # 可以将这个值理解为弹药数量, 每一个差异都是要消灭的敌人
    # 通过逐步提升弹药供给来找到战果最好的消灭方案(斜线最多)
    # 10颗子弹消灭的敌人必然可以由用9颗子弹消灭敌人的最佳方案+第10颗子弹的最佳方案解决
    # 从一个几何的角度去看待LCS问题
    max_supply = len(a) + len(b)

    # 默认把A当作置于上方的x轴, B当作置于下方的y轴
    # k线的下标由x-y决定
    max_x_nth_k = {1: 0}
    snake_d = {1: [(0, -1)]}

    # 0有意义, 所以从1开始计数, range+1
    for supply in range(max_supply + 1):
        # Myers的论文证明了弹药数量的奇偶性与最终所停留的k线的是一致的
        # 所以迭代的步进为2
        for nth_k in range(-supply, supply + 1, 2):

            # 第一个判断的作用: 当处于k_-d线时, 唯一能消耗弹药的方式就是横移到k_-d+1线的x处
            # 两个角度:
            # -d已经是底部了, 不能从更低的k线增量计算
            # 弹药增量是从下往上, 同样的弹药供给, 那么k_-d+1线必然会多消耗一个横移弹药
            # 正确性: k_n+1或k_n-1线最优解可以漂移出增加1个弹药的k_n线最优解
            if nth_k == -supply or (nth_k != supply and max_x_nth_k[nth_k - 1] < max_x_nth_k[nth_k + 1]):
                # 从k_n+1漂移到k_n, x的位置不变, y往下一个单位
                x = max_x_nth_k[nth_k + 1]
                snake_d[nth_k] = snake_d[nth_k + 1][:]
            else:
                # 从k_n-1漂移到k_n, y的位置不变, x向前一个单位
                x = max_x_nth_k[nth_k - 1] + 1
                snake_d[nth_k] = snake_d[nth_k - 1][:]
            # 从k和x可以直接得出y的位置
            y = x - nth_k
            snake_d[nth_k].append((x, y))

            # 本轮弹药补给使用完毕, 开始尝试能否走对角线, 获取战果
            # str下标是从0开始的, 所以实际上a[x] == b[y]相当于自然下标a[x+1] == b[y+1]
            while x < len(a) and y < len(b) and a[x] == b[y]:
                x += 1
                y += 1
                snake_d[nth_k].append((x, y))
            # 最优写回
            max_x_nth_k[nth_k] = x

            # 所有子弹已经打完, 无法获取更多战果
            if x >= len(a) and y >= len(b):
                output_l[:] = snake_d[nth_k]
                return (len(a) + len(b) - supply) // 2


def parse(a: str, b: str, path: list) -> str:
    ret = ''
    prev_x = prev_y = None
    for xy in path:
        x, y = xy
        x -= 1
        y -= 1
        if 0 <= x < len(a) and 0 <= y < len(b) and x != prev_x and y != prev_y and a[x] == b[y]:
            ret += a[x]
            prev_x, prev_y = x, y
    return ret


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


    def main():
        all_char = 'QWERTY'
        for _ in range(500):
            print('------')
            rand_a = ''.join(choice(all_char) for _ in range(randint(3, 10)))
            rand_b = ''.join(choice(all_char) for _ in range(randint(3, 10)))
            print('a:', rand_a)
            print('b:', rand_b)

            output_l = []
            dp_len = longest_common_string(rand_a, rand_b)
            myers_len = diff(rand_a, rand_b, output_l)
            assert dp_len == myers_len == len(parse(rand_a, rand_b, output_l))


    main()
