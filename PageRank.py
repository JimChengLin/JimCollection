from AsyncDB import AsyncDB

FACTOR = 0.15

# 预期协程并发数
CON_NUM = 1000

# 从名字到下标的映射
name_db = AsyncDB('name.db')

# 从下标到数值的映射
data_db = AsyncDB('data.db')


# 将Vertex转化为行列式写入硬盘, 为了读取速度, 下标先列再行
class Vertex:
    counter = 0

    def __init__(self, name: str):
        self.name = name
        self.num = None

    async def init_num(self):
        self.num = 0

    def set_weight(self, weight: float):
        # -1 => 列标 self.num => 行标
        data_db[(-1, self.num)] = weight

    def __repr__(self):
        return 'name: {}, no.{}'.format(self.name, self.num)
