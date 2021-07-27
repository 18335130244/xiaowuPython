from selenium import webdriver


def base_driver():
    # 打开 webDrive 代理器
    driver = webdriver.Chrome(executable_path="../../myproject/testSeleuim/chromedriver_win32/chromedriver.exe")

    # 要被打开的链接
    url = 'https://uat-edurp.ambow.com/'

    driver.get(url)
    return driver