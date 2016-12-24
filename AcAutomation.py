class TrieNode:
    def __init__(self):
        self.trans = {}
        self.reboot = None


class AcAutomation:
    def __init__(self):
        self.root = TrieNode()

    def add_str(self, src: str):
        # 可选优化: 加入 output 链表获得更详细的匹配结果
        curr_node = self.root
        for char in (src + '$'):
            next_node = curr_node.trans.get(char)

            if next_node is None:
                next_node = TrieNode()
                curr_node.trans[char] = next_node
            curr_node = next_node

    def build_reboot(self):  # bfs
        q = list(self.root.trans.values())
        # init node 只能在 root 重启
        for state in q:
            state.reboot = self.root

        while q:
            cursor = q.pop(0)
            for char, sub in cursor.trans.items():
                if char == '$':
                    continue
                q.append(sub)

                # sub 如果失败了, 重启点必然位于 cursor 或者 cursor 的重启点
                # bfs 保证重启点的选取是全局最优的
                parent_reboot = cursor.reboot
                while True:
                    # 能不能继承(延长)这个 reboot? 能
                    if char in parent_reboot.trans:
                        sub.reboot = parent_reboot.trans[char]
                        break
                    else:
                        # 放低要求, 寻找重启点的重启点
                        parent_reboot = parent_reboot.reboot
                        if parent_reboot is None:
                            sub.reboot = self.root
                            break

    def feed(self, src: str):
        curr_state = self.root
        for i, char in enumerate(src):

            while True:
                next_state = curr_state.trans.get(char)

                if next_state is not None:
                    curr_state = next_state
                    if '$' in curr_state.trans:
                        print('end at: {}'.format(i))
                    break

                elif curr_state is self.root:
                    break

                else:
                    curr_state = curr_state.reboot
                    if '$' in curr_state.trans:
                        print('end at: {}'.format(i))


if __name__ == '__main__':
    auto = AcAutomation()
    auto.add_str('abce')
    auto.add_str('bcfa')
    auto.build_reboot()

    auto.feed('abcfabcabcea')
