from math import inf
from random import randint


class SkipListNode:
    def __init__(self):
        self.val = -inf  # 默认 head
        self.arrow_right = None  # type: SkipListNode
        self.arrow_bottom = None  # type: SkipListNode

    def __repr__(self):
        return str(self.val)

    def prt(self):
        print(self, '', end='')
        cursor = self.arrow_right
        while cursor is not None:
            print(cursor.val, '', end='')
            cursor = cursor.arrow_right
        print()
        if self.arrow_bottom is not None:
            return self.arrow_bottom.prt()


class SkipList:
    def __init__(self):
        self.top_node = SkipListNode()  # type: SkipListNode

    def insert(self, val):
        # 坐地铁到最底层, 并记录沿途路径
        path = []
        cursor = self.top_node
        while cursor.arrow_bottom is not None:
            while True:
                if cursor.arrow_right is None:
                    break
                elif cursor.arrow_right.val == val:
                    return
                elif cursor.arrow_right.val < val:
                    cursor = cursor.arrow_right
                else:
                    break
            path.append(cursor)
            cursor = cursor.arrow_bottom

        # 到达底部, 当前 cursor.val < val, 新建一个 node
        while True:
            if cursor.arrow_right is None:
                break
            elif cursor.arrow_right.val < val:
                cursor = cursor.arrow_right
            elif cursor.arrow_right.val == val:
                return
            else:
                break
        new_node = SkipListNode()
        new_node.val = val

        orig_arrow_right = cursor.arrow_right
        cursor.arrow_right = new_node
        new_node.arrow_right = orig_arrow_right

        # 按概率更新路径
        for path_node in reversed(path):
            if randint(0, 1):
                up_new_node = SkipListNode()
                up_new_node.val = val
                up_new_node.arrow_bottom = new_node

                up_orig_arrow_right = path_node.arrow_right
                path_node.arrow_right = up_new_node
                up_new_node.arrow_right = up_orig_arrow_right
                new_node = up_new_node
            else:
                break
        else:
            # 加一层
            if randint(0, 1):
                up_new_node = SkipListNode()
                up_new_node.val = val
                up_new_node.arrow_bottom = new_node

                new_top_node = SkipListNode()
                new_top_node.arrow_bottom = self.top_node
                self.top_node = new_top_node
                new_top_node.arrow_right = up_new_node

    def delete(self, val):
        del_list = []
        cursor = self.top_node
        while cursor.arrow_bottom is not None:
            while True:
                if cursor.arrow_right is None:
                    break
                elif cursor.arrow_right.val == val:
                    del_list.append(cursor)
                    break
                elif cursor.arrow_right.val <= val:
                    cursor = cursor.arrow_right
                else:
                    break
            cursor = cursor.arrow_bottom

        while True:
            if cursor.arrow_right is None:
                break
            elif cursor.arrow_right.val == val:
                del_list.append(cursor)
                break
            elif cursor.arrow_right.val < val:
                cursor = cursor.arrow_right
            else:
                break

        for next_need_del_cursor in del_list:
            next_next_right = next_need_del_cursor.arrow_right.arrow_right
            next_need_del_cursor.arrow_right = next_next_right


if __name__ == '__main__':
    sl = SkipList()
    all = []
    for i in range(100):
        all.append(randint(0, 200))
        sl.insert(all[-1])
    sl.top_node.prt()
    print('---')
    for i in all:
        sl.delete(i)
    sl.top_node.prt()
