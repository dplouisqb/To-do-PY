from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6 import uic
import sys

class UI01(QWidget):
    def __init__(self):
        super().__init__()
        # 載入 UI 文件
        uic.loadUi('D:/dplouisqb/uitest.ui', self)

        # 連接按鈕 quitButton 到退出功能
        self.quitButton.clicked.connect(self.close)

# 主程式
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI01()
    window.show()
    sys.exit(app.exec())