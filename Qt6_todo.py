from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QListWidget, QHBoxLayout
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To Do List")
        self.resize(400, 500)

        # 清單
        self.pending_tasks = []   # 待完成的任務清單
        self.completed_tasks = [] # 已完成的任務清單

        # 元件：標籤、輸入框、按鈕
        self.today_task_list = QListWidget()  # 今日任務清單
        self.completed_task_list = QListWidget()  # 完成任務清單
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Add a task")
        self.add_button = QPushButton("+")
        self.complete_button = QPushButton("Done!")
        self.delete_button = QPushButton("Delete a task")

        # 設定佈局
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.task_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.delete_button)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Today Task:"))
        layout.addWidget(self.today_task_list)
        layout.addWidget(QLabel("Completed Tasks:"))
        layout.addWidget(self.completed_task_list)
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 事件連接
        self.add_button.clicked.connect(self.add_task)
        self.complete_button.clicked.connect(self.complete_task)
        self.delete_button.clicked.connect(self.delete_task)

    def add_task(self):
        title = self.task_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Warning", "Task Name Cannot Be Empty!")
            return

        self.pending_tasks.append({"title": title, "description": None})
        self.today_task_list.addItem(title)
        self.task_input.clear()

    def complete_task(self):
        current_row = self.today_task_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Choose a Task!")
            return

        task = self.pending_tasks.pop(current_row)
        self.completed_tasks.append(task)
        self.today_task_list.takeItem(current_row)
        self.completed_task_list.addItem(task['title'])
        QMessageBox.information(self, "Notice", f"Task Completed: {task['title']}")

    def delete_task(self):
        current_row = self.today_task_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Choose a Task!")
            return

        task = self.pending_tasks.pop(current_row)
        self.today_task_list.takeItem(current_row)
        QMessageBox.information(self, "Notice", f"Task Deleted: {task['title']}")

# 主程式入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
