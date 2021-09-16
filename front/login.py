# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, uic
import requests
import time
from operator import attrgetter


class Ui_MainWindow(object):
    ngrok = 'http://e626-170-0-71-179.ngrok.io'

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Connect")
        MainWindow.resize(469, 442)
        MainWindow.setStyleSheet("background-color: rgb(85, 0, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.botaoEntrar = QtWidgets.QPushButton(self.centralwidget)
        self.botaoEntrar.setGeometry(QtCore.QRect(188, 270, 75, 23))
        self.botaoEntrar.setStyleSheet("color: rgb(255, 255, 255);")
        self.botaoEntrar.setObjectName("botaoEntrar")
        self.label_cpf = QtWidgets.QLabel(self.centralwidget)
        self.label_cpf.setGeometry(QtCore.QRect(28, 220, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_cpf.setFont(font)
        self.label_cpf.setStyleSheet("color:rgb(255, 255, 255)")
        self.label_cpf.setObjectName("label_cpf")
        self.label_2_nome = QtWidgets.QLabel(self.centralwidget)
        self.label_2_nome.setGeometry(QtCore.QRect(28, 180, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2_nome.setFont(font)
        self.label_2_nome.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2_nome.setObjectName("label_2_nome")
        self.lineEdit_CPF = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CPF.setGeometry(QtCore.QRect(68, 220, 341, 20))
        self.lineEdit_CPF.setObjectName("lineEdit_CPF")
        self.lineEdit_NOME = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_NOME.setGeometry(QtCore.QRect(70, 180, 341, 20))
        self.lineEdit_NOME.setObjectName("lineEdit_NOME")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 80, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 469, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.botaoEntrar.clicked.connect(self.login)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.botaoEntrar.setText(_translate("MainWindow", "Entrar"))
        self.label_cpf.setText(_translate("MainWindow", "CPF"))
        self.label_2_nome.setText(_translate("MainWindow", "Nome"))
        self.label.setText(_translate("MainWindow", "Connect Covid"))

    def update(self, signal):
        self.telaDados.label_sinaisVitais.setText(signal)

    def create_json(self) -> dict:
        return {
            'cpf': int(self.lineEdit_CPF.text()),
            'nome': self.lineEdit_NOME.text(),
            'temp': '',
            'freq': '',
            'pressao1': '',
            'pressao2': '',
            'resp': '',
            'status': 'Estável'
        }

    def update_json(self) -> dict:
        return {
            'nome': self.lineEdit_NOME.text(),
            'temp': self.telaDados.doubleSpinBox_temp.value(),
            'freq': self.telaDados.spinBox_freq.value(),
            'pressao1': self.telaDados.spinBox_pressao1.value(),
            'pressao2': self.telaDados.spinBox_pressao1.value(),
            'resp': self.telaDados.spinBox_saturacao.value(),
        }

    def login(self):
        try:
            requests.post(url=f'{self.ngrok}/patient', json=self.create_json())
            paciente = self.getPaciente()
            self.telaDados = uic.loadUi('paciente.ui')
            self.telaDados.label_nomePaciente.setText(paciente['nome'])
            self.telaDados.show()
            self.telaDados.botao.clicked.connect(self.atualizaPaciente)
            self.thread_start = MyThread()
            self.thread_start.ard_signal.connect(self.update)
            self.thread_start.start()

        except:
            print("error")

    def atualizaPaciente(self):
        r = requests.put(
            url=f'{self.ngrok}/patient/{int(self.lineEdit_CPF.text())}', json=self.update_json())
        print(r)

    def getPaciente(self) -> dict:
        rq = requests.get(
            url=f'{self.ngrok}/patient/{int(self.lineEdit_CPF.text())}')
        return rq.json()


class MyThread(QtCore.QThread):
    ard_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while 1:
            resp = ui.getPaciente()
            time.sleep(2)
            self.ard_signal.emit(resp['status'])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
