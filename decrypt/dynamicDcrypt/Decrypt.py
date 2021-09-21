# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : Decrypt.py
# Time       ：2021/8/20 11:51
# Author     ：Yooha
"""

from PyQt5 import QtCore, QtWidgets
import PyQt5
import sys
import os
from PyQt5.QtWidgets import QMessageBox
import frida
import time
import subprocess



#*****************************************************************************************
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(318, 217)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_cocos = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cocos.setGeometry(QtCore.QRect(40, 30, 231, 31))
        self.btn_cocos.setObjectName("btn_cocos")
        self.btn_unity = QtWidgets.QPushButton(self.centralwidget)
        self.btn_unity.setGeometry(QtCore.QRect(40, 100, 231, 31))
        self.btn_unity.setObjectName("btn_unity")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 318, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UCDecer 1.0"))
        self.btn_cocos.setText(_translate("MainWindow", "<Cocos-js> <Cocos-lua> <Unity-slua>"))
        self.btn_unity.setText(_translate("MainWindow", "<Unity-libil2cpp>"))


class WindowAction(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self, decrypt:object):
        super(WindowAction, self).__init__()
        self.decrypt:DecryptApp = decrypt

    def click_cocos(self):
        self.decrypt.dialog_cocos.setupTitle('Cocos2D')
        self.decrypt.dialog_cocos.exec()

    def click_unity(self):
        self.decrypt.dialog_unity.setupTitle('Unity3D')
        self.decrypt.dialog_unity.exec()
#*****************************************************************************************
class Ui_dlg_unity(object):
    def setupUi(self, dlg_unity):
        dlg_unity.setObjectName("dlg_unity")
        dlg_unity.resize(531, 236)
        self.label = QtWidgets.QLabel(dlg_unity)
        self.label.setGeometry(QtCore.QRect(30, 30, 181, 31))
        self.label.setObjectName("label")
        self.unity_dat = QtWidgets.QLineEdit(dlg_unity)
        self.unity_dat.setGeometry(QtCore.QRect(200, 29, 301, 31))
        self.unity_dat.setObjectName("unity_dat")
        self.label_2 = QtWidgets.QLabel(dlg_unity)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 181, 31))
        self.label_2.setObjectName("label_2")
        self.unity_so = QtWidgets.QLineEdit(dlg_unity)
        self.unity_so.setGeometry(QtCore.QRect(200, 90, 301, 31))
        self.unity_so.setObjectName("unity_so")
        self.unity_decrypt = QtWidgets.QPushButton(dlg_unity)
        self.unity_decrypt.setGeometry(QtCore.QRect(190, 160, 121, 31))
        self.unity_decrypt.setObjectName("unity_decrypt")

        self.retranslateUi(dlg_unity)
        QtCore.QMetaObject.connectSlotsByName(dlg_unity)

    def retranslateUi(self, dlg_unity):
        _translate = QtCore.QCoreApplication.translate
        dlg_unity.setWindowTitle(_translate("dlg_unity", "Dialog"))
        self.label.setText(_translate("dlg_unity", "global-metadata.dat文件路径"))
        self.label_2.setText(_translate("dlg_unity", "libil2cpp.so文件路径"))
        self.unity_decrypt.setText(_translate("dlg_unity", "Decrypt"))


class DialogUnityAction(PyQt5.QtWidgets.QDialog):

    def __init__(self, window):
        super(DialogUnityAction, self).__init__(window)
        self.ui = Ui_dlg_unity()
        self.window:WindowAction = window
        self.ui.setupUi(self)
        self.setupAction()

    def setupTitle(self, title):
        self.setWindowTitle(title)

    def setupAction(self):
        self.ui.unity_decrypt.clicked.connect(self.click_decrypt)

    def click_decrypt(self):
        try:
            current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
            text_dat = self.ui.unity_dat.text()
            text_so = self.ui.unity_so.text()
            command = current_path + "/resource/Il2CppDumper/Il2CppDumper.exe " + text_so + ' ' + text_dat + ' ' + current_path + "/output"
            print(command)
            out = Shell.excute_cmd(command)
            if (str(out).find('Press any key to exit') != -1):
                QMessageBox.information(self,"提示", '解密完成!',QMessageBox.Yes | QMessageBox.No)
        except Exception as err:
            QMessageBox.warning(self,"错误", str(err),QMessageBox.Yes | QMessageBox.No)
            exit(2)
#*****************************************************************************************
class Ui_dlg_cocos(object):
    def setupUi(self, dlg_cocos):
        dlg_cocos.setObjectName("dlg_cocos")
        dlg_cocos.resize(374, 207)
        self.label = QtWidgets.QLabel(dlg_cocos)
        self.label.setGeometry(QtCore.QRect(30, 40, 91, 31))
        self.label.setObjectName("label")
        self.cocos_pkg = QtWidgets.QLineEdit(dlg_cocos)
        self.cocos_pkg.setGeometry(QtCore.QRect(140, 40, 211, 31))
        self.cocos_pkg.setObjectName("cocos_pkg")
        self.cocos_decrypt = QtWidgets.QPushButton(dlg_cocos)
        self.cocos_decrypt.setGeometry(QtCore.QRect(60, 90, 91, 31))
        self.cocos_decrypt.setObjectName("cocos_decrypt")
        self.cocos_dump = QtWidgets.QPushButton(dlg_cocos)
        self.cocos_dump.setGeometry(QtCore.QRect(210, 90, 91, 31))
        self.cocos_dump.setObjectName("cocos_dump")
        self.label_2 = QtWidgets.QLabel(dlg_cocos)
        self.label_2.setGeometry(QtCore.QRect(40, 130, 311, 51))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(dlg_cocos)
        QtCore.QMetaObject.connectSlotsByName(dlg_cocos)

    def retranslateUi(self, dlg_cocos):
        _translate = QtCore.QCoreApplication.translate
        dlg_cocos.setWindowTitle(_translate("dlg_cocos", "Dialog"))
        self.label.setText(_translate("dlg_cocos", "请输入应用包名"))
        self.cocos_decrypt.setText(_translate("dlg_cocos", "Decrypt"))
        self.cocos_dump.setText(_translate("dlg_cocos", "Dump"))
        self.label_2.setText(_translate("dlg_cocos", "提示：请点击手机应用的功能界面，以使脚本解密完全"))


class DialogCocosAction(PyQt5.QtWidgets.QDialog):

    def __init__(self, window):
        super(DialogCocosAction, self).__init__(window)
        self.ui = Ui_dlg_cocos()
        self.window:WindowAction = window
        self.ui.setupUi(self)
        self.setupAction()
        self.cocos = None
        self.pkgname = None


    def setupTitle(self, title):
        self.setWindowTitle(title)

    def setupAction(self):
        self.ui.cocos_decrypt.clicked.connect(self.click_decrypt)
        self.ui.cocos_dump.clicked.connect(self.click_dump)


    def click_decrypt(self):
        self.pkgname = self.ui.cocos_pkg.text()
        if (self.pkgname == ''):
            QMessageBox.warning(self, "警告", "请先输入包名！", QMessageBox.Yes | QMessageBox.No)
            return
        else:
            QMessageBox.information(self,"提示","请先确保打开了frida server！",QMessageBox.Yes | QMessageBox.No)
        
        try:
            self.cocos = Process(self.pkgname)
            self.cocos.spawn("./resource/inject.js")
        except Exception as err:
            QMessageBox.warning(self, "警告", str(err), QMessageBox.Yes | QMessageBox.No)

    def click_dump(self):
        if self.cocos:
            try:
                Shell.excute_adb_multiple(['su\n', 'rm -R /sdcard/Download/dump/*.*\n', 'exit\n'])
                Shell.excute_adb_multiple(['su\n', 'chmod 777 /data/data/' +  self.pkgname + '/dump\n', 'exit\n'])
                Shell.excute_adb_multiple(['su\n', 'mv /data/data/' +  self.pkgname + '/dump /sdcard/Download\n', 'exit\n'])
                Shell.excute_adb_simple('adb pull /sdcard/Download/dump ./output/dump\n')
            except Exception as err:
                QMessageBox.warning(self,"错误",str(err),QMessageBox.Yes | QMessageBox.No)
                exit(2)
#*****************************************************************************************
class Process(object):

    def __init__(self, pkgname):
        self.pid = None
        self.pkgname = pkgname
        self.session = None
        self.script = None
        self.device = frida.get_usb_device(timeout=15)
        pass


    def spawn(self, hook):
        self.pid = self.device.spawn(self.pkgname)
        self.device.resume(self.pid)

        while True: # 每0.5秒获取一次session 直至成功
            try:
                time.sleep(0.5)
                self.session = self.device.attach(self.pid)
            except:
                continue
            break

        with open(hook, "r", encoding='utf-8') as f:
            self.script = self.session.create_script(f.read())

        self.script.load()
        self.script.exports.decryptcocos(self.pkgname)
        return True

#*****************************************************************************************
class Shell(object):
    def __init__(self):
        pass

    @classmethod
    def excute_cmd(cls, cmd:str) -> list:
        obj = subprocess.Popen(cmd, shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
        info,err = obj.communicate()
        return (str(info.decode('gbk'))).split('\n')
        

    @classmethod
    def excute_adb_simple(cls, cmd:str) -> list:
        obj = subprocess.Popen(cmd, shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
        return obj.stdout.readlines()

    @classmethod
    def excute_adb_multiple(cls, cmd:list) -> list:
        info = None
        obj = subprocess.Popen(['adb', 'shell'], shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
        for line in cmd:
            obj.stdin.write(line.encode('utf-8'))
        info,err = obj.communicate()
        return (str(info.decode('gbk'))).split('\n')

#*****************************************************************************************
class DecryptApp(object):

    def __init__(self):
        self.application = PyQt5.QtWidgets.QApplication(sys.argv)
        self.ui = Ui_MainWindow()
        self.window = WindowAction(self)
        self.window.setWindowIcon(PyQt5.QtGui.QIcon('./resource/icon.png'))
        self.ui.setupUi(self.window)
        self.setup_action()
        self.dialog_cocos = DialogCocosAction(self.window)
        self.dialog_unity = DialogUnityAction(self.window)
        self.window.show()
        sys.exit(self.application.exec_())

    def setup_action(self):
        self.ui.btn_cocos.clicked.connect(self.window.click_cocos)
        self.ui.btn_unity.clicked.connect(self.window.click_unity)



if __name__ == '__main__':
    DecryptApp()



