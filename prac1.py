import sys
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 基本 GUI")
        self.resize(400, 300)

        # 建立標籤與按鈕
        self.label = QLabel("按下按鈕開始計數！", self)
        self.button = QPushButton("點擊我", self)

        # 計數變數
        self.counter = 0

        # 設定佈局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 連接按鈕點擊事件
        self.button.clicked.connect(self.increment_counter)
        self.button.clicked.connect(self.counter_limiter)

    def increment_counter(self):
        self.counter += 1
        self.label.setText(f"按鈕已被點擊 {self.counter} 次！")

    def counter_limiter(self):
        if self.counter >= 10:
            self.label.setText(f"點擊次數超過 10！")

# 主程式入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())