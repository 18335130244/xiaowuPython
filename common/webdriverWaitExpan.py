from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
# 有关 webdriver_wait 扩展方法


class wait_for_the_attribute_value(object):
    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = webdriver.Chrome.find_element(driver, self.locator).get_attribute(self.attribute)
            # 包含当前属性值
            if self.value in element_attribute:
                return element_attribute == self.value
        except StaleElementReferenceException:
            return False