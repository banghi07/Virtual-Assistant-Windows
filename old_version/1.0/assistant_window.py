# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(419, 310)
        MainWindow.setStyleSheet("QLabel {\n"
                                 "    font: 12pt \"MS Shell Dlg 2\";\n"
                                 "    border: 1px solid black;\n"
                                 "    border-radius: 5px;\n"
                                 "}\n"
                                 "\n"
                                 "QToolButton {\n"
                                 "    border: none\n"
                                 "}\n"
                                 "\n"
                                 "QPlainTextEdit {\n"
                                 "    font: 12pt \"MS Shell Dlg 2\";\n"
                                 "    border: 1px solid black;\n"
                                 "    border-radius: 5px;\n"
                                 "    background: transparent;\n"
                                 "    \n"
                                 "}\n"
                                 "\n"
                                 "QPushButton {\n"
                                 "    border: 1px solid black;\n"
                                 "    border-radius: 5px;\n"
                                 "    background-color: gray;\n"
                                 "}\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(9, 260, 341, 41))
        self.label.setText("")
        self.label.setObjectName("label")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 400, 240))
        self.plainTextEdit.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setMaximumBlockCount(0)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 260, 51, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "..."))
