array = [None for i in range(10)]

head = 0
tail = 9


def queue_rotate():
    global head, tail

    if tail > 0:
        tail -= 1
    else:
        tail = 9


def queue_push(item):
    global head, tail

    array[tail] = item
    head = tail
    queue_rotate()


def queue_pop():
    global head, tail

    result = array[tail]
    array[tail] = None
    queue_rotate()

    return result


for i in range(10):
    queue_push(i)
print(array)
for i in range(10):
    print(queue_pop())

array = [None for i in range(10)]

top = 0


def stack_push(item):
    global top

    array[top] = item
    if top <= 8:
        top += 1


def stack_pop():
    global top

    result = array[top]
    top -= 1
    return result


for i in range(10):
    stack_push(i)
print(array)
for i in range(10):
    print(stack_pop())
