from PySide6.QtWidgets import QApplication, QMainWindow, QTextBrowser, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML 显示和编辑模式切换")
        
        # 主布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # QTextBrowser: 用于显示HTML
        self.text_browser = QTextBrowser()
        self.text_browser.setHtml("<h1>HTML 内容</h1><p>双击这里切换到编辑模式。</p>")
        self.text_browser.setOpenExternalLinks(True)  # 支持外部链接
        self.text_browser.setStyleSheet("border: 1px solid gray;")
        
        # QTextEdit: 用于编辑HTML
        self.text_edit = QTextEdit()
        self.text_edit.hide()  # 初始隐藏
        self.text_edit.setStyleSheet("border: 1px solid gray;")
        
        # 添加到布局
        self.layout.addWidget(self.text_browser)
        self.layout.addWidget(self.text_edit)
        
        # 绑定信号
        self.text_browser.installEventFilter(self)
        self.text_edit.focusOutEvent = self.on_edit_focus_out

    def eventFilter(self, source, event):
        # 确保事件是有效的
        if source == self.text_browser:
            self.switch_to_edit_mode()
            return True
        return super().eventFilter(source, event)
    
    def switch_to_edit_mode(self):
        """切换到编辑模式"""
        self.text_browser.hide()
        self.text_edit.setText(self.text_browser.toHtml())
        self.text_edit.show()
        self.text_edit.setFocus()
    
    def switch_to_view_mode(self):
        """切换到显示模式"""
        self.text_edit.hide()
        self.text_browser.setHtml(self.text_edit.toPlainText())
        self.text_browser.show()
    
    def on_edit_focus_out(self, event):
        """当 QTextEdit 失去焦点时切换回显示模式"""
        self.switch_to_view_mode()
        super(QTextEdit, self.text_edit).focusOutEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    app.exec()
