import os
import time
import logging.config

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.webdriverWaitExpan import wait_for_the_attribute_value
path1 = os.path.dirname(os.path.dirname(__file__))
log_path = os.path.join(path1, "config/log.conf")
logging.info(log_path)
logging.config.fileConfig(log_path)


class Utils:

    # 模拟手势操作
    @staticmethod
    def ActionChains(drive):
        return webdriver.ActionChains(drive)

    # 操作后等待时间后在执行
    @staticmethod
    def wait_time(times):
        return time.sleep(times)


def create_time_name(operaName):
    timeStr = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
    path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(path, 'errorLog', operaName)
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, timeStr + '.png')
    return path


# 拓展 WebElement 方法
class WebElementExpand(WebElement, Utils):

    def __init__(self, parent, id_, w3c=False):
        super().__init__(parent, id_, w3c)

    def click(self):
        # 拦截点击后 并等待 .2 秒
        super().click()
        self.wait_time(.2)

    def send_keys(self, *value):
        # 拦截赋值 并等待 .2 秒
        WebElement.send_keys(self, value)
        self.wait_time(.2)

    def query_selector(self, CSSName):
        return self.find_element(By.CSS_SELECTOR, CSSName)


# 初始化 driver 类型
class WebElementOp(WebDriver, Utils):

    def __init__(self, executable_path, options):
        # 增加父 类方法并增加方法拦截
        super().__init__(executable_path=executable_path, options=options)

    def create_web_element(self, element_id):
        return WebElementExpand(self, element_id, w3c=self.w3c)


# 基础复合合并类型
class DriverExpand(Utils):
    drivers: WebElementOp
    waitCommonTime = .2

    def __init__(self, driveInstant):
        self.drivers = driveInstant

    # 设置 浏览器驱动实例
    def init_drive(self, driveInstant):
        self.drivers = driveInstant

    # 关闭校务标签
    def close_tag(self):
        tagName = self.execute_script('return sessionStorage.currentUrl')
        self.query_selector('#tab-' + tagName + ' .item_close').click()

    # 关闭校务标签
    def button_show_click(self, btNameList: list):
        def deep_node_click(cssName, index: int):
            # 当前元素 是否已经处于选中状态
            try:
                leftMenuObj = {
                    0: '.is-active',
                    1: '.is-active .is-active',
                    2: '.is-active .is-active .el-menu-item.is-active',
                }
                self.query_selector(leftMenuObj[index] + ' span[serarchkey="' + cssName + '"]')
            except NoSuchElementException:
                self.query_selector('span[serarchkey="' + cssName + '"]').click()

        for btnSearchKey in btNameList:
            i = btNameList.index(btnSearchKey)
            logging.info('点击菜单+'+btnSearchKey)
            deep_node_click(btnSearchKey, i)

    # 保存操作失败截图
    def save_screen_file(self, operaName):
        # 元素寻找超时 截图保存
        if self.get_driver().get_screenshot_as_file(create_time_name(operaName)) is True:
            logging.info('保存_{}_操作图片成功'.format(operaName))

    # 获取驱动浏览器实例
    def get_driver(self):
        return self.drivers

    def query_selector(self, CSSName, logCb=None) -> WebElementExpand:
        return self.get_driver().find_element(By.CSS_SELECTOR, CSSName)

    def query_selector_all(self, CSSName):
        return self.get_driver().find_elements(By.CSS_SELECTOR, CSSName)

    # 让浏览器执行 固定脚本
    def execute_script(self, execute_script):
        return self.get_driver().execute_script(execute_script)

    # 返回存在的元素的 文本 非 input
    def check_get_text(self, operaName, loc, times=10):
        try:
            el = WebDriverWait(self.get_driver(), times).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loc)))
        except TimeoutException:
            self.save_screen_file(operaName)
            logging.info('寻找_{}_元素失败'.format(operaName))
            return None
        else:
            return el.text

    # 元素在页面不可见
    def check_not_display(self, operaName, loc, times=10):
        try:
            WebDriverWait(self.get_driver(), times).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, loc)))
            # WebDriverWait(self.get_driver(), times).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, loc)))
        except TimeoutException:
            self.save_screen_file(operaName)
            logging.info('{}_元素依然在页面显示'.format(operaName))
            return None
        else:
            logging.info('{}_不在页面上显示'.format(operaName))
            self.wait_time(1)
            return True

    # 校验元素存在与页面 并处于 可访问状态
    def check_displayed(self, operaName, loc, times=10):
        try:
            el = WebDriverWait(self.get_driver(), times).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loc)))
        except TimeoutException:
            self.save_screen_file(operaName)
            logging.info('元素_{}_不在页面上存在'.format(operaName))
            return None
        else:
            logging.info('{}_元素存在'.format(operaName))
            self.wait_time(.3)
            return el

    # 元素存在并 点击 operaName-> 实际操作名字  queryCssName-> 被查询的 CSS 名字
    def element_click(self, operaName, queryCssName, times=4):
        # visibility_of_element_located 等待元素显示在页面
        try:
            el = WebDriverWait(self.get_driver(), times).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, queryCssName)))
        except TimeoutException:
            self.save_screen_file(operaName)
            logging.info('执行元素点击操作_{}_错误'.format(operaName))
            return None
        else:
            self.wait_time(1)
            el.click()
            logging.info('执行元素点击操作_{}_成功'.format(operaName))
            return el

    # 检测元素属性
    def element_attribute(self, operaName, locator, attribute, value, times=4):
        # visibility_of_element_located 等待元素显示在页面
        try:
            el = WebDriverWait(self.get_driver(), times).until(
                wait_for_the_attribute_value(locator, attribute, value))
        except TimeoutException:
            self.save_screen_file(operaName)
            logging.info('执行元素点击操作_{}_错误'.format(operaName))
            return None
        else:
            self.wait_time(1)
            el.click()
            logging.info('执行元素点击操作_{}_成功'.format(operaName))
            return el


# 打开浏览器 并放回实例
def init_drives(browUrl, exe_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=4000,1600")
    # 打开 webDrive 代理器
    driver = WebElementOp(executable_path=exe_path, options=chrome_options)
    # 要被打开的链接
    driver.get(browUrl)
    return driver


if __name__ == '__main__':
    # driverAddStudent = init_drives('https://uat-edurp.ambow.com/',
    #                                "../../../myproject/testSeleuim/chromedriver_win32/chromedriver.exe")
    #
    # Login(driverAddStudent).xiao_wu_login('wei.xia@ambow.com', 'Ambow88888888')
    a = create_time_name('sss')

    logging.info('hhhhh')
    logging.info(a)
