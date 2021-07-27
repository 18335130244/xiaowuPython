from common.common import init_drives, DriverExpand
from createData import CreateData
from xiaowu.addStudentAndPushXiaowu import AddStudent
from xiaowu.buyClass import ByClass
from xiaowu.login import Login


class AddClass(DriverExpand, CreateData):

    def __init__(self, drive):
        self.init_drive(drive)
        self.init_fake()

    def element_select(self, forName, selectName='.el-select', options='1', otherSelect=None):
        # 删除所有可以被选择的下拉框
        self.execute_script('$("body>.el-popper.el-select-dropdown").remove()')
        # 点击 弹出选择框
        self.query_selector('label[for="' + forName + '"]+.el-form-item__content ' + selectName).click()
        # 填入老师
        if otherSelect is not None:
            self.check_displayed('选择老师',
                                 'body>.el-popper.el-select-dropdown .el-select-dropdown__item:nth-child(' + options[
                                     0] + ')', times=2)
            # 选择指定选项
            self.query_selector(
                'label[for="' + forName + '"]+.el-form-item__content ' + selectName + ' .el-input__inner').send_keys(
                otherSelect)
            self.query_selector(
                'body>.el-select-dropdown.el-popper .el-select-dropdown__item:not([style="display: none;"])').click()
        else:
            # 选择 第一项
            self.element_click(
                'body>.el-popper.el-select-dropdown .el-select-dropdown__item:nth-child(' + options[0] + ')').click()

    def element_cascader(self, forName, selectName='.el-cascader', options='1,1'):
        # 删除所有可以被选择的下拉框
        self.execute_script('$("body>.el-popper.el-cascader__dropdown").remove()')
        # 点击 弹出选择框
        self.query_selector('label[for="' + forName + '"]+.el-form-item__content ' + selectName).click()
        # 选择 第一项
        self.query_selector(
            'body>.el-popper.el-cascader__dropdown .el-cascader-menu:nth-child(1) .el-cascader-node__label:nth-child(' +
            options[0] + ')').click()
        self.element_click('点击_' + forName + '_按钮',
                           'body>.el-popper.el-cascader__dropdown .el-cascader-menu:nth-child(2) .el-cascader-node__label:nth-child(' +
                           options[2] + ')', times=1)

    def element_picker_panel(self, forName, selectName='.el-date-editor'):
        # 删除所有可以被选择的下拉框
        self.execute_script('$("body>.el-popper.el-picker-panel").remove()')
        # 点击 弹出选择框
        self.query_selector('label[for="' + forName + '"]+.el-form-item__content ' + selectName).click()
        # 选择 今天的后一天
        # self.query_selector('body>.el-popper.el-picker-panel .today+.available').click()
        # 按下前一年
        self.query_selector('body>.el-popper.el-picker-panel .el-date-picker__header button[aria-label="前一年"]').click()
        # 选择去年的当月的第一天
        self.query_selector('body>.el-popper.el-picker-panel .el-picker-panel__content .available').click()

    def add_class(self, teacherName='李舟'):
        self.wait_time(1)

        # 点击进入 校务菜单
        self.element_click('点击顶部_校务_按钮', '#tab-0', times=3)

        # 传递需要名字
        self.button_show_click(["校务管理", "课程管理", "班级管理"])

        # 新增班级 按钮
        if self.element_click('新增班级_按钮', '.view .el-button', times=3) is None:
            # 新增班级点击 错误情况下
            self.element_click('新增班级_按钮', '.view .el-button', times=3)

        # 选择 校区
        self.element_cascader(forName='orgId', options='1,1')

        # 选择 立项编号
        self.element_select(forName='subjectCode', options='1')

        # 选择 课程名称
        self.element_select(forName='edaCourseCode', options='4')

        # 选择 任课老师
        self.element_select(forName='teacherId', options='4', otherSelect=teacherName)

        # 选择 开课时间
        self.element_picker_panel(forName='openingTime')

        # 添加班级名称后缀
        classNameSuffix = self.fake.name()
        self.query_selector('label[for="classCourseNameAfter"]+.el-form-item__content .el-input__inner').send_keys(
            classNameSuffix)
        self.query_selector('body').click()

        # 保存班级名字
        classCourseName = self.query_selector(
            'label[for="classCourseName"]+.el-form-item__content .el-input__inner').get_attribute('value')

        # 点击保存按钮
        self.query_selector('.view .el-button:last-child').click()

        # 关闭当前标签
        # self.close_tag()

        # 返回班级名字
        print('新建班级名字为:{}.'.format(classCourseName))
        return classCourseName


# 单独测试时 使用
if __name__ == '__main__':
    # print(os.path.abspath('../ice.png'))
    #
    driverAddStudent = init_drives('https://uat-edurp.ambow.com/',
                                   "../../../myproject/testSeleuim/chromedriver_win32/chromedriver.exe")

    Login(driverAddStudent).xiao_wu_login('wei.xia@ambow.com', 'Ambow88888888')
    # 全屏幕
    driverAddStudent.maximize_window()
    # 新增学生
    # studentName = AddStudent(driverAddStudent).add_student()
    # 新增班级
    className = AddClass(driverAddStudent).add_class()
    # 购买班级-获得订单Id
    # orderNum = ByClass(driverAddStudent).buy_class(studentName, className)
    # 执行 2秒后关闭
    driverAddStudent.wait_time(2)
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
