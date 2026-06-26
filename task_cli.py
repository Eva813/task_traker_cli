"""
Task Tracker CLI - A lightweight command-line TODO application

Usage:
  task add "description"                          - Add a new task
  task list [-s STATUS] [-d DATE]                - List tasks (with optional filters)
  task update ID [-d DESCRIPTION] [-s STATUS]    - Update task
  task delete ID                                 - Delete task
  task mark-done ID                              - Mark task as done
  task mark-in-progress ID                       - Mark task as in-progress
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Default database path
DB_PATH = "tasks.json"

# Task statuses
STATUSES = ["todo", "in-progress", "done"]


# ============================================================================
# TODO 1: 實現 JSON 數據存儲功能
# ============================================================================
def load_database(path=DB_PATH):
    """
    Load tasks from JSON file.
    
    Args:
        path (str): Path to JSON database file
        
    Returns:
        dict: Database with tasks list
    """
    # TODO: 如果檔案存在，讀取並解析 JSON；否則返回空數據庫
    # 提示：使用 Path(path).exists()、json.load() 等
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    else:
        return {"tasks": []}



def save_database(database, path=DB_PATH):
    """
    Save tasks to JSON file.
    
    Args:
        database (dict): Database with tasks list
        path (str): Path to JSON database file
    """
    # TODO: 將數據庫寫入 JSON 檔案，使用 json.dump()
    # 提示：indent=2 可以讓 JSON 更易讀
    with open(path, "w") as f:
        json.dump(database, f, indent=2)


# ============================================================================
# TODO 2: 實現核心任務管理功能
# ============================================================================
def add_task(database, description):
    """
    Add a new task to the database.
    
    Args:
        database (str or dict): File path to JSON database or database dict
        description (str): Task description
        
    Returns:
        dict: The newly created task object
    """
    # Load database if file path is provided
    if isinstance(database, str):
        db = load_database(database)
        db_path = database
    else:
        db = database
        db_path = DB_PATH
    
    # 1. 計算新 task 的 ID (最大 ID + 1)
    if db["tasks"]:
        new_id = max(task["id"] for task in db["tasks"]) + 1
    else:
        new_id = 1
    
    # 2. 創建新 task 字典
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "date": datetime.today().strftime("%Y-%m-%d")
    }
    
    # 3. 添加到 database["tasks"]
    db["tasks"].append(new_task)
    
    # 4. 保存並返回新 task
    save_database(db, db_path)
    return new_task

# 寫法一：生成式（簡潔）
#new_id = max(task["id"] for task in database["tasks"]) + 1

# 寫法二：完整迴圈（等價，較好理解）
#ids = []
#for task in database["tasks"]:
#    ids.append(task["id"])
#new_id = max(ids) + 1


def update_task(database, task_id, description=None, status=None, date=None):
    """
    Update task description, status, and/or date.
    
    Args:
        database (str or dict): File path to JSON database or database dict
        task_id (int): ID of task to update
        description (str): New description (optional)
        status (str): New status (optional)
        date (str): New date in YYYY-MM-DD format (optional)
        
    Returns:
        bool: True if successful, False if task not found
    """
    # Load database if file path is provided
    if isinstance(database, str):
        db = load_database(database)
        db_path = database
    else:
        db = database
        db_path = DB_PATH
    
    # TODO:
    # 1. 找到指定 ID 的 task
    # 2. 如果 description 不為 None，更新 description
    # 3. 如果 status 不為 None，驗證並更新 status
    # 4. 如果 date 不為 None，更新 date
    # 5. 保存數據庫
    # 6. 返回成功/失敗
    for task in db["tasks"]:
        if task["id"] == task_id:
            if description is not None:
                task["description"] = description
            if status is not None:
                if status in STATUSES:
                    task["status"] = status
                else:
                    print(f"Invalid status: {status}. Must be one of {STATUSES}.")
                    return False
            if date is not None:
                task["date"] = date
            save_database(db, db_path)
            return True
    return False


def delete_task(database, task_id):
    """
    Delete a task by ID.
    
    Args:
        database (str or dict): File path to JSON database or database dict
        task_id (int): ID of task to delete
        
    Returns:
        bool: True if successful, False if task not found
    """
    # Load database if file path is provided
    if isinstance(database, str):
        db = load_database(database)
        db_path = database
    else:
        db = database
        db_path = DB_PATH
    
    # TODO:
    # 1. 找到並刪除指定 ID 的 task
    # 2. 保存數據庫
    # 3. 返回成功/失敗
    for i, task in enumerate(db["tasks"]):
        print(i, task)
        if task["id"] == task_id:
            del db["tasks"][i]
            save_database(db, db_path)
            return True
    return False


def list_tasks(database, status=None, date=None, date_operator="="):
    """
    List tasks with optional filters.
    
    Args:
        database (str or dict): File path to JSON database or database dict
        status (str): Filter by status (todo, in-progress, done, or all)
        date (str): Filter by date (format: YYYY-MM-DD)
        date_operator (str): Date comparison operator (<, >, =)
        
    Returns:
        list: Filtered tasks
    """
    # Load database if file path is provided
    if isinstance(database, str):
        db = load_database(database)
    else:
        db = database
    
    # TODO:
    # 1. 從 database["tasks"] 取得所有 tasks
    # 2. 如果 status 指定且不是 "all"，按 status 篩選
    # 3. 如果 date 指定，按日期和 operator 篩選
    # 4. 返回篩選後的 tasks
    tasks = db["tasks"]
    if status and status != "all":
        # 「對 tasks 裡每個 task，如果 task["status"] == status，就把這個 task放進新的 list」
        tasks = [task for task in tasks if task["status"] == status]
    if date:
        if date_operator == "=":
            tasks = [task for task in tasks if task["date"] == date]
        elif date_operator == "<":
            tasks = [task for task in tasks if task["date"] < date]
        elif date_operator == ">":
            tasks = [task for task in tasks if task["date"] > date]
    return tasks


# ============================================================================
# TODO 3: 實現快速狀態更新功能
# ============================================================================
def mark_done(database, task_id):
    """
    Mark a task as done.
    
    Args:
        database (str or dict): File path to JSON database or database dict
        task_id (int): ID of task to mark as done
        
    Returns:
        bool: True if successful, False if task not found
    """
    # TODO: 呼叫 update_task，設置 status="done"
    return update_task(database, task_id, description=None, status="done")



def mark_in_progress(database, task_id):
    """
    Mark a task as in-progress.
    
    Args:
        database (str or dict): File path to JSON database or database dict
        task_id (int): ID of task to mark as in-progress
        
    Returns:
        bool: True if successful, False if task not found
    """
    # TODO: 呼叫 update_task，設置 status="in-progress"
    return update_task(database, task_id, description=None, status="in-progress")



# ============================================================================
# TODO 4: 實現命令行界面和輸出格式
# ============================================================================
def print_task(task):

    """Pretty print a single task."""
    # TODO: 格式化並打印 task 信息
    # 例如: [1] ✓ Buy groceries (todo) - 2026-06-15
    # 或使用簡單文本格式
    status_symbols = {
        "todo": " ",
        "in-progress": "~",
        "done": "✓"
    }
    symbol = status_symbols.get(task["status"], "?")
    print(f"[{task['id']}] {symbol} {task['description']} ({task['status']}) - {task['date']}")
    


def print_tasks(tasks):
    """Pretty print a list of tasks."""
    # TODO:
    # 1. 如果 tasks 為空，打印 "No tasks found"
    # 2. 否則逐個調用 print_task()
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print_task(task)


# ============================================================================
# TODO 5: 實現命令行參數解析和命令路由
# ============================================================================
def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Task Tracker CLI - Manage your tasks from the command line",
        prog="task"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # TODO: 為每個命令創建 subparser：
    # 
    # 步驟 1: 建立子命令
    add_parser = subparsers.add_parser("add", help="Add a new task")
    # 步驟 2: 定義參數（位置參數，必填）
    add_parser.add_argument("description", help="Task description")
    #
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("-s", "--status",
        choices=["todo", "in-progress", "done", "all"],
        default="all", help="Filter by status")
    list_parser.add_argument("-d", "--date", help="Filter by date (YYYY-MM-DD)")
    #
    # ... 依此類推實現 update, delete, mark-done, mark-in-progress ...
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID to update")
    #  -d, -s 短選項 (short option)( 一個字母，快速打字)
    update_parser.add_argument("-d", "--description", help="New task description")
    update_parser.add_argument("-s", "--status",
        choices=["todo", "in-progress", "done"], help="New task status")
        # 是 argparse 的一個參數，用來限制用戶只能輸入特定的值。
    
    # choices 的作用
    #  add_argument("-s", "--status", 
    #      choices=["todo", "in-progress", "done"],
    #      help="New task status")

    # 使用者只能輸入這三個值之一：

    #  ✓ task update 1 -s done          # 可以
    #  ✓ task update 1 -s todo          # 可以
    #  ✓ task update 1 -s in-progress   # 可以
    #  ✗ task update 1 -s complete      # 不行！會報錯
    #  ✗ task update 1 -s DONE          # 不行！大小寫要符合
    
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    done_parser = subparsers.add_parser("mark-done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Task ID to mark as done")

    # ── mark-in-progress ─────────────────────────────
    prog_parser = subparsers.add_parser("mark-in-progress", help="Mark task as in-progress")
    prog_parser.add_argument("id", type=int, help="Task ID")
    
    args = parser.parse_args()
    
    # 加載數據庫
    database = load_database()
    
    # TODO: 根據 args.command 路由到相應的命令處理程序
    # 
    # if args.command == "add":
    #     task_id = add_task(database, args.description)
    #     print(f"✓ Task added (ID: {task_id})")
    #
    # elif args.command == "list":
    #     tasks = list_tasks(database, status=args.status, ...)
    #     print_tasks(tasks)
    #
    # ... 依此類推 ...
    # ── 命令路由 ──────────────────────────────────────
    if args.command == "add":
        task_id = add_task(database, args.description)
        print(f"✓ Task added (ID: {task_id})")

    elif args.command == "list":
        tasks = list_tasks(database, status=args.status, date=args.date)
        print_tasks(tasks)

    elif args.command == "update":
        ok = update_task(database, args.id, args.description, args.status)
        print("✓ Task updated" if ok else "✗ Task not found")

    elif args.command == "delete":
        ok = delete_task(database, args.id)
        print("✓ Task deleted" if ok else "✗ Task not found")

    elif args.command == "mark-done":
        ok = mark_done(database, args.id)
        print("✓ Marked as done" if ok else "✗ Task not found")

    elif args.command == "mark-in-progress":
        ok = mark_in_progress(database, args.id)
        print("✓ Marked as in-progress" if ok else "✗ Task not found")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()