from faker import Faker

# 生成数据类
from common.common_func import DriverExpand


class CreateData(DriverExpand):
    fake: Faker

    def __init__(self, driveInstant):
        self.init_fake()
        super().__init__(driveInstant)

    def init_fake(self):
        self.fake = Faker(locale='zh_cn')
