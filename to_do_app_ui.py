from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem
from PyQt6 import uic
import sys, re

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        # 載入 UI
        uic.loadUi('todo_app.ui', self)

        # 功能

        ## 代辦清單
        self.addButton.clicked.connect(self.add_task)
        self.deleteButton.clicked.connect(self.delete_task)
        self.markCompleteButton.clicked.connect(self.mark_complete)

        ## 購物清單
        self.grocButton.clicked.connect(self.add_groc)
        self.deleteGrocButton.clicked.connect(self.delete_groc)

        ## 雙擊項目來切換圖標
        self.taskList.itemDoubleClicked.connect(self.toggle_task_icon)

        ## 排序按鈕
        self.sortButton_task.clicked.connect(self.toggle_sorting)
        self.sortButton_star.clicked.connect(self.sort_tasks_by_star)

        ## 預設的任務
        self.add_default_tasks()

        ## 排序模式標誌
        self.is_sorted_by_date = False
        self.is_sorted_by_star = False  # 另外一個排序標誌，標誌是否已根據星星排序

    # 代辦清單

    ## 增加任務
    def add_task(self):
        task = self.taskInput.text()
        if self.is_valid_task(task):
            item = QListWidgetItem(task)

            # 預設未標記任務，設置空心星星圖標
            item.setIcon(QIcon("star_empty.jpg"))  # 設置為空心星星圖標
            item.setData(Qt.ItemDataRole.UserRole, "empty")  # 儲存當前狀態為 "empty"

            self.taskList.addItem(item)
            self.taskInput.clear()
        else:
            QMessageBox.warning(self, "Error", "Invalid format. Please enter in the format: (YYYY-MM-DD)/(Task).")

    ## 刪除任務
    def delete_task(self):
        selected_task = self.taskList.currentItem()
        completed_task = self.completedList.currentItem()

        if not selected_task and not completed_task:
            QMessageBox.warning(self, "Error", "No task selected")
            return
        if selected_task:
            self.taskList.takeItem(self.taskList.row(selected_task))
        if completed_task:
            self.completedList.takeItem(self.completedList.row(completed_task))

    ## 完成任務
    def mark_complete(self):
        selected_task = self.taskList.currentItem()
        if selected_task:
            completed_task = f"{selected_task.text()} (Completed)"
            self.completedList.addItem(completed_task)
            self.taskList.takeItem(self.taskList.row(selected_task))
        else:
            QMessageBox.warning(self, "Error", "No task selected")

    # 購物清單的功能

    ## 新增購物
    def add_groc(self):
        task = self.grocInput.text()
        if task.strip():
            item = QListWidgetItem(task)
            item.setCheckState(Qt.CheckState.Unchecked)  # 預設未勾選
            self.grocList.addItem(item)
            self.grocInput.clear()
        else:
            QMessageBox.warning(self, "Error", "Groceries cannot be empty")
            
    ## 刪除購物
    def delete_groc(self):
        selected_groc = self.grocList.currentItem()
        if selected_groc:
            self.grocList.takeItem(self.grocList.row(selected_groc))
        else:
            QMessageBox.warning(self, "Error", "No grocery item selected")

    # 其他

    ## 預設任務
    def add_default_tasks(self):
        # 假設預設有兩個任務，並設置它們的日期
        default_tasks = [
            ("2025-01-12/Task 2", "star_empty.jpg"),
            ("2025-01-11/Task 1", "star_empty.jpg"),
            ("2025-01-11/Task 3", "star_filled.jpg"),  # 已完成
            ("2025-01-12/Task 4", "star_filled.jpg")   # 已完成
        ]

        for task_text, icon in default_tasks:
            item = QListWidgetItem(task_text)
            item.setIcon(QIcon(icon))  # 設置圖標
            item.setData(Qt.ItemDataRole.UserRole, "empty" if icon == "star_empty.jpg" else "filled")  # 設置任務狀態
            self.taskList.addItem(item)

    ## 雙擊項目來切換圖標
    def toggle_task_icon(self, item):
        # 檢查該項目目前儲存的狀態
        if item.data(Qt.ItemDataRole.UserRole) == "empty":
            # 如果狀態為 "empty"，切換為實心星星
            item.setIcon(QIcon("star_filled.jpg"))
            item.setData(Qt.ItemDataRole.UserRole, "filled")  # 更新狀態為 "filled"
        else:
            # 如果狀態為 "filled"，切換為空心星星
            item.setIcon(QIcon("star_empty.jpg"))
            item.setData(Qt.ItemDataRole.UserRole, "empty")  # 更新狀態為 "empty"

    ## 驗證輸入格式
    def is_valid_task(self, task):
        pattern = r"^\d{4}-\d{2}-\d{2}/.+$"  # YYYY-MM-DD/任務
        return bool(re.match(pattern, task))

    ## 切換排序模式
    def toggle_sorting(self):
        if self.is_sorted_by_date:
            # 依任務名稱排序
            self.sort_tasks_by_name()
        else:
            # 依日期排序
            self.sort_tasks_by_date()
        
        # 切換排序標誌
        self.is_sorted_by_date = not self.is_sorted_by_date

    ## 依日期排序
    def sort_tasks_by_date(self):
        # 提取所有項目及其資料
        items = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            items.append((item.text(), item.icon(), item.data(Qt.ItemDataRole.UserRole)))
        
        # 根據日期排序（以字符串形式進行比較）
        items.sort(key=lambda x: x[0].split("/")[0])  # 提取並按日期部分排序

        # 清空列表並重建項目
        self.taskList.clear()
        for text, icon, status in items:
            item = QListWidgetItem(text)
            item.setIcon(icon)
            item.setData(Qt.ItemDataRole.UserRole, status)
            self.taskList.addItem(item)

    ## 依任務名稱排序
    def sort_tasks_by_name(self):
        # 提取所有項目及其資料
        items = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            items.append((item.text(), item.icon(), item.data(Qt.ItemDataRole.UserRole)))
        
        # 根據任務名稱部分排序（即"/"之後的部分）
        items.sort(key=lambda x: x[0].split("/")[1].lower())  # 提取並按名稱部分排序

        # 清空列表並重建項目
        self.taskList.clear()
        for text, icon, status in items:
            item = QListWidgetItem(text)
            item.setIcon(icon)
            item.setData(Qt.ItemDataRole.UserRole, status)
            self.taskList.addItem(item)

    ## 根據星星圖標排序
    def sort_tasks_by_star(self):
        # 提取所有項目及其資料
        items = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            items.append((item.text(), item.icon(), item.data(Qt.ItemDataRole.UserRole)))
        
        # 根據星星狀態排序，"filled" 在前，"empty" 在後
        items.sort(key=lambda x: x[2] == "empty")  # "empty" 排在後面

        # 清空列表並重建項目
        self.taskList.clear()
        for text, icon, status in items:
            item = QListWidgetItem(text)
            item.setIcon(icon)
            item.setData(Qt.ItemDataRole.UserRole, status)
            self.taskList.addItem(item)

# 主程式
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
