from math import sqrt
from collections import deque


def bit_int(n: int) -> int:
    integer = 0
    for i in range(n):
        integer <<= 1
        integer |= 1
    return integer


class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next_node = None


class HashTable:
    def __init__(self, n_bit_slots, n_bit_max_int):
        self.n_bit_slots = n_bit_slots
        self.slots = []
        for i in range(2 ** n_bit_slots):
            self.slots.append(None)

        self.n_bit_max_int = n_bit_max_int
        self.max_int = 2 ** self.n_bit_max_int

        fraction = (sqrt(5) - 1) / 2
        self.fraction_cache = int(fraction * self.max_int)

    def __setitem__(self, key, value):
        index = self.hash(key)
        slot = self.slots[index]
        set_node = HashNode(key, value)
        if slot:
            set_node.next_node = slot
        self.slots[index] = set_node

    def __getitem__(self, key):
        index = self.hash(key)
        slot = self.slots[index]
        while slot:
            if slot.key == key:
                return slot.value
            else:
                slot = slot.next_node

    def __delitem__(self, key):
        q = deque(maxlen=2)
        index = self.hash(key)
        slot = self.slots[index]
        while slot:
            q.append(slot)
            if slot.key == key:
                break
        else:
            return
        try:
            curr_node = q.pop()
        except IndexError:
            curr_node = None
        try:
            prev_node = q.pop()
        except IndexError:
            prev_node = None

        if curr_node and prev_node:
            prev_node.next_node = curr_node.next_node

        # only one node
        elif not prev_node and curr_node:
            self.slots[index] = None

    def hash(self, key):
        index = divmod(key * self.fraction_cache, self.max_int)[1]
        index_bit_length = index.bit_length()

        if index_bit_length > self.n_bit_slots:
            index >>= (index_bit_length - (self.n_bit_max_int - index_bit_length))
        return index


# ------------------------------------------------------

class OpenHashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '{} : {}'.format(self.key, self.value)


class NIL:
    pass


class OpenHashTable:
    def __init__(self, n_bit_slots, n_bit_max_int):
        self.n_bit_slots = n_bit_slots
        self.slots = []
        for i in range(2 ** n_bit_slots):
            self.slots.append(OpenHashNode(None, None))

        self.n_bit_max_int = n_bit_max_int
        self.max_int = 2 ** self.n_bit_max_int

        fraction = (sqrt(5) - 1) / 2
        self.fraction_cache_first = int(fraction * self.max_int)
        self.fraction_cache_second = int(fraction * len(self.slots))

    def __setitem__(self, key, value):
        slot = self.hash(key)
        slot.value = value
        slot.key = key

    def __getitem__(self, key):
        slot = self.hash(key)
        return slot.value

    def __delitem__(self, key):
        slot = self.hash(key)
        slot.value = NIL

    def hash(self, key):
        index = divmod(key * self.fraction_cache_first, self.max_int)[1]
        index_bit_length = index.bit_length()
        if index_bit_length > self.n_bit_slots:
            index >>= (index_bit_length - (self.n_bit_max_int - index_bit_length))

        offset = divmod(key * self.fraction_cache_second, len(self.slots))[1]
        if not offset & 1:
            offset -= 1

        probe_seq = 0
        nil_keep = None
        slot = self.slots[index]
        while probe_seq < len(self.slots):
            if slot.key == key:
                return slot
            elif slot.value == NIL:
                nil_keep = slot
            elif slot.value is None:
                return slot

            probe_seq += 1
            slot = self.slots[(index + probe_seq * offset) % len(self.slots)]

        if nil_keep:
            return nil_keep
        else:
            raise KeyError('The table is full.')


# -------------------------------------------------------
if __name__ == '__main__':
    def hash_table_test():
        hash_table = HashTable(14, 32)
        print(hash_table.hash(123456))
        hash_table[123] = 321
        hash_table[78910] = 456789

        print(hash_table[123], hash_table[78910])
        del hash_table[123]
        print(hash_table[123])


    def open_hash_table_test():
        hash_table = OpenHashTable(14, 32)
        hash_table[123456] = 654321
        print(hash_table[123456])
        for i in range(16383):
            hash_table[i] = i
        for i in range(16383):
            print(hash_table[i])
            if hash_table[i] != i:
                raise KeyError('Something goes wrong')
        del hash_table[123456]
        print(hash_table[123456])
        hash_table[123456] = 123456
        print(hash_table[123456])

    open_hash_table_test()
