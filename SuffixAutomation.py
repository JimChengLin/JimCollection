class State:
    counter = 0

    def __init__(self):
        self.len = None
        self.reboot = None
        self.trans = {}
        self.is_end = False
        self.id = State.counter
        State.counter += 1

    def __repr__(self):
        ret = 'id: {}, len: {},trans: {}, reboot: {}'.format(self.id, self.len,
                                                             [(k, v.id) for k, v in self.trans.items()],
                                                             self.reboot.id if self.reboot is not None else 'void')
        for v in self.trans.values():
            ret += '\n' + str(v)
        return ret


class Automation:
    # 均摊分析可证明线性复杂度
    def __init__(self):
        self.root = State()
        self.root.len = 0
        self.last_state = self.root

    def grow(self, char):
        last_state = self.last_state

        # 每 grow 一个 char, 至少会增加一个状态
        curr_state = State()
        curr_state.len = last_state.len + 1

        while char not in last_state.trans:
            # 所有能趴在 last_state 的 state, 在 grow 了 char 之后, 也应该要能趴在 char 上
            last_state.trans[char] = curr_state

            # 递推同样可知
            if last_state.reboot is not None:
                last_state = last_state.reboot
            else:  # 已经指向了虚空, 从头开始(没地方 reboot 的意思)
                curr_state.reboot = self.root
                break

        else:
            # 开始遇见 repeat pattern 了
            poss_reboot = last_state.trans[char]

            # 因为 repeat 是连续的, 所以长度符合预期.
            # 即, 在 char 和 前一个点重启, 长度差 1
            if poss_reboot.len == last_state.len + 1:
                curr_state.reboot = poss_reboot
            else:
                # 因为是从 last_state 跳跃过来的, 而这如果当了 reboot 点
                # 跳跃之间的 state, 就认为成功了, 这有矛盾, 从图也可以看出来
                # 简单来说, 接受状态没地方放了
                # 解决方案是将 suffix 显化, last_state 不再跳跃到 poss_reboot, 而是 clone
                # 为了正确性, 稍微增加了状态机的冗余
                clone = State()
                clone.reboot = poss_reboot.reboot
                clone.trans = poss_reboot.trans.copy()
                clone.len = last_state.len + 1

                # 所有跳跃到 poss_reboot 的点都重定向至 clone
                while last_state.trans[char] == poss_reboot:
                    last_state.trans[char] = clone

                    if last_state.reboot is not None:
                        last_state = last_state.reboot
                    else:
                        break

                # 本来应该重叠的 reboot 任务剥离出去了, 所以 poss_reboot 要 reboot 于 clone
                # curr_state 又 reboot 于 poss_reboot, 所以 curr_state reboot 于 clone
                poss_reboot.reboot = clone
                curr_state.reboot = poss_reboot.reboot
        self.last_state = curr_state

    def mark_end(self):
        last_state = self.last_state
        while True:
            last_state.is_end = True
            if last_state.reboot is not None and last_state.reboot.id != 0:
                last_state = last_state.reboot
            else:
                break

    def feed(self, src: str):
        curr_state = self.root
        for i, char in enumerate(src):
            if curr_state is self.root:
                print('begin at: {}'.format(i))

            while True:
                next_state = curr_state.trans.get(char)

                if next_state is not None:  # 成功转移状态
                    curr_state = next_state
                    if curr_state.is_end:
                        print('end at: {}, id: {}'.format(i, curr_state.id))
                    break

                elif curr_state is self.root:  # 无法 reboot
                    break

                else:  # 跳至 reboot 继续尝试
                    curr_state = curr_state.reboot
                    if curr_state.is_end:
                        # 重启造成的击杀, i 要 -1
                        print('end at: {}, id: {}'.format(i - 1, curr_state.id))

    def __repr__(self):
        return str(self.root)


if __name__ == '__main__':
    auto = Automation()
    for i in 'abcbc':
        auto.grow(i)
    auto.mark_end()
    auto.feed('sicneacbcbdobcacbcadoabcbc')
