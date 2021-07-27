from faker import Faker


# 生成数据类
class CreateData:
    fake = None

    # 下属类自动实例化变量
    def init_fake(self):
        self.fake = Faker(locale='zh_cn')