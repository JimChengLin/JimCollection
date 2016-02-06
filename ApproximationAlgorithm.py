from typing import List
from bisect import bisect


def trim(input_list: List[int], inaccuracy: float) -> List[int]:
    output_list = [input_list[0]]
    for i in input_list[1:]:
        if i > output_list[-1] * (1 + inaccuracy):
            output_list.append(i)
    return output_list


def approx_subset(options: List[int], target_value: int, inaccuracy: float):
    possible_outputs = [0]

    for option in options:
        possible_outputs = sorted((*possible_outputs, *(i + option for i in possible_outputs)))
        possible_outputs = trim(possible_outputs, inaccuracy / (2 * len(options)))
        possible_outputs = possible_outputs[:bisect(possible_outputs, target_value)]

    print(possible_outputs)


if __name__ == '__main__':
    def approx_main():
        options = [104, 102, 201, 101]
        approx_subset(options, 308, 0.4)


    approx_main()
