from PyQt6.QtWidgets import (
    QApplication, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QWidget, QMessageBox
)
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Interaction")
        self.resize(400, 300)

        # 元件：標籤、輸入框、按鈕
        self.label = QLabel("Type Text:", self)
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type Here")
        self.display_button = QPushButton("Show Text", self)
        self.reverse_button = QPushButton("Reverse Text", self)
        self.clear_button = QPushButton("Clean Text", self)

        # 設定佈局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.display_button)
        layout.addWidget(self.reverse_button)
        layout.addWidget(self.clear_button)
        self.setLayout(layout)

        # 事件連接
        self.display_button.clicked.connect(self.display_text)
        self.reverse_button.clicked.connect(self.reverse_text)
        self.clear_button.clicked.connect(self.clear_text)

    def display_text(self):
        text = self.input_field.text()
        if len(text) >= 10:
            QMessageBox.warning(self, "Warning", "Text Exceeds Limit!")
        elif text.strip():
            self.label.setText(f"Text：{text}")
        else:
            QMessageBox.warning(self, "Warning", "Text Cannot Be Empty!")

    def clear_text(self):
        self.input_field.clear()
        self.label.setText("Type Text:")

    def reverse_text(self):
        text = self.input_field.text()
        if len(text) >= 10:
            QMessageBox.warning(self, "Warning", "Text Exceeds Limit!")
        elif text.strip():
            reversed_text = text[::-1]
            self.label.setText(f"Result：{reversed_text}")
        else:
            QMessageBox.warning(self, "Warning", "Text Cannot Be Empty!")

# 主程式入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())