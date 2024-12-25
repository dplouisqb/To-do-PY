from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6 import uic
import sys

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        # 載入 UI
        uic.loadUi('todo_app.ui', self)

        # 連接功能
##代辦清單
        self.addButton.clicked.connect(self.add_task)
        self.deleteButton.clicked.connect(self.delete_task)
        self.markCompleteButton.clicked.connect(self.mark_complete)

##購物清單
        self.grocButton.clicked.connect(self.add_groc)

##代辦清單
    def add_task(self):
        task = self.taskInput.text()
        if task.strip():
            self.taskList.addItem(task)
            self.taskInput.clear()
        else:
            QMessageBox.warning(self, "Error", "Task cannot be empty")
    
    def delete_task(self):
    # 取得當前選中的 taskList 或 completedList 中的項目
        selected_task = self.taskList.currentItem()
        completed_task = self.completedList.currentItem()

        # 檢查是否有選中項目
        if not selected_task and not completed_task:
            QMessageBox.warning(self, "Error", "No task selected")
            return  # 沒有選中任何項目則返回

        # 檢查是否在 selected_task 和 completed_task 這兩個項目中，都有選中項目
        if selected_task and not selected_task.isSelected():
            selected_task = None  # 如果該項目沒有選中，將其設為 None
        if completed_task and not completed_task.isSelected():
            completed_task = None  # 如果該項目沒有選中，將其設為 None

        # 如果兩邊都沒有選中項目，顯示錯誤訊息
        if not selected_task and not completed_task:
            QMessageBox.warning(self, "Error", "No task selected")
            return  # 沒有選中任何項目則返回

        # 如果在 completedList 中選中，且該項目被選中
        if completed_task and completed_task.isSelected():  
            self.completedList.takeItem(self.completedList.row(completed_task))
            self.completedList.clearSelection()  # 取消選取 completedList 中的項目

        # 如果在 taskList 中選中，且該項目被選中
        if selected_task and selected_task.isSelected():  
            self.taskList.takeItem(self.taskList.row(selected_task))
            self.taskList.clearSelection()  # 取消選取 taskList 中的項目

    def mark_complete(self):
        selected_task = self.taskList.currentItem()
        if selected_task and selected_task.isSelected():
            completed_task = f"{selected_task.text()} (Completed)"  # 標記為完成
            self.completedList.addItem(completed_task)  # 將完成的任務加入完成清單
            self.taskList.takeItem(self.taskList.row(selected_task))  # 從待辦清單中移除
            self.taskList.clearSelection()  # 取消選取 taskList 中的項目
        else:
          QMessageBox.warning(self, "Error", "No task selected")

##購物清單

    def add_groc(self):
        task = self.grocInput.text()
        if task.strip():
            self.grocList.addItem(task  )
            self.grocInput.clear()
        else:
            QMessageBox.warning(self, "Error", "Groceries cannot be empty")
    


# 主程式
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())