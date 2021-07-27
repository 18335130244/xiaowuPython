import os

from common.common import init_drives, DriverExpand
from xiaowu.addStudentAndPushXiaowu import AddStudent
from xiaowu.login import Login


class ByClass(DriverExpand):

    def same_opera(self, labelName, ContentCssName='.el-select'):
        # 删除所有可以被选择的下拉框
        self.execute_script('$("body>.el-popper").remove()')
        # 打开下拉框
        if labelName is not None:
            self.query_selector('label[for="' + labelName + '"]+.el-form-item__content ' + ContentCssName).click()
        else:
            self.query_selector(ContentCssName).click()
        # 选择结果
        self.query_selector('body>.el-popper .el-select-dropdown__item').click()

    # element-ui 日期控件对于的方法点击
    def click_element_date_control(self, labelName, ContentCssName):
        # 删除所有相关的 日期控件内容
        self.execute_script('$("body>.el-picker-panel").remove()')
        # 执行对应 日期控件 点击事件
        self.query_selector('label[for="' + labelName + '"]+.el-form-item__content ' + ContentCssName).click()
        # 选择今天 为付款日期
        self.query_selector('body>.el-picker-panel .today').click()

    def upload_file_img(self, forName):
        self.query_selector('label[for="' + forName + '"]+.el-form-item__content input[type="file"]').send_keys()

    def __init__(self, drive):
        self.init_drive(drive)

    def buy_class(self, childName, className):
        self.wait_time(1)

        # 点击进入 校务菜单
        self.query_selector('#tab-0').click()

        # 传递需要名字
        self.button_show_click(["校务管理", "人员管理", "学生管理"])

        # 设置督导师
        self.check_not_display('加载框 消失', '.view .el-loading-mask', times=2)
        # 给学生切换督导室 -- 夏卫
        self.element_click('选择督导师', '.view .el-table__fixed-body-wrapper .el-tooltip', times=2)
        # 打开选择督导室弹窗
        self.query_selector('.el-dialog[aria-label="设置督导师"] .el-select').click()
        # 设置要选择的督导室名字
        self.query_selector('.el-dialog[aria-label="设置督导师"] .el-select .el-input__inner').send_keys('夏卫')
        # 设置要选择的督导室名字
        self.query_selector('body>.el-select-dropdown.el-popper .el-select-dropdown__item:not([style="display: none;"])').click()
        # 完成督导室选择
        self.query_selector('.el-dialog[aria-label="设置督导师"] .dialog-footer .el-button:nth-child(2)').click()

        # 查看 购班辅 是否存在
        self.check_displayed('购买班辅 按钮', '.view .el-table__fixed-right .btn-block .el-button:nth-child(2)', times=5)
        # 等待学生出现可以购买
        if childName is not None:
            self.query_selector('input[placeholder="请输入学生姓名"]').send_keys(childName)
            # 搜索学生 进入购买班级
            self.element_click('购买班辅 按钮', '.view .el-table__fixed-right .btn-block .el-button:nth-child(2)', times=5)
        else:
            self.query_selector('.view .el-table__fixed-right .btn-block .el-button:nth-child(2)').click()

        if className is not None:
            self.query_selector('label[for="classCourseName"]+.el-form-item__content .el-input__inner').send_keys(className)
            # 搜索
            self.query_selector('.add_top .el-button').click()
            # 全选
            self.element_click('全选班级' + className, '.view .el-checkbox', times=1)
        else:
            # 选择校区 第一个校区或者第二个校区
            self.element_click('选择第一个校区', '.view table.el-table__body tr:nth-child(1) .el-checkbox', times=5)
            self.query_selector('.view table.el-table__body tr:nth-child(3) .el-checkbox').click()

        # 下一步
        self.query_selector('.view .foot_er .el-button:nth-child(2)').click()

        # 成单咨询师
        self.same_opera(labelName='saleId')

        # 选择 付钱尾款日期
        self.click_element_date_control(labelName='buyTime', ContentCssName='.el-date-editor')
        # 本次应付金额
        self.same_opera(labelName=None, ContentCssName='.view .cus-form .el-select')
        # 本次应付金额 输入 return document.querySelector('.view .total span:nth-child(2)').innerHTML.replace(/,/g,'') 获取总金额并转化 为正常显示数字
        self.query_selector('.view .cus-form .el-input-number input').send_keys(self.execute_script("return document.querySelector('.view .total span:nth-child(2)').innerHTML.replace(/,/g,'')"))
        # 上传 交易图片
        self.query_selector('.view .cus_img .el-upload__input[type=file]').send_keys(os.path.abspath('../ice.png'))
        # 等待 图片上传成功
        self.check_displayed('上传图片', '.view .cus_img .is-success img', times=5)
        # 提交订单
        self.query_selector('.view .foot_er .el-button:nth-child(2)').click()

        self.check_displayed('订单编号', '#orderTop div p:nth-child(2)', times=2)
        # 获取订单编号
        orderNumber = self.execute_script('return document.querySelector("#orderTop div p:nth-child(2)").childNodes[1].textContent')
        print('学生_'+childName+'_下单_'+orderNumber)
        # 返回订单 编号
        return orderNumber


# 单独测试时 使用
if __name__ == '__main__':
    # print(os.path.abspath('../ice.png'))
    #
    driverAddStudent = init_drives('http://10.10.102.121:8082/',
                                   "../../../myproject/testSeleuim/chromedriver_win32/chromedriver.exe")

    Login(driverAddStudent).xiao_wu_login('wei.xia@ambow.com', 'Ambow88888888')
    # 全屏幕
    driverAddStudent.maximize_window()
    # 新增学生
    studentName = AddStudent(driverAddStudent).add_student()
    ByClass(driverAddStudent).buy_class(studentName, None)

    # 执行完毕后推出操作
    # driverAddStudent.quit()


