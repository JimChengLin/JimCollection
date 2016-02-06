from typing import List, Dict, Tuple


def rk_match(source: List[int], pattern: List[int], radix_size: int, hash_size: int):
    multiplier = radix_size ** (len(pattern) - 1) % hash_size

    pattern_hash = 0
    curr_source_hash = 0
    for i in range(len(pattern)):
        pattern_hash = (radix_size * pattern_hash + pattern[i]) % hash_size
        curr_source_hash = (radix_size * curr_source_hash + source[i]) % hash_size

    for i in range(len(source) - len(pattern)):
        if curr_source_hash == pattern_hash and source[i:i + len(pattern)] == pattern:
            print('Match in {}'.format(i))

        if i < len(source) - len(pattern) - 1:
            curr_source_hash = (radix_size * (curr_source_hash - source[i] * multiplier) +
                                source[i + len(pattern)]) % hash_size


if __name__ == '__main__':
    def rk_main():
        source = [2, 3, 4, 9, 0, 2, 3, 1, 4, 1, 5, 2, 6, 7, 3, 9, 9, 2, 1]
        pattern = [3, 1, 4, 1, 5]
        rk_match(source, pattern, 10, 13)


def automation_match(source: str, jump_map: Dict[Tuple[int, str], int], end_state: int):
    curr_state = 0
    for i in range(len(source)):
        curr_state = jump_map[(curr_state, source[i])]
        if curr_state == end_state:
            print('Match Tail in {}'.format(i))


def build_jump_map(pattern: str, input_list: List[str]) -> Dict[Tuple[int, str], int]:
    jump_map = {}
    reboot_map = {}

    for curr_state in range(len(pattern) + 1):
        for curr_input in input_list:

            if curr_input not in pattern:
                next_state = 0

            elif curr_state < len(pattern):
                if curr_input == pattern[curr_state]:
                    next_state = curr_state + 1

                    if curr_state > 0:
                        reboot_map[(pattern[curr_state - 1], curr_input)] = next_state
                else:
                    next_state = reboot_map.get((pattern[curr_state - 1], curr_input), 0)
                    if curr_input == pattern[0] and next_state == 0:
                        next_state = 1

            else:
                if curr_input == pattern[0]:
                    next_state = 1
                elif pattern.startswith(pattern[curr_state - 1] + curr_input):
                    next_state = 2
                else:
                    next_state = 0

            jump_map[(curr_state, curr_input)] = next_state
    return jump_map


if __name__ == '__main__':
    def build_main():
        jump_map = build_jump_map('ababaca', ['a', 'b', 'c'])
        for i in sorted(jump_map):
            print('{}:{}'.format(i, jump_map[i]))


    def automation_main():
        jump_map = build_jump_map('ababaca', ['a', 'b', 'c'])
        automation_match('abababacaba', jump_map, 7)


def kmp_match(source: str, pattern: str):
    drift_list = build_kmp_drift_list(pattern)

    matched_num = 0
    for i, curr_char in enumerate(source):
        while matched_num > 0 and curr_char != pattern[matched_num]:
            matched_num = drift_list[matched_num - 1]

        if curr_char == pattern[matched_num]:
            matched_num += 1

        if matched_num == len(pattern):
            print('Match Tail in {}'.format(i))
            matched_num = drift_list[matched_num - 1]


def build_kmp_drift_list(pattern: str) -> List[int]:
    drift_list = [0]
    drift = 0
    for curr_char in pattern[1:]:
        while drift > 0 and curr_char != pattern[drift]:
            # 得出能续接的有哪些，通过减小复用长度
            drift = drift_list[drift]

        if curr_char == pattern[drift]:
            drift += 1

        drift_list.append(drift)
    return drift_list


if __name__ == '__main__':
    def kmp_main():
        kmp_match('abababacaba', 'ababaca')


    kmp_main()
