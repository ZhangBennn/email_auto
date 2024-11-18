# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)
import ui.resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1006, 768)
        MainWindow.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(166, 174, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"font: 9pt \"Microsoft YaHei UI\";")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.leftButtonLayout = QVBoxLayout()
        self.leftButtonLayout.setObjectName(u"leftButtonLayout")
        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setObjectName(u"loginButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setStyleSheet(u"image: url(:/left/img/logo_init.png);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:10px")
        icon = QIcon()
        icon.addFile(u":/left/img/logo_init.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.loginButton.setIcon(icon)
        self.loginButton.setIconSize(QSize(64, 64))

        self.leftButtonLayout.addWidget(self.loginButton)

        self.fileButton = QPushButton(self.centralwidget)
        self.fileButton.setObjectName(u"fileButton")

        self.leftButtonLayout.addWidget(self.fileButton)

        self.sideButton = QPushButton(self.centralwidget)
        self.sideButton.setObjectName(u"sideButton")

        self.leftButtonLayout.addWidget(self.sideButton)

        self.costumerButton = QPushButton(self.centralwidget)
        self.costumerButton.setObjectName(u"costumerButton")

        self.leftButtonLayout.addWidget(self.costumerButton)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy1)
        self.listWidget.setMinimumSize(QSize(80, 0))
        self.listWidget.setMaximumSize(QSize(80, 584))

        self.leftButtonLayout.addWidget(self.listWidget)


        self.mainLayout.addLayout(self.leftButtonLayout)

        self.contentLayout = QVBoxLayout()
        self.contentLayout.setObjectName(u"contentLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.sender_lineEdit = QLineEdit(self.centralwidget)
        self.sender_lineEdit.setObjectName(u"sender_lineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sender_lineEdit)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.subject_lineEdit = QLineEdit(self.centralwidget)
        self.subject_lineEdit.setObjectName(u"subject_lineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.subject_lineEdit)

        self.rec_lineEdit = QLineEdit(self.centralwidget)
        self.rec_lineEdit.setObjectName(u"rec_lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.rec_lineEdit)

        self.body_textEdit = QTextEdit(self.centralwidget)
        self.body_textEdit.setObjectName(u"body_textEdit")
        self.body_textEdit.setStyleSheet(u"")

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.body_textEdit)


        self.contentLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.generateButton = QPushButton(self.centralwidget)
        self.generateButton.setObjectName(u"generateButton")

        self.horizontalLayout.addWidget(self.generateButton)

        self.sendButton = QPushButton(self.centralwidget)
        self.sendButton.setObjectName(u"sendButton")

        self.horizontalLayout.addWidget(self.sendButton)


        self.contentLayout.addLayout(self.horizontalLayout)


        self.mainLayout.addLayout(self.contentLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u90ae\u4ef6\u7ba1\u7406\u7cfb\u7edf", None))
        self.loginButton.setText("")
        self.fileButton.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8\u6587\u4ef6", None))
        self.sideButton.setText(QCoreApplication.translate("MainWindow", u"\u989d\u5916\u4fe1\u606f", None))
        self.costumerButton.setText(QCoreApplication.translate("MainWindow", u"\u5ba2\u6237\u8be6\u60c5", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6536\u4ef6\u4eba", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u4ef6\u4eba", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898", None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u90ae\u4ef6", None))
        self.sendButton.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u90ae\u4ef6", None))
    # retranslateUi

