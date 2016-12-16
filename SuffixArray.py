# 字符串映射成数组的工作, 麻烦且与主逻辑无关. 所以假定, 输入即是数组
src_list = [5, 1, 2, 2, 1, 3, 1, 2, 2, 1, 3, 4]

# 尾部填充补位的 0
for _ in range(2):
    src_list.append(0)


# 将 idx 和 val 绑定, 这很 OOP ヾ(≧O≦)〃嗷~
class Point:
    def __init__(self, idx, val):
        self.idx = idx
        self.val = val
        self.rel_idx = idx

    def __repr__(self):
        return '{}:{}'.format(self.idx, self.val)


point_list = []
for i, point in enumerate(src_list):
    point_list.append(Point(i, point))


def dc3(in_list):
    b1_b2_list = []
    for i, point in enumerate(in_list):
        if point.val != 0 and i % 3 in (1, 2):
            b1_b2_list.append(point)
            point.val = (point.val, in_list[i + 1].val, in_list[i + 2].val)
    b1_b2_list.sort(key=lambda point: point.val)  # 自行替换成 Radix Sort

    # 我们根本不在乎每个 point 的 val(rank) 多大, 只要保持顺序即可, 在这里重写 val
    # 严重注意! 需要判断前后 val 是否相等. 是的话, 虽然顺序不同, 但 val 应该是一样的
    # 意义是将 3 个 char 的大小比较, 浓缩成一个 val, 提供给 b_0(高位) 使用
    curr_rank = 0
    prev_val = None
    for point in b1_b2_list:
        if prev_val is None:
            curr_rank += 1
            prev_val = point.val
            point.val = curr_rank
            continue

        if point.val != prev_val:
            curr_rank += 1
            prev_val = point.val
        point.val = curr_rank

    if curr_rank != len(b1_b2_list):  # 有重复 rank, 即排序未完成, 递归 dc3
        # 建立对象来符合我们的 OOP 抽象
        for _ in range(2):
            # idx 可以设置为任意, 其只是起到 padding 的作用
            b1_b2_list.append(Point(-1, 0))
        dc3(b1_b2_list)

    # 这里 b1_b2 就已经排序完了, 并且有了独特的 val
    # 利用 b1_b2 的 val 可以排序 b0
    b_0_list = []
    for i, point in enumerate(in_list):
        if point.val != 0 and i % 3 == 0:
            b_0_list.append(point)
            # 必然会成功排序 b_0, 因为 b_1 的 val unique
            point.val = (point.val, in_list[i + 1].val)
    b_0_list.sort(key=lambda point: point.val)

    # b_0 和 b_1_b_2 都排序好了, 开始合并
    # 写一遍相对 index
    for i in range(len(in_list)):
        in_list[i].rel_idx = i

    output_list = []
    while True:
        b_0_head = b_0_list[0]
        b_12_head = b1_b2_list[0]

        if b_12_head.rel_idx % 3 == 1:  # b_0 vs b_1
            if src_list[b_0_head.idx] > src_list[b_12_head.idx]:  # b_0 win
                output_list.append(b_12_head)
                del b1_b2_list[0]

            elif src_list[b_0_head.idx] < src_list[b_12_head.idx]:  # b_12 win
                output_list.append(b_0_head)
                del b_0_list[0]

            else:  # 以上两种为能直接决出胜负的情况
                # 如不能, 一定可以用 b_0 之后的 b_1 和 b_1 之后的 b_2 的 val 决出胜负
                if in_list[b_0_head.rel_idx + 1].val > in_list[b_12_head.rel_idx + 1].val:
                    output_list.append(b_12_head)
                    del b1_b2_list[0]
                else:
                    output_list.append(b_0_head)
                    del b_0_list[0]

        else:  # b_0 vs b_2:
            if src_list[b_0_head.idx] > src_list[b_12_head.idx]:
                output_list.append(b_12_head)
                del b1_b2_list[0]

            elif src_list[b_0_head.idx] < src_list[b_12_head.idx]:
                output_list.append(b_0_head)
                del b_0_list[0]

            else:
                if src_list[b_0_head.idx + 1] > src_list[b_12_head.idx + 1]:
                    output_list.append(b_12_head)
                    del b1_b2_list[0]

                elif src_list[b_0_head.idx + 1] < src_list[b_12_head.idx + 1]:
                    output_list.append(b_0_head)
                    del b_0_list[0]

                else:
                    if in_list[b_0_head.rel_idx + 2].val > in_list[b_12_head.rel_idx + 2].val:
                        output_list.append(b_12_head)
                        del b1_b2_list[0]
                    else:
                        output_list.append(b_0_head)
                        del b_0_list[0]

        # 判断是否终结
        if not b_0_list:
            output_list.extend(b1_b2_list)
            break
        elif not b1_b2_list:
            output_list.extend(b_0_list)
            break
    # 以上合并操作, 如果使用 C Macro 可以大幅度简化

    in_list[:] = output_list
    for i in range(len(in_list)):
        in_list[i].val = i
    return in_list


if __name__ == '__main__':
    dc3(point_list)
