from bisect import bisect
from numbers import Number
from queue import Queue
from threading import Thread
from typing import List


# Python多线程有GIL限制，多进程无法简单共享Object，运算速度将会和理论有偏差
# 来回创建与合并List，速度退化为O(n)，最佳实现为O(log^2 n)
def merge(a: List[Number], b: List[Number], output_q: Queue = None) -> List[Number]:
    if len(a) < len(b):
        a, b = b, a

    if len(a) == 0:
        result = []
    else:
        a_median_index = len(a) // 2
        a_median = a[a_median_index]
        a_median_in_b_index = bisect(b, a_median)

        communicate_q = Queue()
        Thread(target=merge, args=(a[:a_median_index], b[:a_median_in_b_index], communicate_q)).start()
        after_median_list = merge(a[a_median_index + 1:], b[a_median_in_b_index:])

        before_median_list = communicate_q.get()
        result = [*before_median_list, a_median, *after_median_list]

    if output_q:
        output_q.put(result)
    else:
        return result


# 此实现亦无法达到最佳值O(log^3 n)
def merge_sort(root: List[Number], output_q: Queue = None) -> List[Number]:
    if len(root) == 1:
        result = root
    else:
        middle = len(root) // 2
        communicate_q = Queue()
        Thread(target=merge_sort, args=(root[:middle], communicate_q)).start()
        b = merge_sort(root[middle:], )
        a = communicate_q.get()
        result = merge(a, b)

    if output_q:
        output_q.put(result)
    else:
        return result


if __name__ == '__main__':
    def sort_main():
        sample = [4, 1, 0, 3, 3, 454, 29, 545, 3434, 8989, 35, 37]
        print(merge_sort(sample))


    def merge_main():
        a = merge([1, 2, 3, 4], [2, 3, 4, 5])
        print(a)


    sort_main()
