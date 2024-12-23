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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)
import ui.resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(996, 768)
        MainWindow.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(166, 174, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"font: 9pt \"Microsoft YaHei UI\";")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMaximumSize(QSize(65536, 65536))
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setObjectName(u"loginButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
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

        self.verticalLayout.addWidget(self.loginButton)

        self.fileButton = QPushButton(self.centralwidget)
        self.fileButton.setObjectName(u"fileButton")
        sizePolicy.setHeightForWidth(self.fileButton.sizePolicy().hasHeightForWidth())
        self.fileButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.fileButton)

        self.sideButton = QPushButton(self.centralwidget)
        self.sideButton.setObjectName(u"sideButton")
        sizePolicy.setHeightForWidth(self.sideButton.sizePolicy().hasHeightForWidth())
        self.sideButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.sideButton)

        self.pushButton_recommend = QPushButton(self.centralwidget)
        self.pushButton_recommend.setObjectName(u"pushButton_recommend")
        sizePolicy.setHeightForWidth(self.pushButton_recommend.sizePolicy().hasHeightForWidth())
        self.pushButton_recommend.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_recommend)

        self.costumerButton = QPushButton(self.centralwidget)
        self.costumerButton.setObjectName(u"costumerButton")
        sizePolicy.setHeightForWidth(self.costumerButton.sizePolicy().hasHeightForWidth())
        self.costumerButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.costumerButton)

        self.listWidget_customer = QListWidget(self.centralwidget)
        self.listWidget_customer.setObjectName(u"listWidget_customer")
        self.listWidget_customer.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidget_customer.sizePolicy().hasHeightForWidth())
        self.listWidget_customer.setSizePolicy(sizePolicy1)
        self.listWidget_customer.setMinimumSize(QSize(80, 0))
        self.listWidget_customer.setMaximumSize(QSize(80, 584))

        self.verticalLayout.addWidget(self.listWidget_customer)

        self.productButton = QPushButton(self.centralwidget)
        self.productButton.setObjectName(u"productButton")
        sizePolicy.setHeightForWidth(self.productButton.sizePolicy().hasHeightForWidth())
        self.productButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.productButton)

        self.label_parsestate = QLabel(self.centralwidget)
        self.label_parsestate.setObjectName(u"label_parsestate")

        self.verticalLayout.addWidget(self.label_parsestate)

        self.listWidget_product = QListWidget(self.centralwidget)
        self.listWidget_product.setObjectName(u"listWidget_product")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.listWidget_product.sizePolicy().hasHeightForWidth())
        self.listWidget_product.setSizePolicy(sizePolicy2)
        self.listWidget_product.setMinimumSize(QSize(80, 0))
        self.listWidget_product.setMaximumSize(QSize(80, 16777215))

        self.verticalLayout.addWidget(self.listWidget_product)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.rec_lineEdit = QLineEdit(self.centralwidget)
        self.rec_lineEdit.setObjectName(u"rec_lineEdit")

        self.gridLayout.addWidget(self.rec_lineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.sender_lineEdit = QLineEdit(self.centralwidget)
        self.sender_lineEdit.setObjectName(u"sender_lineEdit")

        self.gridLayout.addWidget(self.sender_lineEdit, 1, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.subject_lineEdit = QLineEdit(self.centralwidget)
        self.subject_lineEdit.setObjectName(u"subject_lineEdit")

        self.gridLayout.addWidget(self.subject_lineEdit, 2, 1, 1, 1)

        self.horizontalLayout_attachment = QHBoxLayout()
        self.horizontalLayout_attachment.setObjectName(u"horizontalLayout_attachment")

        self.gridLayout.addLayout(self.horizontalLayout_attachment, 3, 1, 1, 1)

        self.body_textEdit = QTextEdit(self.centralwidget)
        self.body_textEdit.setObjectName(u"body_textEdit")
        self.body_textEdit.setStyleSheet(u"")

        self.gridLayout.addWidget(self.body_textEdit, 4, 0, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.generateButton = QPushButton(self.centralwidget)
        self.generateButton.setObjectName(u"generateButton")

        self.horizontalLayout.addWidget(self.generateButton)

        self.sendButton = QPushButton(self.centralwidget)
        self.sendButton.setObjectName(u"sendButton")

        self.horizontalLayout.addWidget(self.sendButton)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 1, 1)

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
        self.pushButton_recommend.setText(QCoreApplication.translate("MainWindow", u"AI\u63a8\u8350", None))
        self.costumerButton.setText(QCoreApplication.translate("MainWindow", u"\u5ba2\u6237\u8be6\u60c5", None))
        self.productButton.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u9669\u8be6\u60c5", None))
        self.label_parsestate.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6536\u4ef6\u4eba", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u4ef6\u4eba", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898", None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u90ae\u4ef6", None))
        self.sendButton.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u90ae\u4ef6", None))
    # retranslateUi

