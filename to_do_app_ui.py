from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem
from PyQt6 import uic
import sys, re

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('todo_app.ui', self)

        # 功能

        ## 代辦清單
        self.addButton.clicked.connect(self.add_task)
        self.deleteButton.clicked.connect(self.delete_task)
        self.markCompleteButton.clicked.connect(self.mark_complete)

        ## 購物清單
        self.grocButton.clicked.connect(self.add_groc)
        self.deleteGrocButton.clicked.connect(self.delete_groc)

        ## 標記
        self.taskList.itemDoubleClicked.connect(self.toggle_task_icon)

        ## 排序
        self.sortButton_task.clicked.connect(self.toggle_sorting_task)
        self.sortButton_comp.clicked.connect(self.toggle_sorting_comp)
        self.sortButton_groc.clicked.connect(self.toggle_sorting_groc)

        ## 預設任務
        self.add_default_tasks()

        ## 排序模式標誌
        self.sort_mode_task = 0  # 0: 按名稱排序, 1: 按日期排序, 2: 按星星排序
        self.sort_mode_comp = 0  # 0: 按名稱排序, 1: 按日期排序
        self.sort_mode_groc = 0  # 0: 按名稱排序, 1: 按勾選排序

    # 代辦清單

    ## 增加任務
    def add_task(self):
        task = self.taskInput.text()
        if self.is_valid_task(task):
            item = QListWidgetItem(task)
            item.setIcon(QIcon("star_empty.png"))
            item.setData(Qt.ItemDataRole.UserRole, "empty")

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
            ("2025-01-12/Task 2", "star_empty.png"),
            ("2025-01-11/Task 1", "star_empty.png"),
            ("2025-01-11/Task 3", "star_empty.png"),  # 已完成
            ("2025-01-12/Task 4", "star_empty.png")   # 已完成
        ]

        for task_text, icon in default_tasks:
            item = QListWidgetItem(task_text)
            item.setIcon(QIcon(icon))  # 設置圖標
            item.setData(Qt.ItemDataRole.UserRole, "empty" if icon == "star_empty.png" else "filled")  # 設置任務狀態
            self.taskList.addItem(item)

    ## 雙擊項目來切換圖標
    def toggle_task_icon(self, item):
        # 檢查該項目目前儲存的狀態
        if item.data(Qt.ItemDataRole.UserRole) == "empty":
            # 如果狀態為 "empty"，切換為實心星星
            item.setIcon(QIcon("star_filled.png"))
            item.setData(Qt.ItemDataRole.UserRole, "filled")  # 更新狀態為 "filled"
        else:
            # 如果狀態為 "filled"，切換為空心星星
            item.setIcon(QIcon("star_empty.png"))
            item.setData(Qt.ItemDataRole.UserRole, "empty")  # 更新狀態為 "empty"

    ## 驗證輸入格式
    def is_valid_task(self, task):
        pattern = r"^\d{4}-\d{2}-\d{2}/.+$"  # YYYY-MM-DD/任務
        return bool(re.match(pattern, task))

    ## 切換代辦清單排序模式
    def toggle_sorting_task(self):
        if self.sort_mode_task == 0:
            # 依任務名稱排序
            self.sort_tasks_by_name(self.taskList)
            self.sort_mode_task = 1  # 下一次將按日期排序
        elif self.sort_mode_task == 1:
            # 依日期排序
            self.sort_tasks_by_date(self.taskList)
            self.sort_mode_task = 2  # 下一次將按星星排序
        elif self.sort_mode_task == 2:
            # 依星星排序
            self.sort_tasks_by_star(self.taskList)
            self.sort_mode_task = 0  # 下一次將按任務名稱排序

    ## 切換已完成清單排序模式
    def toggle_sorting_comp(self):
        if self.sort_mode_comp == 0:
            # 依任務名稱排序
            self.sort_tasks_by_name(self.completedList)
            self.sort_mode_comp = 1  # 下一次將按日期排序
        elif self.sort_mode_comp == 1:
            # 依日期排序
            self.sort_tasks_by_date(self.completedList)
            self.sort_mode_comp = 0  # 下一次將按任務名稱排序

    ## 切換購物清單排序模式
    def toggle_sorting_groc(self):
        if self.sort_mode_groc == 0:
            # 依名稱排序
            self.sort_groc_by_name(self.grocList)
            self.sort_mode_groc = 1  # 下一次將按勾選狀態排序
        elif self.sort_mode_groc == 1:
            # 依勾選狀態排序
            self.sort_groc_by_check(self.grocList)
            self.sort_mode_groc = 0  # 下一次將按名稱排序

    ## 依日期排序
    def sort_tasks_by_date(self, list_widget):
        self.sort_list_by_icon(list_widget, lambda x: x[0].split("/")[0])

    ## 依任務名稱排序
    def sort_tasks_by_name(self, list_widget):
        self.sort_list_by_icon(list_widget, lambda x: x[0].split("/")[1].lower())

    ## 根據星星圖標排序
    def sort_tasks_by_star(self, list_widget):
        self.sort_list_by_icon(list_widget, lambda x: x[2] == "empty")

    ## 依購物名稱排序
    def sort_groc_by_name(self, list_widget):
        self.sort_list_by_check(list_widget, lambda x: x[0].lower())

    ## 依勾選狀態排序
    def sort_groc_by_check(self, list_widget):
        self.sort_list_by_check(list_widget, lambda x: x[2] != Qt.CheckState.Checked)

    ## 根據圖標排序
    def sort_list_by_icon(self, list_widget, key_function):
        # 提取所有項目及其資料
        items = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            items.append((item.text(), item.icon(), item.data(Qt.ItemDataRole.UserRole), item))

        # 根據提供的 key_function 進行排序
        items.sort(key=key_function)

        # 清空列表
        list_widget.clear()

        # 按照排序結果重新添加項目
        for text, icon, status, item in items:
            new_item = QListWidgetItem(text)
            new_item.setIcon(icon)
            new_item.setData(Qt.ItemDataRole.UserRole, status)
            list_widget.addItem(new_item)

    ## 根據勾選狀態排序
    def sort_list_by_check(self, list_widget, key_function):
        # 提取所有項目及其資料
        items = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            items.append((item.text(), item, item.checkState()))  # 改成直接將 checkState 放在第三個位置

        # 根據提供的 key_function 進行排序
        items.sort(key=key_function)

        # 清空列表
        list_widget.clear()

        # 按照排序結果重新添加項目
        for text, item, check_state in items:
            new_item = QListWidgetItem(text)
            new_item.setCheckState(check_state)  # 設置 checkState
            list_widget.addItem(new_item)


# 主程式
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
