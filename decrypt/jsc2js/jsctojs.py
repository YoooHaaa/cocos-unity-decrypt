# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : AdDiscern.py
# Time       ：2021/9/18 16:51
# Author     ：Yooha
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import PyQt5
import sys
from PyQt5.QtWidgets import QMessageBox
import os
import sys
from gzip import GzipFile
from io import BytesIO
import struct


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(639, 335)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 60, 131, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 110, 131, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 160, 131, 16))
        self.label_3.setObjectName("label_3")
        self.edt_path_so = QtWidgets.QLineEdit(self.centralwidget)
        self.edt_path_so.setGeometry(QtCore.QRect(230, 60, 251, 21))
        self.edt_path_so.setObjectName("edt_path_so")
        self.btn_path_so = QtWidgets.QPushButton(self.centralwidget)
        self.btn_path_so.setGeometry(QtCore.QRect(490, 60, 41, 21))
        self.btn_path_so.setObjectName("btn_path_so")
        self.edt_path_jsc = QtWidgets.QLineEdit(self.centralwidget)
        self.edt_path_jsc.setGeometry(QtCore.QRect(230, 110, 251, 21))
        self.edt_path_jsc.setObjectName("edt_path_jsc")
        self.btn_path_jsc = QtWidgets.QPushButton(self.centralwidget)
        self.btn_path_jsc.setGeometry(QtCore.QRect(490, 110, 41, 21))
        self.btn_path_jsc.setObjectName("btn_path_jsc")
        self.edt_path_js = QtWidgets.QLineEdit(self.centralwidget)
        self.edt_path_js.setGeometry(QtCore.QRect(230, 160, 251, 21))
        self.edt_path_js.setObjectName("edt_path_js")
        self.btn_path_js = QtWidgets.QPushButton(self.centralwidget)
        self.btn_path_js.setGeometry(QtCore.QRect(490, 160, 41, 21))
        self.btn_path_js.setObjectName("btn_path_js")
        self.btn_decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_decrypt.setGeometry(QtCore.QRect(220, 220, 161, 23))
        self.btn_decrypt.setObjectName("btn_decrypt")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 639, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "jsc -> js"))
        self.label.setText(_translate("MainWindow", "libcocos2djs.so路径"))
        self.label_2.setText(_translate("MainWindow", "jsc文件路径"))
        self.label_3.setText(_translate("MainWindow", "解密js文件保存路径"))
        self.btn_path_so.setText(_translate("MainWindow", "..."))
        self.btn_path_jsc.setText(_translate("MainWindow", "..."))
        self.btn_path_js.setText(_translate("MainWindow", "..."))
        self.btn_decrypt.setText(_translate("MainWindow", "解密"))


class WindowAction(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self, obj:object):
        super(WindowAction, self).__init__()
        self.obj:Worker = obj


    def click_so(self):
        directory = QFileDialog.getOpenFileName(self,  "请选择so路径", "./", "*.so") 
        self.obj.ui.edt_path_so.setText(directory[0])


    def click_jsc(self):
        directory = QFileDialog.getExistingDirectory(self,  "请选择jsc文件目录", "./") 
        self.obj.ui.edt_path_jsc.setText(directory)


    def click_js(self):
        directory = QFileDialog.getExistingDirectory(self,  "请选择js文件保存路径", "./") 
        self.obj.ui.edt_path_js.setText(directory)


    def click_decrypt(self):
        ret, msg = Decrypt_xxtea(self.obj.ui.edt_path_jsc.text(), Key.parse(self.obj.ui.edt_path_so.text())).run_decrypt(self.obj.ui.edt_path_js.text())
        if ret:
            QMessageBox.information(self, "提示", '解密完成', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "解密出错", msg, QMessageBox.Ok)

#***********************************************************************************
class Key(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, path):
        with open(path, "rb") as js:
            cls.jsbytes = js.read()
            index = cls.jsbytes.find(bytes('jsb-adapter', 'utf-8'))
            return cls.get_key(index)

            
    @classmethod
    def get_key(cls, index):
        cls.key = bytearray()
        key_end = False
        num = 1
        while True:
            if cls.jsbytes[index - num] == 0x0:
                if key_end:
                    cls.key.reverse()
                    return cls.key.decode()
            else:
                if key_end == False:
                    key_end = True
                cls.key.append(cls.jsbytes[index - num])
            num += 1

#***********************************************************************************
class Decrypt_xxtea(object):

    def __init__(self, path: str, key: str) -> None:
        '''
        param:
            path  : jsc文件所在目录
            key   : 解密的key
        '''
        self.delta = 0x9E3779B9
        self.path = path
        self.key = key.encode('utf-8')


    def long2str(self, v, w):
        n = (len(v) - 1) << 2
        if w:
            m = v[-1]
            if (m < n - 3) or (m > n): return ''
            n = m
        s = struct.pack('<%iL' % len(v), *v)
        return s[0:n] if w else s

    def str2long(self, s, w):
        n = len(s)
        m = (4 - (n & 3) & 3) + n
        s = s.ljust(m, b"\0")
        v = list(struct.unpack('<%iL' % (m >> 2), s))
        if w: v.append(n)
        return v

    def decrypt(self, str):
        if str == b'': return str
        v = self.str2long(str, False)
        k = self.str2long(self.key.ljust(16, b"\0"), False)
        n = len(v) - 1
        z = v[n]
        y = v[0]
        q = 6 + 52 // (n + 1)
        sum = (q * self.delta) & 0xffffffff
        while (sum != 0):
            e = sum >> 2 & 3
            for p in range(n, 0, -1):
                z = v[p - 1]
                v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
                y = v[p]
            z = v[n]
            v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff
            y = v[0]
            sum = (sum - self.delta) & 0xffffffff
        return self.long2str(v, True)


    def find_targets(self, path):
        result = []
        if not os.path.exists(path):
            return []
        if not os.path.isdir(path):
            return [path]
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".jsc"):
                    result.append(os.path.join(root, file))
        return result


    def run_decrypt(self, savePath):
        targets = self.find_targets(self.path)
        for target in targets:
            out = target[:-1]
            out = savePath + '/' + out.split('\\')[-1]
            content = open(target, "rb").read()
            if self.key:
                content = self.decrypt(content)
            if content[:2] == b'\037\213':
                try:
                    mock_fp = BytesIO(content)
                    gz = GzipFile(fileobj=mock_fp)
                    content = gz.read()
                except Exception as e:
                    return False, str(e)
            with open(out, 'wb') as _:
                _.write(content)
        return True, ""



#***********************************************************************************
class Worker(object):
    def __init__(self):
        self.init()


    @classmethod
    def init(cls):
        cls.application = PyQt5.QtWidgets.QApplication(sys.argv)
        cls.ui = Ui_MainWindow()
        cls.window = WindowAction(cls)
        cls.window.setWindowIcon(PyQt5.QtGui.QIcon('./icon.png'))
        cls.ui.setupUi(cls.window)
        cls.setup_action()
        cls.window.show()
        sys.exit(cls.application.exec_())


    @classmethod
    def setup_action(cls):
        cls.ui.btn_path_so.clicked.connect(cls.window.click_so)
        cls.ui.btn_path_jsc.clicked.connect(cls.window.click_jsc)
        cls.ui.btn_path_js.clicked.connect(cls.window.click_js)
        cls.ui.btn_decrypt.clicked.connect(cls.window.click_decrypt)
#***********************************************************************************
if __name__ == '__main__':
    Worker()