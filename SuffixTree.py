from typing import Dict

curr_str = ''


class STNode:
    id_counter = 0
    default_suffix_link: 'STNode' = None

    def __init__(self):
        self.content_: Dict[str, STNode] = {}

        self.op: int = None
        self._ed: int = None
        self.suffix_link: STNode = STNode.default_suffix_link
        self.parent: STNode = None

        self.idt = STNode.id_counter
        STNode.id_counter += 1

    def __getitem__(self, key: str):
        return self.content_[key]

    def __setitem__(self, key: str, value: 'STNode'):
        self.content_[key] = value

    def __contains__(self, key: str):
        return key in self.content_

    def __lt__(self, other: 'STNode'):
        return str(self) < str(other)

    def __repr__(self):
        if self.is_root:
            return f'# id:{self.idt}'
        else:
            op, ed = self.op, self.ed
            return f'{curr_str[op:ed]} {op}:{ed} id:{self.idt} lk:{self.suffix_link.idt}'

    def __iter__(self):
        yield from curr_str[self.op:self.ed]

    @property
    def ed(self):
        return self._ed if self._ed != ':ed' else len(curr_str)

    @ed.setter
    def ed(self, val):
        self._ed = val

    @property
    def is_root(self):
        return self.op is None and self.ed is None

    @property
    def is_inner(self):
        return not self.is_root and self.content_

    @property
    def is_leaf(self):
        return not self.is_root and not self.content_


class SuffixTree:
    def __init__(self):
        self.root = STNode()
        STNode.default_suffix_link = self.root

        self.remainder = 0
        self.cursor = 0

        self.act_node = self.root
        self.act_direct = 0
        self.act_offset = 0

    def __repr__(self):
        ret = ''

        def print_node(node: STNode, lv=0):
            nonlocal ret
            if lv == 0:
                prefix = ''
            else:
                prefix = '  ' * (lv - 1) + '--'

            if node is self.act_node:
                prefix += '*'

            ret += f'{prefix}{node}\n'

            for child in sorted(node.content_.values()):
                print_node(child, lv + 1)

        print_node(self.root)

        ret += ', '.join('{}: {}'.format(k, v) for k, v in self.__dict__.items())
        return ret

    def insert_char(self, char: str):
        global curr_str
        curr_str += char
        self.remainder += 1

        def case_root():
            if char not in self.root:
                leaf_node = STNode()
                leaf_node.parent = self.root
                leaf_node.op = self.cursor
                leaf_node.ed = ':ed'
                self.root[char] = leaf_node
                self.remainder -= 1
            else:
                edge_node = self.root[char]
                self.act_direct = edge_node.op
                self.act_offset += 1
                assert self.act_offset == 1

        if self.act_node.is_root and self.act_offset == 0:
            case_root()
        else:
            edge_node = self.act_node[curr_str[self.act_direct]]

            if edge_node.op + self.act_offset == edge_node.ed \
                    and char in edge_node:
                self.act_node = edge_node
                self.act_direct = edge_node[char].op
                self.act_offset = 1
            elif char == curr_str[edge_node.op + self.act_offset]:
                self.act_offset += 1

            else:
                prev_inner_node: STNode = None

                def split_grow():
                    nonlocal prev_inner_node

                    leaf_node = STNode()
                    leaf_node.op = self.cursor
                    leaf_node.ed = ':ed'
                    self.remainder -= 1

                    if (edge_node.is_leaf or edge_node.ed - edge_node.op > 1) \
                            and edge_node.op + self.act_offset != edge_node.ed:
                        inner_node = STNode()
                        if prev_inner_node:
                            prev_inner_node.suffix_link = inner_node
                        prev_inner_node = inner_node

                        inner_node.op = edge_node.op
                        inner_node.ed = inner_node.op + self.act_offset
                        inner_node.parent = edge_node.parent
                        inner_node.parent[curr_str[inner_node.op]] = inner_node

                        edge_node.op = inner_node.ed
                        edge_node.parent = inner_node

                        inner_node[curr_str[edge_node.op]] = edge_node
                        inner_node[curr_str[leaf_node.op]] = leaf_node
                        leaf_node.parent = inner_node
                    else:
                        if prev_inner_node:
                            prev_inner_node.suffix_link = edge_node
                        prev_inner_node = edge_node

                        edge_node[curr_str[leaf_node.op]] = leaf_node
                        leaf_node.parent = edge_node

                def overflow_fix():
                    nonlocal edge_node
                    edge_node = self.act_node[curr_str[self.act_direct]]
                    supply = edge_node.ed - edge_node.op
                    if self.act_offset > supply:
                        self.act_node = edge_node
                        self.act_direct += supply
                        self.act_offset -= supply
                        return overflow_fix()

                while self.remainder > 0:
                    split_grow()

                    if not self.act_node.is_inner:
                        self.act_offset -= 1
                        self.act_direct += 1

                        if self.act_offset > 0:
                            overflow_fix()
                        else:
                            case_root()
                            break

                    else:
                        self.act_node = self.act_node.suffix_link
                        overflow_fix()

                    if edge_node.op + self.act_offset == edge_node.ed \
                            and char in edge_node:
                        self.act_node = edge_node
                        self.act_direct = edge_node[char].op
                        self.act_offset = 1

                        if prev_inner_node:
                            prev_inner_node.suffix_link = self.act_node
                        break
                    elif char == curr_str[edge_node.op + self.act_offset]:
                        break
        self.cursor += 1

    def __contains__(self, item: str):
        edge_node = self.root.content_.get(item[0])
        if edge_node is None:
            return False

        i = 0
        while True:
            for exist_char in edge_node:
                if exist_char != item[i]:
                    return False
                else:
                    i += 1
                    if i == len(item):
                        return True
            edge_node = edge_node.content_[item[i]]


if __name__ == '__main__':
    from random import choice

    st = SuffixTree()


    def bundle_test(test_data):
        global curr_str
        curr_str = ''
        for i, char in enumerate(test_data):
            # print()
            # print('insert', char)
            st.insert_char(char)

            # print(i, 'th')
            # print(st)

            for start in range(i + 1):
                # print('testing', test_data[start:i + 1])
                assert test_data[start:i + 1] in st
        st.__init__()


    alphabet = ('A', 'B', 'C', 'D', 'E')

    for _ in range(10000):
        test_d = ''
        for _ in range(20):
            test_d += choice(alphabet)
        print(test_d)
        bundle_test(test_d)
