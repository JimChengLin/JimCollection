RED = '红'
BLACK = '黑'


class NIL:
    parent = None
    color = BLACK


class RedBlackNode:
    def __init__(self, key=None, value=None):
        self.parent = None  # type: RedBlackNode
        self.small = self.big = NIL  # type: RedBlackNode
        self.color = RED

        self.key = key
        self.value = value

    def __repr__(self):
        return '{}:{}'.format(self.color, self.key, self.value)


class RedBlackTree:
    def __init__(self):
        self.root = NIL

    def __iter__(self):
        for i in self.walk(self.root):
            yield i

    def walk(self, node):
        if node is not NIL:
            for i in self.walk(node.small):
                yield i
            yield node
            for i in self.walk(node.big):
                yield i

    def min(self, cursor=None):
        # Root为NIL没有small和big，不return会出错
        if self.root is NIL:
            return self.root

        if cursor is None:
            cursor = self.root

        while cursor.small is not NIL:
            cursor = cursor.small
        return cursor

    def insert(self, key, value):
        cursor = self.root
        parent = cursor
        while cursor is not NIL:
            parent = cursor
            if key < cursor.key:
                cursor = cursor.small
            else:
                cursor = cursor.big

        insert_node = RedBlackNode(key, value)
        if parent is NIL:
            self.root = insert_node
        else:
            if key < parent.key:
                parent.small = insert_node
            else:
                parent.big = insert_node
            insert_node.parent = parent
        self.insert_fix(insert_node)

    def insert_fix(self, insert_node: RedBlackNode):
        while insert_node is not self.root and insert_node.parent.color == RED:
            if insert_node.parent == insert_node.parent.parent.small:
                uncle_node = insert_node.parent.parent.big

                if uncle_node.color == RED:
                    insert_node.parent.color = uncle_node.color = BLACK
                    insert_node.parent.parent.color = RED
                    insert_node = insert_node.parent.parent

                else:
                    if insert_node == insert_node.parent.big:
                        self.left_rotate(insert_node.parent)
                        insert_node = insert_node.small

                    self.right_rotate(insert_node.parent.parent)
                    insert_node.parent.big.color = RED
                    insert_node.parent.color = BLACK

            else:
                uncle_node = insert_node.parent.parent.small

                if uncle_node.color == RED:
                    insert_node.parent.color = uncle_node.color = BLACK
                    insert_node.parent.parent.color = RED
                    insert_node = insert_node.parent.parent

                else:
                    if insert_node == insert_node.parent.small:
                        self.right_rotate(insert_node.parent)
                        insert_node = insert_node.big

                    self.left_rotate(insert_node.parent.parent)
                    insert_node.parent.small.color = RED
                    insert_node.parent.color = BLACK

        # 在保持黑节点数量的过程中，有可能把根给染红了
        self.root.color = BLACK

    def replace(self, old_node: RedBlackNode, new_node: RedBlackNode):
        if old_node.parent is NIL:
            self.root = new_node
        elif old_node == old_node.parent.small:
            old_node.parent.small = new_node
        else:
            old_node.parent.big = new_node
        new_node.parent = old_node.parent

    def delete(self, del_node):
        # 默认情况，消失的颜色就是删除节点的
        missing_color = del_node.color

        # 没有小弟
        if del_node.small == NIL:
            # 锚点，违背5大性质的路径最低节点，需沿着向上修复，NIL的情况将由self.replace修复
            anchor = del_node.big

            # 大哥顶位
            self.replace(del_node, del_node.big)

        # 没有大哥
        elif del_node.big == NIL:
            anchor = del_node.small

            # 小弟顶位
            self.replace(del_node, del_node.small)

        # 有小弟又有大哥
        else:

            # 接替者为大哥半区的最小值
            successor = self.min(del_node.big)

            # 继承删除节点的颜色，那么消失的颜色就是接替者的
            missing_color = successor.color

            # 接替者不可能有小弟，将锚点置于大哥
            anchor = successor.big

            # 接替者是删除节点的第一个大哥，不需要整编
            if successor.parent == del_node:
                # 锚点有可能是NIL，再赋值
                anchor.parent = successor

            # 接替者位于第一个大哥的小弟半区，不可能是NIL，需要整编
            else:

                # 接替者的大哥顶接替者的位，释放节点
                self.replace(successor, successor.big)

                # 原大哥，仍然是接替者的大哥，指针重定向
                successor.big = del_node.big
                # 指针双向更新
                del_node.big.parent = successor
                # 接替者已经释放完毕

            self.replace(del_node, successor)

            # 全面接管删除点的小弟
            successor.small = del_node.small
            del_node.small.parent = successor

            # 继承颜色
            successor.color = del_node.color

        # 如果弄丢的颜色是红色，就无所谓了。只是把超重的节点，瘦身了一下。
        # 如果是黑色的，子树就变得营养不良了，需要修复。
        if missing_color == BLACK:
            self.delete_fix(anchor)

    def delete_fix(self, anchor: RedBlackNode):
        while anchor is not self.root and anchor.color == BLACK:

            if anchor == anchor.parent.small:
                sibling = anchor.parent.big

                if sibling.color == RED:
                    self.left_rotate(anchor.parent)
                    sibling.color = BLACK
                    sibling.small.color = RED
                    sibling = sibling.small.big

                if sibling.small.color == sibling.big.color == BLACK:
                    sibling.color = RED
                    anchor = anchor.parent

                else:
                    if sibling.small.color == RED:
                        self.right_rotate(sibling)
                        sibling.color = RED
                        sibling.parent.color = BLACK
                        sibling = sibling.parent

                    self.left_rotate(sibling.parent)
                    sibling.color = sibling.small.color
                    sibling.big.color = BLACK
                    sibling.small.color = BLACK
                    break

            else:
                sibling = anchor.parent.small

                if sibling.color == RED:
                    self.right_rotate(anchor.parent)
                    sibling.color = BLACK
                    sibling.big.color = RED
                    sibling = sibling.big.small

                if sibling.big.color == sibling.small.color == BLACK:
                    sibling.color = RED
                    anchor = anchor.parent

                else:
                    if sibling.big.color == RED:
                        self.left_rotate(sibling)
                        sibling.color = RED
                        sibling.parent.color = BLACK
                        sibling = sibling.parent

                    self.right_rotate(sibling.parent)
                    sibling.color = sibling.big.color
                    sibling.small.color = BLACK
                    sibling.big.color = BLACK
                    break

        anchor.color = BLACK

    def right_rotate(self, node: RedBlackNode):
        if node.small is NIL:
            return

        # 如果Node为Root，就没有合适的Parent，建立一个Shadow Node作为Parent
        is_root = False
        if node is self.root:
            is_root = True
            shadow_node = RedBlackNode()
            shadow_node.small, node.parent = node, shadow_node

        if node == node.parent.small:
            node.parent.small, node.small.parent = node.small, node.parent
            node.small, node.parent.small.big.parent = node.parent.small.big, node
            node.parent.small.big, node.parent = node, node.parent.small
        else:
            node.parent.big, node.small.parent = node.small, node.parent
            node.small, node.parent.big.big.parent = node.parent.big.big, node
            node.parent.big.big, node.parent = node, node.parent.big

        if is_root:
            self.root = shadow_node.small
            self.root.parent = NIL

    def left_rotate(self, node: RedBlackNode):
        if node.big is NIL:
            return

        is_root = False
        if node is self.root:
            is_root = True
            shadow_node = RedBlackNode()
            shadow_node.small, node.parent = node, shadow_node

        if node == node.parent.small:
            node.parent.small, node.big.parent = node.big, node.parent
            node.big, node.parent.small.small.parent = node.parent.small.small, node
            node.parent.small.small, node.parent = node, node.parent.small
        else:
            node.parent.big, node.big.parent = node.big, node.parent
            node.big, node.parent.big.small.parent = node.parent.big.small, node
            node.parent.big.small, node.parent = node, node.parent.big

        if is_root:
            self.root = shadow_node.small
            self.root.parent = NIL


# -----------------------------测试
if __name__ == '__main__':

    def main():
        from random import randint

        rb = RedBlackTree()
        right_list = []
        for i in range(50000):
            rand = randint(0, 100)
            rb.insert(rand, rand)
            right_list.append(rand)

        right_list.sort()
        for i, j in zip(rb, right_list):
            print(i)
            if i.key != j:
                raise Exception

        for i in [j for j in rb]:
            rb.delete(i)
        print('after Del')
        for i in rb:
            print(i)


    main()
