# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P:\Projects\MailPrep\ui\mainwindow.ui',
# licensing of 'P:\Projects\MailPrep\ui\mainwindow.ui' applies.
#
# Created: Thu May  2 20:43:25 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow_MailPrep(object):
    def setupUi(self, MainWindow_MailPrep):
        MainWindow_MailPrep.setObjectName("MainWindow_MailPrep")
        MainWindow_MailPrep.resize(451, 199)
        MainWindow_MailPrep.setMinimumSize(QtCore.QSize(451, 199))
        self.centralwidget = QtWidgets.QWidget(MainWindow_MailPrep)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label_jobNumber = QtWidgets.QLabel(self.centralwidget)
        self.label_jobNumber.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_jobNumber.setObjectName("label_jobNumber")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_jobNumber)
        self.lineEdit_jobNumber = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_jobNumber.setObjectName("lineEdit_jobNumber")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_jobNumber)
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_title.setObjectName("label_title")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_title)
        self.lineEdit_title = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_title)
        self.label_department = QtWidgets.QLabel(self.centralwidget)
        self.label_department.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_department.setObjectName("label_department")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_department)
        self.lineEdit_department = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_department.setObjectName("lineEdit_department")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_department)
        self.label_customer = QtWidgets.QLabel(self.centralwidget)
        self.label_customer.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_customer.setObjectName("label_customer")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_customer)
        self.lineEdit_customer = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_customer.setObjectName("lineEdit_customer")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_customer)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.pushButton_createOpen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_createOpen.setBaseSize(QtCore.QSize(0, 0))
        self.pushButton_createOpen.setObjectName("pushButton_createOpen")
        self.verticalLayout_2.addWidget(self.pushButton_createOpen)
        MainWindow_MailPrep.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow_MailPrep)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 451, 20))
        self.menubar.setObjectName("menubar")
        self.menu_MailPrep = QtWidgets.QMenu(self.menubar)
        self.menu_MailPrep.setObjectName("menu_MailPrep")
        MainWindow_MailPrep.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow_MailPrep)
        self.statusbar.setObjectName("statusbar")
        MainWindow_MailPrep.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow_MailPrep)
        self.actionQuit.setObjectName("actionQuit")
        self.menu_MailPrep.addAction(self.actionQuit)
        self.menubar.addAction(self.menu_MailPrep.menuAction())

        self.retranslateUi(MainWindow_MailPrep)
        QtCore.QObject.connect(self.lineEdit_jobNumber, QtCore.SIGNAL("returnPressed()"), self.lineEdit_title.setFocus)
        QtCore.QObject.connect(self.lineEdit_title, QtCore.SIGNAL("returnPressed()"), self.lineEdit_department.setFocus)
        QtCore.QObject.connect(self.lineEdit_department, QtCore.SIGNAL("returnPressed()"), self.lineEdit_customer.setFocus)
        QtCore.QObject.connect(self.lineEdit_customer, QtCore.SIGNAL("returnPressed()"), self.pushButton_createOpen.setFocus)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_MailPrep)

    def retranslateUi(self, MainWindow_MailPrep):
        MainWindow_MailPrep.setWindowTitle(QtWidgets.QApplication.translate("MainWindow_MailPrep", "Mail Prep", None, -1))
        self.label_jobNumber.setText(QtWidgets.QApplication.translate("MainWindow_MailPrep", "Job Number", None, -1))
        self.label_title.setText(QtWidgets.QApplication.translate("MainWindow_MailPrep", "Title", None, -1))
        self.label_department.setText(QtWidgets.QApplication.translate("MainWindow_MailPrep", "Department", None, -1))
        self.label_customer.setText(QtWidgets.QApplication.translate("MainWindow_MailPrep", "Customer", None, -1))
        self.pushButton_createOpen.setText(QtWidgets.QApplication.translate("MainWindow_MailPrep", "Create / Open", None, -1))
        self.menu_MailPrep.setTitle(QtWidgets.QApplication.translate("MainWindow_MailPrep", "File", None, -1))
        self.actionQuit.setText(QtWidgets.QApplication.translate("MainWindow_MailPrep", "Quit", None, -1))

