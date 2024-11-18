# 导入sys
import sys

# 任何一个PySide界面程序都需要使用QApplication
# 我们要展示一个普通的窗口，所以需要导入QWidget，用来让我们自己的类继承
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QVBoxLayout, QPushButton, QDialog, QTextEdit
from PySide6.QtWidgets import QLabel, QLineEdit, QGridLayout, QHBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, QThreadPool, Signal, QThread
from PySide6.QtWebEngineWidgets import QWebEngineView
# 导入我们生成的界面
from ui.main_ui import Ui_MainWindow
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailAI import generate_email
import pandas as pd
import re
import csv

# 定义全局变量来存储信息
global_addInfo = None


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
        self.label_password = QLabel("邮箱密码:")
        self.label_apikey = QLabel("API Key:")

        self.input_username = QLineEdit()
        self.input_account = QLineEdit()
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
        layout.addWidget(self.label_password, 2, 0)
        layout.addWidget(self.input_password, 2, 1)
        layout.addWidget(self.label_apikey, 3, 0)
        layout.addWidget(self.input_apikey, 3, 1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_ok)
        button_layout.addWidget(self.button_cancel)

        layout.addLayout(button_layout, 4, 0, 1, 2)
        self.setLayout(layout)
        
        # 信号与槽
        self.input_username.textChanged.connect(self.check_inputs)
        self.input_account.textChanged.connect(self.check_inputs)
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
            and self.input_password.text().strip()
            and self.input_apikey.text().strip()
        ):
            self.button_ok.setEnabled(True)
        else:
            self.button_ok.setEnabled(False)

class CustomerDetailsDialog(QDialog):
    def __init__(self, customer):
        super().__init__()
        self.setWindowTitle("客户详细信息")
        self.setGeometry(100, 100, 400, 300)

        # 客户详细信息
        details = "\n".join(f"{key}: {value}" for key, value in customer.items())
        label = QLabel(details)
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

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

    try:
        # 连接到 SMTP 服务器
        server = smtplib.SMTP('smtp.qq.com', 587)
        server.starttls()

        # 登录到你的邮箱
        server.login(sender_email, sender_password)

        # 发送邮件
        server.send_message(msg)
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

class EmailThread(QThread):
    # 定义一个信号，用于发送生成的邮件内容和主题
    email_generated = Signal(str, str)

    def __init__(self, apikey, sender_info, customer_data_str, addtion_info):
        super().__init__()
        self.apikey = apikey
        self.sender_info = sender_info
        self.customer_data_str = customer_data_str
        self.addtion_info = addtion_info

    def run(self):
        # 执行耗时的操作
        body = generate_email(self.apikey, self.sender_info, self.customer_data_str, self.addtion_info)[8:-3]
        subject = re.search(r'<title>(.*?)</title>', body, re.IGNORECASE | re.DOTALL).group(1)
        # 发送信号，包含邮件内容和主题
        self.email_generated.emit(body, subject)

# 继承QWidget类，以获取其属性和方法
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.default_csv_path = "./customer_data/customer_details_excel.csv"
        # 设置界面为我们生成的界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.login_ok = False
        self.file_ok = True
        self.customer_ok = False
        self.email_thread = None

        # self.web_view = QWebEngineView(self.ui)
        
        #login
        self.ui.loginButton.clicked.connect(self.show_login_dialog)
        # 左侧客户列表
        self.details_button = self.ui.costumerButton
        self.details_button.clicked.connect(self.show_details_dialog)
        self.details_button.setEnabled(False)

        self.customer_list = self.ui.listWidget
        self.customer_list.itemClicked.connect(self.select_customer)
        self.load_customer_file()

        #读取文件
        self.ui.fileButton.clicked.connect(self.read_file_dialog)
        # 绑定按钮点击事件
        self.ui.sideButton.clicked.connect(self.show_large_text_dialog)

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
        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:  # 接受输入后
            self.username = login_dialog.input_username.text()
            self.account = login_dialog.input_account.text()
            self.password = login_dialog.input_password.text()
            self.apikey = login_dialog.input_apikey.text()
            
            sender_show = f'<{self.username}>' + self.account
            self.ui.sender_lineEdit.setText(sender_show)

            icon = QIcon()
            icon.addFile(u":/left/img/logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.ui.loginButton.setIcon(icon)
            self.ui.loginButton.setIconSize(QSize(64, 64))

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
            self.details_button.setEnabled(True)
            self.customer_ok = True

    def show_details_dialog(self):
        """展示客户详细信息弹窗"""
        if self.selected_customer:
            # 客户详细信息
            dialog = CustomerDetailsDialog(self.selected_customer)
            dialog.exec()
    
    def read_file_dialog(self):
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*)")
        if file_path:
            self.file_ok = True
            if self.ui.body_textEdit.toHtml().strip() and self.login_ok and self.customer_ok:
                self.ui.sendButton.setEnabled(True)
            if self.customer_ok:
                self.ui.generateButton.setEnabled(True)
            # 如果需要读取文件内容，可以在这里处理
            with open(file_path, "r", encoding="utf-8") as file:
                self.file_content = file.read()

    def show_large_text_dialog(self):
        global global_addInfo
        dialog = LargeTextDialog()
        dialog.textEdit.setPlainText(global_addInfo)
        dialog.exec()


    def generate_email(self):
        if self.email_thread and self.email_thread.isRunning():
            QMessageBox.warning(self, "警告", "上一个任务尚未完成！")
            return
        # 在点击生成时，先显示“处理中”提示
        self.ui.body_textEdit.setPlainText("正在处理中，请稍等...")
        self.ui.subject_lineEdit.clear()
        
        self.sender_info = {
            "name": self.username,
            # "phone": self.phone,
            # "company": self.company,
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
        # 创建并启动线程
        self.email_thread = EmailThread(self.apikey, self.sender_info, customer_data_str, global_addInfo)
        self.email_thread.email_generated.connect(self.on_email_generated)
        self.email_thread.finished.connect(self.clean_up_thread)
        self.email_thread.start()

    def on_email_generated(self, body, subject):
        # 任务完成时，更新 UI
        self.body = body
        self.subject = subject
        self.ui.body_textEdit.setHtml(body)
        self.ui.subject_lineEdit.setText(subject)
    
    def send_email(self):
        # 创建消息对象
        msg = MIMEMultipart()
        msg['From'] = self.account
        msg['To'] = self.customer_account
        msg['Subject'] = self.subject

        # 添加邮件正文
        msg.attach(MIMEText(self.body, 'html'))

        try:
            # 连接到 SMTP 服务器
            server = smtplib.SMTP('smtp.qq.com', 587)
            server.starttls()

            # 登录到你的邮箱
            server.login(self.account, self.password)

            # 发送邮件
            server.send_message(msg)
            server.quit()

            QMessageBox.information(self, "成功", "发送成功！")
        except Exception as e:
            QMessageBox.critical(self, "发送失败",f"Error: {str(e)}")
        
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
