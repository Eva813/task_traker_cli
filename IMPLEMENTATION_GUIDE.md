# 實現指南

## 📖 逐步實現指南

### TODO 1: 實現 JSON 數據存儲

#### `load_database()`
```python
def load_database(path=DB_PATH):
    if Path(path).exists():
        with open(path, 'r') as f:
            return json.load(f)
    else:
        return {"tasks": []}
```

要點：
- 使用 `Path(path).exists()` 檢查文件是否存在
- 用 `json.load()` 讀取 JSON 文件
- 如果文件不存在，返回空結構 `{"tasks": []}`

#### `save_database()`
```python
def save_database(database, path=DB_PATH):
    with open(path, 'w') as f:
        json.dump(database, f, indent=2)
```

要點：
- 使用 `json.dump()` 寫入 JSON 文件
- `indent=2` 使 JSON 格式更易讀
- 自動創建文件（如果不存在）

---

### TODO 2: 核心任務管理

#### `add_task()`
```python
def add_task(database, description):
    # 計算新 ID
    if database["tasks"]:
        new_id = max(task["id"] for task in database["tasks"]) + 1
    else:
        new_id = 1
    
    # 創建新任務
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    
    # 添加到數據庫並保存
    database["tasks"].append(new_task)
    save_database(database)
    
    return new_id
```

要點：
- 使用 `max()` 找出最大的 ID
- 使用 `datetime.now().strftime()` 獲得當前日期
- 記得調用 `save_database()` 保存更改

#### `update_task()`
```python
def update_task(database, task_id, description=None, status=None):
    # 尋找任務
    task = None
    for t in database["tasks"]:
        if t["id"] == task_id:
            task = t
            break
    
    if task is None:
        return False
    
    # 更新字段
    if description is not None:
        task["description"] = description
    
    if status is not None:
        if status not in STATUSES:
            raise ValueError(f"Invalid status: {status}")
        task["status"] = status
    
    save_database(database)
    return True
```

要點：
- 驗證狀態值
- 只更新提供的字段
- 返回布林值表示成功/失敗

#### `delete_task()`
```python
def delete_task(database, task_id):
    original_length = len(database["tasks"])
    database["tasks"] = [t for t in database["tasks"] if t["id"] != task_id]
    
    if len(database["tasks"]) < original_length:
        save_database(database)
        return True
    return False
```

要點：
- 使用列表推導式過濾任務
- 檢查長度變化判斷是否刪除成功
- 記得保存更改

#### `list_tasks()`
```python
def list_tasks(database, status=None, date=None, date_operator="="):
    tasks = database["tasks"]
    
    # 按狀態篩選
    if status and status != "all":
        tasks = [t for t in tasks if t["status"] == status]
    
    # 按日期篩選
    if date:
        tasks = [t for t in tasks if compare_dates(t["date"], date, date_operator)]
    
    return tasks

def compare_dates(task_date, filter_date, operator):
    if operator == "=":
        return task_date == filter_date
    elif operator == "<":
        return task_date < filter_date
    elif operator == ">":
        return task_date > filter_date
    return False
```

要點：
- 使用列表推導式篩選
- 支持多個篩選條件
- 字符串日期可以直接比較（因為格式是 YYYY-MM-DD）

---

### TODO 3: 快速狀態函數

```python
def mark_done(database, task_id):
    return update_task(database, task_id, status="done")

def mark_in_progress(database, task_id):
    return update_task(database, task_id, status="in-progress")
```

非常簡單 — 只是包裝 `update_task()`

---

### TODO 4: 輸出格式

#### `print_task()`
```python
def print_task(task):
    status_icon = {
        "todo": "☐",
        "in-progress": "⟳",
        "done": "✓"
    }.get(task["status"], "?")
    
    print(f"  [{task['id']}] {status_icon} {task['description']} ({task['status']}) - {task['date']}")
```

要點：
- 使用字典映射狀態到圖標
- 格式化輸出便於閱讀

#### `print_tasks()`
```python
def print_tasks(tasks):
    if not tasks:
        print("No tasks found")
        return
    
    print("\nTasks:")
    for task in tasks:
        print_task(task)
    print()
```

要點：
- 檢查是否為空
- 添加標題和空行

---

### TODO 5: 命令行解析

```python
def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # ADD 命令
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    
    # LIST 命令
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("-s", "--status", choices=["todo", "in-progress", "done", "all"])
    list_parser.add_argument("-d", "--date", help="Filter by date (YYYY-MM-DD)")
    
    # UPDATE 命令
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("-d", "--description", help="New description")
    update_parser.add_argument("-s", "--status", choices=STATUSES)
    
    # DELETE 命令
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")
    
    # MARK-DONE 命令
    mark_done_parser = subparsers.add_parser("mark-done", help="Mark task as done")
    mark_done_parser.add_argument("id", type=int, help="Task ID")
    
    # MARK-IN-PROGRESS 命令
    mark_prog_parser = subparsers.add_parser("mark-in-progress", help="Mark task as in-progress")
    mark_prog_parser.add_argument("id", type=int, help="Task ID")
    
    args = parser.parse_args()
    database = load_database()
    
    # 命令路由
    if args.command == "add":
        task_id = add_task(database, args.description)
        print(f"✓ Task added (ID: {task_id})")
    
    elif args.command == "list":
        tasks = list_tasks(database, args.status, args.date)
        print_tasks(tasks)
    
    elif args.command == "update":
        if update_task(database, args.id, args.description, args.status):
            print(f"✓ Task {args.id} updated")
        else:
            print(f"✗ Task {args.id} not found")
    
    elif args.command == "delete":
        if delete_task(database, args.id):
            print(f"✓ Task {args.id} deleted")
        else:
            print(f"✗ Task {args.id} not found")
    
    elif args.command == "mark-done":
        if mark_done(database, args.id):
            print(f"✓ Task {args.id} marked as done")
        else:
            print(f"✗ Task {args.id} not found")
    
    elif args.command == "mark-in-progress":
        if mark_in_progress(database, args.id):
            print(f"✓ Task {args.id} marked as in-progress")
        else:
            print(f"✗ Task {args.id} not found")
```

要點：
- 使用 `subparsers` 定義子命令
- `type=int` 自動將字符串轉換為整數
- `choices` 限制選項值
- 記得加載數據庫

---

### TODO 6: 單元測試

#### 測試 Fixture
```python
@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    # 初始化空數據庫
    with open(path, 'w') as f:
        json.dump({"tasks": []}, f)
    
    yield path
    
    # 清理
    os.unlink(path)
```

#### 測試例子
```python
def test_add_single_task(temp_db):
    """Test adding a single task."""
    db = load_database(temp_db)
    task_id = add_task(db, "Buy groceries")
    
    assert task_id == 1
    assert len(db["tasks"]) == 1
    assert db["tasks"][0]["description"] == "Buy groceries"
    assert db["tasks"][0]["status"] == "todo"

def test_delete_existing_task(temp_db):
    """Test deleting an existing task."""
    db = load_database(temp_db)
    task_id = add_task(db, "Buy groceries")
    
    assert delete_task(db, task_id) == True
    assert len(db["tasks"]) == 0
```

要點：
- 使用臨時文件避免污染真實數據
- `assert` 檢查預期結果
- 覆蓋成功和失敗情況

---

## 🎯 調試技巧

### 打印調試信息
```python
print(f"DEBUG: database = {json.dumps(database, indent=2)}")
```

### 測試單個函數
```bash
# 進入 Python 互動模式
uv run python

# 然後
from task_cli import load_database, add_task
db = load_database()
add_task(db, "Test task")
```

### 查看 JSON 文件
```bash
cat tasks.json
```

---

## ✅ 檢查清單

實現每個功能時，檢查：

- [ ] 函數簽名正確
- [ ] 正確處理邊界情況（空列表、不存在的 ID 等）
- [ ] 數據正確保存
- [ ] 返回值正確
- [ ] 有適當的錯誤處理
- [ ] 編寫了測試用例
- [ ] 測試通過

---

祝你實現順利！🚀
