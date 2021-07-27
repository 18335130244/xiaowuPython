from common.common import init_drives, DriverExpand
from createData import CreateData
from xiaowu.addClass import AddClass
from xiaowu.addStudentAndPushXiaowu import AddStudent
from xiaowu.buyClass import ByClass
from xiaowu.login import Login


class Schedule(DriverExpand, CreateData):

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

    def schedule(self, clName):
        self.wait_time(1)

        # 点击进入 校务菜单
        self.element_click('点击顶部_校务_按钮', '#tab-0', times=1)

        # 传递需要名字
        self.button_show_click(["校务管理", "课程管理", "班级管理"])

        # loading 加载状态
        self.check_not_display('班级 loading 加载', '.view .el-loading-mask', times=2)

        if clName is not None:
            # 搜索 班级 className
            self.query_selector('.view input[placeholder="请输入班级名称"]').send_keys(clName)

        # 等待元素出现
        self.check_displayed('等待排课按钮出现', '.view .el-table__fixed-right tr:nth-child(1) td .operation-part .el-button',
                             times=2)
        # 选择排课
        allButton = self.query_selector_all('.view .el-table__fixed-right tr:nth-child(1) td .operation-part .el-button')
        # 确定基础操作按钮 为 4 个
        if len(allButton) is not 4:
            print('{}-班级，已经排过课'.format(clName))
            return clName
        print(allButton[2].get_attribute('textContent'), '=========textContent')

        # 点击排课按钮
        allButton[2].click()
        # 选择 上课周期 默认选择四个
        self.element_more_select(forName='attendClassWeeks', options='1,2,3,4')
        # 选择 选择上课时间段
        # self.query_selector('label[for="classHours"]+.el-form-item__content .el-select ').click()
        # 选择 定制时间
        self.query_selector('.customizingtime').click()
        # 删除 无法选中的内容
        self.execute_script('$("body>.el-time-range-picker.el-popper").remove()')
        # 打开 定制时间 弹窗
        self.query_selector('.el-dialog[aria-label="定制时间"] .el-date-editor').click()
        # 开始时间 17 点
        self.query_selector('body>.el-time-range-picker.el-popper .el-time-spinner__list .el-time-spinner__item:nth-child(18)').click()
        # 点击确认
        self.query_selector('body>.el-time-range-picker.el-popper .el-time-panel__footer .confirm').click()
        # 关闭 定制时间 弹窗
        self.query_selector('.el-dialog[aria-label="定制时间"] .dialog-footer .el-button:nth-child(2)').click()
        # 生成排课
        self.query_selector('.view .add-top .el-row:nth-child(4) .el-button').click()

        # 等待 生成排课
        self.check_displayed('是否生成排课', '.view .mind_list .table .tab_li:nth-child(2)', times=2)

        # 保存排课
        self.query_selector('.view .create_btn .el-button:nth-child(2)').click()

        # 是否存在 aria-label="老师被其他排课占用"
        self.element_click('老师被其他排课占用', '.el-message-box__wrapper[aria-label="老师被其他排课占用"] .el-button--primary', times=3)


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
    studentName = AddStudent(driverAddStudent).add_student()
    # 新增班级
    className = AddClass(driverAddStudent).add_class()
    # 排课
    Schedule(driverAddStudent).schedule(className)
    # 购买班级-获得订单Id
    orderNum = ByClass(driverAddStudent).buy_class(studentName, className)
    # orderNum = ByClass(driverAddStudent).buy_class('yjf-测试-内蒙古胡桂兰', '高二4-6人班（明德）寒-周斌')
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


