from common.common import init_drives, DriverExpand
from createData import CreateData
from xiaowu.addClass import AddClass
from xiaowu.addStudentAndPushXiaowu import AddStudent
from xiaowu.buyClass import ByClass
from xiaowu.login import Login
from xiaowu.schedule import Schedule


class Attendance(DriverExpand, CreateData):

    def __init__(self, drive):
        self.init_drive(drive)
        self.init_fake()

    def element_select(self, forName, selectName='.el-select', options='1'):
        # 删除所有可以被选择的下拉框
        self.execute_script('$("body>.el-popper.el-select-dropdown").remove()')
        # 点击 弹出选择框
        self.query_selector('label[for="' + forName + '"]+.el-form-item__content ' + selectName).click()
        # 选择 第一项
        self.query_selector(
            'body>.el-popper.el-select-dropdown .el-select-dropdown__item:nth-child(' + options[0] + ')').click()

    def element_more_select(self, forName, selectName='.el-select', options='1'):
        # 删除所有可以被选择的下拉框
        self.execute_script('$("body>.el-popper.el-select-dropdown").remove()')
        # 点击 弹出选择框
        self.query_selector('label[for="' + forName + '"]+.el-form-item__content ' + selectName).click()
        # 多个选择
        for nthChild in options:
            if nthChild is not ',':
                self.element_click('点击第{}周'.format(nthChild),
                                 'body>.el-popper.el-select-dropdown .el-select-dropdown__item:nth-child({})'.format(
                                     nthChild), times=1)

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
        self.query_selector('body>.el-popper.el-picker-panel .today+.available').click()

    def attendance_set(self, childName):
        self.wait_time(1)
        # 点击进入 校务菜单
        self.element_click('点击顶部_校务_按钮', '#tab-0', times=1)

        # 传递需要名字
        self.button_show_click(["校务管理", "课酬管理", "考勤管理"])
        self.check_not_display('loading 层消失', '.view .el-loading-mask', times=1)

        # 赋值学生名字
        self.query_selector('.view label[for="stuId"]+.el-form-item__content .el-select').click()
        self.execute_script('$("body>.el-popper.el-picker-panel").remove()')
        self.wait_time(1)
        # 等待选择学生名字
        self.query_selector('.view label[for="stuId"]+.el-form-item__content .el-input__inner').send_keys(childName)
        self.query_selector(
            'body>.el-select-dropdown.el-popper .el-select-dropdown__item:not([style="display: none;"])').click()

        # 筛选数据
        self.query_selector('.view .filterBtn .el-button').click()

        # 手动触发第一次
        self.next_attend()

    def next_attend(self):
        self.check_not_display('loading 层消失', '.view .el-loading-mask', times=1)
        # 选择全部数据
        self.check_displayed('单选出现', '.view .el-table__fixed .el-table__fixed-body-wrapper .el-table__row .el-checkbox',
                             times=1)
        checkBox = self.query_selector_all('.view .el-table__fixed .el-table__fixed-body-wrapper .el-table__row .el-checkbox')
        # 查询当前条 是否可以提交审核
        checkBoxButton = self.query_selector_all('.view .el-table__fixed-right .el-table__row .el-button.el-button--warning')
        numberOfClicks: int = 0
        for checkBoxItem in checkBoxButton:
            print(checkBoxItem.get_attribute('disabled'))
            if checkBoxItem.get_attribute('disabled') is None:
                # 选中当前元素 提交 设置为出勤
                checkBox[checkBoxButton.index(checkBoxItem)].click()
                numberOfClicks = numberOfClicks + 1
        if numberOfClicks is not 0:
            # 点击出勤
            self.element_click('点击出勤', '.filter_click .el-button+.el-button', times=2)
            # 等待 3 秒钟 等待接口调用完毕
            self.check_get_text('是否出勤完成', 'body>.el-message.el-message--info .el-message__content', times=3)
            self.check_not_display('loading 层消失', '.view .el-loading-mask', times=3)
            # 点击提交审核
            self.element_click('提交审核', '.filter_click .el-button', times=2)
        # 下一页按钮
        nextBtn = self.query_selector('.view .btn-next')
        # 是否被禁用
        isDisabled = nextBtn.get_attribute('disabled')
        # 是否不允许去下一页
        if isDisabled is None:
            nextBtn.click()
            self.next_attend()


# 单独测试时 使用
if __name__ == '__main__':
    # print(os.path.abspath('../ice.png'))
    #
    driverAddStudent = init_drives('https://uat-edurp.ambow.com/',
                                   "../../../myproject/testSeleuim/chromedriver_win32/chromedriver.exe")

    Login(driverAddStudent).xiao_wu_login('wei.xia@ambow.com', 'Ambow88888888')
    # 全屏幕
    driverAddStudent.maximize_window()
    # 新增班级
    className = AddClass(driverAddStudent).add_class()
    # className = '高二4-6人班（明德）寒-计健'
    # 排课
    Schedule(driverAddStudent).schedule(className)
    studentNames = []
    # 新增学生
    # studentName = AddStudent(driverAddStudent).add_student()
    for i in range(10):
        driverAddStudent.wait_time(.3)
        print('新增=====================')
        studentName = AddStudent(driverAddStudent).add_student(i)
        studentNames.append(studentName)
        # 购买班级-获得订单Id
        ByClass(driverAddStudent).buy_class(studentName, className)
        print('{}_购买成功'.format(studentName))
        # 审批考勤
        Attendance(driverAddStudent).attendance_set(studentName)
        print('{}_审批考勤成功'.format(studentName))
        print('=====================')
        driverAddStudent.wait_time(.3)
    # 测试
    # Attendance(driverAddStudent).attendance_set('yjf-测试-内蒙古卢莉 - ABSXYN210000995')
    # 执行 2秒后关闭
    driverAddStudent.wait_time(2)
    # 执行完毕后推出操作
    # driverAddStudent.quit()


