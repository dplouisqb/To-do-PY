import os

# 全域變數：用來存儲任務
pending_tasks = []   # 待完成的任務清單
completed_tasks = [] # 已完成的任務清單

def add_task():
    print("Add task")

def show_tasks():
    print("Show tasks")
    
# 新增任務
def add_task():
    title = input("請輸入任務名稱：").strip()
    if not title:
        print("任務名稱不可為空！")
        return
    
    description = input("請輸入任務描述（可選）：").strip()
    due_date = input("請輸入完成期限（格式: YYYY-MM-DD，可選）：").strip()

    # 建立新任務
    new_task = {
        "title": title,
        "description": description or None,
        "due_date": due_date or None,
    }
    pending_tasks.append(new_task)
    print(f"\n成功新增任務：{new_task['title']}\n")

# 刪除任務   
def delete_task():
    print("\n=== 刪除任務 ===")
    show_tasks()

    task_type = input("請選擇任務類型（1: 未完成, 2: 已完成）：").strip()
    if task_type not in ["1", "2"]:
        print("\n無效的選擇！請輸入 1 或 2。\n")
        return

    task_list = pending_tasks if task_type == "1" else completed_tasks
    if not task_list:
        print("\n選擇的任務清單中沒有任務。\n")
        return

    try:
        task_idx = int(input("請輸入要刪除的任務編號：")) - 1
        if 0 <= task_idx < len(task_list):
            task = task_list.pop(task_idx)
            print(f"\n成功刪除任務：{task['title']}\n")
        else:
            print("\n無效的編號！請重新選擇。\n")
    except ValueError:
        print("\n輸入無效！請輸入數字。\n")

# 完成任務
def complete_task():
    if not pending_tasks:
        print("\n目前沒有未完成的任務！\n")
        return

    show_tasks()
    try:
        task_idx = int(input("請輸入要完成的任務編號：")) - 1
        if 0 <= task_idx < len(pending_tasks):
            task = pending_tasks.pop(task_idx)
            completed_tasks.append(task)
            print(f"\n成功完成任務：{task['title']}\n")
        else:
            print("\n無效的編號！請重新選擇。\n")
    except ValueError:
        print("\n輸入無效！請輸入數字。\n")

# 顯示任務清單
def show_tasks():
    print("\n=== 任務清單 ===")
    print("未完成的任務：")
    if not pending_tasks:
        print("\n  目前沒有任何任務！\n")
    else:
        for idx, task in enumerate(pending_tasks, start=1):
            print(f"  {idx}. {task['title']} ({task['description'][:40]})") # 描述部份最多顯示 40 個字元
    
    print("\n已完成的任務：")
    if not completed_tasks:
        print("\n  目前沒有任何任務！\n")
    else:
        for idx, task in enumerate(completed_tasks, start=1):
            print(f"  {idx}. {task['title']} ({task['description'][:40]})") # 描述部份最多顯示 40 個字元
    print()

def main():
    while True:
        print("\n=== To-Do List 管理系統 ===")
        print("1. 顯示任務清單")
        print("2. 新增任務")
        print("3. 完成任務")
        print("4. 刪除任務")
        print("5. 離開系統")
        
        choice = input("請選擇功能（輸入數字）：").strip()
        
        if choice == "1":
            show_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("感謝使用，再見！")
            break
        else:
            print("無效的選擇，請重新輸入。\n")

# 啟動主程式
main()

