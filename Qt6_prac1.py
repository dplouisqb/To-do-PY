import sys
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Click!")
        self.resize(400, 300)

        # 建立標籤與按鈕
        self.label = QLabel("Start！", self)
        self.button_cnt = QPushButton("Click here", self)
        self.button_rst = QPushButton("Reset", self)

        # 計數變數
        self.counter = 0

        # 設定佈局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_rst)
        layout.addWidget(self.button_cnt)
        self.setLayout(layout)

        # 連接按鈕點擊事件
        self.button_cnt.clicked.connect(self.increment_counter)
        self.button_cnt.clicked.connect(self.counter_limiter)
        self.button_rst.clicked.connect(self.counter_reset)

    def increment_counter(self):
        self.counter += 1
        self.label.setText(f"Click {self.counter} times！")

    def counter_limiter(self):
        if self.counter >= 10:
            self.label.setText(f"Click over 10 times！")

    def counter_reset(self):
        self.counter = 0
        self.label.setText(f"Reset!")

# 主程式入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())