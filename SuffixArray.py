# 字符串映射成数组的工作与主逻辑无关. 所以假定, 输入即是数组
src_list = [5, 1, 2, 2, 1, 3, 1, 2, 2, 1, 3, 4]

# 尾部填充补位的 0
for _ in range(2):
    src_list.append(0)


# 将 idx 和 val 绑定, 这很 OOP! ヾ(≧O≦)〃嗷~
# 这或许是第一个用 OOP 思路写的 DC3?
class Point:
    def __init__(self, idx, val):
        self.idx = idx  # 全局变量 src_list 中的 index
        self.val = val  # rank
        self.rel_idx = idx  # 分治法下 sub_list 的 index

    def __repr__(self):
        return 'idx:{}, val:{}, rel_idx:{}'.format(self.idx, self.val, self.rel_idx)


point_list = []
for i, val in enumerate(src_list):
    point_list.append(Point(i, val))
# 后面会修改 point_list, 需要一个拷贝来查找相邻 b_1/b_2
point_orig = point_list[:]


def dc3(in_list):
    b1_b2_list = []
    for i, point in enumerate(in_list):
        if point.val != 0 and i % 3 in (1, 2):
            b1_b2_list.append(point)
            point.val = (point.val, in_list[i + 1].val, in_list[i + 2].val)
    b1_b2_orig = b1_b2_list[:]  # 保留原来的
    b1_b2_list.sort(key=lambda point: point.val)  # 自行替换成 Radix Sort

    # 我们根本不在乎每个 point 的 val(rank) 多大, 只要保持顺序即可. 在这里重写 val
    # 严重注意! 需要判断前后 val 是否相等. 是的话, 虽然顺序不同, 但 val 应该是一样的
    # 这步意义是将 3 个 char 的大小浓缩成一个 val, 提供给 b_0(高位组) 使用
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

    if curr_rank != len(b1_b2_list):  # 表明有重复 rank, 即排序未完成, 递归 dc3
        # 这里调整下 b1_b2 的顺序, 不再按照 in_list 排列
        # 因为既然有重复的 rank, 说明 3 个 char 不足以决出胜负
        # 那就再引入 3 个 char, 正好是一个循环
        # So, [b1_0, b2_0, b1_1, b2_1, ...] => [b1_0, b1_1, ..., b2_0, b2_1, ...]
        b1_b2_list[:] = [*(obj for i, obj in enumerate(b1_b2_orig) if i % 2 == 0),
                         *(obj for i, obj in enumerate(b1_b2_orig) if i % 2 == 1)]

        for _ in range(2):
            # 这里 idx 可以设置为任意值, 其只是起到 padding 的作用
            b1_b2_list.append(Point(-1, 0))
        dc3(b1_b2_list)

    # 这里 b1_b2 就已经排序完了, 并且有了独特的 val
    # 利用 b1_b2 的 val 可以排序 b_0
    b_0_list = []
    for i, point in enumerate(in_list):
        if point.val != 0 and i % 3 == 0:
            b_0_list.append(point)
            # 必然会成功排序 b_0, 因为 b_1 的 val 是有序且独特的
            point.val = (point.val, in_list[i + 1].val)
    b_0_list.sort(key=lambda point: point.val)

    # <-- 写一遍相对 idx, 仅用于 Debug
    for i in range(len(in_list)):
        in_list[i].rel_idx = i
    # -->

    # b_0 和 b1_b2 都排序好了, 开始合并
    out_list = []
    while True:
        b_0_head = b_0_list[0]
        b_12_head = b1_b2_list[0]

        def b_0_win():  # b_0 表示的后缀更大
            out_list.append(b_12_head)
            del b1_b2_list[0]

        def b_12_win():  # b_12 表示的后缀更大
            out_list.append(b_0_head)
            del b_0_list[0]

        if b_12_head.rel_idx % 3 == 1:  # b_0 vs b_1
            if src_list[b_0_head.idx] > src_list[b_12_head.idx]:
                b_0_win()
            elif src_list[b_0_head.idx] < src_list[b_12_head.idx]:
                b_12_win()
            # 以上两种为能直接决出胜负的情况

            else:  # 如不能, 一定可以用 b_0 之后的 b_1 和 b_1 之后的 b_2 决出胜负
                if point_orig[b_0_head.idx + 1].val > point_orig[b_12_head.idx + 1].val:
                    b_0_win()
                else:
                    b_12_win()

        else:  # b_0 vs b_2 原理相仿
            if src_list[b_0_head.idx] > src_list[b_12_head.idx]:
                b_0_win()
            elif src_list[b_0_head.idx] < src_list[b_12_head.idx]:
                b_12_win()

            else:
                if src_list[b_0_head.idx + 1] > src_list[b_12_head.idx + 1]:
                    b_0_win()
                elif src_list[b_0_head.idx + 1] < src_list[b_12_head.idx + 1]:
                    b_12_win()

                else:
                    if point_orig[b_0_head.idx + 2].val > point_orig[b_12_head.idx + 2].val:
                        b_0_win()
                    else:
                        b_12_win()

        # 判断是否终结
        if not b_0_list:
            out_list.extend(b1_b2_list)
            break
        elif not b1_b2_list:
            out_list.extend(b_0_list)
            break

    in_list[:] = out_list
    # 同样, 排序之后, 重写 val
    for i in range(len(in_list)):
        in_list[i].val = i
    return in_list


if __name__ == '__main__':
    result = dc3(point_list)
    for i in result:
        print(i.idx)
