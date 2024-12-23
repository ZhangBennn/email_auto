# 导入sys
import sys

# 任何一个PySide界面程序都需要使用QApplication
# 我们要展示一个普通的窗口，所以需要导入QWidget，用来让我们自己的类继承
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QVBoxLayout, QPushButton, QDialog, QTextEdit
from PySide6.QtWidgets import QLabel, QLineEdit, QGridLayout, QHBoxLayout, QWidget, QFileDialog, QFormLayout, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, QThreadPool, Signal, QThread, QEvent, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QListWidgetItem
# 导入我们生成的界面
from ui.main_ui import Ui_MainWindow
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from EmailAI import generate_email_client
import pandas as pd
import re
import csv
import os
import json
from zhipuai import ZhipuAI
from ParseFileAI import get_summary_of_pdf_client
import shutil
from RecommedAI import recommend_insurance_products

# 定义全局变量来存储信息
global_addInfo = ''


# 状态变量，用于控制显示哪个界面
show_credentials_page = True
global_customer_data_path = "./customer_data/customer_details_excel.csv"


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户登录")
        self.setFixedSize(300, 200)

        # 创建控件
        self.label_username = QLabel("用户名:")
        self.label_account = QLabel("邮箱账号:")
        self.label_phonenum = QLabel("电话:")
        self.label_password = QLabel("邮箱密码:")
        self.label_apikey = QLabel("API Key:")

        self.input_username = QLineEdit()
        self.input_account = QLineEdit()
        self.input_phonenum = QLineEdit()
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)  # 密码模式
        self.input_apikey = QLineEdit()
        self.input_apikey.setEchoMode(QLineEdit.Password)  # 密码模式

        self.button_ok = QPushButton("确定")
        self.button_ok.setEnabled(False)

        self.button_cancel = QPushButton("取消")

        # 布局设置
        layout = QGridLayout()
        layout.addWidget(self.label_username, 0, 0)
        layout.addWidget(self.input_username, 0, 1)
        layout.addWidget(self.label_account, 1, 0)
        layout.addWidget(self.input_account, 1, 1)
        layout.addWidget(self.label_phonenum, 2, 0)
        layout.addWidget(self.input_phonenum, 2, 1)
        layout.addWidget(self.label_password, 3, 0)
        layout.addWidget(self.input_password, 3, 1)
        layout.addWidget(self.label_apikey, 4, 0)
        layout.addWidget(self.input_apikey, 4, 1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_ok)
        button_layout.addWidget(self.button_cancel)

        layout.addLayout(button_layout, 5, 0, 1, 2)
        self.setLayout(layout)
        
        # 信号与槽
        self.input_username.textChanged.connect(self.check_inputs)
        self.input_account.textChanged.connect(self.check_inputs)
        self.input_phonenum.textChanged.connect(self.check_inputs)
        self.input_password.textChanged.connect(self.check_inputs)
        self.input_apikey.textChanged.connect(self.check_inputs)

        # 信号与槽
        self.button_ok.clicked.connect(self.accept)  # 点击确定关闭窗口
        self.button_cancel.clicked.connect(self.reject)  # 点击取消关闭窗口
    
    def check_inputs(self):
        """检查所有输入框是否填写内容"""
        if (
            self.input_username.text().strip()
            and self.input_account.text().strip()
            and self.input_phonenum.text().strip()
            and self.input_password.text().strip()
            and self.input_apikey.text().strip()
        ):
            self.button_ok.setEnabled(True)
        else:
            self.button_ok.setEnabled(False)

class AttachmentRow(QWidget):
    def __init__(self, attachment_name):
        super().__init__()
        self.attachment_name = attachment_name
        self.layout = QHBoxLayout(self)

        # 显示附件名称
        self.label = QLabel(attachment_name)
        self.layout.addWidget(self.label)

        # 创建删除按钮
        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.setVisible(False)  # 初始时不显示删除按钮
        self.layout.addWidget(self.delete_button)

    def enterEvent(self, event: QEvent):
        # 当鼠标进入附件区域时，显示删除按钮
        self.delete_button.setVisible(True)

    def leaveEvent(self, event: QEvent):
        # 当鼠标离开附件区域时，隐藏删除按钮
        self.delete_button.setVisible(False)
        
# class DetailsDialog(QDialog):
#     def __init__(self, title_name, data):
#         super().__init__()
#         self.setWindowTitle(title_name)
#         self.setGeometry(100, 100, 400, 300)

#         # 客户详细信息
#         details = "\n".join(f"{key}: {value}" for key, value in data.items())
#         label = QLabel(details)
#         label.setWordWrap(True)

#         layout = QVBoxLayout()
#         layout.addWidget(label)
#         self.setLayout(layout)

class DetailsDialog(QDialog):
    def __init__(self, title_name, data):
        super().__init__()
        self.setWindowTitle(title_name)
        self.setGeometry(100, 100, 600, 400)

        # 存储原始数据
        self.data = data

        # 创建主布局
        layout = QVBoxLayout()

        # 将数据转换为文本，方便显示在 QTextEdit 中
        details = "\n".join(f"{key}: {value}" for key, value in data.items())

        # 创建一个 QTextEdit 用于显示和编辑数据
        self.text_edit = QTextEdit(details)
        self.text_edit.setPlainText(details)  # 初始显示文本
        layout.addWidget(self.text_edit)

        # 保存按钮
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        # 设置布局
        self.setLayout(layout)

    def save_data(self):
        """保存编辑的数据"""
        # 获取用户在 QTextEdit 中修改后的文本
        edited_text = self.text_edit.toPlainText()

        # 将修改后的文本重新转换为字典格式（假设是简单的键值对文本）
        new_data = {}
        for line in edited_text.split("\n"):
            if ": " in line:  # 确保每行格式为 "key: value"
                key, value = line.split(": ", 1)
                new_data[key.strip()] = value.strip()

        # 更新数据字典
        self.data.update(new_data)

        # 在这里你可以选择将更新的数据保存到文件、数据库等
        print("保存的数据:", self.data)

        # 关闭对话框
        self.accept()

class LargeTextDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("输入prompt")
        self.setGeometry(100, 100, 600, 400)

        # 布局与控件
        layout = QVBoxLayout()
        self.textEdit = QTextEdit(self)
        self.confirmButton = QPushButton("确定", self)
        self.confirmButton.clicked.connect(self.confirm_text)

        # 布局添加
        layout.addWidget(self.textEdit)
        layout.addWidget(self.confirmButton)
        self.setLayout(layout)

    def confirm_text(self):
        text = self.textEdit.toPlainText()
        global global_addInfo
        global_addInfo = text
        self.accept()  # 关闭对话框

def send_email(sender_email, sender_password, recipient, subject, body):
    # 创建消息对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'html'))

    # 选择要添加的附件文件
    attachment_filename = "insurance/“区块链”重点专项2024年度项目申报指南.pdf"  # 附件文件路径
    try:
        # 打开附件文件并读取
        with open(attachment_filename, "rb") as attachment_file:
            # 创建一个MIMEBase对象并设置附件内容
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(attachment_file.read())

            # 对附件内容进行Base64编码
            encoders.encode_base64(attachment)

            # 添加附件头信息
            attachment.add_header('Content-Disposition', 'attachment', filename=attachment_filename)

            # 将附件添加到邮件中
            msg.attach(attachment)

        # 连接到SMTP服务器并发送邮件
        with smtplib.SMTP('smtp.qq.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("Email sent successfully!")
    except Exception as e:
        return f"Error: {str(e)}"

class EmailThread(QThread):
    # 定义一个信号，用于发送生成的邮件内容和主题
    email_generated = Signal(str, str)

    def __init__(self, client, sender_info, customer_data_str, product_info, addtion_info=''):
        super().__init__()
        self.client = client
        self.sender_info = sender_info
        self.customer_data_str = customer_data_str
        self.product_info = product_info
        self.addtion_info = addtion_info

    def run(self):
        # 执行耗时的操作
        body = generate_email_client(self.client, self.sender_info, self.customer_data_str, self.product_info, self.addtion_info)[8:-3]
        subject = re.search(r'<title>(.*?)</title>', body, re.IGNORECASE | re.DOTALL).group(1)
        # 发送信号，包含邮件内容和主题
        self.email_generated.emit(body, subject)

class ParseFileThread(QThread):
    # 定义一个信号，用于发送生成的邮件内容和主题
    process = Signal(str)

    def __init__(self, client, file_dir, file_path=None):
        super().__init__()
        self.client = client
        self.file_dir = file_dir
        self.file_path = file_path

    def run(self):
        # 执行耗时的操作
        if self.file_path is None:
            for file_name in sorted(os.listdir(self.file_dir)):
                if file_name.endswith('.pdf'):
                    json_path = os.path.join(self.file_dir, file_name[:-4] + '.json')
                    if os.path.exists(json_path):
                        # file_json = json.load(open(os.path.join(self.file_dir, file_name[:-4] + '.json'), 'r', encoding='utf-8'))
                        self.process.emit(file_name)
                    else:
                        try:
                            parse_failed = 1
                            while parse_failed:
                                # print(file_name)
                                response = get_summary_of_pdf_client(self.client, os.path.join(self.file_dir, file_name))
                                # 解析响应结果
                                # print("####################################################")
                                file_json = eval(str(response.choices[0].message).split('```')[1].replace('json\\n','').replace('\\n',''))
                                # 发送信号，包含邮件内容和主题
                                # print("####################################################")
                                # print(file_json)
                                # print("####################################################")
                                with open(json_path, 'w', encoding='utf-8') as file:
                                    json.dump(file_json, file, ensure_ascii=False, indent=4)
                                self.process.emit(file_name)
                                parse_failed = 0
                        except Exception as e:
                            print(f"Error processing file {file_name}: {e}")
        else:
            try:
                json_path = self.file_path[:-4] + '.json'
                response = get_summary_of_pdf_client(self.client, self.file_path)
                # 解析响应结果
                # print("####################################################")
                file_json = eval(str(response.choices[0].message).split('```')[1].replace('json\\n','').replace('\\n',''))
                # 发送信号，包含邮件内容和主题
                # print("####################################################")
                # print(file_json)
                # print("####################################################")
                with open(json_path, 'w', encoding='utf-8') as file:
                    json.dump(file_json, file, ensure_ascii=False, indent=4)
                self.process.emit(os.path.basename(self.file_path))
     
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

class RecommendThread(QThread):
    # 定义一个信号，用于发送生成的邮件内容和主题
    process = Signal(str)

    def __init__(self, client, customer_info, file_path):
        super().__init__()
        self.client = client
        self.file_path = file_path
        self.customer_info = customer_info

    def run(self):
        # 执行耗时的操作
        recommed_info = recommend_insurance_products(self.client, self.customer_info, self.file_path)
        # 发送信号，包含邮件内容和主题
        self.process.emit(recommed_info)

# 继承QWidget类，以获取其属性和方法
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.default_csv_path = "./customer_data/customer_details_excel.csv"
        self.default_product_path = "./insurance"
        # 设置界面为我们生成的界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.login_ok = False
        self.file_ok = True
        self.customer_ok = False
        self.email_thread = None
        self.attachments = []
        self.parsestate = {
            "total": 0,
            "success": 0,
        }

        # self.web_view = QWebEngineView(self.ui)
        self.login_dialog = LoginDialog()

        #login
        self.ui.loginButton.clicked.connect(self.show_login_dialog)
        # 左侧客户列表
        self.costomer_details_button = self.ui.costumerButton
        self.costomer_details_button.clicked.connect(self.show_customer_details_dialog)
        self.costomer_details_button.setEnabled(False)

        self.customer_list = self.ui.listWidget_customer
        self.customer_list.itemClicked.connect(self.select_customer)
        self.load_customer_file()

        # 左侧产品列表
        self.product_details_button = self.ui.productButton
        self.product_details_button.clicked.connect(self.show_product_details_dialog)
        # self.product_details_button.setEnabled(False)

        self.product_list = self.ui.listWidget_product
        self.product_list.itemClicked.connect(self.select_product)

        #读取文件
        self.ui.fileButton.clicked.connect(self.read_file_dialog)
        # 绑定按钮点击事件
        self.ui.sideButton.clicked.connect(self.show_large_text_dialog)

        self.ui.pushButton_recommend.clicked.connect(self.recommed)
        self.ui.pushButton_recommend.setEnabled(False)

        self.ui.generateButton.clicked.connect(self.generate_email)
        self.ui.generateButton.setEnabled(False)

        self.ui.sendButton.clicked.connect(self.send_email)
        self.ui.sendButton.setEnabled(False)

        self.ui.body_textEdit.textChanged.connect(self.check_emailBody)
    
    def check_emailBody(self):
        """检查所有输入框是否填写内容"""
        if (
            self.ui.body_textEdit.toHtml().strip()
            and self.login_ok 
            and self.file_ok
        ):
            # self.body = self.ui.body_textEdit.toHtml()
            # self.web_view.setHtml(self.body)
            self.ui.sendButton.setEnabled(True)
        else:
            self.ui.sendButton.setEnabled(False)

    def show_login_dialog(self):
        if self.login_dialog.exec_() == QDialog.Accepted:  # 接受输入后
            self.username = self.login_dialog.input_username.text()
            self.account = self.login_dialog.input_account.text()
            self.phonenum = self.login_dialog.input_phonenum.text()
            self.password = self.login_dialog.input_password.text()
            self.apikey = self.login_dialog.input_apikey.text()
            
            sender_show = f'<{self.username}>' + self.account
            self.ui.sender_lineEdit.setText(sender_show)

            icon = QIcon()
            icon.addFile(u":/left/img/logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.ui.loginButton.setIcon(icon)
            self.ui.loginButton.setIconSize(QSize(64, 64))

            if self.apikey:
                self.email_client = ZhipuAI(api_key=self.apikey) # 填写您自己的APIKey
                self.parsefile_client = ZhipuAI(api_key=self.apikey)
                self.recommend_client = ZhipuAI(api_key=self.apikey)
                # get_summary_of_pdf_client(self.parsefile_client, 'D:/work/pm_hw/email_auto/insurance/安盛天平个人意外伤害保险.pdf')
                self.load_product_file()

            if self.ui.body_textEdit.toHtml().strip() and self.file_ok and self.customer_ok:
                self.ui.sendButton.setEnabled(True)

            if self.file_ok and self.customer_ok:
                self.ui.generateButton.setEnabled(True)
            self.login_ok = True

    def load_customer_file(self):
        """加载客户 CSV 文件"""
        try:
            with open(self.default_csv_path, newline='', encoding='gbk') as csvfile:
                reader = csv.DictReader(csvfile)
                self.customers = list(reader)

            if not self.customers:
                QMessageBox.warning(self, "警告", "文件为空或无有效数据！")
                return

            # 显示客户姓名到侧边栏
            self.customer_list.clear()
            for customer in self.customers:
                self.customer_list.addItem(customer.get("姓名", "未知"))

        except FileNotFoundError:
            QMessageBox.critical(self, "错误", f"未找到文件：{self.default_csv_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载文件时出错：{str(e)}")

    def load_product_file(self):
        """加载客户 CSV 文件"""
        try:
            # with open(self.default_csv_path, newline='', encoding='gbk') as csvfile:
            #     reader = csv.DictReader(csvfile)
            #     self.customers = list(reader)

            # if not self.customers:
            #     QMessageBox.warning(self, "警告", "文件为空或无有效数据！")
            #     return

            # 显示客户姓名到侧边栏
            self.product_list.clear()

            for file_name in sorted(os.listdir(self.default_product_path)):
                if file_name.endswith('.pdf'):
                    # json_path = os.path.join(self.default_product_path, file_name[:-4] + '.json')
                    # if os.path.exists(json_path):
                    #     self.parsestate['success'] += 1
                    self.parsestate['total'] += 1
            self.ui.label_parsestate.setText(f'已解析:{self.parsestate["success"]} / {self.parsestate["total"]}')
            self.ui.label_parsestate.setAlignment(Qt.AlignCenter)
            # 创建并启动线程
            self.parsefile_thread = ParseFileThread(self.parsefile_client, self.default_product_path)
            self.parsefile_thread.process.connect(self.on_file_parsed)
            self.parsefile_thread.finished.connect(self.clean_up_parse_thread)
            self.parsefile_thread.start()


        except FileNotFoundError:
            QMessageBox.critical(self, "错误", f"未找到文件：{self.default_csv_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载文件时出错：{str(e)}")
    
    def remove_attachment(self, row: QWidget):
        # 移除附件行
        row.deleteLater()
        self.attachments.remove(row.attachment_name)

    def select_customer(self, item):
        """选择客户并自动填充发件人字段"""
        customer_name = item.text()
        self.selected_customer = next(
            (customer for customer in self.customers if customer.get("姓名") == customer_name), None
        )

        if self.selected_customer:
            rec_show = f'<{self.selected_customer.get("姓名", "")}>' + f'{self.selected_customer.get("邮箱", "")}'
            self.ui.rec_lineEdit.setText(rec_show)
            self.customer_account = self.selected_customer.get("邮箱", "")
            self.costomer_details_button.setEnabled(True)
            if self.login_ok:
                self.ui.generateButton.setEnabled(True)
            self.ui.pushButton_recommend.setEnabled(True)
            self.customer_ok = True
    
    def select_product(self, item):
        product_name = item.text()
        json_path = os.path.join(self.default_product_path, f'{product_name}.json')
        with open(json_path, 'r', encoding='utf-8') as file:
            self.selected_product = json.load(file)
        self.json_path = json_path
        product = f'{product_name}.pdf'
        if product in self.attachments:
            return
        self.attachments.append(product)
        attachment_row = AttachmentRow(product)
        attachment_row.delete_button.clicked.connect(lambda _, row=attachment_row: self.remove_attachment(row))
        self.ui.horizontalLayout_attachment.addWidget(attachment_row)

        # self.details_button.setEnabled(True)
        # if self.login_ok:
        #     self.ui.generateButton.setEnabled(True)
        #     self.product_ok = True

    def show_customer_details_dialog(self):
        """展示客户详细信息弹窗"""
        if self.selected_customer:
            # 客户详细信息
            dialog = DetailsDialog("客户详细信息", self.selected_customer)
            dialog.exec()
    
    def show_product_details_dialog(self):
        """展示客户详细信息弹窗"""
        if self.selected_product:
            # 客户详细信息
            dialog = DetailsDialog("产品概要信息", self.selected_product)
            dialog.exec()
        with open(self.json_path, 'w', encoding='utf-8') as file:
            json.dump(self.selected_product, file, ensure_ascii=False, indent=4)
    
    def read_file_dialog(self):
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*)")
        if file_path:
            # 检查文件是否已经在目标文件夹中
            target_path= os.path.join(self.default_product_path, os.path.basename(file_path))
            if not os.path.exists(target_path):
                # 如果文件不存在，进行复制
                shutil.copy(file_path, target_path)
                self.parsestate['total'] += 1
                self.ui.label_parsestate.setText(f'已解析:{self.parsestate["success"]} / {self.parsestate["total"]}')
                self.ui.label_parsestate.setAlignment(Qt.AlignCenter)
                # 创建并启动线程
                self.parseonefile_thread = ParseFileThread(self.parsefile_client, self.default_product_path)
                self.parseonefile_thread.process.connect(self.on_file_parsed)
                self.parseonefile_thread.finished.connect(self.clean_up_parseone_thread)
                self.parseonefile_thread.start()

            self.file_ok = True
            if self.ui.body_textEdit.toHtml().strip() and self.login_ok and self.customer_ok:
                self.ui.sendButton.setEnabled(True)
            if self.customer_ok:
                self.ui.generateButton.setEnabled(True)
                self.ui.pushButton_recommend.setEnabled(True)

    def show_large_text_dialog(self):
        global global_addInfo
        dialog = LargeTextDialog()
        dialog.textEdit.setPlainText(global_addInfo)
        dialog.exec()

    def recommed(self):
        if self.customer_ok:
            # 创建 QLabel 控件
            label = QLabel("正在处理中，请稍等...")
            # 可选：设置样式或其他属性
            label.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
            # 添加到布局中
            self.ui.horizontalLayout_attachment.addWidget(label)
            # 创建并启动线程
            self.recommend_thread = RecommendThread(self.recommend_client, self.selected_customer, self.default_product_path)
            self.recommend_thread.process.connect(self.on_recommend)
            self.recommend_thread.finished.connect(self.clean_up_recommend_thread)
            self.recommend_thread.start()
    
    def generate_email(self):
        if self.email_thread and self.email_thread.isRunning():
            QMessageBox.warning(self, "警告", "上一个任务尚未完成！")
            return
        # 在点击生成时，先显示“处理中”提示
        self.ui.body_textEdit.setPlainText("正在处理中，请稍等...")
        self.ui.subject_lineEdit.clear()
        
        self.sender_info = {
            "name":  self.username,
            "电话": self.phonenum,
            "邮箱": self.account,
        }

        row = self.selected_customer
        # 在这里对每一行进行处理
        # 创建一个字符串，包含所有列的信息
        customer_data_str = (
            f"姓名: {row['姓名']}, "
            f"性别: {row['性别']}, "
            f"年龄: {row['年龄']}, "
            f"职业: {row['职业']}, "
            f"婚姻状况: {row['婚姻状况']}, "
            f"子女情况: {row['子女情况']}, "
            f"保险需求: {row['保险需求']}, "
            f"经济状况: {row['经济状况']}, "
            f"兴趣爱好: {row['兴趣爱好']}, "
            f"其他备注: {row['其他备注']}")

        # 显示处理中的状态
        self.ui.body_textEdit.setHtml("处理中，请稍候...")
        self.ui.subject_lineEdit.setText("处理中...")

        global global_addInfo

        #合并附件的产品信息
        product_info = ""
        for i in range(len(self.attachments)):
            json_path = os.path.join(self.default_product_path, self.attachments[i][:-4] + ".json")
            with open(json_path, 'r', encoding='utf-8') as file:
                json_info = json.load(file)
            product_info += str(json_info) + "\n"
        # 创建并启动线程
        self.email_thread = EmailThread(self.email_client, self.sender_info, customer_data_str, product_info, global_addInfo)
        self.email_thread.email_generated.connect(self.on_email_generated)
        self.email_thread.finished.connect(self.clean_up_thread)
        self.email_thread.start()

    def on_email_generated(self, body, subject):
        # 任务完成时，更新 UI
        self.body = body
        self.subject = subject
        self.ui.body_textEdit.setHtml(body)
        self.ui.subject_lineEdit.setText(subject)
    
    def on_file_parsed(self, file_name):
        # 检查列表中是否已经存在这个项
        items = [self.product_list.item(i).text() for i in range(self.product_list.count())]

        if file_name[:-4] not in items:
            file_json = json.load(open(os.path.join(self.default_product_path, file_name[:-4] + '.json'), 'r', encoding='utf-8'))
            #异常用红色表示
            if len(str(file_json)) < 10:
                item_fail = QListWidgetItem(file_name[:-4])  # 创建一个新的列表项
                label = QLabel(file_name[:-4])  # 创建标签并设置文本
                label.setStyleSheet("color: red;")  # 设置标签的文本颜色为红色
                self.product_list.addItem(item_fail)  # 添加项
                self.product_list.setItemWidget(item_fail, label)  # 将标签设置为项的内容
            else:
                self.product_list.addItem(file_name[:-4])
            self.parsestate["success"] += 1
            # 更新解析状态
            self.ui.label_parsestate.setText(f'已解析:{self.parsestate["success"]} / {self.parsestate["total"]}')
            self.ui.label_parsestate.setAlignment(Qt.AlignCenter)
        # 将数据保存为JSON格式的文件
        # file_path = os.path.join(self.default_product_path, file_name[:-4] + ".json")
        # with open(file_path, 'w', encoding='utf-8') as file:
        #     json.dump(data, file, ensure_ascii=False, indent=4)

    def on_recommend(self, recommendation):
        #将推荐产品添加附件中
        recommendation = json.loads(recommendation.replace("'", "\""))
        if not isinstance(recommendation, list):
            return
        self.clear_attachments()
        items = [self.product_list.item(i).text() for i in range(self.product_list.count())]
        for product in recommendation:
            if product in items:
                self.attachments.append(product+'.pdf')
                attachment_row = AttachmentRow(product+'.pdf')
                attachment_row.delete_button.clicked.connect(lambda _, row=attachment_row: self.remove_attachment(row))
                self.ui.horizontalLayout_attachment.addWidget(attachment_row)

    def clear_attachments(self):
        # 清空 attachments 列表
        self.attachments.clear()
        
        # 获取 horizontalLayout_attachment 中的所有子组件
        for i in reversed(range(self.ui.horizontalLayout_attachment.count())):
            widget = self.ui.horizontalLayout_attachment.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # 删除每个子组件

    def send_email(self):
        # 创建消息对象
        msg = MIMEMultipart()
        msg['From'] = self.account
        msg['To'] = self.customer_account
        msg['Subject'] = self.subject

        # 添加邮件正文
        msg.attach(MIMEText(self.body, 'html'))

        # 选择要添加的附件文件
        try:
            # 遍历附件文件列表，添加多个附件
            for attachment_filename in self.attachments:
                attachment_path = os.path.join(self.default_product_path, attachment_filename)
                if os.path.exists(attachment_path):  # 检查附件文件是否存在
                    # 打开附件文件并读取
                    with open(attachment_path, "rb") as attachment_file:
                        # 创建一个MIMEBase对象并设置附件内容
                        attachment = MIMEBase('application', 'octet-stream')
                        attachment.set_payload(attachment_file.read())

                        # 对附件内容进行Base64编码
                        encoders.encode_base64(attachment)

                        # 添加附件头信息
                        attachment.add_header('Content-Disposition', 'attachment', filename=attachment_filename)

                        # 将附件添加到邮件中
                        msg.attach(attachment)
                else:
                    print(f"附件 {attachment_filename} 不存在！")

            # 连接到SMTP服务器并发送邮件
            with smtplib.SMTP('smtp.qq.com', 587) as server:
                server.starttls()
                server.login(self.account, self.password)
                server.send_message(msg)
                server.quit()
                QMessageBox.information(self, "成功", "发送成功！")

        except Exception as e:
            QMessageBox.critical(self, "发送失败",f"Error: {str(e)}")
    
    def clear_attachment_layout(self):
        # 遍历 horizontalLayout_attachment 中的所有控件
        for i in reversed(range(self.ui.horizontalLayout_attachment.count())):
            widget = self.ui.horizontalLayout_attachment.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # 删除每个控件

    def clean_up_recommend_thread(self):
        self.recommend_thread = None

    def clean_up_parse_thread(self):
        self.parsefile_thread = None

    def clean_up_parseone_thread(self):
        self.parseonefile_thread = None

    def clean_up_thread(self):
        self.email_thread = None

    def closeEvent(self, event):
        if self.email_thread and self.email_thread.isRunning():
            self.email_thread.quit()
            self.email_thread.wait()
        super().closeEvent(event)
        
# 程序入口
if __name__ == "__main__":
    # 初始化QApplication，界面展示要包含在QApplication初始化之后，结束之前
    app = QApplication(sys.argv)
 
    # 初始化并展示我们的界面组件
    window = MyWidget()
    window.show()
    
    # 结束QApplication
    sys.exit(app.exec())
