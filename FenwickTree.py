eg_arr = [1, 2, 3, 4, 5, 6, 7]
tree_arr = [0] * (len(eg_arr) + 1)


def get_cum_val(idx):
    sum_ = tree_arr[0]
    while idx > 0:
        sum_ += tree_arr[idx]
        idx &= (idx - 1)
    return sum_


def put_val(idx, val):
    while True:
        tree_arr[idx] += val
        idx += (idx & (-idx))
        if idx > len(tree_arr) - 1:
            break


if __name__ == '__main__':
    for i in range(len(eg_arr)):
        put_val(i + 1, eg_arr[i])
    for i in range(len(eg_arr)):
        print(get_cum_val(i + 1))
