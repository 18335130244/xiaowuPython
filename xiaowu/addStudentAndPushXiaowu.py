import time

from xiaowu.login import Login

from common.common import init_drives, DriverExpand
from createData import CreateData


class AddStudent(CreateData, DriverExpand):

    def __init__(self, drive):
        # 手动初始化浏览器 实例
        self.init_drive(drive)
        # 手动初始化 自动生成数据
        self.init_fake()

    def same_opera(self, forName, selectName='.el-select'):
        # 打开根进状态下拉框
        self.query_selector('label[for="' + forName + '"]+.el-form-item__content ' + selectName).click()
        # 被激活的 el-popper 元素
        item = self.execute_script('return $("body>.el-popper:visible")[0]')
        # 选择待跟进
        item.find_element_by_css_selector('.el-select-dropdown__item').click()

    def add_student(self, n):
        # 填写用户信息
        studentName = 'yjf-测试-内蒙古' + self.fake.name() + '_' + str(n)
        print('新增学生' + studentName)
        self.wait_time(1)
        # 动态添加 学生
        self.query_selector('#tab-2').click()

        # 传递需要名字
        self.button_show_click(["意向客户"])
        
        self.query_selector('.handle-box .el-button').click()
        self.query_selector('input[placeholder="请输入客户名称"]').send_keys(studentName)
        self.query_selector('input[placeholder="请输入联系电话"]').send_keys(self.fake.phone_number())

        # 执行相同操作 跟进状态
        self.same_opera('contactStatus')

        # 执行相同操作 渠道选择
        self.same_opera('channel')

        # 执行相同操作 咨询校区/分公司
        self.query_selector('label[for="parentOrgChildOrg"]+.el-form-item__content .el-cascader').click()
        # 移动到校区第一级选择区域
        self.ActionChains(self.get_driver()).move_to_element(
            self.query_selector('body>.el-popper .el-cascader-node')).perform()
        time.sleep(.2)
        self.query_selector('body>.el-popper .el-cascader-menu:nth-child(2) .el-cascader-node').click()

        # 保存按钮
        self.query_selector('footer button:nth-child(2)').click()

        # 同步到校务
        self.element_click('同步到校务', '#customer .el-table__row .el-checkbox', 5)
        self.query_selector('#customer .handle-box:nth-child(2) .el-button:last-child').click()

        print('新增' + studentName + '成功，同步校务完成')
        # 返回学生名字
        return studentName


# 单独测试时 使用
if __name__ == '__main__':
    driverAddStudent = init_drives('https://uat-edurp.ambow.com/',
                                   "../../../myproject/testSeleuim/chromedriver_win32/chromedriver.exe")

    Login(driverAddStudent).xiao_wu_login('wei.xia@ambow.com', 'Ambow88888888')
    # 全屏幕
    driverAddStudent.maximize_window()
    AddStudent(driverAddStudent).add_student('1')

    # 执行完毕后推出操作
    # driverAddStudent.quit()
