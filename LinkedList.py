class DoubleLinkedNode:
    def __init__(self, value, prev_node=None, next_node=None):
        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node

    def __repr__(self):
        return '{}'.format(self.value)


class DoubleLinkedList:
    def __init__(self):
        self.sentinel = DoubleLinkedNode(None)
        self.sentinel.prev_node = self.sentinel
        self.sentinel.next_node = self.sentinel
        self.gc_node = None

    def __iter__(self):
        curr_node = self.sentinel.next_node
        while curr_node.value is not None:
            yield curr_node
            curr_node = curr_node.next_node

    def search(self, value):
        for curr_node in self:
            if curr_node.value == value:
                return curr_node

    def delete(self, index):
        count = -1
        for curr_node in self:
            count += 1
            if count == index:
                prev_node = curr_node.prev_node
                next_node = curr_node.next_node
                prev_node.next_node = next_node
                next_node.prev_node = prev_node

                curr_node.next_node = self.gc_node
                self.gc_node = curr_node
                break

    def insert(self, index, value):
        count = -1
        for curr_node in self:
            count += 1
            if count == index:
                prev_node = curr_node.prev_node

                if self.gc_node:
                    insert_node = self.gc_node
                    self.gc_node = self.gc_node.next_node

                    insert_node.value = value
                    insert_node.prev_node = prev_node
                    insert_node.next_node = curr_node
                else:
                    insert_node = DoubleLinkedNode(value, prev_node, curr_node)

                prev_node.next_node = insert_node
                curr_node.prev_node = insert_node
                return

        prev_node = self.sentinel.prev_node
        next_node = self.sentinel

        if self.gc_node:
            insert_node = self.gc_node
            self.gc_node = self.gc_node.next_node

            insert_node.value = value
            insert_node.prev_node = prev_node
            insert_node.next_node = next_node
        else:
            insert_node = DoubleLinkedNode(value, prev_node, next_node)

        prev_node.next_node = insert_node
        next_node.prev_node = insert_node


class SingleLinkedNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

    def __repr__(self):
        return '{}'.format(self.value)


class SingleLinkedList:
    def __init__(self):
        self.init_node = None
        self.gc_node = None

    def search(self, value):
        curr_node = self.init_node
        while curr_node:
            if curr_node.value == value:
                return curr_node
            else:
                curr_node = curr_node.next_node

    def delete(self, index):
        prev_node = curr_node = next_node = None

        count = -1
        node_cursor = self.init_node
        while node_cursor:
            count += 1

            if count == index - 1:
                prev_node = node_cursor
            elif count == index:
                curr_node = node_cursor
            elif count == index + 1:
                next_node = node_cursor
                break
            node_cursor = node_cursor.next_node

        # gc
        curr_node.next_node = self.gc_node
        self.gc_node = curr_node

        # middle
        if prev_node and curr_node and next_node:
            prev_node.next_node = next_node

        # just after the start
        elif not prev_node and curr_node and next_node:
            self.init_node = next_node

        # just before the end
        elif prev_node and curr_node and not next_node:
            prev_node.next_node = None

        # only one
        elif not prev_node and not next_node:
            self.init_node = None

    def insert(self, index, value):
        prev_node = curr_node = None

        count = -1
        node_cursor = self.init_node
        while node_cursor:
            count += 1

            if count == index - 1:
                prev_node = node_cursor
            elif count == index:
                curr_node = node_cursor
                break

            if node_cursor.next_node:
                node_cursor = node_cursor.next_node
            else:
                prev_node = node_cursor
                break

        if self.gc_node:
            insert_node = self.gc_node
            self.gc_node = self.gc_node.next_node
            insert_node.value = value
        else:
            insert_node = SingleLinkedNode(value)

        # middle
        if prev_node and curr_node:
            prev_node.next_node = insert_node
            insert_node.next_node = curr_node

        # just behind the start
        elif not prev_node and curr_node:
            self.init_node = insert_node
            insert_node.next_node = curr_node

        # just before the end
        elif prev_node and not curr_node:
            prev_node.next_node = insert_node
            insert_node.next_node = None

        # no one
        elif not prev_node and not curr_node:
            self.init_node = insert_node
            insert_node.next_node = None

    def __iter__(self):
        curr_node = self.init_node
        while curr_node:
            yield curr_node.value
            curr_node = curr_node.next_node
