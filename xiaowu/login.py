from common.common_func import DriverExpand
import logging


class Login(DriverExpand):
    def __init__(self, drive):
        print('Login')
        super().__init__(drive)

    def xiao_wu_login(self, account, password):
        self.query_selector('input[placeholder="邮箱登录"]').send_keys(account)
        logging.info('输入账号_{}'.format(account))
        self.query_selector('input[placeholder="密码"]').send_keys(password)
        logging.info('输入密码_{}'.format(password))
        self.query_selector('button').click()
        logging.info('登录成功')
