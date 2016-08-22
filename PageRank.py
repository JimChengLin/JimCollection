from AsyncDB import AsyncDB

FACTOR = 0.15

# 预期协程并发数
CON_NUM = 1000

# 从名字到下标的映射
name_db = AsyncDB('name.db')

# 从下标到数值的映射
data_db = AsyncDB('data.db')


# 为了读取速度, 下标先列再行
class Vertex:
    counter = 0

    def __init__(self, name: str):
        self.name = name
        self.subscript = None

    async def async_init(self):
        # 若已存入硬盘, 无须分配下标
        subscript = await name_db[self.name]
        if subscript is None:
            # 分配到下标并写回
            subscript = Vertex.counter
            name_db[self.name] = self.subscript
            Vertex.counter += 1
        self.subscript = subscript

    def set_weight(self, weight: float):
        assert self.subscript is not None
        # (-1: 列标, self.subscript: 行标)
        data_db[(-1, self.subscript)] = weight

    def connect_to(self, vertex_subscript_l):
        # 节点必须一次性连接完毕, 参数可能是Vertex or subscript
        for v_s in vertex_subscript_l:
            if isinstance(v_s, Vertex):
                pass
            elif isinstance(v_s, int):
                pass
            else:
                raise Exception
