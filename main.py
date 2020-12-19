from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import QLineEdit
import pymysql.cursors
from PyQt5.QtWidgets import QTreeWidgetItem, QMessageBox, QComboBox

class login(QMainWindow):
    '''
    定义一个登录页面
    '''
    def __init__(self):
        '''初始化界面'''
        super(login, self).__init__()
        self.setGeometry(500, 150, 400, 600)
        self.setWindowTitle('XX学校信息管理平台')
        self.title = self.newlabel('XX学校信息管理平台', size=[0, 0, 400, 200])
        self.username = self.newlabel('用户名', fz=17, size=[50, 170, 50, 100])
        self.password = self.newlabel('密码', fz=17, size=[50, 250, 50, 100])
        self.username_box = self.new_input(palce_size=[120, 205, 200, 30], fz=16)
        self.password_box = self.new_input(palce_size=[120, 285, 200, 30], fz = 16)
        self.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
        self.checkbox1 = self.checkbox(s='学生登录', fz=15, place=[100, 350, 200, 30])
        self.checkbox2 = self.checkbox(s='教师登录', fz=15, place=[220, 350, 200, 30])
        self.bg = QButtonGroup(self)
        self.bg.addButton(self.checkbox1, 1)
        self.bg.addButton(self.checkbox2, 2)
        self.bg.buttonClicked.connect(self.login_action)
        self.choose = ''
        self.button = self.new_button(s='登录', fz=17, place=[160, 400, 80, 40])
        self.button.clicked.connect(self.commit)
        self.super = self.new_button(s='管理员登录', fz=12, place=[0, 570, 100, 30])
        self.super.setStyleSheet("color:grey;border:none;")
        self.super.clicked.connect(self.check)
# -------------管理员登录

    def check(self):
        self.title.hide()
        self.button.hide()
        newbutton = self.new_button(s='登录', fz=17, place=[160, 400, 80, 40])
        self.checkbox2.hide()
        self.checkbox1.hide()
        self.title = self.newlabel('管理员登录', size=[0, 0, 400, 200])
        self.title.show()
        newbutton.show()
        self.super.hide()
        newbutton.clicked.connect(lambda: self.root(self.username_box.text(), self.password_box.text(), newbutton))

    def root(self, username, password, button):
        if username == 'root' and password == 'root':
            QMessageBox.information(self, 'what', '登录成功!')
            self.hide()
            self.win4 = login()
            self.win4.username.hide()
            self.win4.password.hide()
            self.win4.username_box.hide()
            self.win4.password_box.hide()
            self.win4.button.hide()
            self.win4.checkbox2.hide()
            self.win4.checkbox1.hide()
            self.win4.title.hide()
            self.win4.super.hide()
            self.win4.add = self.win4.new_button(s='添加', fz=17, place=[160, 100, 80, 40])
            self.win4.delete = self.win4.new_button(s='删除', fz=17, place=[160, 170, 80, 40])
            self.win4.change = self.win4.new_button(s='修改', fz=17, place=[160, 240, 80, 40])
            self.win4.search = self.win4.new_button(s='查找', fz=17, place=[160, 310, 80, 40])
            self.win4.add.clicked.connect(self.add_method)
            self.win4.delete.clicked.connect(self.delete_method)
            self.win4.change.clicked.connect(self.change_method)
            self.win4.search.clicked.connect(self.search_method)
            self.win4.show()
        else:
            QMessageBox.information(self, 'what', '对不起您的用户名或者密码有误')


# ---------------以下是管理员的方法

    def add_method(self):
        self.win4.add.hide()
        self.win4.delete.hide()
        self.win4.change.hide()
        self.win4.search.hide()
        self.win4.l1 = self.win4.newlabel(s='请输入想添加的表单名', fz=17, size=[25, 40, 170, 30])
        self.win4.box1 = self.win4.new_input(fz=17, palce_size=[225, 40, 150, 30])
        self.win4.l2 = self.win4.newlabel(s='添加的内容(逗号分隔)', fz=17, size=[25, 80, 170, 30])
        self.win4.box2 = self.win4.new_input(fz=17, palce_size=[225, 80, 150, 30])
        self.win4.l1.show()
        self.win4.box1.show()
        self.win4.l2.show()
        self.win4.box2.show()
        btn = self.win4.new_button(s='点击确认提交', fz=17, place=[135, 120, 130, 40])
        model = QTreeWidget(self.win4)
        model.setGeometry(30, 180, 340, 400)
        btn.clicked.connect(lambda: self.showplace(model, self.win4.box1.text(), self.win4.box2.text()))
        model.show()
        btn.show()

    def showplace(self, model, tablename, insertcontent):
        model.clear()
        connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                                user='lab_33726443',
                                password='e2c26752cdf8_#@Aa',
                                db='jodio',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        if insertcontent != '':
            insertcontent = insertcontent.split(',')
            for i in range(len(insertcontent)):
                insertcontent[i] = insertcontent[i].strip()
                insertcontent[i] = '"'+insertcontent[i] +'"'
                if insertcontent[i] == '""':
                    insertcontent[i] = 'null'
            insertcontent = ','.join(insertcontent)
            insert = 'insert into %s values(%s)' % (tablename, insertcontent)
            cs2 = connection.cursor()
            cs2.execute(insert)
            connection.commit()
            QMessageBox.information(self, 'what', '添加成功！')
        sql = 'select * from %s' % tablename
        cs1 = connection.cursor()
        cs1.execute(sql)
        self.win4.re = cs1.fetchall()
        model.setColumnCount(len(self.win4.re[0]))
        header = []
        for key in self.win4.re[0]:
            header.append(key)
        model.setHeaderLabels(header)
        for ii in range(len(self.win4.re[0])):
            model.setColumnWidth(ii, 100)
        for i in range(len(self.win4.re)):
            a = QTreeWidgetItem(model)
            n = 0
            for key in self.win4.re[0]:
                a.setText(n, self.win4.re[i][key])
                n += 1
            model.addTopLevelItem(a)
        connection.close()

    def delete_method(self):
        self.win4.add.hide()
        self.win4.delete.hide()
        self.win4.change.hide()
        self.win4.search.hide()
        self.win4.l1 = self.win4.newlabel(s='请输入想删除的表单名', fz=17, size=[25, 40, 170, 30])
        self.win4.box1 = self.win4.new_input(fz=17, palce_size=[225, 40, 150, 30])
        self.win4.l2 = self.win4.newlabel(s='删除元素的主键值', fz=17, size=[25, 80, 170, 30])
        self.win4.box2 = self.win4.new_input(fz=17, palce_size=[225, 80, 150, 30])
        self.win4.l1.show()
        self.win4.box1.show()
        self.win4.l2.show()
        self.win4.box2.show()
        btn = self.win4.new_button(s='点击确认删除', fz=17, place=[135, 120, 130, 40])
        model = QTreeWidget(self.win4)
        model.setGeometry(30, 180, 340, 400)
        btn.clicked.connect(lambda: self.showplace2(model, self.win4.box1.text(), self.win4.box2.text()))
        model.show()
        btn.show()

    def showplace2(self, model, tablename, deletecontent):
        model.clear()
        connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                                user='lab_33726443',
                                password='e2c26752cdf8_#@Aa',
                                db='jodio',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        if deletecontent != '':
            if tablename == 'student':
                delete = 'delete from student where s = %s' % (deletecontent)
                cs2 = connection.cursor()
                cs2.execute(delete)
            if tablename == 'sc':
                delete = 'delete from sc where s = %s and c = %s' %(deletecontent.split(',').strip()[0], deletecontent.split(',').strip()[1])
                cs2 = connection.cursor()
                cs2.execute(delete)
            if tablename == 'teacher':
                delete = 'delete from teacher where t = %s' % (deletecontent)
                cs2 = connection.cursor()
                cs2.execute(delete)
            if tablename == 'class':
                delete = 'delete from class where c = %s' % (deletecontent)
                cs2 = connection.cursor()
                cs2.execute(delete)
            QMessageBox.information(self, 'what', '删除成功！')
        sql = 'select * from %s' % tablename
        cs1 = connection.cursor()
        cs1.execute(sql)
        self.win4.re = cs1.fetchall()
        model.setColumnCount(len(self.win4.re[0]))
        header = []
        for key in self.win4.re[0]:
            header.append(key)
        model.setHeaderLabels(header)
        for ii in range(len(self.win4.re[0])):
            model.setColumnWidth(ii, 100)
        for i in range(len(self.win4.re)):
            a = QTreeWidgetItem(model)
            n = 0
            for key in self.win4.re[0]:
                a.setText(n, self.win4.re[i][key])
                n += 1
            model.addTopLevelItem(a)
        connection.close()

    def change_method(self):
        self.win4.add.hide()
        self.win4.delete.hide()
        self.win4.change.hide()
        self.win4.search.hide()
        self.win4.l1 = self.win4.newlabel(s='请输入想改变的表单名', fz=17, size=[25, 40, 170, 30])
        self.win4.box1 = self.win4.new_input(fz=17, palce_size=[225, 40, 150, 30])
        self.win4.l2 = self.win4.newlabel(s='请输入需改变的列名', fz=17, size=[25, 80, 170, 30])
        self.win4.box2 = self.win4.new_input(fz=17, palce_size=[225, 80, 150, 30])
        self.win4.l3 = self.win4.newlabel(s='改变元组的主键值', fz=17, size=[25, 120, 170, 30])
        self.win4.box3 = self.win4.new_input(fz=17, palce_size=[225, 120, 150, 30])
        self.win4.l4 = self.win4.newlabel(s='改变的值', fz=17, size=[25, 160, 170, 30])
        self.win4.box4 = self.win4.new_input(fz=17, palce_size=[225, 160, 150, 30])
        self.win4.l1.show()
        self.win4.box1.show()
        self.win4.l2.show()
        self.win4.box2.show()
        self.win4.l3.show()
        self.win4.box3.show()
        self.win4.l4.show()
        self.win4.box4.show()
        btn = self.win4.new_button(s='点击确认删除', fz=17, place=[135, 200, 130, 40])
        model = QTreeWidget(self.win4)
        model.setGeometry(30, 260, 340, 320)
        btn.show()
        model.show()
        btn.clicked.connect(lambda: self.showplace3(model, self.win4.box1.text(), self.win4.box2.text(), self.win4.box3.text(), self.win4.box4.text()))
    
    def showplace3(self, model, tablename, columnname, mainkey, value):
        model.clear()
        connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                                user='lab_33726443',
                                password='e2c26752cdf8_#@Aa',
                                db='jodio',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        if value != '':
            value = '"' + value + '"'
            if tablename == 'student':
                update = 'update %s set %s=%s where s = %s' % (tablename, columnname, value, mainkey)
                cs2 = connection.cursor()
                cs2.execute(update)
            if tablename == 'sc':
                update = 'update %s set %s=%s where s = %s and c = %s' % (tablename, columnname, value, mainkey.split(',').strip()[0], mainkey.split(',').strip()[1])
                cs2 = connection.cursor()
                cs2.execute(update)
            if tablename == 'teacher':
                update = 'update %s set %s=%s where t = %s' % (tablename, columnname, value, mainkey)
                cs2 = connection.cursor()
                cs2.execute(update)
            if tablename == 'class':
                update = 'update %s set %s=%s where c = %s' % (tablename, columnname, value, mainkey)
                cs2 = connection.cursor()
                cs2.execute(update)
            connection.commit()
            QMessageBox.information(self, 'what', '更新成功！')
        sql = 'select * from %s' % tablename
        cs1 = connection.cursor()
        cs1.execute(sql)
        self.win4.re = cs1.fetchall()
        model.setColumnCount(len(self.win4.re[0]))
        header = []
        for key in self.win4.re[0]:
            header.append(key)
        model.setHeaderLabels(header)
        for ii in range(len(self.win4.re[0])):
            model.setColumnWidth(ii, 100)
        for i in range(len(self.win4.re)):
            a = QTreeWidgetItem(model)
            n = 0
            for key in self.win4.re[0]:
                a.setText(n, self.win4.re[i][key])
                n += 1
            model.addTopLevelItem(a)
        connection.close()

    def search_method(self):
        self.win4.add.hide()
        self.win4.delete.hide()
        self.win4.change.hide()
        self.win4.search.hide()
        self.win4.l1 = self.win4.newlabel(s='请输入想搜索的表单名', fz=17, size=[25, 40, 170, 30])
        self.win4.box1 = self.win4.new_input(fz=17, palce_size=[225, 40, 150, 30])
        self.win4.l2 = self.win4.newlabel(s='请输入搜索的列名', fz=17, size=[25, 80, 170, 30])
        self.win4.box2 = self.win4.new_input(fz=17, palce_size=[225, 80, 150, 30])
        self.win4.l3 = self.win4.newlabel(s='请输入查找的值', fz=17, size=[25, 120, 170, 30])
        self.win4.box3 = self.win4.new_input(fz=17, palce_size=[225, 120, 150, 30])
        self.win4.l1.show()
        self.win4.box1.show()
        self.win4.l2.show()
        self.win4.box2.show()
        self.win4.l3.show()
        self.win4.box3.show()
        btn = self.win4.new_button(s='点击确认搜索', fz=17, place=[135, 160, 130, 40])
        model = QTreeWidget(self.win4)
        model.setGeometry(30, 220, 340, 360)
        model.show()
        btn.show()
        btn.clicked.connect(lambda: self.showplace4(model, self.win4.box1.text(), self.win4.box2.text(), self.win4.box3.text()))

    def showplace4(self, model, tablename, columnname, value):
        model.clear()
        connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                                user='lab_33726443',
                                password='e2c26752cdf8_#@Aa',
                                db='jodio',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        cs1 = connection.cursor()
        sql1 = 'select * from %s' % (tablename)
        cs1.execute(sql1)
        self.win4.re = cs1.fetchall()
        if value != '':
            try:
                value = '"' + value + '"'
                sql = 'select * from %s where %s = %s' % (tablename, columnname, value)
                cs = connection.cursor()
                cs.execute(sql)
                self.win4.re = cs.fetchall()
                if self.win4.re == []:
                    QMessageBox.information(self, 'what','未找到')
                else:
                    model.clear()
            except :
                QMessageBox.information(self, 'what', '请检查您的输入内容')
        model.setColumnCount(len(self.win4.re[0]))
        header = []
        for key in self.win4.re[0]:
            header.append(key)
        model.setHeaderLabels(header)
        for ii in range(len(self.win4.re[0])):
            model.setColumnWidth(ii, 100)
        for i in range(len(self.win4.re)):
            a = QTreeWidgetItem(model)
            n = 0
            for key in self.win4.re[0]:
                a.setText(n, self.win4.re[i][key])
                n += 1
            model.addTopLevelItem(a)
        connection.close()
# ---------------

    def newlabel(self, s='', fz=30, size = [100, 100, 200, 200]):
        '新文本框'
        font = QFont()
        font.setFamily("Avenir")
        font.setPointSize(fz)
        label = QLabel(self)
        label.setFont(font)
        label.setText(s)
        label.setGeometry(size[0], size[1], size[2], size[3])
        label.setAlignment(Qt.AlignCenter)
        return label

    def new_input(self, fz=30, palce_size = [100, 100, 200, 200]):
        '输入框'
        box = QLineEdit(self)
        box.setGeometry(palce_size[0], palce_size[1], palce_size[2], palce_size[3])
        font = QFont()
        font.setFamily("Avenir")
        font.setPointSize(fz)
        box.setFont(font)
        return box

    def checkbox(self, fz=30, s='', place = [100, 100, 200, 200]):
        checkbox = QRadioButton(s, self)
        checkbox.setGeometry(place[0], place[1], place[2], place[3])
        font = QFont()
        font.setFamily("Avenir")
        font.setPointSize(fz)
        checkbox.setFont(font)
        return checkbox

    def new_button(self, s='', fz=30, place = [100, 100, 200, 200]):
        button = QPushButton(s, self)
        button.setGeometry(place[0], place[1], place[2], place[3])
        font = QFont()
        font.setFamily("Avenir")
        font.setPointSize(fz)
        button.setFont(font)
        button.setFont(font)
        return button
        
    def commit(self):
        '点击登录进行提交'
        if self.choose == '':
            QMessageBox.information(self, 'what','请选择之后再进行登录')
        else:
            username = self.username_box.text()
            password = self.password_box.text()
            result = self.login_test(self.choose)
            if self.choose:
                for i in range(len(result)):
                    if username == result[i]['t'] and password == result[i]['password']:
                        QMessageBox.information(self, 'what','恭喜您登录成功')
                        self.close()
                        self.new_face(self.choose)
                        break
                else:
                    QMessageBox.information(self, 'what','对不起您输入的账号密码有误')
            else:
                for i in range(len(result)):
                    if username == result[i]['s'] and password == result[i]['password']:
                        QMessageBox.information(self, 'what','恭喜您登录成功')
                        self.close()
                        self.new_face(self.choose)
                        break
                else:
                    QMessageBox.information(self, 'what','对不起您输入的账号密码有误')

    def login_action(self):
        '选择登陆方式，老师或者学生'
        sender = self.sender()
        if sender == self.bg:
            if self.bg.checkedId() == 2:
                print('您将作为教师登录')
                self.choose = True
            elif self.bg.checkedId() == 1:
                print('您将作为学生登录')
                self.choose = False
    # 为数据库创建其他的用户来修改权限
    def login_test(self, is_teacher = True):
        '连接数据库以获取登陆信息'
        connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                                user='lab_33726443',
                                password='e2c26752cdf8_#@Aa',
                                db='jodio',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        if is_teacher:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT t, password FROM `teacher`"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
            finally:
                connection.close()
        else:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT s, password FROM `student`"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
            finally:
                connection.close()

    def new_face(self, choose):
        '教师服务端'
        self.win2 = login()
        self.win2.username.hide()
        self.win2.password.hide()
        self.win2.username_box.hide()
        self.win2.password_box.hide()
        self.win2.button.hide()
        self.win2.checkbox2.hide()
        self.win2.checkbox1.hide()
        self.win2.title.hide()
        self.win2.super.hide()
        if choose:
            title = self.win2.newlabel(s='教师端', fz=17, size=[0, 0, 400, 50])
            welcome = self.win2.newlabel(s='欢迎老师!', fz=14, size=[0, 0, 100, 60])
            bt1 = self.win2.new_button(s='学生信息查询', fz=15, place=[30, 150, 120, 40])
            bt2 = self.win2.new_button(s='所教课程查询', fz=15, place=[30, 250, 120, 40])
            bt3 = self.win2.new_button(s='学生成绩查询', fz=15, place=[30, 350, 120, 40])
            bt4 = self.win2.new_button(s='工资查询', fz=15, place=[250, 150, 120, 40])
            bt5 = self.win2.new_button(s='学生成绩修改', fz=15, place=[250, 250, 120, 40])     
            bt6 = self.win2.new_button(s='教师信息查询', fz=15, place=[250, 350, 120, 40])
            bt1.setObjectName('1')
            bt2.setObjectName('2')
            bt3.setObjectName('3')
            bt4.setObjectName('4')
            bt5.setObjectName('5')
            bt6.setObjectName('6')
            bt1.clicked.connect(lambda: self.deal(self.choose))
            bt2.clicked.connect(lambda: self.deal(self.choose))
            bt3.clicked.connect(lambda: self.deal(self.choose))
            bt4.clicked.connect(lambda: self.deal(self.choose))
            bt5.clicked.connect(lambda: self.deal(self.choose))
            bt6.clicked.connect(lambda: self.deal(self.choose))
        else:
            title = self.win2.newlabel(s='学生端', fz=17, size=[0, 0, 400, 50])
            welcome = self.win2.newlabel(s='欢迎!', fz=14, size=[0, 0, 100, 60])
            bt1 = self.win2.new_button(s='学生信息查询', fz=15, place=[30, 150, 120, 40])
            bt2 = self.win2.new_button(s='选课', fz=15, place=[30, 250, 120, 40])
            bt3 = self.win2.new_button(s='学生成绩查询', fz=15, place=[250, 150, 120, 40])
            bt6 = self.win2.new_button(s='教师信息查询', fz=15, place=[250, 250, 120, 40])
            bt1.setObjectName('1')
            bt2.setObjectName('2')
            bt3.setObjectName('3')
            bt6.setObjectName('6')
            bt1.clicked.connect(lambda: self.deal(self.choose))
            bt2.clicked.connect(lambda: self.deal(self.choose))
            bt3.clicked.connect(lambda: self.deal(self.choose))
            bt6.clicked.connect(lambda: self.deal(self.choose))
        self.win2.show()
                    
    def deal(self, choose):
        '针对第二个交互界面选项结果处理'
        connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                                user='lab_33726443',
                                password='e2c26752cdf8_#@Aa',
                                db='jodio',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        button = self.win2.sender()
        self.win2.hide()
        self.win3 = login()
        self.win3.username.hide()
        self.win3.password.hide()
        self.win3.username_box.hide()
        self.win3.password_box.hide()
        self.win3.button.hide()
        self.win3.checkbox2.hide()
        self.win3.checkbox1.hide()
        self.win3.title.hide()
        self.t_or_c = 0
        print('你选择的是%s' % button.objectName())
        if button.objectName() == '1':
            # 学生信息查询
            if choose:
                lb = self.win3.newlabel(s='学生信息查询', fz=15, size=[0, 0, 400, 50])
                lb2 = self.win3.newlabel(s='请输入查询的学号', fz=15, size=[0, 70, 150, 30])
                box1 = self.win3.new_input(fz=15, palce_size=[150, 70, 150, 30])
                bt1 = self.win3.new_button(s='查询', fz=15, place=[310, 70, 60, 30])
                bt1.clicked.connect(lambda: self.exe(re, box1.text(), model))
                model = QTreeWidget(self.win3)
                model.setGeometry(30, 120, 340, 420)
                model.setColumnCount(6)
                model.setHeaderLabels(['学号', '姓名', '性别', '年龄', '住址', '联系方式'])
                model.setColumnWidth(0, 100)
                model.setColumnWidth(1, 100)
                model.setColumnWidth(2, 100)
                model.setColumnWidth(3, 100)
                model.setColumnWidth(4, 100)
                model.setColumnWidth(5, 100)
                cs1 = connection.cursor()
                sql = 'select * from student'
                cs1.execute(sql)
                re = cs1.fetchall()
                for i in re:
                    a = QTreeWidgetItem(model)
                    a.setText(0, '%s' % i['s'])
                    a.setText(1, i['sname'])
                    a.setText(2, i['sex'])
                    a.setText(3, i['age'])
                    a.setText(4, i['address'])
                    a.setText(5, i['phone'])
                    model.addTopLevelItem(a)
            else:
                lb = self.win3.newlabel(s='学生信息查询', fz=15, size=[0, 0, 400, 50])
                model = QTreeWidget(self.win3)
                model.setGeometry(30, 70, 340, 470)
                model.setColumnCount(4)
                model.setHeaderLabels(['学号', '姓名', '性别', '年龄'])
                model.setColumnWidth(0, 100)
                model.setColumnWidth(1, 100)
                model.setColumnWidth(2, 100)
                model.setColumnWidth(3, 100)
                cs1 = connection.cursor()
                sql = 'select s, sname, sex, age from student'
                cs1.execute(sql)
                re = cs1.fetchall()
                for i in re:
                    a = QTreeWidgetItem(model)
                    a.setText(0, '%s' % i['s'])
                    a.setText(1, i['sname'])
                    a.setText(2, i['sex'])
                    a.setText(3, i['age'])
                    model.addTopLevelItem(a)

        if button.objectName() == '2':
            if choose:
                lb = self.win3.newlabel(s='所教课程查询', fz=15, size=[0, 0, 400, 50])
                qbox = QComboBox(self.win3)
                qbox.setGeometry(20, 70, 100, 30)
                qbox.addItems(['课程号', '老师工号'])
                qbox.currentIndexChanged[int].connect(self.getchoice)
                box1 = self.win3.new_input(fz=15, palce_size=[150, 70, 150, 30])
                bt1 = self.win3.new_button(s='查询', fz=15, place=[310, 70, 60, 30])
                bt1.clicked.connect(lambda: self.cexe(re, box1.text(), model, self.t_or_c))
                sql = 'select * from class'
                cs3 = connection.cursor()
                cs3.execute(sql)
                re = cs3.fetchall()
                model = QTreeWidget(self.win3)
                model.setGeometry(30, 120, 340, 420)
                model.setColumnCount(3)
                model.setHeaderLabels(['课程号', '教师工号', '课程名'])
                model.setColumnWidth(0, 100)
                model.setColumnWidth(1, 100)
                model.setColumnWidth(2, 100)
                for i in re:
                    a = QTreeWidgetItem(model)
                    a.setText(0, '%s' % i['c'])
                    a.setText(1, i['t'])
                    a.setText(2, i['cname'])
                    model.addTopLevelItem(a)
            else:
                lb = self.win3.newlabel(s='选课', fz=15, size=[0, 0, 400, 50])
                lb2 = self.win3.newlabel(s='请输入课程号', fz=15, size=[0, 70, 150, 30])
                box1 = self.win3.new_input(fz=15, palce_size=[150, 70, 150, 30])
                bt1 = self.win3.new_button(s='选课', fz=15, place=[310, 70, 60, 30])
                bt1.clicked.connect(lambda: self.chooseclass(box1.text()))

        if button.objectName() == '3':
            if choose:
                lb = self.win3.newlabel(s='学生成绩查询', fz=15, size=[0, 0, 400, 50])
                qbox = QComboBox(self.win3)
                qbox.setGeometry(20, 70, 100, 30)
                qbox.addItems(['学生学号', '课程号'])
                qbox.currentIndexChanged[int].connect(self.getchoice)
                box1 = self.win3.new_input(fz=15, palce_size=[150, 70, 150, 30])
                bt1 = self.win3.new_button(s='查询', fz=15, place=[310, 70, 60, 30])
                bt1.clicked.connect(lambda: self.scoreexe(re, box1.text(), model, self.t_or_c))
                sql = 'select * from sc'
                cs3 = connection.cursor()
                cs3.execute(sql)
                re = cs3.fetchall()
                model = QTreeWidget(self.win3)
                model.setGeometry(30, 120, 340, 420)
                model.setColumnCount(3)
                model.setHeaderLabels(['课程号', '学生学号', '分数'])
                model.setColumnWidth(0, 100)
                model.setColumnWidth(1, 100)
                model.setColumnWidth(2, 100)
                for i in re:
                    a = QTreeWidgetItem(model)
                    a.setText(0, '%s' % i['c'])
                    a.setText(1, i['s'])
                    a.setText(2, i['score'])
                    model.addTopLevelItem(a)
            else:
                lb = self.win3.newlabel(s='学生成绩查询', fz=15, size=[0, 0, 400, 50])
                sql = 'select * from sc where s=%s' % self.username_box.text()
                cs3 = connection.cursor()
                cs3.execute(sql)
                re = cs3.fetchall()
                model = QTreeWidget(self.win3)
                model.setGeometry(30, 120, 340, 420)
                model.setColumnCount(3)
                model.setHeaderLabels(['课程号', '学生学号', '分数'])
                model.setColumnWidth(0, 100)
                model.setColumnWidth(1, 100)
                model.setColumnWidth(2, 100)
                for i in re:
                    a = QTreeWidgetItem(model)
                    a.setText(0, '%s' % i['c'])
                    a.setText(1, i['s'])
                    a.setText(2, i['score'])
                    model.addTopLevelItem(a)
    
        if button.objectName() == '4':
            sql = 'select money from teacher where t = %s' % self.username_box.text()
            cs4 = connection.cursor()
            cs4.execute(sql)
            re = cs4.fetchall()
            lb = self.win3.newlabel(s='工资查询', fz=15, size=[0, 0, 400, 50])
            lb = self.win3.newlabel(s='您的工资为%s每月，合年薪%d' % (re[0]['money'], int(re[0]['money']) * 12), fz=20, size=[0, 100, 400, 100])

        if button.objectName() == '5':
            lb = self.win3.newlabel(s='学生成绩修改', fz=15, size=[0, 0, 400, 50])
            lb1 = self.win3.newlabel(s='请输入要修改学生的学号', fz=15, size=[0, 70, 200, 30])
            box1 = self.win3.new_input(fz=15, palce_size=[200, 70, 150, 30])
            lb2 = self.win3.newlabel(s='请输入要修改课程的课程号', fz=15, size=[0, 120, 200, 30])
            box2 = self.win3.new_input(fz=15, palce_size=[200, 120, 150, 30])
            lb3 = self.win3.newlabel(s='请输入想要修改的成绩', fz=15, size=[0, 170, 200, 30])
            box3 = self.win3.new_input(fz=15, palce_size=[200, 170, 150, 30])
            bt = self.win3.new_button(s='点击修改', fz=15, place=[140, 220, 120, 30])
            bt.clicked.connect(lambda : self.modify(re, box1.text(), box2.text(), box3.text()))
            sql = 'select * from sc'
            cs5 = connection.cursor()
            cs5.execute(sql)
            re = cs5.fetchall()

        if button.objectName() == '6':
            lb = self.win3.newlabel(s='教师信息查询', fz=15, size=[0, 0, 400, 50])
            lb2 = self.win3.newlabel(s='请输入查询的工号', fz=15, size=[0, 70, 150, 30])
            box1 = self.win3.new_input(fz=15, palce_size=[150, 70, 150, 30])
            bt1 = self.win3.new_button(s='查询', fz=15, place=[310, 70, 60, 30])
            bt1.clicked.connect(lambda: self.texe(re, box1.text(), model))
            sql = 'select * from teacher'
            cs6 = connection.cursor()
            cs6.execute(sql)
            re = cs6.fetchall()
            model = QTreeWidget(self.win3)
            model.setGeometry(30, 120, 340, 420)
            model.setColumnCount(6)
            model.setHeaderLabels(['工号', '姓名', '性别', '住址', '联系方式', '职称'])
            model.setColumnWidth(0, 100)
            model.setColumnWidth(1, 100)
            model.setColumnWidth(2, 100)
            model.setColumnWidth(3, 100)
            model.setColumnWidth(4, 100)
            model.setColumnWidth(5, 100)
            for i in re:
                a = QTreeWidgetItem(model)
                a.setText(0, '%s' % i['t'])
                a.setText(1, i['tname'])
                a.setText(2, i['sex'])
                a.setText(3, i['address'])
                a.setText(4, i['phone'])
                a.setText(5, i['title'])
                model.addTopLevelItem(a)

        back = self.win3.new_button(s='返回', fz=15, place=[340, 560, 50, 25])
        self.win3.show()
        connection.close()
        back.clicked.connect(self.back)
    
    def exe(self, re, value, model):
        '查询学生信息'
        model.clear()
        ans = []
        for i in re:
            if i['s'] == value:
                ans.append(i)
        for i in ans:
                a = QTreeWidgetItem(model)
                a.setText(0, '%s' % i['s'])
                a.setText(1, i['sname'])
                a.setText(2, i['sex'])
                a.setText(3, i['age'])
                a.setText(4, i['address'])
                a.setText(5, i['phone'])
                model.addTopLevelItem(a)
    
    def texe(self, re, value, model):
        '查询老师信息'
        model.clear()
        ans = []
        for i in re:
            if i['t'] == value:
                ans.append(i)
        for i in ans:
                a = QTreeWidgetItem(model)
                a.setText(0, '%s' % i['t'])
                a.setText(1, i['tname'])
                a.setText(2, i['sex'])
                a.setText(3, i['address'])
                a.setText(4, i['phone'])
                a.setText(5, i['title'])
                model.addTopLevelItem(a)
    
    def cexe(self, re, value, model, t_or_c):
        model.clear()
        ans = []
        if t_or_c == 0:
            for i in re:
                if i['c'] == value:
                    ans.append(i)
        elif t_or_c == 1:
            for i in re:
                if i['t'] == value:
                    ans.append(i)
        for i in ans:
                a = QTreeWidgetItem(model)
                a.setText(0, i['c'])
                a.setText(1, i['t'])
                a.setText(2, i['cname'])
                model.addTopLevelItem(a)

    def scoreexe(self, re, value, model, t_or_c):
        model.clear()
        ans = []
        if t_or_c == 1:
            for i in re:
                if i['c'] == value:
                    ans.append(i)
        elif t_or_c == 0:
            for i in re:
                if i['s'] == value:
                    ans.append(i)
        for i in ans:
                a = QTreeWidgetItem(model)
                a.setText(0, i['c'])
                a.setText(1, i['s'])
                a.setText(2, i['score'])
                model.addTopLevelItem(a)

    def modify(self, re, sid, cid, score):
        connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                                user='lab_33726443',
                                password='e2c26752cdf8_#@Aa',
                                db='jodio',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        cs9 = connection.cursor()
        sql = 'select class.c, s, class.t from class, sc where t = %s and class.c = sc.c' % self.username_box.text()
        cs9.execute(sql)
        respond = cs9.fetchall()
        for i in respond:
            if i['c'] == cid:
                break
        else:
            QMessageBox.information(self, 'what', '对不起您没有权限修改这项成绩')
            return False
        for i in respond:
            if i['s'] == sid:
                break
        else:
            QMessageBox.information(self, 'what', '对不起该学生并未选择该课程')
            return False
        sql3 = 'update sc set score=%s where c=%s and s=%s' % (score, cid, sid)
        cs0 = connection.cursor()
        cs0.execute(sql3)
        connection.commit()
        QMessageBox.information(self, 'what', '修改成功！')
        connection.close()

    def getchoice(self, i=0):
        self.t_or_c = i

    def back(self):
        self.win2.show()
        self.win3.hide()

    def chooseclass(self, cid):
        connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                                user='lab_33726443',
                                password='e2c26752cdf8_#@Aa',
                                db='jodio',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        sql = 'insert into sc(s, c) values(%s, %s)' % (self.username_box.text(), cid)
        try:
            with connection.cursor() as cs1:
                cs1.execute(sql)
                connection.commit()
            QMessageBox.information(self, 'what', '恭喜您选课成功')
        except :
            QMessageBox.information(self, 'what', '未成功选课，请查看您是否已经选过或者是大纲中是否包含此课程')
        connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win1 = login()
    win1.show()
    sys.exit(app.exec_())
