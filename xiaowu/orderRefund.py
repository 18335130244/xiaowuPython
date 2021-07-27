
from common.common import init_drives, DriverExpand
from xiaowu.addStudentAndPushXiaowu import AddStudent
from xiaowu.buyClass import ByClass
from xiaowu.login import Login


class orderRefund(DriverExpand):

    def __init__(self, drive):
        self.init_drive(drive)

    def order_list(self, orderNumber):
        self.wait_time(1)

        # 点击进入 校务菜单
        self.query_selector('#tab-0').click()
        # 订单编号存在 不在重复进入 校务管理

        # 传递需要名字
        self.button_show_click(["校务管理", "销售管理", "订单列表"])

        # 查看按钮是否存在
        el = self.check_displayed('查看订单详情按钮', '.view .el-table__fixed-right .el-button:nth-child(2)', times=5)
        # 等待学生列表可以点击
        if orderNumber is not None:
            self.query_selector('input[placeholder="请输入订单编号"]').send_keys(orderNumber)
            # 搜索学生 进入购买班级
            self.element_click('查看' + orderNumber + '详情按钮', '.view .el-table__fixed-right .el-button:nth-child(2)',
                             times=5)
        else:
            el.click()
        self.check_displayed('退费列表', '.view .el-table__expanded-cell', times=3)
        allSel = self.query_selector_all('.view .el-table__expanded-cell')
        # 全部退费
        self.query_selector('.view .el-checkbox').click()

        for index in range(len(allSel)):
            itemEl = allSel[index]
            print(index)
            # 选择全部课节
            itemEl.find_element_by_css_selector('.all-sel').click()
            # 填写理由
            itemEl.find_element_by_css_selector('label[for="refundReason"]+.el-form-item__content .el-textarea__inner').send_keys('就退费')
            if index is not 0:
                itemEl.find_element_by_css_selector('label[for="refundFee"]+.el-form-item__content .el-input__inner').clear()
                itemEl.find_element_by_css_selector('label[for="refundFee"]+.el-form-item__content .el-input__inner').send_keys('0')

        # 提交并保存
        self.query_selector('.footer .el-button:nth-child(2)').click()

        # 查找-- 确认退费是否存在
        sureRefundPrice = self.check_displayed('确认退费', '.el-dialog[aria-label="确认退费"]', times=1)
        if sureRefundPrice is not None:
            sureRefundPrice.find_element_by_css_selector('.dialog-footer .el-button:nth-child(2)').click()

        # 关闭当前标签
        # self.close_tag()


# 单独测试时 使用
if __name__ == '__main__':
    # print(os.path.abspath('../ice.png'))
    #
    driverAddStudent = init_drives('https://uat-edurp.ambow.com/',
                                   "../../../myproject/testSeleuim/chromedriver_win32/chromedriver.exe")

    Login(driverAddStudent).xiao_wu_login('wei.xia@ambow.com', 'Ambow88888888')
    # 全屏幕
    driverAddStudent.maximize_window()
    # # 新增学生
    # studentName = AddStudent(driverAddStudent).add_student()
    # # 购买班级-获得订单Id
    # orderNum = ByClass(driverAddStudent).buy_class(studentName)
    orderNum = None
    # 查看订单是否有误
    orderRefund(driverAddStudent).order_list(orderNum)

    # 执行完毕后推出操作
    # driverAddStudent.quit()

# 单独测试时 使用
# if __name__ == '__main__':
#     driverAddStudent = init_drives('https://uat-edurp.ambow.com/',
#                                    "../../../myproject/testSeleuim/chromedriver_win32/chromedriver.exe")
#     Login(driverAddStudent).xiao_wu_login('wei.xia@ambow.com', 'Ambow88888888')
#     # 全屏幕
#     driverAddStudent.maximize_window()
#     Order(driverAddStudent).order_list('ABRCSXYMDXQC21385919511921950720')
#     print(driverAddStudent.execute_script('return document.querySelector("#orderTop div p:nth-child(2)").innerText.substr(5)'))


