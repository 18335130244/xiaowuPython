from selenium.webdriver.common.by import By

from common.common_func import DriverExpand


class Login(DriverExpand):
    def __init__(self, drive):
        print('Login')
        super().__init__(drive)

    def xiao_wu_login(self, account, password):
        self.query_selector('input[placeholder="邮箱登录"]').send_keys(account)
        self.query_selector('input[placeholder="密码"]').send_keys(password)
        self.query_selector('button').click()
