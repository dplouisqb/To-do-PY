from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To Do List")
        self.resize(600, 800)

        # 清單
        self.pending_tasks = []   # 待完成的任務清單
        self.completed_tasks = [] # 已完成的任務清單

        # 元件：標籤、輸入框、按鈕
        self.task_list = QLabel()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Input task...")
        self.add_button = QPushButton("New task")
        self.complete_button = QPushButton("Done!")
        self.delete_button = QPushButton("Delete")
        self.show_completed_button = QPushButton("Show completed task")

        # 設定佈局
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.show_completed_button)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("To do list"))
        layout.addWidget(self.task_list)
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 事件連接
        self.add_button.clicked.connect(self.add_task)
        self.complete_button.clicked.connect(self.complete_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.show_completed_button.clicked.connect(self.show_completed_tasks)

    def add_task(self):
        title = self.task_input.text().strip()
        if not title:
            QMessageBox.warning(self, "警告", "任務名稱不可為空！")
            return

        self.pending_tasks.append({"title": title, "description": None})
        self.task_list.addItem(title)
        self.task_input.clear()

    def complete_task(self):
        current_row = self.task_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "請選擇一個任務！")
            return

        task = self.pending_tasks.pop(current_row)
        self.completed_tasks.append(task)
        self.task_list.takeItem(current_row)
        QMessageBox.information(self, "通知", f"已完成任務：{task['title']}")

    def delete_task(self):
        current_row = self.task_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "請選擇一個任務！")
            return

        task = self.pending_tasks.pop(current_row)
        self.task_list.takeItem(current_row)
        QMessageBox.information(self, "通知", f"已刪除任務：{task['title']}")

    def show_completed_tasks(self):
        if not self.completed_tasks:
            QMessageBox.information(self, "通知", "目前沒有已完成的任務。")
            return

        completed_titles = "\n".join([task['title'] for task in self.completed_tasks])
        QMessageBox.information(self, "已完成任務", f"已完成的任務：\n\n{completed_titles}")

# 主程式入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
